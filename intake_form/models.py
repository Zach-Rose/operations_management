from django.db import models

class Contributor(models.Model):
    name = models.CharField(max_length=100, default='Unnamed Contributor')

    def __str__(self):
        return self.name

class ProcessStep(models.Model):
    name = models.CharField(max_length=100, default='Unnamed Step')
    duration_value = models.IntegerField(default=0)
    duration_unit = models.CharField(max_length=10, default='seconds')
    contributors = models.ManyToManyField(Contributor, related_name='steps')

    def __str__(self):
        return self.name

class Process(models.Model):
    name = models.CharField(max_length=100, default='Unnamed Process')
    description = models.TextField(default='')
    ideal_duration = models.DurationField(default='0:00:00')
    steps = models.ManyToManyField(ProcessStep, related_name='processes')

    def __str__(self):
        return self.name