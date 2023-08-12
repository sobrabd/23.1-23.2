from django.contrib import admin
from .models import Category, Dog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)


@admin.register(Dog)
class DogAmin(admin.ModelAdmin):
    list_display = ('name', 'category',)
    list_filter = ('category',)
