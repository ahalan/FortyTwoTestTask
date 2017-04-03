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
        if request.is_ajax():
            entries = HttpRequestEntry.objects.all()
            context = {
                'entries': entries[:settings.HTTP_LOG_ENTRIES_ON_PAGE]
            }
            return render(request, self.template_name, context)
        return HttpResponseBadRequest()


class RequestsHistoryPageView(TemplateView):
    """ Class based view for home page """

    template_name = "requests.html"
