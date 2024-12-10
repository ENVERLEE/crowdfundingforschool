from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    CREATOR_STATUS_CHOICES = [
        ('none', '일반회원'),
        ('pending', '창작자 신청중'),
        ('approved', '승인된 창작자'),
        ('rejected', '창작자 신청 거절'),
    ]

    nickname = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    address_detail = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    
    # 후원자 관련 필드
    total_backed_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_backed_projects = models.IntegerField(default=0)
    
    # 포인트 관련 필드
    points = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_points_received = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_points_used = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    last_point_received_at = models.DateTimeField(null=True, blank=True)
    
    # 창작자 관련 필드
    is_creator = models.BooleanField(default=False)
    creator_status = models.CharField(
        max_length=20, 
        choices=CREATOR_STATUS_CHOICES, 
        default='none'
    )
    creator_application_date = models.DateTimeField(null=True, blank=True)
    creator_approved_date = models.DateTimeField(null=True, blank=True)
    creator_rejection_reason = models.TextField(blank=True)
    total_created_projects = models.IntegerField(default=0)
    total_raised_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # 창작자 프로필 필드
    company_name = models.CharField(max_length=100, blank=True)
    business_registration_number = models.CharField(max_length=20, blank=True)
    company_description = models.TextField(blank=True)
    
    balance = models.IntegerField(default=100000)  # 신규 가입자에게 10만원 지급
    
    class Meta:
        db_table = 'user'
        
    def __str__(self):
        return self.username or self.email
        
    def add_points(self, amount, admin_message=''):
        self.points += amount
        self.total_points_received += amount
        PointHistory.objects.create(
            user=self,
            amount=amount,
            balance=self.points,
            transaction_type='receive',
            admin_message=admin_message
        )
        self.save()
        
    def use_points(self, amount):
        if self.points >= amount:
            self.points -= amount
            self.total_points_used += amount
            PointHistory.objects.create(
                user=self,
                amount=amount,
                balance=self.points,
                transaction_type='use'
            )
            self.save()
            return True
        return False

class PointHistory(models.Model):
    TRANSACTION_TYPES = [
        ('receive', '포인트 지급'),
        ('use', '포인트 사용'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    admin_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
