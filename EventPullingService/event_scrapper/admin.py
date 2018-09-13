import csv
import datetime
from django import forms
from django.contrib import admin
from event_scrapper import models
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from import_export.admin import ImportExportModelAdmin
from event_scrapper.tasks import process_venue_scrapping


@admin.register(models.Venue)
class VenueAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_filter = ('id', 'name', 'is_active')
    search_fields = ('id', 'name', 'is_active')
    actions = ['download_as_csv',
               'trigger_selected_venue_scrapping_next_month']

    def download_as_csv(self, request, queryset):
        csv_file = open('venue.csv', 'wb')
        writer = csv.writer(csv_file)
        writer.writerow(["id", "name", "is_active", "url"])

        queryset = queryset.order_by('id')

        for s in queryset:
            writer.writerow([s.id, s.name, s.is_active,
                             s.url_config['venue_url']])
        csv_file.close()

        csv_file = open('venue.csv', 'r')
        response = HttpResponse(csv_file, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=venue.csv'
        messages.info(request, "Venue file download comlplete.")
        return None

    def trigger_selected_venue_scrapping_next_month(self, request, queryset):
        for venue in queryset:
            process_venue_scrapping.delay(venue.id)
        messages.info(
            request, "Venue Scrapping started. Please check Event Log for more info.")
        return None
        return None

    download_as_csv.short_description = 'Download all venue information as CSV file.'
    trigger_selected_venue_scrapping_next_month.short_description = 'Scrape Data for selected venue for Next Month.'


@admin.register(models.Event)
class EventAdmin(ImportExportModelAdmin):
    list_display = ('name', 'venue', 'start_date', 'start_time', 'end_date',
                    'end_time', 'event_tag', 'minimum_cost', 'category', 'summary', 'description')
    list_filter = ('venue', 'start_date', 'event_start_time',
                   'end_date', 'event_end_time', 'tags', 'category')
    search_fields = ('name', 'venue', 'start_date', 'event_start_time',
                     'end_date', 'event_end_time', 'tags', 'category')
    actions = ['download_as_csv']

    def start_time(self, obj):
        if obj.event_start_time:
            return obj.event_start_time.strftime('%I:%M %p')
        return None

    def end_time(self, obj):
        if obj.event_end_time:
            return obj.event_end_time.strftime('%I:%M %p')
        return None

    def summary(self, obj):
        if obj and obj.event_metadata:
            return obj.event_metadata['summary']
        return '-'

    def event_tag(self, obj):
        if obj and obj.tags:
            return obj.tags['tags']
        return '-'

    def download_as_csv(self, request, queryset):
        csv_file = open('event.csv', 'wb')
        writer = csv.writer(csv_file)
        writer.writerow(["id", "event_id", "name", "venue", "description", "start_date",
                         "event_start_time", "end_date", "event_end_time", "tags", "organizer_name"])

        queryset = queryset.order_by('id')

        for s in queryset:
            writer.writerow([s.id, s.name, s.venue, s.description, s.start_date,
                             s.event_start_time, s.end_date, s.event_end_time, s.tags, s.organizer_name])
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


@admin.register(models.AtlPullEventLogs)
class AtlPullEventLogsAdmin(admin.ModelAdmin):
    list_display = ('status', 'start_time', 'end_time', 'description')
    list_filter = ('status',)
    search_fields = ('status',)
    actions = ['download_logs_as_csv']

    def download_logs_as_csv(self, request, queryset):
        return None

    download_logs_as_csv.short_description = 'Download event scraping event information as CSV file.'


@admin.register(models.AtlByDayOrganizer)
class AtlByDayOrganizerAdmin(admin.ModelAdmin):
    list_display = ('organizer_id', 'organizer',
                    'slug', 'phone', 'url', 'status')
    list_filter = ('organizer', 'status')
    search_fields = ('organizer_id', 'organizer',
                     'slug', 'phone', 'url', 'status')


@admin.register(models.AtlByDayVenue)
class AtlByDayVenueAdmin(admin.ModelAdmin):
    list_display = ('venue_id', 'venue', 'url', 'address', 'city', 'status')
    list_filter = ('venue', 'status')
    search_fields = ('venue_id', 'venue', 'address', 'city', 'status')


@admin.register(models.AtlByDayEvent)
class AtlByDayEventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'title', 'start_date',
                    'end_date', 'cost', 'venue', 'status')
    list_filter = ('venue', 'status')
    search_fields = ('event_id', 'title', 'start_date',
                     'end_date', 'cost', 'venue', 'status')


@admin.register(models.AtlByDayTag)
class AtlByDayTagAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'name', 'slug', 'url')
    list_filter = ('name', 'slug')
    search_fields = ('tag_id', 'name', 'slug', 'url')


@admin.register(models.AtlByDayCategory)
class AtlByDayCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'name', 'slug', 'url')
    list_filter = ('name', 'slug')
    search_fields = ('category_id', 'name', 'slug', 'url')
