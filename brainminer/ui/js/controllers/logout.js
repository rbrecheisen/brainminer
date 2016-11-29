'use strict';

angular.module('controllers')

    .controller('LogoutController', ['$location', 'TokenService', 'UserService',

        function($location, TokenService, UserService) {
            TokenService.delete();
            UserService.setCurrentUser(null);
            $location.path('/login');
        }]);