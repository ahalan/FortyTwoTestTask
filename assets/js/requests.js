function getRequestHistory(url) {
    $.get(url, function (data) {
        $(".request-history").html(data);
    });
};