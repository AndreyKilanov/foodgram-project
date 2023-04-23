from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    message = 'У вас не хватает прав для этого действия'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or obj.author == request.user)
