import csv
import datetime
from django import forms
from django.contrib import admin
from event_scrapper import models
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from import_export.admin import ImportExportModelAdmin

@admin.register(models.Venue)
class VenueAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_filter = ('id', 'name', 'is_active')
    search_fields = ('id', 'name', 'is_active')
    actions = ['download_as_csv', 'trigger_selected_venue_scrapping_current_month', 'trigger_selected_venue_scrapping_next_month']
    
    def download_as_csv(self, request, queryset):
        csv_file = open('venue.csv', 'wb')
        writer = csv.writer(csv_file)
        writer.writerow(["id", "name", "is_active", "url"])

        queryset = queryset.order_by('id')
        
        for s in queryset:
            writer.writerow([s.id, s.name, s.is_active, s.url_config['venue_url']])
        csv_file.close()
        
        csv_file = open('venue.csv', 'r')
        response = HttpResponse(csv_file, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=venue.csv'
        messages.info(request, "Venue file download comlplete.")
        return None

    def trigger_selected_venue_scrapping_current_month(self, request, queryset):
        return None

    def trigger_selected_venue_scrapping_next_month(self, request, queryset):
        return None

    download_as_csv.short_description = 'Download all venue information as CSV file.'
    trigger_selected_venue_scrapping_current_month.short_description = 'Scrape Data for selected venue for Current Month.'
    trigger_selected_venue_scrapping_next_month.short_description = 'Scrape Data for selected venue for Next Month.'


@admin.register(models.Event)
class EventAdmin(ImportExportModelAdmin):
    list_display = ('name', 'venue', 'start_date', 'start_time', 'end_date', 'end_time', 'tags', 'minimum_cost', 'category')
    list_filter = ('name', 'venue', 'start_date', 'event_start_time',  'end_date', 'event_end_time', 'tags', 'category')
    search_fields = ('name', 'venue', 'start_date', 'event_start_time', 'end_date', 'event_end_time', 'tags', 'category')
    actions = ['download_as_csv']

    def start_time(self, obj):
        if obj.event_start_time:
            return obj.event_start_time.strftime('%I:%M %p')
        return None

    def end_time(self, obj):
        if obj.event_end_time:
            return obj.event_end_time.strftime('%I:%M %p')
        return None
    
    def download_as_csv(self, request, queryset):
        csv_file = open('event.csv', 'wb')
        writer = csv.writer(csv_file)
        writer.writerow(["id", "event_id", "name", "venue", "description", "start_date", "event_start_time", "end_date", "event_end_time", "tags", "organizer_name"])

        queryset = queryset.order_by('id')
        
        for s in queryset:
            writer.writerow([s.id, s.name, s.venue, s.description, s.start_date, s.event_start_time, s.end_date, s.event_end_time, s.tags, s.organizer_name])
        csv_file.close()
        
        csv_file = open('event.csv', 'r')
        response = HttpResponse(csv_file, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=event.csv'
        messages.info(request, "Event file download comlplete.")
        return None

    download_as_csv.short_description = 'Download all venue information as CSV file.'


@admin.register(models.Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'config')
    list_filter = ('name', 'config')
    search_fields = ('name', 'config')

@admin.register(models.ScrapingEventLogs)
class ScrapingEventLogsAdmin(admin.ModelAdmin):
    list_display = ('venue', 'status', 'start_time', 'end_time', 'description')
    list_filter = ('venue', 'status')
    search_fields = ('venue', 'status')
    actions = ['download_logs_as_csv']
    
    def download_logs_as_csv(self, request, queryset):
        return None

    download_logs_as_csv.short_description = 'Download event scraping event information as CSV file.'

