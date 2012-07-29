from django.db import models
from feed.models import Feed
from mongoengine import *
from mongoengine import signals
from mongoengine.django.auth import User

class Activity(Document):
    participants = ListField(ReferenceField(User))
    num_participants = IntField()
    
    @classmethod
    def post_save(cls, sender, document, **kwargs):
        pass

signals.post_save.connect(Activity.post_save, sender=Activity)