from __future__ import unicode_literals

from django.views.generic.base import TemplateView


class RequestsView(TemplateView):
    """ Class based view for home page """

    template_name = "requests_list.html"