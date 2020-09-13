from django.contrib.auth.models import User, Group
from rest_framework import serializers
from app import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Invoice
        fields = ['__all__']
