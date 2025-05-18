from django.urls import path,include
from MeetingsAppApi import views




urlpatterns = [
    path('register/', views.RegisterViewset.as_view({'post': 'create'})),
    path('login/', views.LoginViewSet.as_view()),  # If using ObtainAuthToken
    path('Users/',views.UserProfilesApi.as_view()),
    path('Users/<int:pk>/',views.UserProfilesApi.as_view()),
    path('LoggedInUser/',views.LoggedInUser.as_view()),
    path('Meetings/',views.MeetingsAPI.as_view())
]