from rest_framework import permissions

from users.models import UserRoles


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAmdinOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return bool(request.user.is_admin)


class WriteAdmin(permissions.BasePermission):
    '''POST, PUT, PATCH, DEL только для admin'''
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return (
                request.user.is_authenticated
                and request.user.is_admin
            )

        return True


class WriteOwnerOrPersonal(permissions.BasePermission):
    '''Создают авторизованные, редактируют только владельцы или персонал'''
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return (
                request.user.is_authenticated
                and (
                    request.user == obj.author
                    or request.user.role in [
                        UserRoles.MODERATOR, UserRoles.ADMIN
                    ]
                )
            )

        return True
