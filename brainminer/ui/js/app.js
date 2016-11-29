'use strict';

angular.module('controllers', []);
angular.module('services', ['ngResource', 'ngCookies']);
angular.module('app', ['ngRoute', 'controllers', 'services'])

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
                });

            $locationProvider.html5Mode(false);
        }]);