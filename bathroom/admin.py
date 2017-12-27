# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import restroom
from .models import review

admin.site.register(restroom)
admin.site.register(review)
