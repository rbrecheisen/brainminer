'use strict';

angular.module('services')

    .service('FileSetService', ['$http', 'TokenService', 'environ',

        function($http, TokenService, environ) {

            var fileSetsUri = 'http://'
                + environ.SERVER_HOST + ':'
                + environ.SERVER_PORT + '/repositories';

            return {

                create: function() {

                }
            }
        }]);