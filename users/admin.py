from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (User, Profile, UserMessage, CourseSchedule, MemberPayment)
from .forms import (ChangeMemberChildForm, ChangeMember0Form,
    ChangeMember1Form, ChangeMember2Form, ChangeMember3Form)

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
        'mc_state', 'total_amount', 'settled')
    list_editable = ('is_trusted', 'sector', 'mc_state', 'total_amount',
        'settled' )
    list_filter = ('sector', 'mc_state', 'settled')
    search_fields = ('fiscal_code', 'address')
    #actions = ['control_mc', 'reset_all', 'control_pay']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        member = self.get_object(request, object_id)
        if member.parent:
            self.form = ChangeMemberChildForm
            self.inlines = [ MemberPaymentInline, ]
        elif member.sector == '0-NO':
            self.form = ChangeMember0Form
            self.inlines = []
        elif member.sector == '1-YC':
            self.form = ChangeMember1Form
            self.inlines = [ MemberPaymentInline, ]
        elif member.sector == '2-NC':
            self.form = ChangeMember2Form
            self.inlines = [ MemberPaymentInline, ]
        elif member.sector == '3-FI':
            self.form = ChangeMember3Form
            self.inlines = []
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
