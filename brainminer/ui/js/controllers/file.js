'use strict';

angular.module('controllers')

    .controller('FileController', ['$scope', '$location', '$routeParams', '$timeout', 'Upload', 'TokenService', 'UserService', 'RepositoryService', 'FileService',

        function($scope, $location, $routeParams, $timeout, Upload, TokenService, UserService, RepositoryService, FileService) {

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: $scope.currentUser.is_admin ? '#/admin' : '#/', text: 'Dashboard'},
                {url: '#/repositories', text: 'Repositories'},
                {url: '#/repositories/' + $routeParams.id, text: $routeParams.id},
                {url: '#/repositories/' + $routeParams.id + '/files', text: $routeParams.file_id}];

            RepositoryService.get($routeParams.id).then(function(response) {
                
                $scope.repository = response.data;
                $scope.breadcrumbs = [
                    {url: $scope.currentUser.is_admin ? '#/admin' : '#/', text: 'Dashboard'},
                    {url: '#/repositories', text: 'Repositories'},
                    {url: '#/repositories/' + $scope.repository.id, text: $scope.repository.name},
                    {url: '#/repositories/' + $scope.repository.id + '/files', text: '0'}];
                
                // if($routeParams.file_id > 0) {
                //     FileService.get($routeParams.file_id).then(function(response) {
                //         $scope.repository.file = response.data;
                //         $scope.breadcrumbs = [
                //             {url: $scope.currentUser.is_admin ? '#/admin' : '#/', text: 'Dashboard'},
                //             {url: '#/repositories', text: 'Repositories'},
                //             {url: '#/repositories/' + $scope.repository.id, text: $scope.repository.name},
                //             {url: '#/repositories/' + $scope.repository.id + '/files', text: '0'}];
                //     });
                // }
            });

            $scope.uploadFiles = function(file, errFiles) {
                $scope.f = file;
                $scope.errFile = errFiles && errFiles[0];
                if(file) {
                    file.upload = Upload.upload({
                        url: 'http://0.0.0.0:5000/repositories/' + $scope.repository.id + '/files',
                        data: {file: file, 'type': 'text', 'modality': 'none'}
                    });
                    file.upload.then(function(response) {
                        $timeout(function() {
                            file.result = response.data;
                        });
                    }, function(error) {
                        alert(JSON.stringify(error));
                    }, function(evt) {
                        file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
                    });
                }
            };

            $scope.cancelUpload = function() {
                $location.path('/repositories/' + $scope.repository.id + '/files');
            };
        }]);