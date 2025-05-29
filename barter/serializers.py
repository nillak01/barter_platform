# barter/serializers.py
from rest_framework import serializers
from .models import Item, Offer, UserProfile, User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['rating', 'phone', 'location']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile']

class ItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'title', 'description', 'category', 'condition',
                 'owner', 'created_at', 'updated_at', 'image']
        read_only_fields = ['owner', 'created_at', 'updated_at']

class OfferSerializer(serializers.ModelSerializer):
    from_item = ItemSerializer(read_only=True)
    to_item = ItemSerializer(read_only=True)
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'from_item', 'to_item', 'from_user', 'to_user',
                 'message', 'status', 'created_at', 'updated_at']
        read_only_fields = ['from_user', 'to_user', 'created_at', 'updated_at']