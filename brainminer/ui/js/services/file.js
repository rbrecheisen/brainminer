'use strict';

angular.module('services')

    .service('FileService', ['$http', 'Upload', 'TokenService', 'environ',

        function($http, Upload, TokenService, environ) {

            var filesUri = 'http://'
                + environ.SERVER_HOST + ':'
                + environ.SERVER_PORT + '/repositories';

            return {

                get: function(id, file_id) {
                    return $http({
                        method: 'GET',
                        url: filesUri + '/' + id + '/files/' + file_id,
                        headers: TokenService.header()
                    })
                },

                upload: function(id, file) {
                    return Upload.upload({
                        url: filesUri + '/' + id + '/files',
                        data: {file: file},
                        headers: TokenService.header()
                    });
                }
            }
        }]);