from rest_framework import serializers
from django.utils import timezone
from .models import SubscriptionPlan, Subscription, PinnedPost, SubscriptionHistory

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """Сериализатор для тарифных планов"""

    class Meta:
        model = SubscriptionPlan
        fields = (
            'id', 'name', 'price', 'duration_days', 'features',
            'is_active', 'created_at'
        )
        read_only_fields = ('id', 'created_at')

    def to_representation(self, instance):
        """ Переопределения для гарантии корректного вывода"""
        data = super().to_representation(instance)

        #! Убедится что feauters - это объект
        if not data.get('fuatures'):
          data['features'] = {}

        return data


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки"""
    plan_info = SubscriptionPlanSerializer(source='plan', read_only=True)
    user_info = serializers.SerializerMethodField()
    is_active = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()

    class Meta:
        model = Subscription
        fields = (
            'id', 'user', 'user_info', 'plan', 'plan_info', 'status',
            'start_date', 'end_date', 'auto_renew', 'is_active',
            'days_remaining', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'user', 'status', 'start_date', 'end_date',
            'created_at', 'updated_at'
        )

    def get_user_info(self, obj):
      """ Возращает информацию о пользователе """
      return {
        'id': obj.user.id,
        'username': obj.user.username,
        'full_name': obj.user.full_name,
        'email': obj.user.email,
      }


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания подписки"""

    class Meta:
        model = Subscription
        fields = ('plan',)

    def validate_plan(self, value):
        """ Валидация тарифного плана """
        if not value.is_active:
          raise serializers.ValidationError(
            "Selected plan is not active."
          )
        return value

    def validate(self, attrs):
       """ Обзая валидация  """
       user = self.context['request'].user

       #! Проверяем есть ли активная подписка
       if hasattr(user, 'subscription') and user.subscription.is_active():
         raise serializers.ValidationError({
           'non_field_errors': ['User already has active subscription.']
         })

       return attrs

    def create(self, validated_data):
       """ Создает подписку """
       validated_data['user'] = self.context['request'].user
       validated_data['status'] = 'panding'
       validated_data['start_date'] = timezone.now()
       validated_data['end_date'] = timezone.now()
       return super().create(validated_data)


class PinnedPostSerializer(serializers.ModelSerializer):
    """Сериализатор для закрепленного поста"""
    post_info = serializers.SerializerMethodField()

    class Meta:
        model = PinnedPost
        fields = ['id', 'post', 'post_info', 'pinned_at']
        read_only_fields = ['id', 'pinned_at']

    def get_post_info(self, obj):
      """ Возращает ифнормацию о посте """
      return{
        "id": obj.post.id,
        "title": obj.post.title,
        "slug": obj.post.slug,
        "content": obj.post.content,
        "image": obj.post.image,
        "views_count": obj.post.views_count,
        "created_at": obj.post.created_at,
      }

    def validate_post(self, value):
      """ Валидация поста для закрепления """
      user = self.context['request'].user

      #! Проверям, что пост принадлежит пользователю
      if value.author != user:
        raise serializers.ValidationError(
          "You can only pinned your posts"
        )

      #! Проверяем что пост опублекован
      if value.status != 'published':
        raise serializers.ValidationError(
          "Only published post be pinned"
        )
      return value

    def validate(self, attrs):
      user = self.context['request'].user

      #! Проверяем есть ли активная подписка
      if not hasattr(user, 'subscription') or not user.subscription.is_active:
        raise serializers.ValidationError({
          'non_field_errors': ['Active subscription required to pin posts.']
        })
      return attrs

    def create(self, validated_data):
      """ Создает закрепленный пост """
      validated_data['user'] = self.context['request'].user
      return super().create(validated_data)


class SubscriptionHistorySerializer(serializers.ModelSerializer):
    """Сериализатор для истории подписки"""

    class Meta:
        model = SubscriptionHistory
        fields = [
            'id', 'action', 'description', 'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserSubscriptionStatusSerializer(serializers.Serializer):
    """Сериализатор для статуса подписки пользователя"""
    has_subscription = serializers.BooleanField()
    is_active = serializers.BooleanField()
    subscription = SubscriptionSerializer(allow_null=True)
    pinned_post = PinnedPostSerializer(allow_null=True)
    can_pin_posts = serializers.BooleanField()

    def to_representation(self, instance):
       """ Формирует ответ с информацие о подписке пользователя """
       user = isinstance
       has_subsription = hasattr(user, 'subsription')
       subsription = user.subsription if has_subsription else None
       is_active = subsription.is_active if subsription else False
       pinned_post = getattr(user, 'pinned_post', None) if is_active else None
       return {
        'has_subsription': has_subsription,
        'is_active': is_active,
        'subsription': SubscriptionSerializer(subsription).data if subsription else None,
        'pinned_post': PinnedPostSerializer(pinned_post).data if pinned_post else None,
        'can_pin_post': is_active,
       }


class PinPostSerializer(serializers.Serializer):
    """Сериализатор для закрепления поста"""
    post_id = serializers.IntegerField()

    def validate_post(self, value):
      """ Валидация ID поста """
      from apps.main.models import Post

      try:
        post = Post.objects.get(id=value, status='published')
      except Post.DoesNotExist:
        raise serializers.ValidationError(
          'Post not found or not published'
        )
      user = self.context['request'].user
      if post.author != user:
        raise serializers.ValidationError(
          'You can only pin your own posts'
        )
      return value

    def validate(self, attrs):
      """Общая валидация"""
      user = self.context['request'].user

      #! Проверяем подписка
      if hasattr(user, 'subscription') or not user.subscription.is_actve:
        raise serializers.ValidationError({
          'non_field_errors':['Active subscription required to pin posts.']
        })
      return attrs


class UnpinPostSerializer(serializers.Serializer):
    """Сериализатор для открепления поста"""
    def validate(self, attrs):
      user = self.context['request'].user

      if not hasattr(user, 'pinned_post'):
        raise serializers.ValidationError({
          'non_field_errors': ['No pinned post found.']
        })
      return attrs
