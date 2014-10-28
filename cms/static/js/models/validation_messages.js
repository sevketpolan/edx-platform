define(["backbone", "gettext"], function (Backbone, gettext) {
    /**
     * Model for validation messages shown on components in Studio.
     */
    var ValidationMessages = Backbone.Model.extend({
        defaults: {
            summary: {},
            detailed_messages: [],
            show_detailed_only_when_root: false,
            root: false,
            additional_root_classes: "",
            additional_inline_classes: ""
        },

        getSummaryMessage: function () {
            var summaryMessage;
            if ("message" in this.get("summary")) {
                summaryMessage = this.get("summary");
            }
            else {
                summaryMessage = {"message" : gettext("This component has validation issues.")};
            }

            if (!("type" in summaryMessage)) {
                summaryMessage.type = this.getSummaryType();
            }
            return summaryMessage;
        },

        getSummaryType: function () {
            var detailedMessages = this.get("detailed_messages");
            for (var i = 0; i < detailedMessages.length; i++) {
                if (detailedMessages[i].type === "error") {
                    return "error";
                }
            }
            return "warning";
        },

        getDisplayName: function (messageType) {
            if (messageType === "warning") {
                // Translators: This message will be added to the front of messages of type warning,
                // e.g. "Warning: this component has not been configured yet".
                return gettext("Warning");
            }
            else if (messageType === "error") {
                // Translators: This message will be added to the front of messages of type error,
                // e.g. "Error: required field is missing".
                return gettext("Error");
            }
            else {
                return null;
            }
        },

        getDetailedMessages: function () {
            if (this.get("show_detailed_only_when_root") && !this.get("root")) {
                return [];
            }
            return this.get("detailed_messages");
        },

        getAdditionalClasses: function () {
            var classes = this.get("root") ? this.get("additional_root_classes") : this.get("additional_inline_classes");
            return classes;
        }

    });
    return ValidationMessages;
});

