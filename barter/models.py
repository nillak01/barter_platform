# barter/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


image = models.ImageField(upload_to='items/', blank=True, null=True)

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Новое'),
        ('used', 'Б/у'),
        ('broken', 'Требует ремонта'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='items/', null=True, blank=True)

    def __str__(self):
        return self.title

class Offer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
        ('completed', 'Завершено'),
    ]

    from_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='outgoing_offers')
    to_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='incoming_offers')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_offers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_offers')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Предложение от {self.from_user} для {self.to_user}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=5.0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"Профиль {self.user.username}"