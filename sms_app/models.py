from django.db import models


# Subscribers have a subscription to receive text message alerts.
class Subscriber(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    language = models.CharField(max_length=2)


# Publishers are permitted to send in a text message that will trigger an alert to be sent to all of the subscribers.
class Publisher(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
