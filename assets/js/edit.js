var editForm = {
    elements: {
        notifications: $('.notifications'),
        notificationsText: $('.notifications-text'),
        submitBtn: $('.btn-edit-submit'),
        form: $('.profile-edit-form'),
        formGroupBlock: $('.form-group'),
        helpBlock: $('.help-block'),
        dateInput: $('.datepicker'),
        thumbnailImg: $('.thumbnail img')
    },
    hasError: 'has-error',

    init: function (url) {
        var self = this;
        self.url = url;

        self.elements.dateInput.datepicker({
            format: "yyyy-mm-dd",
            autoclose: true
        });

        self.elements.notifications.hide();

        self.elements.form.submit(function (e) {
            e.preventDefault();
            self.actionSubmit(self);
        });
    },

    actionSubmit: function (self) {
        var data = new FormData(self.elements.form[0]);

        self.elements.notifications.hide();
        self.elements.submitBtn.button('loading');
        self.elements.form.find(":input").prop("disabled", true);

        $.ajax({
            type: "POST",
            url: self.url,
            data: data,
            crossDomain: false,
            cache: false,
            contentType: false,
            processData: false,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success: function (data) {
                self.elements.formGroupBlock.removeClass(self.hasError);
                self.elements.helpBlock.html('');

                self.elements.form.find(":input").prop("disabled", false);
                self.elements.submitBtn.button('reset');

                if (data.success) {
                    self.elements.notifications.show();
                    self.elements.notificationsText.text('Profile saved successfully!');
                    self.elements.thumbnailImg.attr('src', data.payload.photo_url)
                } else {
                    $.each(data.payload.errors, function (key, value) {
                        var $el = $('#id_' + key);
                        $el.closest('.form-group').addClass(self.hasError);
                        $el.next(".help-block").text(value);
                    })
                }
            }
        });
    }
};
