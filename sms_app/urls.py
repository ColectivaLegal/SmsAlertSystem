from django.conf.urls import url

from . import views

urlpatterns = [
    # SmsAlertSystem URLs
    url(r'alertform/$', views.alert_form, name="alertform"),
    url(r'alertform/sent/$', views.alert_sent, name="alert_sent"),
    url(r'followup/$', views.followup_form, name="followup"),
    url(r'followup/sent/$', views.followup_sent, name="followup_sent"),
]
