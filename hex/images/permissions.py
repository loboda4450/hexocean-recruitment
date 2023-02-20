from rest_framework.permissions import BasePermission, SAFE_METHODS


class HasImagePermission(BasePermission):
    """Check whether user is authenticated and have valid image permissions or not"""
    message = 'You have to upgrade your account tier first'

    def has_permission(self, request, view):
        return all(key in request.user.get_all_permissions()
                   for key in ('images.add_image', "images.delete_image", 'images.view_image')) and \
            bool(request.user and request.user.is_authenticated)


class ReadOnly(BasePermission):
    """Grant readonly privileges to non-authicanted users"""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

