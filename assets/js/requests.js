var requests = {
    requestsBlock: $(".request-history"),
    nonViewedSelector: "#non_viewed_count",
    prioritySelector: ".priority",

    init: function (opts) {
        var self = this;

        self.title = opts.title;
        self.history_url = opts.url;
        self.on_page = Number(opts.on_page);
        self.numbers = []
        for (var i = 1; i <= opts.on_page; i++) {
            self.numbers.push(i);
        }
        self.is_init = true;
        self.sort_enabled = false;

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

    fillSelect: function (self) {
        $(self.prioritySelector).each(function () {
            var select = $(this);
            var selected_opt = select.attr('data-value');

            $.each(self.numbers, function (index, value) {
                var selected = selected_opt == value;
                select.append(new Option(index + 1, value, selected, selected));
            });
        });

        $(self.prioritySelector).focus(function () {
            self.sort_enabled = true;
        });

        $(self.prioritySelector).change(function () {
            $.ajax({
                type: "POST",
                url: self.history_url,
                data: {
                    'entry_id': $(this).closest('tr').attr('data-id'),
                    'priority': $(this).val(),
                },
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            });

            self.sort_enabled = false;
            setTimeout(function () {
                self.getRequestHistory(self);
            }, self.timeout);
        });
    },

    getRequestHistory: function (self) {
        if (!self.sort_enabled) {
            $.get(self.url, function (data) {
                self.requestsBlock.html(data);
                self.fillSelect(self);

                // Update page title with (n) new requests
                var counter = $(self.nonViewedSelector).val();
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
};
