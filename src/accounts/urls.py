from rest_framework import routers
from django.urls import path, include
from .views import UserViewSet, GroupViewSet, PermissionViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'permissions', PermissionViewSet)

from .views import UserSignUpView, UserSignIpView

urlpatterns = [
    path('api/', include(router.urls)),
    path('signup/', UserSignUpView.as_view()),
    path('signin/', UserSignIpView.as_view())
]