import random

from django.db import models
from django.utils.translation import ugettext_lazy as _

from app.utils import distance_on_unit_sphere_kilometers


class StationManager(models.Manager):

    def create_random_station(self):
        lng = random.randrange(-18000, 18000) / 100.0
        ltd = random.randrange(-9000, 9000) / 100.0
        return self.create(longitude=lng, latitude=ltd)

    def check_point(self, ltd, lng):
        res = False
        for s in self.all():
            d = distance_on_unit_sphere_kilometers(ltd, lng, s.latitude, s.longitude)
            if d <= self.model.action_radius:
                res = True
                continue
        return res


class Station(models.Model):
    action_radius = 50

    longitude = models.FloatField(_('Longitude'))
    latitude = models.FloatField(_('Latitude'))

    objects = StationManager()

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return u"{0}".format(self.id)