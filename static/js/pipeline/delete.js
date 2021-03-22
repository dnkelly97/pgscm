$(document).ready(function() {
        $("#delete_query_button").on('click', function(event) {
            console.log('here');
            console.log($('#select_query_form').serialize());
        });
});
