from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (User, Profile, UserMessage, CourseSchedule, MemberPayment)

class UserAdmin(UserAdmin):
    list_display = ('get_full_name', 'is_staff', 'is_active', 'is_superuser')
    list_editable = ('is_staff', 'is_active')

admin.site.register(User, UserAdmin)

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'subject', )
    ordering = ('-id', )

@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('full', 'abbrev')
    ordering = ('abbrev', )

class MemberPaymentInline(admin.TabularInline):
    model = MemberPayment
    fields = ('date', 'amount')
    extra = 0

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'parent', 'is_trusted', 'sector',
        'mc_state', 'settled')
    list_editable = ('is_trusted', 'sector', 'mc_state', 'settled' )
    list_filter = ('sector', 'mc_state', 'settled')
    search_fields = ('fiscal_code', 'address')
    inlines = [ MemberPaymentInline, ]
    #actions = ['control_mc', 'reset_all', 'control_pay']
