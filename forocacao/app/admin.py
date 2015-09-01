from django.contrib import admin
from django import forms
from django.utils.translation import ugettext as _

from suit_redactor.widgets import RedactorWidget

from .models import Event, Activity, Profession, Attendee, AttendeeType, AttendeePayment, PaymentMethod, EventBadge, Font, AttendeeReceipt, Content, Field

def has_approval_permission(request, obj=None):
    if request.user.has_perm('users.can_approve_participant'):
        return True
    return False


class ContentForm(forms.ModelForm):
    class Meta:
        widgets = {
            'text': RedactorWidget(editor_options={'lang': 'es', 'minHeight': '300'})
        }

class ContentAdmin(admin.ModelAdmin):
    form = ContentForm

admin.site.register(Content, ContentAdmin)

class AttendeeTypeInline(admin.TabularInline):
    model = Event.types.through

class EventBadgeInline(admin.TabularInline):
    model = EventBadge

class AttendeePaymentInline(admin.TabularInline):
    model = AttendeePayment

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "payment_method":
            if self.parent_obj:
                kwargs["queryset"] = PaymentMethod.objects.filter(id__in=self.parent_obj.event.payment_methods.all())
            if not request.user.is_superuser:
                kwargs["queryset"] = PaymentMethod.objects.filter(id__in=request.user.event.payment_methods.all())
        return super(AttendeePaymentInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super(AttendeePaymentInline, self).get_formset(
            request, obj, **kwargs)

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        AttendeeTypeInline,
        EventBadgeInline,
    ]

class ActivityAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class ProfessionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class AttendeeReceiptAdmin(admin.ModelAdmin):
    list_display = ['attendee', 'date' ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(AttendeeReceiptAdmin, self).get_form(request, obj, **kwargs)

        # if not superuser, limit type and profession to user's event
        if not request.user.is_superuser:
            form.base_fields['attendee'].queryset = Attendee.objects.filter(id__in=request.user.event.user_set.all())

        # show balance
        form.base_fields['attendee'].label_from_instance = lambda obj: "%s %s (%s %s)" % (obj.first_name, obj.last_name, _('Balance'), obj.balance())

        return form


class AttendeePaymentAdmin(admin.ModelAdmin):
    list_display = ['attendee', 'payment_method', 'amount' ]

class AttendeeAdmin(admin.ModelAdmin):

    list_display = ['id','first_name','last_name','email','profession','balance']
    readonly_fields = ('balance', 'event_price', 'extra_price', 'total_price', 'paid')

    def my_url_field(self, obj):
        return '<a href="%s%s">%s</a>' % ('http://url-to-prepend.com/', obj.url_field, obj.url_field)
    my_url_field.allow_tags = True
    my_url_field.short_description = 'Column description'

    list_filter = ('event__name','country','profession','type')
    search_fields = ['id','first_name','last_name']

    inlines = [
        AttendeePaymentInline,
    ]


    fieldsets = (
        (None, {
            'fields': ('event','event_price','extra_price','total_price','paid','balance','type','first_name', 'last_name', 'email', 'profession', 'other_profession',
            'phone','country','nationality','extra','sponsored','sponsor','photo')
        }),
        ('Informacion de actividades y biografia', {
            'classes': ('collapse',),
            'fields': ('text','activities',)
        }),
        ('Permisos de usuario', {
            'classes': ('collapse',),
            'fields': ['username', 'password', 'is_active','last_login','date_joined']
        }),
    )

    def get_queryset(self, request):
        qs = super(AttendeeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(event=request.user.event)

    def get_form(self, request, obj=None, **kwargs):
        if not has_approval_permission(request, obj):
            self.fieldsets[2][1]['fields'] = ['username', 'password', 'is_active','last_login','date_joined']
        form = super(AttendeeAdmin, self).get_form(request, obj, **kwargs)

        # required fields (not required in original model)
        form.base_fields['first_name'].required = True
        form.base_fields['last_name'].required = True
        form.base_fields['email'].required = True
        form.base_fields['password'].required = False
        form.base_fields['username'].required = False

        # if update, limit type and profession to current event
        if obj:
            form.base_fields['profession'].queryset = Profession.objects.filter(id__in=obj.event.professions.all())
            form.base_fields['activities'].queryset = Activity.objects.filter(id__in=obj.event.activities.all())
            form.base_fields['type'].queryset = AttendeeType.objects.filter(id__in=obj.event.types.all())

        # if not superuser, limit type and profession to user's event
        if not request.user.is_superuser:
            form.base_fields['profession'].queryset = Profession.objects.filter(id__in=request.user.event.professions.all())
            form.base_fields['activities'].queryset = Activity.objects.filter(id__in=request.user.event.activities.all())
            form.base_fields['type'].queryset = AttendeeType.objects.filter(id__in=request.user.event.types.all())
            form.base_fields['event'].initial = request.user.event
            form.base_fields['event'].widget = forms.HiddenInput()
            form.base_fields['event'].label = ''
            #self.readonly_fields = ('event',)

        return form

    def save_model(self, request, obj, form, change):
        obj.username = obj.email
        obj.save()



admin.site.register(Event, EventAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(AttendeeType)
admin.site.register(AttendeePayment, AttendeePaymentAdmin)
admin.site.register(AttendeeReceipt, AttendeeReceiptAdmin)
admin.site.register(PaymentMethod)
admin.site.register(Font)
admin.site.register(Field)
