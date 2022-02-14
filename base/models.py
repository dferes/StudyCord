from django.db import models
from django.contrib.auth.models import AbstractUser # Django already has the model included
from django.db.models.deletion import CASCADE # Do I need this import? (auto generated when 'cascade' was used) 


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default='avatar.svg') # relies on a third party package called 'pillow', which is an image processing library
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic =  models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) # if a topic is deleted, set room to null...may need to fix this later
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # null is allowed, forms can be blank?

    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    
    updated = models.DateTimeField(auto_now=True)         # auto time stamp for when any of the fields are changed
    created = models.DateTimeField(auto_now_add=True)     # automatically takes a time stamp when an instance (a room) is first created

    class Meta:
        ordering = ['-updated', '-created']  # odd bit of syntax here: ['updated', 'created'] would order the Room objects in descending order
                                             # but using '-': ['-updated', '-created'] orders the rooms in ascending order   

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # If a room gets deleted, delete all children (the messages)
    body = models.TextField() # not nullable
    updated =  models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']  # odd bit of syntax here: ['updated', 'created'] would order the Room objects in descending order
                                             # but using '-': ['-updated', '-created'] orders the rooms in ascending order   

    def __str__(self):
        return self.body[:50]
