var Messenger = {
    elements: {
        messageInput: $('.chat-footer input'),
        sendMessageButton: $('.chat-footer button'),
        messageList: $('.chat-messages'),
        messageArea: $('.chat-area'),
        membersCounterBadge: $('.badge')
    },

    init: function (opts) {
        var self = this;

        self.channel = opts.channel;
        self.uuid = opts.username;

        self.pubnub = new PubNub({
            subscribeKey: opts.subscribeKey,
            publishKey: opts.publishKey,
            uuid: self.uuid,
            ssl: true
        });

        self.subscribe(self);
        self.addListener(self);

        self.elements.messageInput.on('keyup', function (e) {
            (e.keyCode || e.charCode) === 13 && self.publishMessage(self)
        });
        self.elements.sendMessageButton.on('click', self.publishMessage(self));
    },

    // hereNow: function (self) {
    //     self.pubnub.hereNow({
    //             channels: [self.channel],
    //         },
    //         function (status, response) {
    //             var channel = response.channels[self.channel];
    //             self.elements.membersCounterBadge.text(channel.occupancy);
    //             console.log(channel)
    //         }
    //     );
    // },

    addListener: function (self) {
        self.pubnub.addListener({
            message: function (m) {
                self.displayContents(self, m.message);
            },
            presence: function (m) {
                // if(m.action === 'join') {
                //     self.pubnub.setState({
                //             state: {
                //                 isTyping: false
                //             },
                //             channels: [self.channel]
                //         },
                //         function (status, response) {
                //             console.log(status, response)
                //         }
                //     );
                // }
                //
                // if(m.action === 'state-change') {
                //     self.pubnub.setState({
                //             state: {
                //                 isTyping: true
                //             },
                //             channels: [self.channel]
                //         },
                //         function (status, response) {
                //             console.log(status, response)
                //         }
                //     );
                //     if(m.data.isTyping === true) {
                //         console.log(m.uuid + ' is typing...')
                //     }
                // }
                // self.displayOccupancy(self, m);
            },
            status: function (status) {
                if (status.category === 'PNConnectedCategory') {
                    self.fetchHistory(self);
                }
            }
        });
    },

    subscribe: function (self) {
        self.pubnub.subscribe({
            channels: [self.channel],
            withPresence: true
        });
    },

    publishMessage: function (self) {
        var config = {
            channel: self.channel,
            message: {
                username: self.uuid,
                text: self.elements.messageInput.val()
            }
        };

        self.pubnub.publish(config, function (status, response) {
            if (status.error) console.log(status)
        });

        self.elements.messageInput.val('');
        self.elements.messageArea.animate({
            scrollTop: self.elements.messageArea.prop("scrollHeight")
        }, 1000);
    },

    fetchHistory: function (self) {
        self.pubnub.history({
                channel: self.channel,
                count: 30
            },
            function (status, response) {
                response.messages.forEach(function (message) {
                    self.displayContents(self, message.entry, message.timetoken);
                });
            }
        );
    },

    displayContents: function (self, message, timetoken) {
        if (!message || !message.text) return;

        var date = new Date(),
            username = message.username,
            text = message.text;

        if (timetoken) date = new Date(timetoken / 1e4);

        var content = '<li class="clearfix"><div class="chat-messages-body clearfix">';
        var header = '\
            <div class="header"> \
                <strong class="primary-font">' + username + '</strong> \
                <small class="pull-right text-muted"> \
                    <span class=""></span>' + date.getFormattedDate() + ' \
                </small> \
            </div>';

        if (!message.action) content = content + header;
        content = content + '<p>' + text + '</p></div></li>';

        self.elements.messageList.append(content)
    },

    // displayOccupancy: function (self, presence) {
    //     self.elements.membersCounterBadge.text(presence.occupancy);
    //
    //     if (presence.uuid === self.uuid) return;
    //     if ((presence.action === 'join')    ||
    //         (presence.action === 'timeout') ||
    //         (presence.action === 'leave')) {
    //
    //         var status = (presence.action === 'join') ? 'joined' : 'left';
    //         var message = {
    //             text: presence.uuid + ' ' + status + ' chat',
    //             username: presence.uuid,
    //             action: true
    //         };
    //         self.displayContents(self, message)
    //     }
    // }
};
