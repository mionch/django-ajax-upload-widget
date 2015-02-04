# -*- coding: utf-8 -*-
import uuid

from django import forms

from ajax_upload.models import UploadedFile


def normalize_polish_chars(text):
    if type(text) is not unicode:
        text = unicode(text, 'utf-8')
    trans_tab = {u'ą': 'a', u'ć': 'c', u'ę': 'e', u'ł': 'l', u'ń': 'n', u'ó': 'o', u'ś': 's', u'ż': 'z', u'ź': 'z',
                 u'Ą': 'A', u'Ć': 'C', u'Ę': 'E', u'Ł': 'L', u'Ń': 'N', u'Ó': 'O', u'Ś': 'S', u'Ż': 'Z', u'Ź': 'Z'}
    return ''.join(trans_tab.get(char, char) for char in text)


class UploadedFileForm(forms.ModelForm):
    def __init__(self, data=None, files=None, **kwargs):
        for __, uploaded_file in files.iteritems():
            uploaded_file.name = normalize_polish_chars(uploaded_file.name)
        super(UploadedFileForm, self).__init__(data=data, files=files, **kwargs)

    class Meta:
        model = UploadedFile
        fields = ('file',)

    def clean_file(self):
        data = self.cleaned_data['file']
        # Change the name of the file to something unguessable
        # Construct the new name as <unique-hex>-<original>.<ext>
        data.name = u'%s-%s' % (uuid.uuid4().hex, data.name)
        return data
