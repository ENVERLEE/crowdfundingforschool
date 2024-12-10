from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Pledge
from projects.models import Project, Reward

@login_required
def pledge_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        reward_id = request.POST.get('reward_id')
        amount = request.POST.get('amount')
        
        pledge = Pledge.objects.create(
            user=request.user,
            project=project,
            reward_id=reward_id,
            amount=amount,
            status='pending'
        )
        messages.success(request, '후원이 신청되었습니다. 관리자 승인 후 처리됩니다.')
        return redirect('pledge_detail', pledge_id=pledge.id)
    
    rewards = project.rewards.all()
    return render(request, 'payments/pledge_form.html', {
        'project': project,
        'rewards': rewards
    })

@login_required
def pledge_detail(request, pledge_id):
    pledge = get_object_or_404(Pledge, id=pledge_id)
    if pledge.user != request.user and not request.user.is_staff:
        messages.error(request, '접근 권한이 없습니다.')
        return redirect('project_list')
    return render(request, 'payments/pledge_detail.html', {'pledge': pledge})

@login_required
def pledge_list(request):
    if request.user.is_staff:
        pledges = Pledge.objects.all().order_by('-created_at')
    else:
        pledges = Pledge.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'payments/pledge_list.html', {'pledges': pledges})

@user_passes_test(lambda u: u.is_staff)
def pledge_approve(request, pledge_id):
    pledge = get_object_or_404(Pledge, id=pledge_id)
    if request.method == 'POST':
        admin_message = request.POST.get('admin_message', '')
        pledge.approve(admin_message)
        messages.success(request, '후원이 승인되었습니다.')
    return redirect('pledge_list')

@user_passes_test(lambda u: u.is_staff)
def pledge_reject(request, pledge_id):
    pledge = get_object_or_404(Pledge, id=pledge_id)
    if request.method == 'POST':
        admin_message = request.POST.get('admin_message', '')
        pledge.reject(admin_message)
        messages.success(request, '후원이 거절되었습니다.')
    return redirect('pledge_list')
