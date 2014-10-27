define(["jquery", "underscore", "js/views/baseview", "js/models/validation_messages"],
    function ($, _, BaseView, ValidationMessagesModel) {
        var ValidationMessages = BaseView.extend({

            // takes ValidationMessagesModel as a model
            initialize: function() {
                BaseView.prototype.initialize.call(this);
                this.template = this.loadTemplate('component-validation-messages');
            },

            render: function () {
                var getIcon = function (validationType) {
                    if (validationType === 'error') {
                        return 'icon-exclamation-sign';
                    }
                    else if (validationType === 'warning') {
                        return 'icon-warning-sign';
                    }
                    return null;
                };
                this.$el.html(this.template({
                    messages: this.model,
                    getIcon: getIcon
                }));
                return this;
            }

        });

        return ValidationMessages;
    });