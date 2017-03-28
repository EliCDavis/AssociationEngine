module.exports = AppDirective;

function AppDirective() {
    return {
        'restrict': 'E',
        'templateUrl': 'partial/directives/app.html',
        'controller': /*@ngInject*/ function(SocketConnectionService) {}
    };
}
