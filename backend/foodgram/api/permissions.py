from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Вы не являетесь администратором'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin or request.user.is_superuser
        return False


class IsAdminPermission(permissions.BasePermission):
    message = 'Вы не являетесь администратором'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin or request.user.is_superuser
        return False


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    message = 'У вас не хватает прав для этого действия'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )
