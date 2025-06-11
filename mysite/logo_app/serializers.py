from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from datetime import timedelta

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']

class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'avatar', 'email']

class HighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlight
        fields = ['id', 'home', 'icon', 'description']

class HomeSerializers(serializers.ModelSerializer):
    highlight = HighlightSerializer()
    class Meta:
        model = Home
        fields = ['id', 'title', 'description', 'image', 'highlight']

class WhyCourseHighlightSerialize(serializers.ModelSerializer):
    class Meta:
        model = WhyCourseHighlight
        fields = ['id', 'highlight_title', 'highlight_icon', 'highlight_description']

class WhyCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyCourse
        fields = ['id', 'title', 'description',  'title_of_number1', 'description_of_number1', 'title_of_number2', 'description_of_number2']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video', 'goal', 'video_time', 'status']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

class CourseDetailSerializer(serializers.ModelSerializer):
    course_lessons = LessonSerializer(many=True, read_only=True)
    category = CategorySerializer()
    class Meta:
         model = Course
         fields = ['id', 'category', 'title', 'description', 'course_lessons']

class CourseCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseListSerializer(serializers.ModelSerializer):
    total_duration = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'brief_description', 'image', 'price', 'status_course', 'total_duration', 'lessons_count', 'is_favorite']

    def get_total_duration(self, obj):
        total = sum((lesson.video_time for lesson in obj.course_lessons.all()), timedelta())
        return str(total)

    def get_lessons_count(self, obj):
        return obj.course_lessons.count()

    def get_is_favorite(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, course=obj).exists()
        return False

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'course']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)

class FavoriteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'course']

class PurchaseCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedCourse
        fields = ['course']

    def validate(self, data):
        user = self.context['request'].user
        course = data['course']
        if PurchasedCourse.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("Курс уже куплен")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return PurchasedCourse.objects.create(user=user, **validated_data)

class UserProfileListSerializer(serializers.ModelSerializer):
    favorites = FavoriteSerializer(many=True, read_only=True)
    purchased_courses = PurchaseCourseSerializer(many=True, read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'avatar', 'role', 'favorites', 'purchased_courses']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['course', 'city', 'region', 'rating', 'comment']
        extra_kwargs = {'user': {'read_only': True}}

class ReviewListSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    class Meta:
        model = Review
        fields = ['id', 'user', 'course', 'city', 'region', 'rating', 'comment']





