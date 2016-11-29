'use strict';

angular.module('controllers')

    .controller('RepositoriesController', ['$scope', '$location', '$route', 'TokenService', 'UserService', 'RepositoryService',

        function ($scope, $location, $route, TokenService, UserService, RepositoryService) {

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin', text: 'Dashboard'},
                {url: '#/repositories', text: 'Repositories'}
            ];

            RepositoryService.getAll().then(function(response) {
                $scope.repositories = [];
                for(var i = 0; i < response.data.length; i++) {
                    $scope.repositories.push(response.data[i]);
                }
            }, function(error) {
                    alert(JSON.stringify(error));
            });

            $scope.createRepository = function() {
                $location.path('/repositories/0');
            };
        }])

    .controller('RepositoryController', ['$scope', '$location', '$routeParams', 'TokenService', 'UserService', 'RepositoryService',

        function($scope, $location, $routeParams, TokenService, UserService, RepositoryService) {

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin-dashboard', text: 'Dashboard'},
                {url: '#/repositories', text: 'Repositories'},
                {url: '#/repositories/' + $routeParams.id, text: $routeParams.id}];

            $scope.repository = {};
            $scope.repository.id = $routeParams.id;
            $scope.repository.name = '';

            if($scope.repository.id > 0) {
                RepositoryService.get($scope.repository.id).then(function(response) {
                    $scope.repository = response.data;
                    $scope.breadcrumbs = [
                        {url: '#/admin-dashboard', text: 'Dashboard'},
                        {url: '#/repositories', text: 'Repositories'},
                        {url: '#/repositories/' + $routeParams.id, text: $scope.repository.name}]
                }, function(error) {
                    alert(JSON.stringify(error));
                });
            }

            $scope.saveRepository = function(repository) {
                if(repository.id > 0) {
                    RepositoryService.update(repository.id, repository.name).then(function(x) {
                        $location.path('/repositories');
                    }, function(error) {
                        alert(JSON.stringify(error));
                    });
                } else {
                    if( ! repository.name)
                        alert('Name is empty');
                    RepositoryService.create(repository.name).then(function(x) {
                        $location.path('/repositories');
                    }, function(error) {
                        alert(JSON.stringify(error));
                    });
                }
            };

            $scope.deleteRepository = function(repository) {
                if(repository.id > 0) {
                    RepositoryService.delete(repository.id).then(function(x) {
                       $location.path('/repositories');
                    }, function(error) {
                        alert(JSON.stringify(error));
                    });
                }
            };

            $scope.cancelSave = function() {
                $location.path('/repositories');
            };
        }]);