from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Transaction
from .serializers import TransactionSerializer

from .models import User
from .serializers import (
    PasswordChangeSerializer,
    ReactiveUserSerializer,
    RegisterSerializer,
    TokenPairSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# 쿠키에 토큰을 저장하는 방식의 로그인 뷰
class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data

        # access token을 쿠키에 저장
        access_token = data.get("access")
        refresh_token = data.get("refresh")

        if access_token:
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                max_age=3600,
            )

        if refresh_token:
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                samesite="Lax",
                secure=False,
                max_age=7 * 24 * 3600,
            )

        return response


# 로그아웃 뷰
class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"detail": "Token is invalid or expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    # 프로필 조회
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    # 정보 수정
    def patch(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 회원 탈퇴 (is_active=False로 비활성화 처리)
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(
            {"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


# 비밀번호 변경
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                {"detail": "비밀번호가 변경되었습니다."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReactiveUserView(APIView):
    def post(self, request):
        serializer = ReactiveUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
<<<<<<< HEAD
            return Response({"detail": "계정이 다시 활성화되었습니다."},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   # 거래내역 조회
class TransactionView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(account__user=user)

        t_type = queryset.values_list('transaction_type')
        if t_type:
            queryset = queryset.filter(transaction_type=t_type)

        amount_min = self.request.query_params.get('amount_min')
        amount_max = self.request.query_params.get('amount_max')
        if amount_min:
            queryset = queryset.filter(amount__gte=int(amount_min))
        if amount_max:
            queryset = queryset.filter(amount__lte=int(amount_max))

        account_number = self.request.query_params.get('account_number')
        if account_number:
            queryset = queryset.filter(account_number=account_number)

        return queryset.order_by('-created_at')
=======
            return Response(
                {"detail": "계정이 다시 활성화되었습니다."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
>>>>>>> 8c562c67e1d95bec1382a4073f7b7a15cd223dd1
