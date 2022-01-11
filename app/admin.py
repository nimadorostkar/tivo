from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry
from .models import Profile, Discounts, Package, Requests, Contact
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin


admin.site.site_header= " دستیار املاک "
admin.site.site_title= "  دستیار املاک  "
admin.site.register(LogEntry)







#------------------------------------------------------------------------------
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('phone',)
admin.site.register(Profile, ProfileAdmin)




#------------------------------------------------------------------------------
class DiscountsAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'active')
    list_filter = ('active',)
    search_fields = ('code',)
admin.site.register(Discounts, DiscountsAdmin)






#------------------------------------------------------------------------------
class PackageAdmin(admin.ModelAdmin):
    list_display = ('month', 'price')
admin.site.register(Package, PackageAdmin)







#------------------------------------------------------------------------------
class RequestsAdmin(ModelAdminJalaliMixin,admin.ModelAdmin):
    list_display = ('domain', 'user', 'package', 'date_created', 'final_price', 'paid', 'status')
    list_filter = ('package','date_created', 'paid', 'status')
    search_fields = ('user', 'domain')
admin.site.register(Requests, RequestsAdmin)








#------------------------------------------------------------------------------
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'j_created_on')
    list_filter = ('name', 'created_on')
    search_fields = ('name', 'phone', 'body')

admin.site.register(Contact, ContactAdmin)












#End
