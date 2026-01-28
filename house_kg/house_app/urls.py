from django.urls import path, include
from .views import (UserProfileListAPIView, UserProfileDetailAPIView,
                    RegionViewSet, CityViewSet, DistrictViewSet,
                    PropertyListAPIView, PropertyDetailAPIView,
                    PropertyCreateAPIView, PropertyEditAPIView,
                    ReviewCreateAPIView, ReviewEditAPIView,
                    RegisterView, CustomLoginView, LogoutView,
                    PredictPrice)
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register(r'regions', RegionViewSet)
router.register(r'cities', CityViewSet)
router.register(r'districts', DistrictViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserProfileListAPIView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('properties/', PropertyListAPIView.as_view(), name='property_list'),
    path('properties/<int:pk>/', PropertyDetailAPIView.as_view(), name='property_detail'),
    path('properties_create/', PropertyCreateAPIView.as_view(), name='property_create'),
    path('properties_create/<int:pk>/', PropertyEditAPIView.as_view(), name='property_edit'),
    path('reviews', ReviewCreateAPIView.as_view(), name='review_create'),
    path('reviews/<int:pk>/', ReviewEditAPIView.as_view(), name='review_edit'),
    path('register/', RegisterView.as_view(), name='register_list'),
    path('login/', CustomLoginView.as_view(), name='login_list'),
    path('logout/', LogoutView.as_view(), name='logout_list'),
    path('predict/', PredictPrice.as_view(), name='predict_price')
]