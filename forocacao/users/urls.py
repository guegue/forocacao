# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the UserListView
    url(
        regex=r'^$',
        view=views.UserListView.as_view(),
        name='list'
    ),

    # URL pattern for the UserRedirectView
    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),

    # URL pattern for the UserDetailView
    url(
        regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),

    # URL pattern for the UserBadgeJPEG
    url(
        regex=r'^(?P<username>[\w.@+-]+)/jpeg/$',
        view=views.UserBadgeJPEG.as_view(),
        name='jpeg'
    ),

    # URL pattern for the UserBadgeView
    url(
        regex=r'^(?P<username>[\w.@+-]+)/badge/$',
        view=views.UserBadgeView.as_view(),
        name='badge'
    ),

    # URL pattern for the UserUpdateView
    url(
        regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),
]
