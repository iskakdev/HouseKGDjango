from rest_framework import serializers
from .models import (UserProfile, Region, City, District,
                     Property, PropertyImages, Review, House)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name']


class UserProfileDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'created_date']


class UserProfileNameSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class RegionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'region_name']


class CitySerializers(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name']


class DistrictSerializers(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'district_name']


class PropertyImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = PropertyImages
        fields = ['images']


class PropertyListSerializers(serializers.ModelSerializer):
    city = CitySerializers()
    property_images = PropertyImageSerializers(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ['id', 'price', 'city', 'property_images',
                  'property_type', 'area', 'floor', 'total_floor']


class PropertyCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'title', 'description', 'property_type', 'region',
                  'city', 'district', 'address', 'area', 'price', 'rooms',
                  'floor', 'total_floor', 'condition', 'documents', 'seller',
                  'created_date']


class ReviewSerializers(serializers.ModelSerializer):
    user_buyer = UserProfileNameSerializers(many=True, read_only=True)
    user_seller = UserProfileNameSerializers(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user_buyer', 'user_seller', 'rating',
                  'comment', 'created_date']


class ReviewCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class PropertyDetailSerializers(serializers.ModelSerializer):
    region = RegionSerializers()
    city = CitySerializers()
    district = DistrictSerializers()
    property_reviews = ReviewSerializers(many=True, read_only=True)
    get_avg_rating = serializers.ModelSerializer()
    get_count_people = serializers.ModelSerializer()

    class Meta:
        model = Property
        fields = ['id', 'area', 'title', 'get_avg_rating', 'get_count_people',
                  'address', 'created_date', 'region', 'city',
                  'district', 'seller', 'floor', 'total_floor',
                  'condition', 'documents', 'description', 'rooms', 'property_reviews']

    def get_avg_rating(self, obj):
        return obj.get_avg_ratig()

    def get_count_people(self, obj):
        return obj.get_count_people()


class HousePredictSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'
