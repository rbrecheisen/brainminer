'use strict';

angular.module('controllers')

    .controller('AdminController', ['$scope', '$location', 'TokenService', 'UserService',

        function($scope, $location, TokenService, UserService) {

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/', text: 'Dashboard'}
            ];
        }]);