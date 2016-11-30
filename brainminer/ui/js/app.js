'use strict';

angular.module('controllers', []);
angular.module('services', ['ngResource', 'ngCookies']);
angular.module('app', ['ngRoute', 'controllers', 'services', 'ngFileUpload'])

    .constant('environ', window.environ)

    .config(['$routeProvider', '$locationProvider',

        function($routeProvider, $locationProvider) {

            $routeProvider
                .when('/login', {
                    templateUrl: 'partials/login.html',
                    controller: 'LoginController'
                })
                .when('/logout', {
                    templateUrl: 'partials/login.html',
                    controller: 'LogoutController'
                })
                .when('/', {
                    templateUrl: 'partials/dashboard.html',
                    controller: 'DashboardController'
                })
                .when('/admin', {
                    templateUrl: 'partials/admin.html',
                    controller: 'AdminController'
                })
                .when('/repositories', {
                    templateUrl: 'partials/repository/repositories.html',
                    controller: 'RepositoriesController'
                })
                .when('/repositories/:id?', {
                    templateUrl: 'partials/repository/repository.html',
                    controller: 'RepositoryController'
                })
                .when('/repositories/:id?/files/:file_id?', {
                    templateUrl: 'partials/repository/file.html',
                    controller: 'FileController'
                })
                .when('/repositories/:id?/file-sets/:file_set_id?', {
                    templateUrl: 'partials/repository/file-set.html',
                    controller: 'FileSetController'
                })
                .when('/users', {
                   templateUrl: 'partials/user/users.html',
                    controller: 'UsersController'
                })
                .when('/users/:id?', {
                   templateUrl: 'partials/user/user.html',
                    controller: 'UserController'
                });

            $locationProvider.html5Mode(false);
        }]);