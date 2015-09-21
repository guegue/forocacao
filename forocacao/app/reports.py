# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _

from model_report.report import reports, ReportAdmin
from model_report.utils import yesno_format

from .models import *


class AttendeeReport(ReportAdmin):
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
    ]

    override_field_labels = { 
            'type__name': _('Type'),
            'profession__name': _('Profession'),
            'sponsor__name': _('Sponsor'),
            }
    override_field_formats = {
        'extra': yesno_format,
        'main': yesno_format,
        'sponsored': yesno_format,
    }
    list_order_by = ('last_name', 'first_name')
    list_filter = ('event',)

    type = 'report'

reports.register('attendee-report', AttendeeReport)
