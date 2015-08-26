# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from filer.fields.image import FilerImageField
from django_countries.fields import CountryField
from model_utils import Choices
from colorfield.fields import ColorField

from forocacao.users.models import User

class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Title'))
    slug = models.SlugField()
    STATUS = Choices(('inactive',_('inactive')), ('draft', _('draft')), ('published', _('published')), ('frontpage',_('frontpage')))
    status = models.CharField(choices=STATUS, default=STATUS.draft, max_length=20, verbose_name=_('Status'))
    activities_label = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Activities label'))
    activities = models.ManyToManyField('Activity', blank=True, verbose_name=_('Activities'))
    text = models.TextField(blank=True,
                                 verbose_name=_('Event description'),
                                 help_text='Try and enter few some more lines')
    logo = FilerImageField(blank=True, null=True, related_name='event_logos', verbose_name=_('Logo'))
    image = FilerImageField(blank=True, null=True, related_name='event_images', verbose_name=_('Image'))
    image_footer = FilerImageField(blank=True, null=True, related_name='event_footers', verbose_name=_('Image footer') )
    start = models.DateField(blank=True, null=True, verbose_name=_('Start'))
    end = models.DateField(blank=True, null=True, verbose_name=_('End'))
    types = models.ManyToManyField('AttendeeType', through='AttendeeTypeEvent')
    professions = models.ManyToManyField('Profession', verbose_name=_('Proffesions'))
    payment_methods = models.ManyToManyField('PaymentMethod', verbose_name=_('Payment Methods'))
    badge_size_x = models.IntegerField(null=True, blank=True, verbose_name=_('Badge size X'))
    badge_size_y = models.IntegerField(null=True, blank=True, verbose_name=_('Badge size Y'))
    badge_color = ColorField(default='ffffff', verbose_name=_('Badge color'))

    class Meta:
        ordering = ['-start']
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __unicode__(self):
        return self.name

class Activity(models.Model):
    #event = models.ForeignKey('Event', verbose_name=_('Event'))
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    slug = models.SlugField()
    organizer = models.ForeignKey('users.User', null=True, blank=True, verbose_name=_('Organizer'))
    text = models.TextField(blank=True,
                                 verbose_name=_('Activity description'),
                                 help_text='Try and enter few some more lines')
    image = FilerImageField(blank=True, null=True, related_name='activity_images', verbose_name=_('Image'))
    image_footer = FilerImageField(blank=True, null=True, related_name='activity_footers', verbose_name=_('Image footer'))
    start = models.DateTimeField(blank=True, null=True, verbose_name=_('Start'))
    end = models.DateTimeField(blank=True, null=True, verbose_name=_('End'))

    class Meta:
        ordering = ['name']
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")

    def __unicode__(self):
        return self.name

class Profession(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    slug = models.SlugField()
    text = models.TextField(blank=True,
                                 verbose_name=_('Profession description'),
                                 help_text='Try and enter few some more lines')

    class Meta:
        ordering = ['name']
        verbose_name = _("Profession")
        verbose_name_plural = _("Professions")

    def __unicode__(self):
        return self.name

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))

    class Meta:
        ordering = ['name']
        verbose_name = _("Payment Method")
        verbose_name_plural = _("Payment Methods")

    def __unicode__(self):
        return self.name

class AttendeeTypeEvent(models.Model):
    attendeetype = models.ForeignKey('AttendeeType', verbose_name=_('Attendee Type'))
    event = models.ForeignKey('Event', verbose_name=_('Event'))
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('Price'))
    eb_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('EB Price'))

    class Meta:
        verbose_name = _("Attendee Type in Event")
        verbose_name_plural = _("Attendee Types in Events")

class AttendeeType(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))

    class Meta:
        ordering = ['name']
        verbose_name = _("Attendee Type")
        verbose_name_plural = _("Attendee Types")

    def __unicode__(self):
        return self.name

class AttendeeReceipt(models.Model):
    attendee = models.ForeignKey('users.User', verbose_name=_('Attendee'), related_name='receipts')
    date = models.DateField(verbose_name=_('Date'))
    reference = models.CharField(max_length=20, verbose_name=_('Reference'))
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Note'))

    class Meta:
        ordering = ['-date']
        verbose_name = _("Attendee Receipt")
        verbose_name_plural = _("Attendee Receipts")

    def __unicode__(self):
        return "%s" % (self.date,)


class AttendeePayment(models.Model):
    attendee = models.ForeignKey('users.User', verbose_name=_('Attendee'), related_name='payments')
    payment_method = models.ForeignKey('PaymentMethod', verbose_name=_('Payment Method'))
    date = models.DateField(verbose_name=_('Date'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Amount'))
    reference = models.CharField(max_length=20, verbose_name=_('Reference'))
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Note'))

    class Meta:
        ordering = ['-date']
        verbose_name = _("Attendee Payment")
        verbose_name_plural = _("Attendee Payments")

    def __unicode__(self):
        return "%s" % (self.amount,)


class Font(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Name'))
    filename = models.CharField(max_length=250, unique=True, verbose_name=_('Filename'))

    class Meta:
        ordering = ['name']
        verbose_name = _("Font")
        verbose_name_plural = _("Fonts")

    def __unicode__(self):
        return self.name

class EventBadge(models.Model):
    event = models.ForeignKey('Event', verbose_name=_('Event'))
    FIELDS = (('event',_('Event')), ('name', _('Complete name')), ('first_name', _('First name')), ('last_name', _('Last name')),
            ('profession',_('Profession')), ('country',_('Country')), ('type',_('Type')), ('email',_('E-mail')), ('text', _('Text')),
            ('logo',_('Logo')), ('photo',_('Photo')))
    field = models.CharField(max_length=50, choices=FIELDS, verbose_name=_('Field'))
    color = ColorField(default='', null=True, blank=True, verbose_name=_('Color'))
    font = models.ForeignKey('Font', null=True, blank=True, verbose_name=_('Font'))
    size = models.IntegerField(verbose_name=_('Size'))
    x = models.IntegerField(verbose_name=_('X'))
    y = models.IntegerField(verbose_name=_('Y'))
    format = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Extra'))

    class Meta:
        ordering = ['field']
        verbose_name = _("Badge")
        verbose_name_plural = _("Badges")

    def __unicode__(self):
        return self.field

class Attendee(User):
    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = _("Attendee")
        verbose_name_plural = _("Attendees")
        proxy = True

    def balance(self):
        price = self.price()
        if not self.payments.count():
            return price
        else:
            paid = self.payments.aggregate(sum=Sum('amount'))['sum']
            return price - paid
    balance.short_description = _("Balance")

    def price(self):
        if not self.type:
            return 0
        try:
            price = self.event.attendeetypeevent_set.get(attendeetype=self.type).price
        except AttendeeTypeEvent.DoesNotExist:
            price = "error"
        return price
    price.short_description = _("Price")

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)
    full_name.short_description = _("Name")

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)
