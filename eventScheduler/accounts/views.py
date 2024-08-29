from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import UserProfileSerializer


class UserProfileListCreateView(ListCreateAPIView):
    """
    List all user profiles or create a new user profile.
    Only authenticated users can create a new user profile.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Associate the user profile with the authenticated user when creating a new user profile.
        """
        user = self.request.user
        serializer.save(user=user)


class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user profile.
    Only authenticated users can update or delete a user profile
    and only the owner of the profile can update or delete it.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]
