from django.contrib import admin

from ads.models import CategoryModel, AdModel, Selection

admin.site.register(AdModel)
admin.site.register(CategoryModel)
admin.site.register(Selection)
