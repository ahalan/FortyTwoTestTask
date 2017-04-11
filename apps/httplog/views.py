from __future__ import unicode_literals

import json

from django.views.generic.base import View, TemplateView
from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from django.conf import settings

from apps.httplog.models import HttpRequestEntry


class RequestsHistoryPageView(TemplateView):
    """ Class based view for requests page """

    template_name = "requests.html"


class RequestsHistoryView(View):
    """ Class based view for request history block """

    template_name = "block/requests_list.html"

    def get(self, request):
        """
        Returns last entries and count of non viewed entries.
        
        If passed variable 'viewed' = True then all non viewed
        entries will be updated as viewed.
        """

        if request.is_ajax():
            viewed = request.GET.get('viewed', False)

            entries = HttpRequestEntry.objects.all()
            new_entries = entries.filter(viewed=False)

            if viewed:
                new_entries.update(viewed=True)

            return render(request, self.template_name, {
                'entries': entries[:settings.HTTP_LOG_ENTRIES_ON_PAGE],
                'non_viewed_count': new_entries.count()
            })
        return HttpResponseBadRequest()

    def post(self, request):
        """
        Updates entries priority

        Requires list of objects with 'id' and 'priority'
        entry keys passed in json format.
        """

        entries_json = request.POST.get('entries')

        if not entries_json:
            return HttpResponse("Missing argument `entries`")

        entries = json.loads(entries_json)

        for entry in entries:
            HttpRequestEntry.objects.filter(id=entry['id']) \
                                    .update(priority=int(entry['priority']))
        return HttpResponse("Success")
