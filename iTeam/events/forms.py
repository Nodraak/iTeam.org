#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-21 18:54:29
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-09-02 14:53:30

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


from django import forms
from django.conf import settings


class EventForm(forms.Form):
    title = forms.CharField(
        label='Titre',
        widget=forms.TextInput(
            attrs={
                'autofocus': '',
                'placeholder': 'Titre'
            }
        )
    )
    place = forms.CharField(
        label='Lieu',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Lieu'
            }
        ),
        required=False
    )
    date_start = forms.DateTimeField(
        label='Date de debut',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Date de début aaaa-mm-jj hh:mm'
            }
        )
    )
    image = forms.ImageField(
        required=False
    )
    type = forms.ChoiceField(
        label='Type d\'événement',
        widget=forms.RadioSelect,
        choices=settings.EVENTS_MODEL_TYPES,
        initial='O',
        required=False,
    )
    is_draft = forms.ChoiceField(
        label='Status de l\'événement',
        widget=forms.RadioSelect,
        choices=settings.MODEL_IS_DRAFT,
        initial='1',
        required=False,
    )
    text = forms.CharField(
        label='Texte',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Texte',
                'rows': '15'
            }
        )
    )

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        img = cleaned_data.get('image')

        if img and img.size > settings.SIZE_MAX_IMG:
            msg = (
                u'Fichier trop lourd (%d Ko / %d Ko max). Pour ne pas saturer le serveur, merci '
                u'de réduire la résolution de l\'image.') % (img.size/1024, settings.SIZE_MAX_IMG/1024)
            self._errors['image'] = self.error_class([msg])

            if 'image' in cleaned_data:
                del cleaned_data['image']

        return cleaned_data
