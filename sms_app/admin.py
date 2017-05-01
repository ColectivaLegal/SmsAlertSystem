from django.contrib import admin

from .models import Publisher, Subscriber

admin.site.register([Publisher, Subscriber])
