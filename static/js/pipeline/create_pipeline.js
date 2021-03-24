$(document).ready(function() {
        $("#create_pipeline_submit_button").on('click', function(event) {
            event.preventDefault();
            console.log('hey! pipeline button clicked');
            $.ajax({ data: $('#create_pipeline_form').serialize(),
                    type: 'post',
                    url: '/pipeline/create/',
                    success: function(response) {
                        console.log(response['success']);
                        var action = document.getElementById('define_stages_form').action;
                        action = action.replace('null', response['pipeline_id']);
                        document.getElementById('define_stages_form').action = action;
                        $('#define_stages_formholder').html(response['html']);
                        $('#define_stages_modal').modal();
                    },
                    error: function (request, status, error) {
                         console.log(request.responseText);
                    }
            });
        });
});