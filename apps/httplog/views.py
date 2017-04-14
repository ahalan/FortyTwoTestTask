from __future__ import unicode_literals

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
            on_page = entries[:settings.HTTP_LOG_ENTRIES_ON_PAGE]
            new_entries = entries.filter(viewed=False)

            if viewed:
                new_entries.update(viewed=True)

            return render(request, self.template_name, {
                'entries': sorted(on_page, key=lambda x: x.priority),
                'non_viewed_count': new_entries.count()
            })
        return HttpResponseBadRequest()

    def post(self, request):
        """
        Updates entries priority
        
        Requires arguments: `entry_id` and `priority`
        """
        entry_id = request.POST.get('entry_id')
        priority = request.POST.get('priority')

        if not entry_id or not priority:
            return HttpResponse("Missing argument `entry_id` or `priority`")

        HttpRequestEntry.objects.filter(id=entry_id)\
                                .update(priority=int(priority))
        return HttpResponse("Success")
