from mongoengine import *
from mongoengine.django.auth import User
from place.models import Place

class Activity(Document):
    participants = ListField(ReferenceField(User))
    num_participants = IntField()
    title = StringField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    place = ReferenceField(Place)
    detail = StringField()
    created_time = DateTimeField()