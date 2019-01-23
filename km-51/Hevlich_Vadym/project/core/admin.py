from django.contrib import admin
from .models import Repo, Result, Category

admin.site.register(Repo)
admin.site.register(Result)
admin.site.register(Category)
