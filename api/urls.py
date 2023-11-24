from django.urls import path

from api import views


urlpatterns = [
    path('advertisements/', views.AdvertisementsApiView.as_view()),
    path('advertisements/<slug:category>/', views.AdvertisementsApiView.as_view()),
    
    path('advertisement/<int:pk>/', views.AdvertisementView.as_view()),
    path('advertisement/create/', views.AdvertisementCreateAPIView.as_view()),
    path('advertisement/manage/<int:advertisement_id>/', views.AdvertisementUpdateDesroyAPIView.as_view()),
    
    path('request/add/<int:advertisement_id>/', views.AddRequestView.as_view()),
    path('requests/', views.RequestListAPIView.as_view()),
    
    path('request/<int:advertisement_id>/', views.RequestListAPIView.as_view()),
    path('request/confirm/<int:request_id>/', views.ConfirmRequestView.as_view()),
    
    path('register/', views.UserRegisterView.as_view()),
]