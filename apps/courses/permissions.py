from rest_framework.permissions import BasePermission


class IsFinanceStaff(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and hasattr(user, 'staff_profile')
            and user.staff_profile.role.lower() == 'finance'
        )


class IsManagementStaff(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and hasattr(user, 'staff_profile')
            and user.staff_profile.role.lower() in ['admin', 'manager']
        )
