from django import forms
from .models import CreatorProfile, CreatorUpdate

class CreatorProfileForm(forms.ModelForm):
    class Meta:
        model = CreatorProfile
        fields = [
            'name', 'bio', 'profile_image', 'website',
            'facebook', 'twitter', 'instagram'
        ]

class CreatorUpdateForm(forms.ModelForm):
    class Meta:
        model = CreatorUpdate
        fields = ['title', 'content']
