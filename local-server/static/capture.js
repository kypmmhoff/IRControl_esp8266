angular.module('controlapp',[])
    .controller('remotecontroller', ['$http','$timeout',
    function($http, $timeout){
        var ctxt = this;
        ctxt.label = 'Serial logger';
        ctxt.buffer = 'Waiting ...';
    } ]);