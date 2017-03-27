module.exports = SensorListingDirective;

function SensorListingDirective() {
    return {
        'restrict': 'E',
        'controllerAs': 'sensorListing',
        'templateUrl': 'partial/directives/sensor-listing.html',
        'controller': /*@ngInject*/ function($scope, GraphService) {

            var self = this;

            self.nodes = [];

            GraphService.Nodes$.safeApply($scope, function(nodes) {
                self.nodes = nodes;
            }).subscribe();

        }
    };
}