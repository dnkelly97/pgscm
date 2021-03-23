$(document).ready(function() {
        $("#delete_query_button").on('click', function(event) {
            console.log('here');
            console.log($('#select_query_form').serialize());
            $.ajax({ data: $('#select_query_form').serialize(),
                    type: 'post',
                    url: $(this).attr('action'),
                    success: function(response) {
                        console.log(response['html']);
                        if(response['success']){
                            $('#saved_query_menu').html(response['html']);
                        }
                    },
                    error: function (request, status, error) {
                         console.log(request.responseText);
                    }
           });
        });
});
