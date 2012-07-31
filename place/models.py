from mongoengine.document import Document
from mongoengine.fields import GeoPointField, ListField, \
    StringField
    
class Type(Document):
    name = StringField()

class Place(Document):
    location = GeoPointField()
    types = ListField(StringField())
    name = StringField()
    address = StringField()
    google_place_id = StringField()
