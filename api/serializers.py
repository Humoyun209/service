from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Advertisement, Category, Request


class RequestCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    advertisement = serializers.PrimaryKeyRelatedField(queryset=Advertisement.objects.all())
    
    class Meta:
        model = Request
        fields = ['id', 'user', 'advertisement']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class AdvertisementSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField('username', queryset=User.objects.all())
    category = CategorySerializer()

    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'image', 'author', 'category']


class AdWithRequestSerializer(serializers.ModelSerializer):
    requests = RequestCreateSerializer(many=True)

    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'image', 'requests']


class AdvertisementForManageSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField('name', queryset=Category.objects.all())
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'image', 'category', 'author']
    
    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



