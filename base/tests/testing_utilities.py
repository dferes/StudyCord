import json
import time
from base.models import User, Topic, Room, Message


def populate_test_db():
    user = User.objects.create_user(
        username='test_user',
        email='testuser@email.com',
        password='password_123',
        bio='Hello, I am a new user'
    )
    
    user2 = User.objects.create_user(
        username='test_user2',
        email='testuser2@email.com',
        password='password_123',
        bio='Look, another new user'
    )
    
    topic = Topic.objects.create(name='Python')
    topic2 = Topic.objects.create(name='Haskell')
    
    Room.objects.create(
        host=user,
        topic=topic,
        name='Learning Python',
        description='Learning python for server side web development.'
        # participants=user
    )
    
    Room.objects.create(
        host=user2,
        topic=topic2,
        name='Learning Haskell',
        description='Learning Haskell for server side web development.',
        #participants=user2
    )
