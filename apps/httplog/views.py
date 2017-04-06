from __future__ import unicode_literals

from django.views.generic.base import View, TemplateView
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.conf import settings

from apps.httplog.models import HttpRequestEntry


class RequestsHistoryView(View):
    """ Class based view for home page """

    template_name = "block/requests_list.html"

    def get(self, request):
        def is_non_viewed(entry, last_id):
            entry.non_viewed = entry.id > last_id
            return entry

        if request.is_ajax():
            last_entry_id = HttpRequestEntry.objects.first().id
            last_viewed_id = request.session.get('last_viewed_id')
            entries = HttpRequestEntry.objects.all()[
                      :settings.HTTP_LOG_ENTRIES_ON_PAGE]

            entries = [is_non_viewed(e, last_viewed_id) for e in entries]
            new_entries_count =  len([e for e in entries if e.non_viewed])
            request.session['last_viewed_id'] = last_entry_id

            return render(request, self.template_name, {
                'entries': entries,
                'non_viewed_count': new_entries_count
            })
        return HttpResponseBadRequest()


class RequestsHistoryPageView(TemplateView):
    """ Class based view for home page """

    template_name = "requests.html"
