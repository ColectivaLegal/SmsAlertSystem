from string import Template

import boto3
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from sms_app.asset_file import AssetFile
from sms_app.messaging import Message
from sms_app.models import Subscriber
from .forms import AlertForm


@login_required
def alert_form(request):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            Alert(form.cleaned_data['address']).send_to_everyone()
            return HttpResponseRedirect('/alertform/sent/')
    else:
        form = AlertForm()

    return render(request, 'alertform/index.html', {'form': form})


@login_required
def sent_form(request):
    return render(request, 'alertform/sent.html')


class Alert(object):
    def __init__(self, address):
        self._address = address
        self._translation_mapping = {}
        self._logger = logging.getLogger("rapidsms")

    def send_to_everyone(self):
        sns_client = boto3.client('sns', region_name="us-west-2")

        subscribers = Subscriber.objects.all()
        for subscriber in subscribers:
            response = sns_client.publish(
                PhoneNumber=subscriber.phone_number,
                Message=self._alert_translation(subscriber.language)
            )
            self._logger.debug("Received SNS response: {}".format(response))

    def _alert_translation(self, lang):
        if lang in self._translation_mapping:
            return self._translation_mapping[lang]

        contents = Message(AssetFile(lang).action_alert_file()).contents()
        result = Template(contents).substitute({'address': self._address})

        self._translation_mapping[lang] = result
        return result
