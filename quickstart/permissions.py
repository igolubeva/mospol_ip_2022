from rest_framework import permissions


class CanModerateAdvices(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['partial_update', 'destroy', 'publish', 'patch']:
            return request.user.has_perm('advice.moderate_advices')
        return True