'use strict';

angular.module('controllers', []);

angular.module('services', ['ngResource', 'ngCookies']);

angular.module('app', ['ngRoute', 'controllers', 'services'])

    .config(['$routeProvider', '$locationProvider',

        function($routeProvider, $locationProvider) {

            $routeProvider
                .when('/', {
                    templateUrl: 'partials/login.html',
                    controller: 'login'
                });

            $locationProvider.html5Mode(false);
        }]);