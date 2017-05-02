module.exports = ToolbarDirective;

function ToolbarDirective() {
    return {
        'restrict': 'E',
        'templateUrl': 'partial/directives/toolbar.html',
        'controller': /*@ngInject*/ function($scope) {
            var self = this;

        }
    };
}