'use strict';

angular.module('controllers')

    .controller('LoginController', ['$scope', '$cookies', '$location', 'TokenService', 'UserService',

        function($scope, $cookies, $location, TokenService, UserService) {

            $scope.username = 'root';
            $scope.password = 'secret';

            $scope.login = function() {
                TokenService.create($scope.username, $scope.password).then(function(response) {
                    TokenService.update(response.data.token);
                    UserService.setCurrentUser(response.data.current_user);
                    if(UserService.getCurrentUser().is_admin)
                        $location.path('/admin');
                    else
                        $location.path('/');
                })
            };
        }]);