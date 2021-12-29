# from typing_extensions import Required
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from .utils import send_activation_code

User = get_user_model()

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(
        min_length=4, required=True
    )
    name = serializers.CharField(required=True)
    last_name = serializers.CharField()

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже зарегистрирован"
            )
        return email

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError(
                "Пароль не совпадает"
            )
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code(
            user.email, user.activation_code
        )
        return user


class ActivationSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        if not User.objects.filter(
            email=email, activation_code=code
        ).exists():
            raise serializers.ValidationError(
            "Пользователь не найден"
        )
        return data
    

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(
            email=email
        ).exists():
            raise serializers.ValidationError(
                "Пользователь не найден"
            )
        return email

    def validate(self, data):
        request = self.context.get('request')
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(
                username=email,
                password=password,
                request=request
            )
            if not user:
                raise serializers.ValidationError(
                    'Неверный email или пароль'
                )
        else:
            raise serializers.ValidationError(
                "Email и пароль обязательно указать"
            )

        data['user'] = user
        
        return data



        
