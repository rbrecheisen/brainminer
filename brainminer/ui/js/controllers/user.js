'use strict';

angular.module('controllers')

    .controller('UsersController', ['$scope', '$location', '$route', 'TokenService', 'UserService',

        function($scope, $location, $route, TokenService, UserService) {

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin', text: 'Dashboard'},
                {url: '#/users', text: 'Users'}
            ];

            UserService.getAll().then(function(response) {
                $scope.users = [];
                for(var i = 0; i < response.data.length; i++) {
                    var user = response.data[i];
                    if(user.is_visible) {
                        // Convert the boolean variables to string values because the <select>
                        // element does not handle booleans
                        user.is_admin = user.is_admin ? 'true' : 'false';
                        user.is_active = user.is_active ? 'true': 'false';
                        $scope.users.push(user);
                    }
                }
            });

            $scope.createUser = function() {
                $location.path('/users/0');
            };
        }])

    .controller('UserController', ['$scope', '$location', '$routeParams', 'TokenService', 'UserService',

        function($scope, $location, $routeParams, TokenService, UserService) {

            TokenService.check();

            $scope.currentUser = UserService.getCurrentUser();
            $scope.breadcrumbs = [
                {url: '#/admin', text: 'Dashboard'},
                {url: '#/users', text: 'Users'},
                {url: '#/users/' + $routeParams.id, text: 'User'}
            ];

            $scope.user = {};
            $scope.user.id = $routeParams.id;
            $scope.user.password1 = '';
            $scope.user.password2 = '';
            $scope.user.name = '';
            $scope.user.username = '';
            $scope.user.email = '';
            $scope.user.first_name = '';
            $scope.user.last_name = '';
            $scope.user.is_admin = 'false';
            $scope.user.is_active = 'true';

            if($scope.user.id > 0) {
                UserService.get($scope.user.id).then(function (response) {
                    var user = response.data;
                    if(user.is_visible) {
                        $scope.user.name = user.first_name + ' ' + user.last_name;
                        $scope.user.username = user.username;
                        $scope.user.email = user.email;
                        $scope.user.first_name = user.first_name;
                        $scope.user.last_name = user.last_name;
                        $scope.user.is_admin = user.is_admin ? 'true': 'false';
                        $scope.user.is_active = user.is_active ? 'true': 'false';
                        $scope.breadcrumbs = [
                            {url: '#/admin-dashboard', text: 'Dashboard'},
                            {url: '#/users', text: 'Users'},
                            {url: '#/users/' + $routeParams.id, text: $scope.user.name}
                        ];
                    } else {
                        alert('User not visible');
                    }
                });
            }

            $scope.saveUser = function(user) {
                if(user.id > 0) {
                    if(user.password1 == user.password2)
                        alert('Old and new password cannot be the same');
                    UserService.update(user.id, user.username, user.password1, user.password2, user.email, user.first_name, user.last_name, user.is_admin=='true', user.is_active=='true').then(function(x) {
                        $location.path('/users');
                    });
                } else {
                    if(!user.username)
                        alert('Username cannot be empty');
                    if(!user.first_name)
                        alert('First name cannot be empty');
                    if(!user.last_name)
                        alert('Last name cannot be empty');
                    if(!user.email)
                        alert('Email cannot be empty');
                    if(!user.password1)
                        alert('Password cannot be empty');
                    if(!user.password2)
                        alert('Password confirmation cannot be empty');
                    if(user.password1 != user.password2)
                        alert('Password and confirmation do not match');
                    UserService.create(user.username, user.password1, user.email, user.first_name, user.last_name, user.is_admin=='true', user.is_active=='true').then(function(x) {
                        $location.path('/users');
                    });
                }
            };

            $scope.deleteUser = function(user) {
                if(user.id > 0) {
                    if(user.username == 'root')
                        alert('Cannot delete \'root\' user');
                    UserService.delete(user.id).then(function(x) {
                        $location.path('/users');
                    });
                }
            };

            $scope.cancelSave = function() {
                $location.path('/users');
            }
        }]);