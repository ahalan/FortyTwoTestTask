var requests = {
    requestsBlock: $(".request-history"),

    tableBodySelector: ".table tbody",
    tableRowSelector: ".table tbody tr",
    nonViewedSelector: "#non_viewed_count",

    init: function (opts) {
        var self = this;

        self.title = opts.title;
        self.history_url = opts.url;
        self.is_init = true;
        self.interval = 0;

        self.isFocused(self);
        self.getRequestHistory(self);

        setInterval(function () {
            self.isFocused(self);
        }, 500);
    },

    isFocused: function (self) {
        self.timeout = 1000;
        self.url = self.history_url;

        if (self.is_init) {
            self.is_init = false;
        } else {
            if (!document.hidden) {
                self.url = self.history_url + "?viewed=true";
            } else {
                self.timeout = 800;
            }
        }
    },

    initSortable: function (self) {
        var fixHelper = function (e, ui) {
            ui.children().each(function () {
                $(this).width($(this).width());
            });
            return ui;
        };

        $(self.tableBodySelector).sortable({
            update: function (event, ui) {
                var entries = [];

                // clearInterval(self.interval);

                $(self.tableRowSelector).each(function () {
                    var $firstChild = $(this).children('td:first-child');

                    $firstChild.html($(this).index());

                    entries.push({
                        id: $(this).attr('data-id'),
                        priority: $firstChild.text()
                    })
                });

                $.ajax({
                    type: "POST",
                    url: self.history_url,
                    data: {
                        'entries': JSON.stringify(entries)
                    },
                    dataType: 'json',
                    beforeSend: function (xhr) {
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    }
                });
            },
            helper: fixHelper
        }).disableSelection();

    },

    getRequestHistory: function (self) {
        $.get(self.url, function (data) {
            self.requestsBlock.html(data);

            // Update page title with (n) new requests
            var counter = $(self.nonViewedSelector).val();
            if (counter != 0) {
                document.title = self.title + " (" + counter + ")";
            } else {
                document.title = self.title;
            }

            self.initSortable(self);

            self.interval = setInterval(function () {
                self.getRequestHistory(self);
            }, self.timeout);

        });
    }
};
