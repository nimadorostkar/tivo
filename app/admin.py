from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry
from .models import Profile, Area, Item, ItemImage, Slider, Fav, Contact, Ownership, Settings
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin


admin.site.site_header= " دستیار املاک "
admin.site.site_title= "  دستیار املاک  "
admin.site.register(LogEntry)







#------------------------------------------------------------------------------
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'user_type', 'user_name','phone','sales_expert')
    list_filter = ('user_type', "date_created")
    search_fields = ['user_name', 'phone']
admin.site.register(models.Profile, ProfileAdmin)









#------------------------------------------------------------------------------
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'j_created_on')
    list_filter = ('name', 'created_on')
    search_fields = ('name', 'phone', 'body')

admin.site.register(Contact, ContactAdmin)












#End
