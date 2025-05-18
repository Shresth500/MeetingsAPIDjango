from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status # For status Codes
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from MeetingsAppApi import permissions
from MeetingsAppApi import models
from MeetingsAppApi import serializers

# Create your views here.

class RegisterViewset(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email')

class LoginViewSet(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfilesApi(APIView):
    serializers_class = serializers.UserProfileSerializer
    permission_classes = (permissions.UpdateOwnProfile,IsAuthenticatedOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email')

    def get(self,request,pk=None,format=None):
        if pk is None:
            users = models.UserProfile.objects.all()
            serializers = self.serializers_class(users,many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)
        
        user = models.UserProfile.objects.get(pk = pk)
        serializers = self.serializers_class(user)
        return Response(serializers.data, status=status.HTTP_200_OK)

class LoggedInUser(APIView):
    serializers_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self,request,format=None):
        serializer = self.serializers_class(request.user)
        return Response(serializer.data,status = status.HTTP_200_OK)
    

class MeetingsAPI(APIView):
    serializers_classes = (serializers.Meetings,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self,request,format=None):
        user = request.user
        meetings = models.Meetings.objects.filter(User = user)
        meeting_name = request.GET.get('name')
        if meeting_name:
            meetings = meetings.filter(Name__icontains=meeting_name)

        serializer = self.serializers_classes[0](meetings, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        data = request.data.copy()

        user_id = request.user.id
        if not user_id:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Ensure attendee_ids is a list and add the logged-in user
        attendee_ids = data.get('attendee_ids', [])
        if isinstance(attendee_ids, str):
            attendee_ids = [attendee_ids]
        if isinstance(attendee_ids, list):
            attendee_ids.append(str(user_id))
        else:
            attendee_ids = [str(user_id)]

        data['attendee_ids'] = attendee_ids

        serializer = self.serializers_classes[0](data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
