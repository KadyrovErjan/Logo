from .serializers import *
from .models import *
from rest_framework import status, viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from .permissions import UserEdit, CheckUserOwner, CheckUserStudent

class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(generics.GenericAPIView):
    serializer_class = CustomLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'detail': 'Невалидный токен'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class UserProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticated, UserEdit]

class HomeAPIView(generics.ListAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializers

class WhyCourseAPIView(generics.ListAPIView):
    queryset = WhyCourse.objects.all()
    serializer_class = WhyCourseSerializer


class TitleForCourseAPIView(generics.ListAPIView):
    queryset = TitleForCourse.objects.all()
    serializer_class = TitleCourseSerializer


class TitleForReviewAPIView(generics.ListAPIView):
    queryset = TitleForReview.objects.all()
    serializer_class = TitleForReviewSerializer

class EmailTitleAPIView(generics.ListAPIView):
    queryset = EmailTitle.objects.all()
    serializer_class = EmailTitleSerializer

class TitleCourseAPIView(generics.ListAPIView):
    queryset = TitleCourse.objects.all()
    serializer_class = TitleCourseSerializer

class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer

class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseCreateSerializers
    permission_classes = [permissions.IsAuthenticated, CheckUserOwner]


class CourseEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializers
    permission_classes = [permissions.IsAuthenticated, CheckUserOwner]

class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonCreateSerializer
    permission_classes = [permissions.IsAuthenticated, CheckUserOwner]


class LessonEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonCreateSerializer
    permission_classes = [permissions.IsAuthenticated, CheckUserOwner]

class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

class FavoriteListAPIView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteListSerializer

class FavoriteCreateAPIView(generics.CreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated, CheckUserStudent]

class FavoriteDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, CheckUserStudent]

    def delete(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        favorite = Favorite.objects.filter(user=request.user, course_id=course_id).first()
        if favorite:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Избранное не найдено"}, status=status.HTTP_404_NOT_FOUND)


class PurchaseCourseAPIView(generics.CreateAPIView):
    serializer_class = PurchaseCourseSerializer
    permission_classes = [permissions.IsAuthenticated, CheckUserStudent]


class CourseReviewCreateAPIView(generics.CreateAPIView):
    queryset = CourseReview.objects.all()
    serializer_class = CourseReviewSerializer
    permission_classes = [permissions.IsAuthenticated, CheckUserStudent]


    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError("Вы уже оставили отзыв для этого курса.")

class CourseReviewListAPIView(generics.ListAPIView):
    queryset = CourseReview.objects.all()
    serializer_class = CourseReviewListSerializer

class LessonReviewCreateAPIView(generics.CreateAPIView):
    queryset = LessonReview.objects.all()
    serializer_class = LessonReviewSerializer
    permission_classes = [permissions.IsAuthenticated, CheckUserStudent]


    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError("Вы уже оставили отзыв для этого курса.")

class LessonReviewListAPIView(generics.ListAPIView):
    queryset = LessonReview.objects.all()
    serializer_class = LessonReviewListSerializer

class EmailCreateAPIView(generics.CreateAPIView):
    serializer_class = EmailCreateSerializer

# class OwnerListSerializer(generics.ListAPIView):
#     queryset = UserProfile.objects.all()



