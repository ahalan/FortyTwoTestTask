var Messenger = {
    elements: {
        messageInput: $('.chat-footer input'),
        sendMessageButton: $('.chat-footer button'),
        messageList: $('.chat-messages'),
        messageArea: $('.chat-area'),
        membersCounterBadge: $('.badge'),
        inputTypingIndicator: $('.typing-indicator'),
        membersMap: $('.chat-map')[0]
    },

    init: function (opts) {
        var self = this;

        self.markers = [];
        self.isUserTyping = false;
        self.is_first_init = true;
        self.channel = opts.channel;
        self.uuid = opts.username;
        self.lat = opts.latitude;
        self.lng = opts.longitude;

        // Initialization of google map
        self.center = new google.maps.LatLng(self.lat, self.lng);
        self.map = new google.maps.Map(self.elements.membersMap, {
            zoom: 5,
            center: self.center
        });

        // Initialization PubNub instance
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
                self.setUserState(self, true);
            }
            if ((e.keyCode || e.charCode) === 13) {
                self.setUserState(self, false);
                self.publishMessage(self);
            }
        });

        self.elements.sendMessageButton.on('click', function (e) {
            self.setUserState(self, false);
            self.publishMessage(self);
        });
    },

    addListener: function (self) {
        self.pubnub.addListener({
            message: function (entry) {
                self.displayContents(self, entry.message);
            },
            presence: function (event) {
                self.updateTypingState(self, event);
                self.displayOccupancy(self, event);
                self.updateMap(self, event);
            },
            status: function (status) {
                if (status.category === 'PNConnectedCategory') {
                    self.fetchHistory(self);
                    self.updateMap(self);
                    self.setUserState(self, false);
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

        self.setUserState(self, false);
        self.elements.messageInput.val('');

        // Scroll to last message
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
                // Scroll to last message
                self.elements.messageArea.animate({
                    scrollTop: self.elements.messageArea.prop("scrollHeight")
                }, 1000);
            }
        );
    },

    displayContents: function (self, message, timetoken) {
        if (!message || !message.text) return;

        var date = new Date(),
            username = message.username,
            text = message.text;

        // Convert timetoken to readable date format
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

        // Ingore own presence events
        if (presence.uuid === self.uuid) return;

        if ((presence.action === 'join') ||
            (presence.action === 'timeout') ||
            (presence.action === 'leave')) {

            // Show message about user join/left
            var status = (presence.action === 'join') ? 'joined' : 'left';
            var message = {
                text: presence.uuid + ' ' + status + ' chat',
                username: presence.uuid,
                action: true
            };
            self.displayContents(self, message)
        }
    },

    setUserState: function (self, isTyping) {
        self.isUserTyping = isTyping;
        self.pubnub.setState({
            state: {
                isTyping: self.isUserTyping,
                latlng: [self.lat, self.lng]
            },
            channels: [self.channel]
        });
    },

    updateTypingState: function (self, event) {
        // Ignore own presence events
        if (event.uuid === self.uuid) return;

        // Add typing
        if (event.action === 'state-change' && event.state.isTyping) {
            self.elements.inputTypingIndicator.text(event.uuid + ' is typing...')
        }
        // Remove typing
        else if ((event.action === 'state-change' && event.state.isTyping === false) ||
            event.action === 'timeout' ||
            event.action === 'leave') {

            self.setUserState(self, false);
            self.elements.inputTypingIndicator.html('');
        }
    },

    updateMap: function (self, event) {
        // Init map with members markers once
        if (self.is_first_init) {

            // Add maker for self
            self.addMarker(self, self.lat, self.lng, self.uuid);

            // Get active users
            self.pubnub.hereNow({
                channels: [self.channel],
                includeState: true
            }, function (status, response) {
                var users = response.channels[self.channel].occupants;

                // Add makers for currently online users
                $.each(users, function (index, user) {
                    if (user.state) {
                        var latlng = user.state.latlng;
                        self.addMarker(self, latlng[0], latlng[1], user.uuid)
                    }
                });

                self.is_first_init = false;
            });
        } else if (event) {
            // Ingore own presence events
            if (event.uuid === self.uuid) return;

            // Add marker of new member
            if (event.action === 'state-change' && event.state) {
                var latlng = event.state.latlng;
                self.addMarker(self, latlng[0], latlng[1], event.uuid)

            // Remove marker
            } else if (event.action === 'leave') {
                self.removeMarker(self, event.uuid)
            }
        }
    },

    getMarkerByUuid: function (self, uuid) {
         // Getting marker by uuid
        return $.grep(self.markers, function (e) {return e.uuid === uuid;});
    },

    addMarker: function (self, lat, lng, uuid) {
        var markers = self.getMarkerByUuid(self, uuid);

        // Add marker on map and to markers list
        if (markers == 0) {
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(lat, lng),
                map: self.map,
                title: uuid,
                uuid: uuid
            });
            self.markers.push(marker);
        }
    },

    removeMarker: function (self, uuid) {
        var markers = self.getMarkerByUuid(self, uuid);

        // Remove marker from map and markers list
        if (markers !== 0) {
            markers[0].setMap(null);
            self.markers = self.markers.filter(function (el) {
                return el.uuid !== uuid;
            });
        }
    }
};
