from rest_framework.permissions import BasePermission


class IsFieldOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.field.owner == request.user
    
