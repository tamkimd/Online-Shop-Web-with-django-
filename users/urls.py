from rest_framework import routers
from django.urls import path, include
from .views import UserViewSet,RoleViewSet,MyTokenObtainPairView

router = routers.DefaultRouter()

router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login', MyTokenObtainPairView.as_view(), name='token_obtain_pair')
]