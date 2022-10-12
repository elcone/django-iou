from django.contrib import admin

from . import models


admin.site.register(models.User)
admin.site.register(models.Loan)
admin.site.register(models.UserBalance)
