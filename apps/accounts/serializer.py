from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
  """ Сериализватор для регистрации пользователя """
  password = serializers.CharField(
    write_only=True,
    validators=[validate_password]
  )
  password_confirm = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = (
      'email', 'first_name', 'last_name',
      'username', 'password_confirm', 'password'
    )

  def validate(self, attrs):
    if attrs['password'] != attrs['password_confirm']:
      return serializers.ValidationError(
        {'password': 'Password fields didnt, match.'}
      )
    return attrs
  
  def create(self, validated_data):
    validated_data.pop('password_confirm')
    user = User.objects.create_user(**validated_data)
    return user


class UserLoginSerializer(serializers.Serializer):
  """ Сериализатор для входа пользователя """
  email = serializers.EmailField()
  password = serializers.CharField(write_only=True)

  def validate(self, attrs):
    email = attrs.get('email')
    password = attrs.get('password')
    if email and password:
      user = authenticate(
        request = self.context.get('request'),
        username = email,# Передаем email в качестве имени
        password = password
      )
      if not user:
        raise serializers.ValidationError(
            'User not found.'
          )
      if not user.is_active:
        raise serializers.ValidationError(
            'User account is disabled.'
          )
      attrs['user'] = user
      return attrs
    else:
      raise serializers.ValidationError(
        'Must include "email" and "password".'
      )


class UserProfileSerializer(serializers.ModelSerializer):
  """ Сериализация для профиля пользователя """
  full_name = serializers.ReadOnlyField()
  posts_count = serializers.SerializerMethodField()
  comments_count = serializers.SerializerMethodField()
  
  class Meta:
    model = User
    fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'avatar', 'bio', 'created_at', 'updated_at',
            'posts_count', 'comments_count'
        )
    read_only_fields = ('id', 'created_at', 'updated_at')

  def get_post_count(self, obj):
    return obj.posts.count()
  
  def get_comments_count(self, obj):
    return obj.pcomments.count()


class UserUpdateSerializer(serializers.ModelSerializer):
  """ Сериализвтор для обновления профиля пользователя """

  class Meta:
    model = User
    fields = (
      'first_name', 'last_name', 'avatar', 'bio'
    )
  
  def update(self, instance, validated_data):
    for attrs, value in validated_data.items():
      setattr(instance, attrs, value)
    instance.save()
    return instance


class ChangePasswordSerializer(serializers.Serializer):
  """Сериализатор для смены пароля"""
  old_password = serializers.CharField(required=True)
  new_password = serializers.CharField(
      required=True,
      validators=[validate_password]
  )
  new_password_confirm = serializers.CharField(required=True)
  
  def validate_old_password(self, value):
    user = self.context['request'].user
    if not user.check_password(value):
      raise serializers.ValidationError(
        'Old password is incorrect.'
      )
    return value
  
  def validate(self, attrs):
    if attrs('new_passeord') != attrs['new_passeord_confirm']:
      raise serializers.ValidationError(
        {'new_passeord': 'Passwoed fields didnt match'}
      )
    return attrs
  
  def save(self):
    user = self.context['request'].user
    user.set_password(self.validated_data['new_password'])
    user.save()
    return user
