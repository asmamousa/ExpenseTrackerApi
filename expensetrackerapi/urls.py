from django.urls import path
from .views import SignUpView, LoginView, ExpensesModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('expenses', ExpensesModelViewSet, basename='expenses')

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='sign-up'),
    path('login/', LoginView.as_view(), name='login'),

]

urlpatterns += router.urls