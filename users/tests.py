from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


# 회원가입 테스트
class UserRegisterTest(APITestCase):
    def test_user_register_success(self):
        url = reverse("register")
        data = {
            "email": "test@example.com",
            "nickname": "testuser",
            "name": "테스트",
            "phone_number": "01012345678",
            "password": "testpassword1",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())


# 토큰 테스트
class LoginCookieTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="login@example.com", password="testpassword1"
        )

    def test_login_sets_token_cookie(self):
        url = reverse("login")
        response = self.client.post(
            url, {"email": "login@example.com", "password": "testpassword1"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.cookies)
        self.assertIn("refresh_token", response.cookies)

    def test_authenticated_request_using_cookie(self):
        login_url = reverse("login")
        response = self.client.post(
            login_url, {"email": "login@example.com", "password": "testpassword1"}
        )
        access_token = response.cookies.get("access_token").value

        self.client.cookies["access_token"] = access_token

        protected_url = reverse("my_profile")
        response = self.client.get(protected_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "login@example.com")


class UserProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword1",
            nickname="테스트",
            name="홍길동",
            phone_number="01012345678",
            is_active=True,
        )

        login_url = reverse("login")
        response = self.client.post(
            login_url, {"email": "test@example.com", "password": "testpassword1"}
        )

        self.client.cookies["access_token"] = response.cookies.get("access_token").value

    # 프로필 조회
    def test_profile_view(self):
        url = reverse("my_profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["phone_number"], self.user.phone_number)

    # 비밀번호 변경
    def test_password_change(self):
        url = reverse("change_password")
        response = self.client.post(
            url, {"old_password": "testpassword1", "new_password": "testpassword123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("testpassword123"))

    def test_update_profile(self):
        url = reverse("my_profile")
        response = self.client.patch(
            url,
            {
                "nickname": "수정된닉네임",
                "name": "홍길동",
                "phone_number": "01099998888",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.nickname, "수정된닉네임")

    # 허용되지 않은 필드 수정 시도
    def test_invalid_field_update(self):
        url = reverse("my_profile")
        response = self.client.patch(
            url, {"nickname": "새닉네임", "email": "user@example.com"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("허용되지 않은 필드", str(response.data))

    def test_soft_delete_user(self):
        url = reverse("my_profile")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_reactive_user(self):
        self.user.is_active = False
        self.user.save()

        url = reverse("reactive_user")
        response = self.client.post(
            url, {"email": "test@example.com", "password": "testpassword1"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
