from rest_framework import permissions


class OrderPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # check is user is owner or moderator
        return (request.user == obj.user) or (request.user.role == 'manager')
