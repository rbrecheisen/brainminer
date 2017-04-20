'use strict';

angular.module('services')

    .service('TaskService', ['$http', 'TokenService', 'environ',

    function($http, TokenService, environ) {

        var tasksUri = 'http://'
            + environ.SERVER_HOST + ':'
            + environ.SERVER_PORT + '/tasks';

        return {

            execute: function(pipelineName, params) {
                return $http({
                    method: 'POST',
                    url: tasksUri,
                    headers: TokenService.header(),
                    data: {
                        'pipeline_name': pipelineName,
                        'params': params
                    }
                })
            }
        }
    }]);