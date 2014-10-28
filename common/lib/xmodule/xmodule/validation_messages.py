class ValidationMessageType(object):
    """
    The type for a validation message -- currently 'warning' or 'error'.
    """
    warning = 'warning'
    error = 'error'



# TODO: move this into the xblock repo once it has a formal validation contract
class ValidationMessages(object):

    """
    The type for a validation message -- currently 'warning' or 'error'.
    """
    warning_type = 'warning'
    error_type = 'error'

    """
    Add a single validation message for an xblock.
    """
    def add_message(self, message_text, message_type, action_class=None, action_runtime_event=None):
        assert isinstance(message_text, unicode)
        self.message_text = message_text
        self.message_type = message_type
        self.action_class = action_class
        self.action_label = action_label

