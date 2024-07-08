from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


app_name = 'api'

router = DefaultRouter()
router.register(r'entries', EntryViewSet, basename='entry')

urlpatterns = router.urls

urlpatterns += [
  path('listcontainers/', ContainerListView.as_view(), name='container-list'),
  path('createcontainer/', ContainerCreateView.as_view(), name='create-container'),
  path('signup/', SignupView.as_view(), name='signup'),
  path('login/', LoginView.as_view(), name='login'),
  path('user/', UserView.as_view(), name='user-detail'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
  path('deletecontainer/<int:pk>/', ContainerDeleteView.as_view(), name='delete-container'),
  path('editcontainer/<int:pk>/', EditContainerView.as_view(), name='edit-container'),
]         