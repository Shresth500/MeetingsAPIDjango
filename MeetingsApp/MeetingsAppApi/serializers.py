from rest_framework import serializers
from MeetingsAppApi import models

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id','name','email','password')
        extra_kwargs = {
            'password':{
                'write_only':True,
                'style': {'input_type':'password'}
            }
        }

    # Overriding the default create method of serializers.ModelSerializer

    def create(self,validated_data):
        user = models.UserProfile.objects.create_user(
            name = validated_data['name'],
            email = validated_data['email'],
            password = validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)

class Meetings(serializers.ModelSerializer):
    """Serializing an Attendee model"""
    attendee_ids = serializers.PrimaryKeyRelatedField(
        source='User',  # related_name on ManyToMany
        queryset=models.UserProfile.objects.all(),
        many=True,
        write_only=True
    )

    attendees = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Meetings
        fields = ['Name', 'Description', 'Date', 'StartTime', 'EndTime', 'attendee_ids', 'attendees']
    
    def create(self,validated_data):
        users = validated_data.pop('User')  # 'User' because source='User'
        meeting = models.Meetings.objects.create(**validated_data)
        meeting.save()
        for user in users:
            models.Attendee.objects.create(User=user, Meeting=meeting)

        return meeting
