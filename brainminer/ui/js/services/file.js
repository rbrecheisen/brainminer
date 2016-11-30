'use strict';

angular.module('services')

    .service('FileService', ['$http', 'Upload', 'TokenService', 'environ',

        function($http, Upload, TokenService, environ) {

            var filesUri = 'http://'
                + environ.SERVER_HOST + ':'
                + environ.SERVER_PORT + '/repositories';

            return {

                upload: function(id, file) {
                    Upload.upload({
                        url: filesUri + '/' + id + '/files',
                        data: {file: file, 'type': 'text', 'modality': 'none'}
                    }).then(function(response) {
                        console.log('Success ' + response.config.data.file.name + 'uploaded. Response: ' + response.data);
                    }, function(error) {
                        console.log(JSON.stringify(error));
                    }, function(event) {
                        var progressPercentage = parseInt(100.0 * event.loaded / event.total);
                        console.log('progress: ' + progressPercentage + '% ' + event.config.data.file.name);
                    });
                    // return $http({
                    //     method: 'POST',
                    //     url: filesUri + '/' + id + '/files',
                    //     data: file,
                    //     headers: TokenService.header()
                    // });
                }
            }
        }]);