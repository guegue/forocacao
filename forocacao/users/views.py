# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import base64
from PIL import Image, ImageDraw, ImageFont


from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from braces.views import LoginRequiredMixin
from easy_thumbnails.files import get_thumbnailer

from .models import User


class UserBadgeJPEG(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    def get(self, request, username):
        participant = self.get_object()
        event = participant.event

        img = Image.new('RGBA', (event.badge_size_x, event.badge_size_y), event.badge_color)
        draw = ImageDraw.Draw(img)

        match = {
                'event': event.name,
                'name': "%s %s" % (participant.first_name.partition(' ')[0], participant.last_name.partition(' ')[0] ),
                'first_name': participant.first_name,
                'last_name': participant.last_name,
                'profession': participant.profession,
                'country': participant.country.name,
                'type': participant.type,
                'email': participant.email,
            }
        for field in event.eventbadge_set.all():
            x = field.x
            y = field.y
            size = field.size
            if field.field == 'logo':
                if participant.event.logo:
                    logo = Image.open(participant.event.logo.file.file)
                    logo.thumbnail((size,size))
                    img.paste(logo, (x,y))
            elif field.field == 'photo':
                if participant.photo:
                    photo = Image.open(participant.photo)
                    photo.thumbnail((size,size))
                    img.paste(photo, (x,y))
            else:
                if field.field == 'text':
                    content = field.format
                else:
                    content = match[field.field]
                fnt = ImageFont.truetype(field.font.filename, size)
                color = field.color
                draw.text((x,y), ("%s") % (content), font=fnt, fill=color)

        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return HttpResponse(response, content_type="image/png")

class UserBadgeView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"

    template_name = 'users/user_badge.html'


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['first_name', 'last_name', 'phone', 'activities' ] #FIXME : add all needed fields

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
