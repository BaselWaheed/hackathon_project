from rest_framework import serializers
from .models import Place , Category





class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id' , 'cat_name']





class PlaceSerializers(serializers.ModelSerializer):
    category = CategorySerializers()
    class Meta:
        model = Place
        fields = ['id' , 'place_name' ,'governorate' , 'category']