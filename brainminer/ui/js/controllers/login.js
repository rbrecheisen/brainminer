'use strict';

angular.module('controllers')

    .controller('login', ['$scope', '$cookies', '$location'],

        function($scope, $cookies, $location) {

            $scope.username = 'root';
            $scope.password = 'secret';

            $scope.login = function() {
                alert('User unknown!');
            };
        });