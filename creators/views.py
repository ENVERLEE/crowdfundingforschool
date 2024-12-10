from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CreatorProfile, CreatorUpdate
from .forms import CreatorProfileForm, CreatorUpdateForm

def creator_detail(request, creator_id):
    creator = get_object_or_404(CreatorProfile, id=creator_id)
    projects = creator.user.project_set.all()
    updates = creator.updates.all().order_by('-created_at')
    return render(request, 'creators/creator_detail.html', {
        'creator': creator,
        'projects': projects,
        'updates': updates
    })

@login_required
def creator_profile_edit(request):
    profile, created = CreatorProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CreatorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필이 수정되었습니다.')
            return redirect('creator_detail', creator_id=profile.id)
    else:
        form = CreatorProfileForm(instance=profile)
    return render(request, 'creators/profile_form.html', {'form': form})

@login_required
def creator_update_create(request, project_id):
    creator = get_object_or_404(CreatorProfile, user=request.user)
    if request.method == 'POST':
        form = CreatorUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.creator = creator
            update.project_id = project_id
            update.save()
            messages.success(request, '업데이트가 등록되었습니다.')
            return redirect('project_detail', project_id=project_id)
    else:
        form = CreatorUpdateForm()
    return render(request, 'creators/update_form.html', {'form': form})
