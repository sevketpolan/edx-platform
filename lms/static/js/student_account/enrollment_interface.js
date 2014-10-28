var edx = edx || {};

(function($, _, gettext) {
    'use strict';

    edx.student = edx.student || {};
    edx.student.account = edx.student.account || {};

    edx.student.account.EnrollmentInterface = function (){};
    var me = edx.student.account.EnrollmentInterface;
    me.courseUrl = '/enrollment/v0/course/';
    me.studentUrl = '/enrollment/v0/student';
    me.trackSelectionUrl = '/course_modes/choose/'
    me.defaultNumAttempts = 5;
    me.headers = {
        'X-CSRFToken': $.cookie('csrftoken')
    };
    
    me.studentInformation = function(course_key) {
        // retrieve student enrollment information
    };

    me.courseInformation = function(course_key) {
        // retrieve course information from the enrollment API
    };

    me.modeInArray = function(mode_slug, course_modes) {
        // finds whether or not a particular course mode slug exists
        // in an array of course modes
        var result = _.find(course_modes, function(mode){ return mode.slug === mode_slug; });
        return result != undefined;
    };

    me.enroll = function(course_key, forward_url){
        // attempt to enroll a student in a course
        console.log('Enrolling student in course: ' + course_key);
        console.log('with enrollment point: ' + me.courseUrl + course_key)
        $.ajax({
            url: me.courseUrl + course_key,
            type: 'POST',
            data: {},
            headers: me.headers
        }).done(function(data){
            me.postEnrollmentHandler(course_key, data, forward_url);
        }
        ).fail(function(data, textStatus) {
            me.enrollmentFailureHandler(course_key, data, forward_url);
        });
    };

    me.enrollmentFailureHandler = function(course_key, data, forward_url) {
        // handle failures to enroll via the API
        if(data.status == 400) {
            // This status code probably means we don't have permissions to register for this course.
            // look at the contents of the response
            var course = $.parseJSON(data.responseText);
            // see if it's a professional ed course
            if("course_modes" in course && me.modeInArray('professional', course.course_modes)) {
                // forward appropriately
                forward_url = me.trackSelectionUrl + course_key;
            }
        }
        // TODO: if we have a paid registration mode, add item to the cart and send them along

        // TODO: we should figure out how to handle errors here eventually
        window.location.href = forward_url;
    };

    me.postEnrollmentHandler = function(course_key, data, forward_url) {
        // Determine whether or not the course needs to be redirected to
        // a particular page.
        var course = data.course;
        var course_modes = course.course_modes;
        
        // send the user to the track selection page, because it will do the right thing
        forward_url = trackSelectionUrl + course_key;

        window.location.href = forward_url;

    };
})(jQuery, _, gettext);
