from rest_framework import permissions

class IsOwnerReadOnly(permissions.BasePermission): # Update ni faqat ozini akkauntin qilolsin boshqalaniki qilolmidi
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id