from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "nickname", "name", "phone_number", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            nickname=validated_data["nickname"],
            name=validated_data["name"],
            phone_number=validated_data.get("phone_number", ""),
            password=validated_data["password"],
        )
        return user


class TokenPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )

        if not user:
            raise serializers.ValidationError("이메일 또는 비밀번호가 잘못되었습니다.")
        if not user.is_active:
            raise serializers.ValidationError("탈퇴한 계정입니다.")

        refresh = self.get_token(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_name": user.name,
        }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_name"] = user.name
        return token


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "nickname", "name", "phone_number")


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("nickname", "name", "phone_number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.partial:
            allowed_fields = set(self.fields.keys())
            received_fields = set(self.initial_data.keys())

            extra_fields = received_fields - allowed_fields
            if extra_fields:
                raise serializers.ValidationError(
                    {
                        "non_field_errors": [
                            f"허용되지 않은 필드 포함: {', '.join(extra_fields)}"
                        ]
                    }
                )


# 비밀번호 변경
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("현재 비밀번호가 올바르지 않습니다.")
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value


# 탈퇴 회원 복구


class ReactiveUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # 이메일 단일 필드 검증: 형식 검증만 필요하면 생략 가능
    def validate_email(self, value):
        return value

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "해당 이메일의 사용자가 존재하지 않습니다."}
            )

        if user.is_active:
            raise serializers.ValidationError({"email": "이미 활성화된 계정입니다."})

        if not user.check_password(password):
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."}
            )

        self.user = user  # save에서 사용할 사용자 객체 저장
        return attrs

    def save(self):
        self.user.is_active = True
        self.user.save()
        return self.user
