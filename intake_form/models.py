from django.db import models

class Contributor(models.Model):
    name = models.CharField(max_length=100, default='Unnamed Contributor')

    def __str__(self):
        return self.name

class ProcessStep(models.Model):
    name = models.CharField(max_length=100, default='Unnamed Activity')
    duration_value = models.IntegerField(default=0, verbose_name='Flow Time')
    duration_unit = models.CharField(max_length=10, default='seconds', verbose_name='Flow Time unit')
    contributors = models.ManyToManyField(Contributor, related_name='steps', verbose_name='Resources')

    def __str__(self):
        return self.name

class Process(models.Model):
    name = models.CharField(max_length=100, default='Unnamed Process')
    description = models.TextField(default='')
    tack_time = models.DurationField(default='0:00:00')
    steps = models.ManyToManyField(ProcessStep, related_name='processes')

    def __str__(self):
        return self.name