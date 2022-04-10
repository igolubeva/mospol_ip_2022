from django.contrib.auth.models import User, Group
from rest_framework import serializers
from quickstart.models import Advice
from rest_framework.serializers import ValidationError


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class AdviceUserSerializer(serializers.ModelSerializer):
    can_moderate = serializers.SerializerMethodField()
    name = serializers.CharField(source='get_full_name')

    def get_can_moderate(self, obj):
        return obj.has_perm('advice.moderate_advices')

    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'can_moderate')



class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class AdviceSerializer(serializers.ModelSerializer):
    text = serializers.CharField()

    class Meta:
        model = Advice
        fields = ('id', 'text', 'is_published', 'created_at', 'author')


class AdviceRetriveUpdateSerializer(serializers.ModelSerializer):
    text = serializers.CharField()

    class Meta:
        model = Advice
        fields = ('id', 'text', 'is_published', 'created_at', 'author')


class AdviceCreateSerializer(serializers.ModelSerializer):
    text = serializers.CharField()

    class Meta:
        model = Advice
        fields = ('id', 'text', 'is_published', 'created_at', 'author')

    def validate_is_published(self, is_published):
        user = self.context['request'].user
        if is_published and not user.has_perm('advice.moderate_advices'):
            raise ValidationError('Добавлять опубликованные советы могут только модераторы')
        return is_published

