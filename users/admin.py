from datetime import date, timedelta

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.mail import EmailMessage
from django.db.models import Q

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
    actions = [ 'control_mc', 'control_pay', 'reset_all', ]

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

    def control_mc(self, request, queryset):
        queryset = queryset.filter( Q( sector = '1-YC' ) | Q( sector = '2-NC' ))
        for member in queryset:
            if member.mc_state == None:
                member.mc_state = '0-NF'
                member.save()
            elif (member.mc_state.startswith('0') or
                member.mc_state == '5-NI'):
                if member.med_cert:
                    member.mc_state = '1-VF'
                    member.save()
            elif member.mc_state == '2-RE':
                if member.mc_expiry<date.today() + timedelta(days=30):
                    member.mc_state = '6-IS'
                    member.save()
                elif member.mc_expiry<date.today():
                    member.mc_state = '3-SV'
                    member.save()
            elif member.mc_state.startswith('6'):
                if member.mc_expiry<date.today():
                    member.mc_state = '3-SV'
                    member.save()

    control_mc.short_description = 'Controlla CM/CMA'

    def control_pay(self, request, queryset):
        queryset = queryset.filter( Q( sector = '1-YC' ) | Q( sector = '2-NC' ))
        for member in queryset:
            if member.settled == 'YES':
                continue
            elif member.total_amount == 0.00:
                member.settled = 'VI'
                member.save()
            else:
                paid = 0.00
                payments = MemberPayment.objects.filter(member_id = member.pk)
                for payment in payments:
                    paid += payment.amount
                if paid >= member.total_amount:
                    member.settled = 'YES'
                    member.save()
                else:
                    member.settled = 'NO'
                    member.save()

    control_pay.short_description = 'Controlla i pagamenti'

    def reset_all(self, request, queryset):
        queryset.update(sign_up='', privacy='', settled='', total_amount=0.00)
        for member in queryset:
            MemberPayment.objects.filter(member_id = member.pk).delete()

    reset_all.short_description = 'Resetta i dati'
