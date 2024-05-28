from rest_framework.permissions import BasePermission


class IsUserAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_net_admin)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsRepairMan(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_net_repair)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsUserOperator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_net_operator)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)



