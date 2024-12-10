# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpForm, UserProfileForm, CreatorApplicationForm
from .models import User, PointHistory
from projects.models import Project
from payments.models import Pledge

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '회원가입이 완료되었습니다. 관리자의 포인트 지급을 기다려주세요.')
            return redirect('projects:project_list')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필이 수정되었습니다.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    point_history = PointHistory.objects.filter(user=request.user)
    pledges = request.user.pledge_set.all().order_by('-created_at')
    backed_projects = Pledge.objects.filter(
        user=request.user,
        status='paid'
    ).select_related('project')
    created_projects = []
    if request.user.is_creator:
        created_projects = Project.objects.filter(creator=request.user)
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'point_history': point_history,
        'pledges': pledges,
        'backed_projects': backed_projects,
        'created_projects': created_projects
    })

@login_required
def creator_apply(request):
    if request.user.creator_status not in ['none', 'rejected']:
        messages.error(request, '이미 창작자 신청을 하셨습니다.')
        return redirect('profile')
        
    if request.method == 'POST':
        form = CreatorApplicationForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.creator_status = 'pending'
            user.creator_application_date = timezone.now()
            user.save()
            messages.success(request, '창작자 신청이 완료되었습니다. 관리자 승인을 기다려주세요.')
            return redirect('profile')
    else:
        form = CreatorApplicationForm(instance=request.user)
    
    return render(request, 'accounts/creator_apply.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    # 포인트를 받지 않은 신규 회원 조회
    pending_users = User.objects.filter(
        points=0,
        total_points_received=0
    ).order_by('date_joined')

    # 승인 대기중인 창작자 신청 조회
    pending_creators = User.objects.filter(
        creator_status='pending'
    ).order_by('creator_application_date')

    return render(request, 'accounts/admin_dashboard.html', {
        'pending_users': pending_users,
        'pending_creators': pending_creators,
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def give_initial_points(request, user_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        user = User.objects.get(id=user_id)
        points = int(request.POST.get('points', 0))
        message = request.POST.get('message', '')

        if points <= 0:
            messages.error(request, '포인트는 0보다 커야 합니다.')
            return redirect('admin_dashboard')

        user.add_points(points, 'initial', message)
        messages.success(request, f'{user.username}님에게 {points} 포인트가 지급되었습니다.')

    except User.DoesNotExist:
        messages.error(request, '사용자를 찾을 수 없습니다.')
    except ValueError:
        messages.error(request, '올바른 포인트 값을 입력해주세요.')
    except Exception as e:
        messages.error(request, f'오류가 발생했습니다: {str(e)}')

    return redirect('admin_dashboard')

@login_required
@user_passes_test(lambda u: u.is_staff)
def approve_creator(request, user_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        user = User.objects.get(id=user_id)
        if user.creator_status != 'pending':
            messages.error(request, '대기 중인 창작자 신청이 아닙니다.')
            return redirect('admin_dashboard')

        user.creator_status = 'approved'
        user.save()
        
        # 승인 알림 이메일 발송
        subject = '창작자 신청이 승인되었습니다'
        message = f'''안녕하세요 {user.username}님,
        
회원님의 창작자 신청이 승인되었습니다.
이제 프로젝트를 등록하실 수 있습니다.

감사합니다.'''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )

        messages.success(request, f'{user.username}님의 창작자 신청이 승인되었습니다.')

    except User.DoesNotExist:
        messages.error(request, '사용자를 찾을 수 없습니다.')
    except Exception as e:
        messages.error(request, f'오류가 발생했습니다: {str(e)}')

    return redirect('admin_dashboard')

@login_required
@user_passes_test(lambda u: u.is_staff)
def reject_creator(request, user_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        user = User.objects.get(id=user_id)
        if user.creator_status != 'pending':
            messages.error(request, '대기 중인 창작자 신청이 아닙니다.')
            return redirect('admin_dashboard')

        reason = request.POST.get('reason', '')
        if not reason:
            messages.error(request, '거절 사유를 입력해주세요.')
            return redirect('admin_dashboard')

        user.creator_status = 'rejected'
        user.save()
        
        # 거절 알림 이메일 발송
        subject = '창작자 신청이 거절되었습니다'
        message = f'''안녕하세요 {user.username}님,
        
회원님의 창작자 신청이 거절되었습니다.

거절 사유:
{reason}

문의사항이 있으시면 관리자에게 연락해주세요.
감사합니다.'''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )

        messages.success(request, f'{user.username}님의 창작자 신청이 거절되었습니다.')

    except User.DoesNotExist:
        messages.error(request, '사용자를 찾을 수 없습니다.')
    except Exception as e:
        messages.error(request, f'오류가 발생했습니다: {str(e)}')

    return redirect('admin_dashboard')

@login_required
def become_creator(request):
    if request.method == 'POST':
        request.user.is_creator = True
        request.user.save()
        messages.success(request, '창작자 등록이 완료되었습니다.')
        return redirect('creator_profile_edit')
    return render(request, 'accounts/become_creator.html')
