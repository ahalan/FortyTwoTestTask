var requests = {
    requestsBlock: $(".request-history"),

    init: function (url) {
        var self = this;
        self.url = url;

        self.getRequestHistory(self.url);
        setTimeout(function () {
            self.getRequestHistory(self.url)
        }, 10000);
    },
    getRequestHistory: function (url) {
        $.get(url, function (data) {
            $(self.requestsBlock).html(data);
        });
    }
}
