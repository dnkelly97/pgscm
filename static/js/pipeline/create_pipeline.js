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

$(document).ready(function() {
        $("#id_num_stages").on('change', function(event) {
            event.preventDefault();
            var num_stages = $('#id_num_stages');
            if(num_stages.val() != '0'){
                document.getElementById("message").style = "display: none;";
                $.ajax({ data: num_stages.serialize(),
                    type: 'get',
                    url: '/pipeline/get_stages/',
                    success: function(response) {
                        $("#define_stages").html(response['html']);
                        document.getElementById("define_stages").style = "display: block;";
                        document.getElementById("create_pipeline_submit_button").style = "display: block;";
                    },
                    error: function (request, status, error) {
                         console.log(request.responseText);
                    }
                });
            }
            else {
                $('#message').html("The number of stages must be greater than 0");
                document.getElementById("message").style = "display: block;";
                document.getElementById("create_pipeline_submit_button").style = "display: none;";
                document.getElementById("define_stages").style = "display: none;";
            }
        });
});