# barter/forms.py
from django import forms
from .models import Item, Offer, UserProfile, User
from django.contrib.auth.forms import UserCreationForm


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'condition', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class OfferForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_item'].queryset = Item.objects.filter(owner=user, is_active=True)

    class Meta:
        model = Offer
        fields = ['from_item', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'location', 'avatar']

class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")