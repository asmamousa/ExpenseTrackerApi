from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MyUser, Expenses
from django.contrib.auth import authenticate

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'password']

    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return lower_email

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid email or password')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')

        data['user'] = user
        return data


class ExpensesSerializer(serializers.ModelSerializer):
    # We explicitly include the currency if you want the API to show/allow it
    amount_currency = serializers.CharField(source='amount.currency', read_only=True)

    class Meta:
        model = Expenses
        fields = ['id', 'description', 'amount', 'amount_currency', 'category', 'date']
        read_only_fields = ['user']
