from django import forms
from .models import Project, Reward

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'subtitle', 'category', 'target_amount',
            'start_date', 'end_date', 'description', 'risks',
            'thumbnail'
        ]
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = [
            'title', 'description', 'amount', 'stock',
            'delivery_date', 'shipping_fee'
        ]
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }
