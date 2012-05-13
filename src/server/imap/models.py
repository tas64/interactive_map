from django.db import models

class ImmobileObject(models.Model):
    name = models.TextField(max_length=255)
    phone = models.TextField(max_length=20, null=True, blank=True)

    latitude = models.FloatField() #-90:90
    longitude = models.FloatField() #-180:180

    def __unicode__(self):
        return '%s [%f, %f]' % (self.name, self.latitude, self.longitude)

    def get_json(self):
        return {'id' : self.id,
                'name' : self.name,
                'phone' : self.phone,
                'latitude' : self.latitude,
                'longitude' : self.longitude,
                }


class MovableObject(models.Model):
    name = models.TextField(max_length=255)
    type = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return 'movable %s' % self.name

    def get_json(self):
        return {'id' : self.id, 'name' : self.name, 'type' : self.type }

class LocationPoint(models.Model):

    movable_object = models.ForeignKey(MovableObject)

    hour = models.IntegerField()
    minute = models.IntegerField()
    second = models.FloatField()

    latitude = models.FloatField() #-90:90
    longitude = models.FloatField() #-180:180

    def get_json(self):
        return {'movable_id' : self.movable_object_id,
                'movable_name' : self.movable_object.name,
                'id' : self.id,
                'hour' : self.hour,
                'minute' : self.minute,
                'second' : self.second,
                'latitude' : self.latitude,
                'longitude' : self.longitude
        }

def __unicode__(self):
    return '%d:%d:%f [%f,%f]' % (self.hour, self.minute, self.second, self.latitude, self.longitude)



