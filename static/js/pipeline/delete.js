$(document).ready(function() {
        $("#delete_query_button").on('click', function(event) {
            console.log('here');
            console.log($('#select_query_form').serialize());
            $.ajax({ data: $('#select_query_form').serialize(),
                    type: 'post',
                    url: $(this).attr('action'),
                    success: function(response) {

                    },
                    error: function (request, status, error) {
                         console.log(request.responseText);
                    }
           });
        });
});
