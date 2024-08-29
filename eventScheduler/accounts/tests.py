from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import UserProfile


# test the user registration endpoint
class RegistrationTestCase(APITestCase):
    """
    Test case for user registration endpoint using djoser endpoint /auth/users/ .
    """

    def test_registration(self):
        """
        Test for user registration with valid data.
        """
        data = {
            "username": "lynn",
            "password": "PASwwordLit",
            "email": "lynn@gmail.com",
        }
        response = self.client.post("/auth/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# test case for the userprofile model
class UserProfileTestCase(APITestCase):
    """
    Test case for the UserProfile model.
    """
    profile_list_url = reverse("all-profiles")

    def setUp(self):
        """
        Create a new user and obtain a json web token for the user.
        """
        # create a new user making a post request to djoser endpoint
        self.user = self.client.post(
            "/auth/users/", data={"username": "mario", "password": "i-keep-jumping"}
        )
        # obtain a json web token for the newly created user
        response = self.client.post(
            "/auth/jwt/create/",
            data={"username": "mario", "password": "i-keep-jumping"},
        )
        self.token = response.data["access"]
        self.api_authentication()

    def api_authentication(self):
        """
        Authenticate the user using the obtained token.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    # retrieve a list of all user profiles while the request user is authenticated
    def test_userprofile_list_authenticated(self):
        """
        Test to retrieve a list of all user profiles while the request user is authenticated.
        """
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # retrieve a list of all user profiles while the request user is unauthenticated
    def test_userprofile_list_unauthenticated(self):
        """
        Test to retrieve a list of all user profiles while the request user is unauthenticated.
        """
        self.client.force_authenticate(user=None)
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # check to retrieve the profile details of the authenticated user
    def test_userprofile_detail_retrieve(self):
        """
        Test to retrieve the profile details of the authenticated user.
        """
        response = self.client.get(reverse("profile", kwargs={"pk": 1}))
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # populate the user profile that was automatically created using the signals
    def test_userprofile_profile(self):
        """
        Test to populate the user profile that was automatically created using the signals.
        """
        profile_data = {
            "description": "I am a very famous game character",
            "location": "nintendo world",
            "is_creator": "true",
        }
        response = self.client.put(
            reverse("profile", kwargs={"pk": 1}), data=profile_data
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
