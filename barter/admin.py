from django.contrib import admin
from .models import Category, Item, Offer, UserProfile

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'condition', 'created_at')
    list_filter = ('category', 'condition', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('owner',)
    date_hierarchy = 'created_at'

class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_item', 'to_item', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    raw_id_fields = ('from_user', 'to_user', 'from_item', 'to_item')
    date_hierarchy = 'created_at'

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'phone', 'location')
    search_fields = ('user__username', 'phone')
    raw_id_fields = ('user',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(UserProfile, UserProfileAdmin)