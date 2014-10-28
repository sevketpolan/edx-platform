/**
 * The UnitOutlineChildView is used to render each Section,
 * Subsection, and Unit within the Unit Outline component on the unit
 * page.
 */
define(['js/views/xblock_outline'],
    function(XBlockOutlineView) {
        var UnitOutlineChildView = XBlockOutlineView.extend({
            initialize: function() {
                XBlockOutlineView.prototype.initialize.call(this);
                this.currentUnitId = this.options.currentUnitId;
            },

            getContext: function() {
                return $.extend(
                    XBlockOutlineView.prototype.getContext.call(this),
                    {currentUnitId: this.currentUnitId}
                );
            },

            createChildView: function(view, options) {
                return XBlockOutlineView.prototype.createChildView.call(
                    this, UnitOutlineChildView, $.extend(options, {currentUnitId: this.currentUnitId})
                );
            }
        });

        return UnitOutlineChildView;
    }); // end define()
