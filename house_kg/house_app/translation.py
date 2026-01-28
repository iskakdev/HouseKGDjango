from .models import (Region, City,
                     District, Property, Review)
from modeltranslation.translator import TranslationOptions,register


@register(Region)
class ProductTranslationOptions(TranslationOptions):
    fields = ('region_name',)


@register(City)
class ProductTranslationOptions(TranslationOptions):
    fields = ('city_name',)


@register(District)
class ProductTranslationOptions(TranslationOptions):
    fields = ('district_name',)


@register(Property)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'address')
