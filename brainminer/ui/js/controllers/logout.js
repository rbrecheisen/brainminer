'use strict';

angular.module('controllers')

    .controller('logout', ['$location',

        function($location) {

            alert('User logging out!');
        }]);