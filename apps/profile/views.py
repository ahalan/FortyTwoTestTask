from __future__ import unicode_literals

from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "profile/about.html"