from rest_framework import permissions


# Custom permissions classes
class UdateOwmProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True
        # if the user is trying to update, put or delete(It will check the user and it request is matching or not)
        return obj.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    """Allow user to update their own status"""
    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_profile.id == request.user.id
