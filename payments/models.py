from django.db import models
from django.conf import settings

class Pledge(models.Model):
    STATUS_CHOICES = [
        ('pending', '승인대기'),
        ('approved', '승인완료'),
        ('rejected', '승인거절'),
        ('cancelled', '취소됨'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    reward = models.ForeignKey('projects.Reward', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_message = models.TextField(blank=True, help_text='관리자 메시지')

    def __str__(self):
        return f"{self.user.username} - {self.project.title} ({self.amount})"

    def approve(self, admin_message=''):
        if self.status == 'pending':
            self.status = 'approved'
            self.admin_message = admin_message
            self.save()
            
            # 프로젝트 후원 금액 업데이트
            self.project.current_amount += self.amount
            self.project.save()
            
            # 사용자 후원 통계 업데이트
            self.user.total_backed_amount += self.amount
            self.user.total_backed_projects += 1
            self.user.save()
            
            # 창작자 모금액 업데이트
            creator = self.project.creator
            creator.total_raised_amount += self.amount
            creator.save()

    def reject(self, admin_message):
        if self.status == 'pending':
            self.status = 'rejected'
            self.admin_message = admin_message
            self.save()
