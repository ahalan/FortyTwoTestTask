var Messenger = {
    elements: {
        messageInput: $('.chat-footer input'),
        sendMessageButton: $('.chat-footer button'),
        messageList: $('.chat-messages'),
        messageArea: $('.chat-area'),
        membersCounterBadge: $('.badge'),
        inputTypingIndicator: $('.typing-indicator')
    },

    init: function (opts) {
        var self = this;

        self.channel = opts.channel;
        self.uuid = opts.username;
        self.isUserTyping = false;

        self.pubnub = new PubNub({
            subscribeKey: opts.subscribeKey,
            publishKey: opts.publishKey,
            uuid: self.uuid,
            ssl: true
        });

        self.subscribe(self);
        self.addListener(self);
        self.addEvents(self);
    },

    addEvents: function (self) {
        self.elements.messageInput.on('keyup', function (e) {
            if (self.elements.messageInput.val() !== '' && !self.isUserTyping) {
                self.setTypingState(self, true);
            }
            if ((e.keyCode || e.charCode) === 13) {
                self.setTypingState(self, false);
                self.publishMessage(self);
            }
        });
        self.elements.sendMessageButton.on('click', function (e) {
            self.setTypingState(self, false);
            self.publishMessage(self);
        });
    },

    addListener: function (self) {
        self.pubnub.addListener({
            message: function (m) {
                self.displayContents(self, m.message);
            },
            presence: function (m) {
                self.updateTypingState(self, m);
                self.displayOccupancy(self, m);
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

        self.setTypingState(self, false);
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

    displayOccupancy: function (self, presence) {
        self.elements.membersCounterBadge.text(presence.occupancy);

        if (presence.uuid === self.uuid) return;
        if ((presence.action === 'join') ||
            (presence.action === 'timeout') ||
            (presence.action === 'leave')) {

            var status = (presence.action === 'join') ? 'joined' : 'left';
            var message = {
                text: presence.uuid + ' ' + status + ' chat',
                username: presence.uuid,
                action: true
            };
            self.displayContents(self, message)
        }
    },

    setTypingState: function (self, isTyping) {
        self.isUserTyping = isTyping;
        self.pubnub.setState({
            state: {isTyping: self.isUserTyping},
            channels: [self.channel]
        });
    },

    updateTypingState: function (self, event) {
        // We don't want to receive our own presence events
        if (event['uuid'] === self.uuid) return;

        // Add typing
        if (event['action'] === 'state-change' && event['state']['isTyping']) {
            self.elements.inputTypingIndicator.text(event.uuid + ' is typing...')
        }
        // Remove typing
        else if ((event['action'] === 'state-change' && event['state']['isTyping'] === false) ||
            event['action'] === 'timeout' ||
            event['action'] === 'leave') {
            self.setTypingState(self, false);
            self.elements.inputTypingIndicator.html('');
        }
    }

};
