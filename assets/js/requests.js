var requests = {
    requestsBlock: $(".request-history"),
    nonViewedCountId: "#non_viewed_count",

    init: function (url) {
        var self = this;
        self.url = url;

        self.getRequestHistory(self);
    },

    getRequestHistory: function (self) {
        $.get(self.url, function (data) {
            self.requestsBlock.html(data);

            var counter = $(self.nonViewedCountId).val();
            if (counter != 0) {
                document.title = "Requests (" + counter + ")";
            } else {
                document.title = "Requests";
            }

            setTimeout(function () {
                self.getRequestHistory(self);
            }, 5000);
        });
    }
}
