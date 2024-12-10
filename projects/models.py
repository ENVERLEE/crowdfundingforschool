from django.db import models
from django.conf import settings

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('tech', '테크/가전'),
        ('fashion', '패션'),
        ('design', '디자인'),
        ('art', '예술'),
        ('food', '푸드'),
        ('publishing', '출판'),
        ('music', '음악'),
        ('film', '영화/비디오'),
    ]

    STATUS_CHOICES = [
        ('draft', '작성중'),
        ('pending', '심사중'),
        ('active', '진행중'),
        ('successful', '성공'),
        ('failed', '실패'),
    ]

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    target_amount = models.DecimalField(max_digits=15, decimal_places=2)
    current_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    risks = models.TextField()
    thumbnail = models.ImageField(upload_to='projects/thumbnails/')

    def __str__(self):
        return self.title

class Reward(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='rewards')
    title = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    stock = models.IntegerField(default=-1)  # -1 means unlimited
    delivery_date = models.DateField()
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.project.title} - {self.title}"

class Pledge(models.Model):
    supporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_pledges')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pledges')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='pledges')
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.supporter.username} - {self.project.title} - {self.amount}원"
