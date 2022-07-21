from django.contrib import admin

from ads.models import CategoryModel, AdModel

admin.site.register(AdModel)
admin.site.register(CategoryModel)
