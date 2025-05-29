from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Item, Offer
from .serializers import ItemSerializer, OfferSerializer
from .permissions import IsOwnerOrReadOnly, IsOfferParticipant

class ItemListAPIView(generics.ListCreateAPIView):
    queryset = Item.objects.filter(is_active=True)
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.filter(is_active=True)
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class OfferListAPIView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Offer.objects.filter(from_user=user) | Offer.objects.filter(to_user=user)

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

class OfferDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Offer.objects.filter(from_user=user) | Offer.objects.filter(to_user=user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Только получатель может менять статус
        if instance.to_user != request.user:
            return Response(
                {'detail': 'У вас нет прав на изменение этого предложения'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)