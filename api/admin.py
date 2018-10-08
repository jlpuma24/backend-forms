# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from api.models import *

admin.site.register(Company)
admin.site.register(Worker)
admin.site.register(BodyPart)
admin.site.register(BodyPartForm)
admin.site.register(FilledForms)
