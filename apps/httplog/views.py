from __future__ import unicode_literals

from django.views.generic.base import TemplateView


class RequestsHistoryView(TemplateView):
    """ Class based view for home page """

    template_name = "block/requests_list.html"


class RequestsHistoryPageView(TemplateView):
    """ Class based view for home page """

    template_name = "requests.html"