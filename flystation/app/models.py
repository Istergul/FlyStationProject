import random
import math

from django.db import models
from django.utils.translation import ugettext_lazy as _


class StationManager(models.Manager):

    def create_random_station(self):
        lng = random.randrange(-1800000, 1800000) / 10000.0
        ltd = random.randrange(-900000, 900000) / 10000.0
        return self.create(lng_dgr=lng, ltd_dgr=ltd)

    def find_points(self, ltd_dgr, lng_dgr):
        earth_radius = 6371
        angular_radius = float(self.model.action_radius) / earth_radius

        ltd_rad = math.radians(ltd_dgr)
        lng_rad = math.radians(lng_dgr)

        ltd_range = (ltd_rad - angular_radius, ltd_rad + angular_radius)

        delta_lng = math.asin(math.sin(angular_radius) / math.cos(ltd_rad))
        lng_range = (lng_rad - delta_lng, lng_rad + delta_lng)

        fltr = {
            "ltd_rad__gte": ltd_range[0],
            "ltd_rad__lte": ltd_range[1],
            "lng_rad__gte": lng_range[0],
            "lng_rad__lte": lng_range[1],
        }
        points_aprxm_ids = self.values_list('id', flat=True).filter(**fltr)

        points = self.filter(id__in=points_aprxm_ids).extra(
            where=['acos(sin(%s) * sin(ltd_rad) + cos(%s) * cos(ltd_rad) * cos(lng_rad - (%s))) <= %s'],
            params=[ltd_rad, ltd_rad, lng_rad, angular_radius]
        )

        return points


class Station(models.Model):
    action_radius = 30

    lng_dgr = models.FloatField(_('Longitude in degrees'))
    ltd_dgr = models.FloatField(_('Latitude in degrees'))
    lng_rad = models.FloatField(_('Longitude in radians'))
    ltd_rad = models.FloatField(_('Latitude in radians'))

    objects = StationManager()

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return u"{0}".format(self.id)

    def save(self, *args, **kwargs):
        self.lng_rad = math.radians(self.lng_dgr)
        self.ltd_rad = math.radians(self.ltd_dgr)
        super(Station, self).save(*args, **kwargs)

    def to_json(self):
        return {
            "id": self.id,
            "lng_dgr": self.lng_dgr,
            "ltd_dgr": self.ltd_dgr,
        }