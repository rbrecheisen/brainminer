'use strict';

angular.module('services')

    .service('UserService', ['$http', 'TokenService', 'environ',

        function($http, TokenService, environ) {

            var usersUri = 'http://'
                + environ.SERVER_HOST+ ':'
                + environ.SERVER_PORT + '/users';

            var currentUser = null;

            return {

                getByUsername: function(username) {
                    return $http({
                        method: 'GET',
                        url: usersUri + '?username=' + username,
                        headers: TokenService.header()
                    })
                },

                getCurrentUser: function() {
                    return currentUser;
                },

                setCurrentUser: function(user) {
                    currentUser = user;
                }
            }
        }]);