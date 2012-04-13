from django.db import models

class ImmobileObject(models.Model):
    name = models.TextField(max_length=255)
    phone = models.TextField(max_length=20, null=True, blank=True)

    latitude_degree = models.IntegerField()
    latitude_minute = models.FloatField()
    is_north = models.BooleanField()

    longitude_degree = models.IntegerField()
    longitude_minute = models.FloatField()
    is_east = models.BooleanField()

    def __unicode__(self):
        return '%s [%d %f, %d %f]' % (self.name, self.latitude_degree, self.latitude_minute,
                                         self.longitude_degree, self.longitude_minute)

    def get_json(self):
        return {'id' : self.id,
                'name' : self.name,
                'phone' : self.phone,
                'latitude_degree' : self.latitude_degree,
                'latitude_minute' : self.latitude_minute,
                'is_north' : self.is_north,
                'longitude_degree' : self.longitude_degree,
                'longitude_minute' : self.longitude_minute,
                'is_east' : self.is_east
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

    latitude_degree = models.IntegerField()
    latitude_minute = models.FloatField()
    is_north = models.BooleanField()

    longitude_degree = models.IntegerField()
    longitude_minute = models.FloatField()
    is_east= models.BooleanField()

    def get_json(self):
        return {'movable_id' : self.movable_object_id,
                'movable_name' : self.movable_object.name,
                'id' : self.id,
                'hour' : self.hour,
                'minute' : self.minute,
                'second' : self.second,
                'latitude_degree' : self.latitude_degree,
                'latitude_minute' : self.latitude_minute,
                'is_north' : self.is_north,
                'longitude_degree' : self.longitude_degree,
                'longitude_minute' : self.longitude_minute,
                'is_east' : self.is_east
        }

def __unicode__(self):
    return '%d:%d:%f [%d %f, %d %f]' % (self.hour, self.minute, self.second, self.latitude_degree, self.latitude_minute,
                                     self.longitude_degree, self.longitude_minute)



