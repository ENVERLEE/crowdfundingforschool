from django.contrib import admin
from .models import Project, Reward

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'target_amount', 'current_amount', 'created_at')
    search_fields = ('title', 'creator__username')
    list_filter = ('created_at',)

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'amount', 'stock')
    search_fields = ('title', 'project__title')
    list_filter = ('project',)
