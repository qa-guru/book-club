from typing import Any

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from clubs.api.v1.filters import ClubFilter
from clubs.api.v1.serializers import ClubSerializer, BookReviewSerializer
from clubs.models import Club, BookReview


User = get_user_model()


class IsClubOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Club) -> bool:
        return obj.owner == request.user


class ClubViewSet(ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = ClubFilter

    permission_classes_by_action: dict[str, list[type[permissions.BasePermission]] | Any] = {
        "create": [permissions.IsAuthenticated],
        "update": [IsClubOwner],
        "partial_update": [IsClubOwner],
        "destroy": [IsClubOwner],
    }

    def get_permissions(self) -> list[permissions.BasePermission]:
        try:
            permission_classes = self.permission_classes_by_action[self.action]
        except KeyError:
            permission_classes = self.permission_classes

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer: BaseSerializer) -> None:
        club = serializer.save(owner=self.request.user)
        club.members.add(self.request.user)
        return club

    @extend_schema(methods=["POST"], request=None, responses={204: None})
    @extend_schema(methods=["DELETE"], request=None, responses={204: None})
    @action(detail=True, methods=["POST", "DELETE"], url_path="members/me")
    def manage_membership(self, request: Request, pk: int | None = None) -> Response:
        club = self.get_object()

        if request.method == "POST":
            if request.user in club.members.all():
                return Response({"detail": "User is already a member of this club."}, status=status.HTTP_400_BAD_REQUEST)
            club.members.add(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.method == "DELETE":
            if club.owner == request.user:
                return Response({"detail": "Club owner cannot leave the club."}, status=status.HTTP_400_BAD_REQUEST)

            if request.user not in club.members.all():
                return Response({"detail": "User is not a member of this club."}, status=status.HTTP_400_BAD_REQUEST)

            club.members.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReviewViewSet(ModelViewSet):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]