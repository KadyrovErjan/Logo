from rest_framework import permissions

class UserEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id:
            return True
        return False


class CheckUserOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'Владелец':
            return True
        return False

class CheckUserStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'Студент':
            return True
        return False