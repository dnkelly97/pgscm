$(document).ready(function() {
        $("#create_pipeline_submit_button").on('click', function(event) {
            event.preventDefault();
            console.log('hey! pipeline button clicked');
            $.ajax({ data: $('#create_pipeline_form').serialize(),
                    type: 'post',
                    url: '/pipeline/create/',
                    success: function(response) {
                        console.log(response);
                    },
                    error: function (request, status, error) {
                         console.log(request.responseText);
                    }
            });
        });
});