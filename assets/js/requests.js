var requests = {
    requestsBlock: $(".request-history"),
    nonViewedCountId: "#non_viewed_count",

    init: function (url) {
        var self = this;

        self.history_url = url;
        self.is_first_init = true;
        self.title = 'Requests';

        self.isFocused(self);
        self.getRequestHistory(self);

        setInterval(function () {
            self.isFocused(self);
        }, 500);
    },

    isFocused: function (self) {
        self.timeout = 1000;
        self.url = self.history_url;

        if (self.is_first_init) {
            self.is_first_init = false;
        } else {
            if (!document.hidden) {
                self.url = self.history_url + "?viewed=true";
            } else {
                self.timeout = 800;
            }
        }
    },

    getRequestHistory: function (self) {
        $.get(self.url, function (data) {
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
            }, self.timeout);
        });
    }
}
