from django.urls import path, include
from .views import UserRegistrationView, UserLoginView, UserLogoutView, FootballFieldListAPIView,\
                    FootballFieldCreateAPIView, FootballFieldDeleteAPIView, FootballFieldDetailAPIView, FootballFieldUpdateAPIView,\
                    BookingCreateAPIView, BookingDeleteAPIView, BookingDetailAPIView, BookingListAPIView, BookingUpdateAPIView, AvailableFootballFieldsAPIView



urlpatterns = [
    path("api/auth/register/", UserRegistrationView.as_view(), name='registration'),
    path('api/auth/login/', UserLoginView.as_view(), name='login'),
    path('api/auth/logout/', UserLoginView.as_view(), name='logout'),
    path('api/stadium/list', FootballFieldListAPIView.as_view(), name='get-stadium'),
    path('api/stadium/detail/<int:pk>', FootballFieldDetailAPIView.as_view(), name='detail-stadium'),
    path('api/stadium/update/<int:pk>', FootballFieldUpdateAPIView.as_view(), name='update-stadium'),
    path('api/stadium/delete/<int:pk>', FootballFieldDeleteAPIView.as_view(), name='delete-stadium'),
    path('api/stadium/create/', FootballFieldCreateAPIView.as_view(), name='create-stadium'),
    path('api/stadium/book/create', BookingCreateAPIView.as_view(), name='create-booking'),
    path('api/stadium/book/update/<int:pk>', BookingUpdateAPIView.as_view(), name='update-booking'),
    path('api/stadium/book/detail/<int:pk>', BookingDetailAPIView.as_view(), name='delete-booking'),
    path('api/stadium/book/list/', BookingListAPIView.as_view(), name='list-booking'),
    path('api/stadium/book/delete/<int:pk>', BookingDeleteAPIView.as_view(), name='delete-booking'),
    path('api/stadium/book/filter/', AvailableFootballFieldsAPIView.as_view(), name='filter'),
   
 
]