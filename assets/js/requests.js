var requests = {
    requestsBlock: $(".request-history"),
    nonViewedCountId: "#non_viewed_count",

    init: function (url) {
        var self = this;
        self.history_url = url;
        self.title = 'Requests';
        self.timeout = 3000;
        self.focused_on_init = !document.hidden;

        self.getRequestHistory(self);
    },

    getRequestHistory: function (self) {
        var url = self.history_url;
        var timeout = self.timeout;

        // check if user viewed requests on tab
        if (!document.hidden && !self.focused_on_init) {
            url = self.history_url + "?viewed=true";
            timeout = self.timeout;
        } else if (document.hidden) {
            timeout = self.timeout / 6;
        }

        $.get(url, function (data) {
            self.focused_on_init = false;
            self.requestsBlock.html(data);

            // Update page title with (n) new requests
            var counter = $(self.nonViewedCountId).val();
            if (counter != 0) {
                document.title = self.title + " (" + counter + ")";
            } else {
                document.title = self.title;
            }

            setTimeout(function () {
                self.getRequestHistory(self);
            }, timeout);
        });
    }
}
