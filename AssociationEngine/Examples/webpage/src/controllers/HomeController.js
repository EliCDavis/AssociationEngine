module.exports = HomeController;

/** @ngInject */
function HomeController($scope, observeOnScope, GraphService) {

    var self = this;

    $scope.items = ["none", "weak"];
    $scope.selectedItem = "none";
    $scope.getSelectedText = function() {
        if ($scope.selectedItem !== undefined) {
            return "Obfuscating " + $scope.selectedItem;
        } else {
            return "Please select a scope";
        }
    };

    observeOnScope($scope, 'selectedItem').map(val => val.newValue).subscribe(GraphService.ObfuscateMode$);

}