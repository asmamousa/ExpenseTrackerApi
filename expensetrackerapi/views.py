from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Expenses
from .serializers import SignUpSerializer, LoginSerializer, ExpensesSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from django.utils.dateparse import parse_date

class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            data={
                'token': str(refresh.access_token)
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response(
            data={
                'token': str(refresh.access_token)
            },
            status=status.HTTP_200_OK
        )


class ExpensesModelViewSet(ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Expenses.objects.filter(user=self.request.user)

        category = self.request.query_params.get('category')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        timeframe = self.request.query_params.get('timeframe')
        now = timezone.now()

        if category:
            queryset = queryset.filter(category=category)
        if timeframe:
            if timeframe == 'week':
                queryset = queryset.filter(date__gte=now - timedelta(days=7))
            elif timeframe == 'month':
                queryset = queryset.filter(date__gte=now - timedelta(days=30))
            elif timeframe == '3months':
                queryset = queryset.filter(date__gte=now - timedelta(days=90))

        else:
            if start_date and end_date:
                queryset = queryset.filter(date__range=[start_date, end_date])
            elif start_date:
                queryset = queryset.filter(date__gte=start_date)
            elif end_date:
                queryset = queryset.filter(date__lte=end_date)

        return queryset.order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


