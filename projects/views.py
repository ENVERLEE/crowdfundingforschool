from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib import messages
from django.db import transaction
from .models import Project, Reward, Pledge
from .forms import ProjectForm, RewardForm

def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})

@login_required
def project_create(request):
    RewardFormSet = inlineformset_factory(
        Project, Reward, form=RewardForm,
        extra=1, can_delete=True, min_num=1, validate_min=True,
        max_num=10
    )
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        formset = RewardFormSet(request.POST, instance=Project())
        
        if form.is_valid() and formset.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            
            rewards = formset.save(commit=False)
            for reward in rewards:
                reward.project = project
                reward.save()
                
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ProjectForm()
        formset = RewardFormSet(instance=Project())
    
    return render(request, 'projects/project_form.html', {
        'form': form,
        'reward_formset': formset
    })

@login_required
@transaction.atomic
def pledge_create(request, project_id, reward_id):
    project = get_object_or_404(Project, pk=project_id)
    reward = get_object_or_404(Reward, pk=reward_id, project=project)
    user = request.user

    # 본인 프로젝트는 후원할 수 없음
    if project.creator == user:
        messages.error(request, '본인의 프로젝트는 후원할 수 없습니다.')
        return redirect('projects:project_detail', pk=project_id)

    # 잔액 확인
    if user.balance < reward.amount:
        messages.error(request, '잔액이 부족합니다.')
        return redirect('projects:project_detail', pk=project_id)

    # 재고 확인
    if reward.stock == 0:
        messages.error(request, '해당 리워드의 재고가 없습니다.')
        return redirect('projects:project_detail', pk=project_id)

    try:
        with transaction.atomic():
            # 잔액 차감
            user.balance -= reward.amount
            user.save()

            # 프로젝트 모금액 증가
            project.current_amount += reward.amount
            project.save()

            # 재고가 설정된 경우 감소
            if reward.stock > 0:
                reward.stock -= 1
                reward.save()

            # 후원 기록 생성
            Pledge.objects.create(
                supporter=user,
                project=project,
                reward=reward,
                amount=reward.amount
            )

        messages.success(request, '후원이 완료되었습니다.')
    except Exception as e:
        messages.error(request, '후원 처리 중 오류가 발생했습니다.')

    return redirect('projects:project_detail', pk=project_id)
