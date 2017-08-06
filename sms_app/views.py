from string import Template

import boto3
import logging
import abc

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from sms_app.asset_file import AssetFile
from sms_app.messaging import Message
from sms_app.models import Subscriber
from sms_app.subscription_states import SubscriptionStates
from .forms import AlertForm, FollowUpForm


@login_required
def alert_form(request):
    if request.method == 'POST':
        print("Received alert form POST")
        form = AlertForm(request.POST)
        if form.is_valid():
            print("alert form POST is valid")
            notification = CachedNotification(
                AlertNotification(form.cleaned_data['address'])
            )

            Notifier(
                boto3.client('sns', region_name="us-west-2"),
                Subscriber.objects.filter(state=SubscriptionStates.COMPLETE_STATE)
            ).send(notification)

            print("notifications sent")
            return HttpResponseRedirect('sms_app/alertform/sent/')
    else:
        form = AlertForm()

    return render(request, 'alertform/form.html', {'form': form})


@login_required
def alert_sent(request):
    return render(request, 'alertform/sent.html')


@login_required
def followup_form(request):
    if request.method == 'POST':
        form = FollowUpForm(request.POST)
        if form.is_valid():
            notification = CachedNotification(
                FollowUp(
                    form.cleaned_data['num_people'],
                    form.cleaned_data['city'],
                    form.cleaned_data['target_name'],
                    form.cleaned_data['target_phone_num'],
                )
            )

            Notifier(
                boto3.client('sns', region_name="us-west-2"),
                Subscriber.objects.filter(state=SubscriptionStates.COMPLETE_STATE)
            ).send(notification)

            return HttpResponseRedirect('sms_app/followup/sent/')
    else:
        form = FollowUpForm()

    return render(request, 'followup/form.html', {'form': form})


@login_required
def followup_sent(request):
    return render(request, 'followup/sent.html')


class Notification(object):
    @abc.abstractmethod
    def message(self, lang):
        raise NotImplemented()


class AlertNotification(Notification):
    def __init__(self, address):
        self._address = address

    def message(self, lang):
        contents = Message(AssetFile(lang).action_alert_file()).contents()
        return Template(contents).substitute({'address': self._address})


class FollowUp(Notification):
    def __init__(self, num_people, city, target_name, target_phone_num):
        self._num_people = num_people
        self._city = city
        self._target_name = target_name
        self._target_phone_num = target_phone_num

    def message(self, lang):
        contents = Message(AssetFile(lang).follow_up_file()).contents()
        return Template(contents).substitute({
            'num_people': self._num_people,
            'city': self._city,
            'target_name': self._target_name,
            'target_phone_num': self._target_phone_num,
        })


class CachedNotification(Notification):
    def __init__(self, notification):
        self._notification = notification
        self._translation_mapping = {}

    def message(self, lang):
        if lang in self._translation_mapping:
            return self._translation_mapping[lang]

        result = self._notification.message(lang)
        self._translation_mapping[lang] = result
        return result


class Notifier(object):
    def __init__(self, sns_client, subscribers):
        self._sns_client = sns_client
        self._subscribers = subscribers
        self._logger = logging.getLogger("rapidsms")

    def send(self, notification):
        for subscriber in self._subscribers:
            response = self._sns_client.publish(
                PhoneNumber=subscriber.phone_number,
                Message=notification.message(subscriber.language)
            )
            self._logger.debug("Received SNS response: {}".format(response))
