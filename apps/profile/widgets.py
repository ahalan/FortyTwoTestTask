from __future__ import unicode_literals

from django import forms


class CalendarWidget(forms.TextInput):

    class Media:
        js = (
            'lib/bootstrap-datepicker/js/bootstrap-datepicker.min.js',
        )
        css = {
            'all': (
                'lib/bootstrap-datepicker/css/bootstrap-datepicker3.min.css',
            )
        }

    def __init__(self, attrs=None):
        if attrs and 'class' in attrs:
            attrs['class'] += ' datepicker'
        else:
            attrs = {'class': 'form-control datepicker'}
        super(CalendarWidget, self).__init__(attrs=attrs)
