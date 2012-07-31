from mongoengine import *
from mongoengine.django.auth import User

class Feed(Document):
    content = GenericReferenceField()
    user = ReferenceField(User)