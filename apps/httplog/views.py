from __future__ import unicode_literals

from django.views.generic.base import View, TemplateView
from django.shortcuts import render
from django.http import HttpResponseBadRequest

from apps.httplog.models import HttpRequestEntry

class RequestsHistoryView(View):
    """ Class based view for home page """

    template_name = "block/requests_list.html"

    def get(self, request):
        if request.is_ajax():
            entries = HttpRequestEntry.objects.all()[:10]
            return render(request, self.template_name, {'entries': entries})
        else:
            return HttpResponseBadRequest()


class RequestsHistoryPageView(TemplateView):
    """ Class based view for home page """

    template_name = "requests.html"