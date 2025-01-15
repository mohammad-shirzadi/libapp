from django.contrib.auth.models import User
from libapp.models import bookModel,borrowModel
from rest_framework import serializers

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class bookSerializer(serializers.ModelSerializer):
    class Meta:
        model = bookModel
        fields = '__all__'

class borrowSerializer(serializers.Serializer):
    borrowID = serializers.IntegerField()
    Bbook = bookSerializer()
    Buser = userSerializer()
    borrowdate = serializers.DateField()
    returndate = serializers.DateField()