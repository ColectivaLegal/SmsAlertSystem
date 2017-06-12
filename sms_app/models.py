from django.db import models


# Subscribers have a subscription to receive text message alerts.
class Subscriber(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    language = models.CharField(max_length=3)
    state = models.CharField(max_length=20)

    def __str__(self):
        return "|{}|{}|{}|".format(self.phone_number, self.language, self.state)


# Publishers are permitted to send in a text message that will trigger an alert to be sent to all of the subscribers.
class Publisher(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
