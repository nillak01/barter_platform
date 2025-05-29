from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение, позволяющее только владельцам объекта редактировать его.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешение на чтение даётся всем (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешение на запись даётся только владельцу объекта
        return obj.owner == request.user


class IsOfferParticipant(permissions.BasePermission):
    """
    Разрешение, позволяющее доступ только участникам обмена (отправителю или получателю предложения).
    """
    def has_object_permission(self, request, view, obj):
        return obj.from_user == request.user or obj.to_user == request.user