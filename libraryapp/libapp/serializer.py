from django.contrib.auth.models import User
from libapp.models import bookModel,borrowModel
from rest_framework import serializers

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class bookSerializer(serializers.ModelSerializer):
    class Meta:
        model = bookModel
        fields = '__all__'

class borrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = borrowModel
        fields = '__all__'
        