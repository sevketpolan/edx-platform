var edx = edx || {};

(function($, _, Backbone, gettext) {
    'use strict';

    edx.student = edx.student || {};
    edx.student.account = edx.student.account || {};


    edx.student.account.LoginModel = Backbone.Model.extend({

        defaults: {
            email: '',
            password: '',
            remember: false
        },

        urlRoot: '',

        initialize: function( obj ) {
            this.urlRoot = obj.url;
        },

        sync: function(method, model) {
            var headers = {
                'X-CSRFToken': $.cookie('csrftoken')
            };

            $.ajax({
                url: model.urlRoot,
                type: 'POST',
                data: model.attributes,
                headers: headers
            })
            .done(function() {
                // check for enrollment
                // try to enroll

                var enrollment = edx.student.account.EnrollmentInterface;
                var query = new URI(window.location.search);
                var url = '/dashboard';
                var query_map = query.search(true);
                
                // check for forwarding url
                if("next" in query_map) {
                    var next = query_map['next'];
                    if(!window.isExternal(next)){
                        url = next;
                    }
                }

                model.trigger('sync');

                // if we need to enroll in the course, mark as enrolled
                if("enrollment_action" in query_map && query_map["enrollment_action"] === "enroll"){
                    var course_id = query_map['course_id'];
                    enrollment.enroll(course_id, url);
                }
                else {
                    window.location.href = url;
                }


            })
            .fail( function( error ) {
                model.trigger('error', error);
            });
        }
    });
})(jQuery, _, Backbone, gettext);
