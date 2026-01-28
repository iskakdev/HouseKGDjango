from django_filters import FilterSet
from .models import Property


class PropertyFilter(FilterSet):
    class Meta:
        model = Property
        fields = {
            'region': ['exact'],
            'city': ['exact'],
            'district': ['exact'],
            'property_type': ['exact'],
            'price': ['gt', 'lt'],
            'area': ['exact'],
            'rooms': ['exact'],
            'floor': ['exact'],
            'condition': ['exact'],
            'documents': ['exact']
        }
