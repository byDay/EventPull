from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from event_scrapper import models

@admin.register(models.Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_filter = ('id', 'name', 'is_active')
    search_fields = ('id', 'name', 'is_active')


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'venue' , 'description', 'date', 'event_start_time', 'event_end_time', 'tags')
    list_filter = ('id', 'name', 'venue' , 'description', 'date', 'event_start_time', 'event_end_time', 'tags')
    search_fields = ('id', 'name', 'venue' , 'description', 'date', 'event_start_time', 'event_end_time', 'tags')


@admin.register(models.Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'config')
    list_filter = ('name', 'config')
    search_fields = ('name', 'config')
