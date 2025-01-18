from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from dimpro.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

router = routers.DefaultRouter()
# router.register(r'tomates', TomateViewSet)
router.register(r'products', ProductViewSet)
router.register(r'contacts',ContactViewSet)
router.register(r'orders',OrderViewSet)
router.register(r'users', UserViewSet)
router.register(r'staff', StaffViewSet, basename="staff")


urlpatterns = [
    path("", include(router.urls)),
    path("login/", UserLoginView.as_view()),
    path("user", UserProfileView.as_view()),
    path("register", UserRegistrationView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]