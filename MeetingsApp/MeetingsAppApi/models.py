from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# Create your models here.


class UserProfileManager(BaseUserManager):
    def create_user(self, name,email, password=None):
        if not email:
            raise ValueError('User Must have an email address')

        if not name:
            raise ValueError("User must enetr a user name")

        if not password:
            raise ValueError('User must enter a password')

        email = self.normalize_email(email=email)
        user = self.model(email=email,name=name)

        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_superuser(self,name,email,password=None):
        """Creating super user"""

        user = self.create_user(name=name,email=email,password=password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using = self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name
    
    def __str__(self):
        return self.email
    
class Meetings(models.Model):
    Id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=255,unique=True)
    Description = models.TextField()
    Date = models.DateField()
    StartTime = models.TimeField()
    EndTime = models.TimeField()
    User = models.ManyToManyField(UserProfile,through='Attendee')

    def __str__(self):
        return self.Name
    
class Attendee(models.Model):
    User = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    Meeting = models.ForeignKey(Meetings,on_delete=models.CASCADE)
