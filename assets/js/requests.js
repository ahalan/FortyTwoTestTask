var requests = {
    requestsBlock: $(".request-history"),
    nonViewedCountId: "#non_viewed_count",

    init: function (url) {
        var self = this;
        self.url = url;
        self.title = 'Requests';
        self.getRequestHistory(self);

        window.onfocus = function () {
            self.focused = true;
        };
        window.onblur = function () {
            self.focused = false;
        };
    },

    getRequestHistory: function (self) {
        var url = self.url;
        if (self.focused) {
            url = self.url + "?viewed=true";
        }

        $.get(url, function (data) {
            self.requestsBlock.html(data);
            // Update page title with
            var counter = $(self.nonViewedCountId).val();
            if (counter != 0) {
                document.title = self.title + " (" + counter + ")";
            } else {
                document.title = self.title;
            }

            setTimeout(function () {
                self.getRequestHistory(self);
            }, 500);
        });
    }
}
