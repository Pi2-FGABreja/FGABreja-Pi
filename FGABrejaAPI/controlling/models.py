from django.db import models
import datetime
import json


class Heat(models.Model):
    temperature = models.FloatField()
    duration = models.IntegerField()
    process_stage = models.CharField(max_length=50)


class Hop(models.Model):
    minutes = models.IntegerField()
    weight = models.FloatField()


class Recipe(models.Model):
    hops_order = models.CharField(max_length=255)
    heat_order = models.CharField(max_length=255)

    def set_hop_order(self, order):
        hop_order = {}
        for index, hop in enumerate(order, start=1):
            hop_order[index] = hop.id
        self.hop_order = json.dumps(hop_order)

    def get_hop_order(self):
        return json.loads(self.hop_order)

    def set_heat_order(self, order):
        heat_order = {}
        for index, heat in enumerate(order, start=1):
            heat_order[index] = heat.id
        self.heat_order = json.dumps(heat_order)

    def get_heat_order(self):
        return json.loads(self.heat_order)


class Process(models.Model):
    initial_datetime = models.DateTimeField(auto_now=True)
    final_datetime = models.DateTimeField(null=True)
    recipe = models.ForeignKey('Recipe')
    iodine_test = models.BooleanField(default=False)
    malt = models.BooleanField(default=False)
    state = models.IntegerField()
    level_pot1 = models.BooleanField(default=False)
    level_pot2 = models.BooleanField(default=False)
    actual_heat = models.ForeignKey('Heat')
    actual_heat_time = models.DateTimeField(null=True)

    def change_heat(self):
        delta = datetime.datetime.now() - self.actual_heat_time
        if delta >= datetime.timedelta(minutes=self.actual_heat.duration):
            return True
        elif self.actual_heat_time is None:
            return True
        else:
            return False

