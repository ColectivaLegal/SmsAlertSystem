from django.conf.urls import url

from . import views

urlpatterns = [
    # SmsAlertSystem URLs
    url(r'^$', views.alert_form, name="alertform"),
    url(r'^sent/', views.sent_form, name="sentform"),
]
