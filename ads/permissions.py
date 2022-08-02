from django.http import Http404
from rest_framework.permissions import BasePermission

from ads.models import AdModel, Selection
from users.models import User


class SelectionUpdatePermission(BasePermission):
    message = 'Managing others selection not permitted'

    def has_permission(self, request, view):
        try:
            entity = Selection.objects.get(pk=view.kwargs["pk"])
        except Selection.DoesNotExist:
            raise Http404
        if entity.owner_id == request.user.id:
            return True
        return False


class AdUpdatePermission(BasePermission):
    message = 'Managing others ads not permitted'

    def has_permission(self, request, view):
        if request.user.role in [User.MEMBER, User.ADMIN]:
            return True
        try:
            entity = AdModel.objects.get(pk=view.kwargs["pk"])
        except AdModel.DoesNotExist:
            raise Http404
        if entity.author_id == request.user.id:
            return True
        return False
