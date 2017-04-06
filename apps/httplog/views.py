from __future__ import unicode_literals

from django.views.generic.base import View, TemplateView
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.conf import settings

from apps.httplog.models import HttpRequestEntry


class RequestsHistoryPageView(TemplateView):
    """ Class based view for home page """

    template_name = "requests.html"


class RequestsHistoryView(View):
    """ Class based view for home page """

    template_name = "block/requests_list.html"

    def get(self, request):
        if request.is_ajax():
            viewed = request.GET.get('viewed', False);
            entries = HttpRequestEntry.objects.all()
            new_entries_count = entries.filter(viewed=False).count()

            if viewed:
                entries.update(viewed=True)

            return render(request, self.template_name, {
                'entries': entries[:settings.HTTP_LOG_ENTRIES_ON_PAGE],
                'non_viewed_count': new_entries_count
            })
        return HttpResponseBadRequest()
