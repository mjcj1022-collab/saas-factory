from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet, UserViewSet, APIKeyViewSet, RegisterView, LoginView

router = DefaultRouter()
router.register("orgs", OrganizationViewSet, basename="org")
router.register("users", UserViewSet, basename="user")
router.register("api-keys", APIKeyViewSet, basename="apikey")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]
