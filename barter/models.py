# barter/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


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


class ItemImage(models.Model):
    """
    Модель для хранения изображений товаров.
    Поддерживает несколько изображений для одного товара.
    """
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар'
    )
    image = models.ImageField(
        upload_to='items/images/%Y/%m/%d/',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])
        ],
        verbose_name='Изображение'
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name='Основное изображение'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    thumbnail = ProcessedImageField(
        upload_to='items/thumbnails/',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 80},
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['item', 'is_primary']),
            models.Index(fields=['order']),
        ]

    def __str__(self):
        return f"Изображение #{self.id} для {self.item.name}"

    def save(self, *args, **kwargs):
        """
        Автоматически устанавливает is_primary=False для других изображений товара,
        если текущее изображение помечено как основное.
        """
        if self.is_primary:
            ItemImage.objects.filter(item=self.item).exclude(id=self.id).update(is_primary=False)
        super().save(*args, **kwargs)

    @property
    def thumbnail_url(self):
        """
        Возвращает URL миниатюры изображения (можно реализовать с помощью sorl-thumbnail или django-imagekit)
        """
        return self.image.url



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