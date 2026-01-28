from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField()
    RoleChoices = (
        ('seller', 'seller'),
        ('buyer', 'buyer'))
    role = models.CharField(max_length=32, choices=RoleChoices, default='buyer')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Region(models.Model):
    region_name = models.CharField(max_length=64)

    def __str__(self):
        return self.region_name


class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=64)

    def __str__(self):
        return self.city_name


class District(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    district_name = models.CharField(max_length=64)

    def __str__(self):
        return self.district_name


class Property(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    PropertyTypeChoices = (
        ('apartment', 'apartment'),
        ('house', 'house'),
        ('area', 'area'),
        ('commercial real estate', 'commercial real estate')
    )
    property_type = models.CharField(max_length=32, choices=PropertyTypeChoices)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.IntegerField()
    rooms = models.IntegerField()
    floor = models.IntegerField()
    total_floor = models.IntegerField()
    ConditionChoices = (
        ('homemade', 'homemade'),
        ('renovation', 'renovation'),
        ('good', 'good'),
        ('average', 'average'),
        ('unfinished', 'unfinished')
    )
    condition = models.CharField(max_length=32, choices=ConditionChoices)
    documents = models.BooleanField()
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}, {self.description}'

    def get_avg_rating(self):
        reviews = self.property_reviews.all()
        if reviews.exists():
            return round(sum(i.rating for i in reviews) / reviews.count(), 1)
        return 0

    def get_count_people(self):
        reviews = self.property_reviews.all()
        return reviews.count()


class PropertyImages(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_images')
    images = models.ImageField(upload_to='property_images/')


class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_reviews')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_buyer')
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_seller')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment


class House(models.Model):
    GrLivArea = models.IntegerField()
    YearBuilt = models.IntegerField()
    GarageCars = models.IntegerField()
    TotalBsmtSF = models.IntegerField()
    FullBath = models.IntegerField()
    OverallQual = models.IntegerField()
    Neighborhood = models.CharField(max_length=50)
    predicted_price = models.FloatField(null=True, blank=True)
