'use strict';

angular.module('controllers')

    .controller('TasksController', ['$scope', '$location', '$route', 'TokenService', 'UserService',

    function($scope, $location, $route, TokenService, UserService) {

        TokenService.check();

        $scope.currentUser = UserService.getCurrentUser();
        $scope.breadcrumbs = [
            {url: $scope.currentUser.is_admin ? '#/admin' : '#/', text: 'Dashboard'},
            {url: '#/tasks', text: 'Tasks'}
        ];

        $scope.createTask = function() {
            if($scope.currentUser.is_admin) {
                $location.path('/tasks/0');
            }
        };
    }])

    .controller('TaskController', ['$scope', '$location', '$route', 'TokenService', 'UserService', 'TaskService',

    function($scope, $location, $route, TokenService, UserService, TaskService) {

        TokenService.check();

        $scope.currentUser = UserService.getCurrentUser();
        $scope.breadcrumbs = [
            {url: $scope.currentUser.is_admin ? '#/admin' : '#/', text: 'Dashboard'},
            {url: '#/tasks', text: 'Tasks'}
        ];

        $scope.executeTask = function() {
            TaskService.execute("", {})
        }
    }]);