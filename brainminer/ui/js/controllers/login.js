'use strict';

angular.module('controllers')

    .controller('LoginController', ['$scope', '$cookies', '$location', 'TokenService', 'UserService',

        function($scope, $cookies, $location, TokenService, UserService) {

            $scope.username = 'root';
            $scope.password = 'secret';

            $scope.login = function() {
                TokenService.create($scope.username, $scope.password).then(function(response) {
                    var admin = response.data.is_admin;
                    TokenService.update(response.data.token);
                    UserService.getByUsername($scope.username).then(function(response) {
                        UserService.setCurrentUser(response.data[0]);
                        if(admin)
                            $location.path('/admin');
                        else
                            $location.path('/');
                    }, function(error) {
                        alert(JSON.stringify(error));
                    })
                }, function(error) {
                    alert(JSON.stringify(error));
                })
            };
        }]);