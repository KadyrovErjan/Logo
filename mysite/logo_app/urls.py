from .views import *
from rest_framework import routers
from django.urls import path, include

router = routers.SimpleRouter()
# router.register(r'?', ?ViewSet, basename='?')

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='login'),
    path('home/', HomeAPIView.as_view(), name='home'),
    path('whycourse/', WhyCourseAPIView.as_view(), name='whycourse'),
    path('courses/', CourseListAPIView.as_view(), name='course_list'),
    path('courses/<int:pk>', CourseDetailAPIView.as_view(), name='course_detail'),
    path('courses/create/<int:pk>', CourseEditAPIView.as_view(), name='course_edit'),
    path('courses/buy/', PurchaseCourseAPIView.as_view(), name='purchase-course'),
    path('lesson/create/<int:pk>', LessonEditAPIView.as_view(), name='lesson-edit'),
    path('favorite/create', FavoriteCreateAPIView.as_view(), name='favorite_create'),
    path('favorite/', FavoriteListAPIView.as_view(), name='favorite_list'),
    path('favorites/remove/<int:course_id>/', FavoriteDeleteAPIView.as_view(), name='remove-favorite'),
    path('reviews/create/', ReviewCreateAPIView.as_view(), name='create-review'),
    path('reviews/<int:pk>/', ReviewEditAPIView.as_view(), name='create-edit'),
    path('reviews/', CourseReviewListAPIView.as_view(), name='review_list'),
]
