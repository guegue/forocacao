# -*- coding: utf-8 -*-

from django.db.models import Q
from django.utils.translation import ugettext as _

from braces.views import LoginRequiredMixin
from model_report.report import reports, ReportAdmin
from model_report.utils import yesno_format

from .models import *


class PaymentReport(LoginRequiredMixin, ReportAdmin):
    title = _('Reporte de Pagos')
    model = AttendeePayment
    fields = [
        'date',
        'payment_method__name',
        'attendee_id',
        'attendee__first_name',
        'attendee__middle_name',
        'attendee__last_name',
        'attendee__second_lastname',
        'attendee__profession__name',
        'attendee__other_profession',
        #'attendee__country__name', # FIXME: 'NoneType' object has no attribute 'to'
        #'attendee__country', # FIXME: no subreport :(
        'amount',
        'reference',
        'note',
    ]
    override_field_labels = { 
            'payment_method__name': _('Payment Method'),
            'attendee_id': _('ID'),
            'attendee__profession__name': _('Profession'),
            }
    #list_group_by = ('attendee_id',)
    list_filter = ('attendee__event', 'attendee_id','attendee__country','attendee__profession','payment_method')
    list_order_by = ('attendee__first_name', 'attendee__last_name')
    exclude = {'field': 'attendee__is_staff', 'value': True}

    type = 'report'

class AccountingReport(LoginRequiredMixin, ReportAdmin):
    title = _('Reporte Contable')
    model = Attendee
    fields = [
        'id',
        'first_name',
        'middle_name',
        'last_name',
        'second_lastname',
        'type__name',
        'profession__name',
        'other_profession',
        'country',
        'self.price',
        'self.paid',
        'self.balance',
    ]

    inlines = [PaymentReport]

    override_field_labels = { 
            'id': _('ID'),
            'self.price': _('Price'),
            'self.paid': _('Paid'),
            'self.balance': _('Balance'),
            'profession__name': _('Profession'),
            'type__name': _('Type'),
            }
    override_field_formats = {
        'extra': yesno_format,
        'main': yesno_format,
        'sponsored': yesno_format,
    }
    list_order_by = ('first_name', 'last_name')
    #list_order_by = ('id', )
    list_filter = ('event','id','type','country','profession',)
    exclude = {'field': 'is_staff', 'value': True}

    type = 'report'

class AttendeeReport(LoginRequiredMixin, ReportAdmin):
    title = _('Listado de participantes')
    model = Attendee
    fields = [
        'id',
        'extra',
        'main',
        'type__name',
        'first_name',
        'last_name',
        'email',
        'profession__name',
        'other_profession',
        'phone',
        'country',
        'sponsored',
        'sponsor__name',
        'self.balance',
    ]

    override_field_labels = { 
            'id': _('ID'),
            'type__name': _('Type'),
            'profession__name': _('Profession'),
            'sponsor__name': _('Sponsor'),
            'self.balance': _('Balance'),
            }
    override_field_formats = {
        'extra': yesno_format,
        'main': yesno_format,
        'sponsored': yesno_format,
    }
    list_order_by = ('first_name', 'last_name')
    list_filter = ('event','country','profession')
    exclude = {'field': 'is_staff', 'value': True}
    selectable_fields = True

    type = 'report'

reports.register('attendee-report', AttendeeReport)
reports.register('accounting-report', AccountingReport)
reports.register('payment-report', PaymentReport)
