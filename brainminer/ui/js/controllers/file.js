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
                    {url: '#/repositories/' + $scope.repository.id + '/files', text: $routeParams.file_id}];
                
                if($routeParams.file_id > 0) {
                    FileService.get($routeParams.file_id).then(function(response) {
                        $scope.file = response.data;
                        $scope.breadcrumbs = [
                            {url: $scope.currentUser.is_admin ? '#/admin' : '#/', text: 'Dashboard'},
                            {url: '#/repositories', text: 'Repositories'},
                            {url: '#/repositories/' + $scope.repository.id, text: $scope.repository.name},
                            {url: '#/repositories/' + $scope.repository.id + '/files', text: $scope.file.name}];
                    });
                }
            });

            $scope.uploadFile = function(file) {
                FileService.upload($scope.repository.id, file).then(function(response) {
                    $timeout(function() {
                        console.log('Successfully uploaded file ' + response.config.data.file.name);
                        $location.path('/repositories/' + $scope.repository.id);
                    });
                }, function(error) {
                    console.log('Upload failed with status ' + error.status);
                }, function(progress) {
                    console.log('Upload progress: ' + parseInt(100.0 * progress.loaded / progress.total) + '%');
                });
            };

            $scope.cancelUpload = function() {
                $location.path('/repositories/' + $scope.repository.id + '/files');
            };
        }]);