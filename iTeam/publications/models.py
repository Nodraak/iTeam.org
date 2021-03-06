#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-21 18:34:56
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-10-27 16:58:57

# This file is part of iTeam.org.
# Copyright (C) 2014 Adrien Chardon (Nodraak).
#
# iTeam.org is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# iTeam.org is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with iTeam.org. If not, see <http://www.gnu.org/licenses/>.


import string
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify


def image_path(instance, filename):
    dir = str(instance.pk)
    filename = u'original.' + string.lower(filename.split('.')[-1])

    return os.path.join('publications', dir, filename)


class Publication(models.Model):
    title = models.CharField(max_length=settings.SIZE_MAX_TITLE, verbose_name=u'Titre')
    subtitle = models.CharField(max_length=settings.SIZE_MAX_TITLE, blank=True, verbose_name=u'Sous-titre')

    author = models.ForeignKey(User, verbose_name=u'Auteur')
    pub_date = models.DateTimeField('Date de publication')

    image = models.ImageField(
        upload_to=image_path,
        blank=True,
        null=True,
        default=None
    )

    type = models.CharField(
        max_length=1,
        choices=settings.PUBLICATIONS_MODEL_TYPES,
        default='P',
    )

    text = models.TextField()

    is_draft = models.BooleanField(default=True)

    def image_url(self):
        if self.image:
            return self.image.url
        elif self.type == 'T':
            return '/static/images/tutoriel.png'
        elif self.type == 'N':
            return '/static/images/news.png'
        else:
            return '/static/images/publication.png'

    def get_absolute_url(self):
        return reverse('publications:detail', args=[self.pk, slugify(self.title)])
