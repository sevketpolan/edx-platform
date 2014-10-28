import json


class ValidationMessage(object):

    error_type = "error"
    warning_type = "warning"

    def __init__(self, text, message_type=None, action_class=None, action_label=None, action_runtime_event=None):
        assert isinstance(text, unicode), "Message text must be unicode"
        self.text = text
        self.type = message_type
        self.action_class = action_class
        self.action_label = action_label
        self.action_runtime_event = action_runtime_event

    def to_json(self):
        return self.__dict__

    def __unicode__(self):
        return self.text


class ValidationMessages(object):

    def __init__(self):
        self.summary = None
        self.detailed_messages = []
        self.show_detailed_only_when_root = False
        self.additional_root_classes = ""
        self.additional_inline_classes = ""
        self.is_empty = True

    def set_detailed_message_visibility(self, only_visible_when_root):
        self.show_detailed_only_when_root = only_visible_when_root

    def set_summary(self, summary_validation_message):
        self.summary = summary_validation_message
        self.is_empty = False

    def add_detailed_message(self, validation_message):
        self.detailed_messages.insert(0, validation_message)
        self.is_empty = False

    def add_detailed_messages(self, validation_messages):
        for message in validation_messages:
            self.detailed_messages.insert(0, message)

    def set_additional_root_classes(self, additional_root_classes):
        self.additional_root_classes = additional_root_classes

    def set_additional_inline_classes(self, additional_inline_classes):
        self.additional_inline_classes = additional_inline_classes

    def to_json(self):
        dict_representation = {
            "detailed_messages": [message.to_json() for message in self.detailed_messages],
            "show_detailed_only_when_root": self.show_detailed_only_when_root,
            "additional_root_classes": self.additional_root_classes,
            "additional_inline_classes": self.additional_inline_classes,
            "is_empty": self.is_empty
        }
        if self.summary:
            dict_representation["summary"] = self.summary.to_json()
        return json.dumps(dict_representation)


