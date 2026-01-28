from rest_framework import serializers
from .models import (UserProfile, Region, City, District, Property, PropertyImages, Review)
from .serializers import (UserProfileListSerializer, UserProfileDetailSerializers,
                          PropertyListSerializers, PropertyDetailSerializers,
                          ReviewCreateSerializers, RegionSerializers,
                          CitySerializers, DistrictSerializers, PropertyCreateSerializers,
                          UserSerializer, LoginSerializer, HousePredictSerializer)
from rest_framework import viewsets, generics, status, views
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PropertyFilter
from .pagination import PropertyPagination
from .permission import CreatePropertyPermission, CreateReviewPermission
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
import joblib
from django.conf import settings
import os

scaler_path = os.path.join(settings.BASE_DIR, 'scaler.pkl')
scaler = joblib.load(scaler_path)

model_path = os.path.join(settings.BASE_DIR, 'model.pkl')
model = joblib.load(model_path)

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


Neighborhoods = [
    'Blueste', 'BrDale', 'BrkSide', 'ClearCr', 'CollgCr', 'Crawfor', 'Edwards',
    'Gilbert', 'IDOTRR', 'MeadowV', 'Mitchel', 'NAmes', 'NPkVill', 'NWAmes',
    'NoRidge', 'NridgHt', 'OldTown', 'SWISU', 'Sawyer', 'SawyerW', 'Somerst',
    'StoneBr', 'Timber', 'Veenker'
]


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class UserProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializers

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializers


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializers


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializers


class PropertyListAPIView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyListSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['title']
    ordering_fields = ['price', 'created_date', 'area']
    pagination_class = PropertyPagination


class PropertyDetailAPIView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializers


class PropertyCreateAPIView(generics.CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyCreateSerializers
    permission_classes = [CreatePropertyPermission]

    def get_queryset(self):
        return Property.objects.filter(seller=self.request.user)


class PropertyEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyCreateSerializers
    permission_classes = [CreatePropertyPermission]

    def get_queryset(self):
        return Property.objects.filter(seller=self.request.user)


class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializers

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user)


class ReviewEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializers

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user)


class PredictPrice(views.APIView):
    def post(self, request):
        serializer = HousePredictSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            new_neighborhood = data.get('Neighborhood')
            neighborhood1or_0 = [1 if new_neighborhood == i else 0 for i in Neighborhoods]

            features = [
                data['GrLivArea'],
                data['YearBuilt'],
                data['GarageCars'],
                data['TotalBsmtSF'],
                data['FullBath'],
                data['OverallQual'],
            ] + neighborhood1or_0
            scaled_data = scaler.transform([features])
            pred = model.predict(scaled_data)[0]
            house = serializer.save(predicted_price=round(pred))

            return Response({'Predict Price': round(pred), 'data': HousePredictSerializer(house).data}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)