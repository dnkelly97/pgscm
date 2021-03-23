$(document).ready(function() {
        $("#id_save_query").on('click', function(event) {
            event.preventDefault();
            document.getElementById('save_failure_message').style.display = 'none';
            document.getElementById('save_success_message').style.display = 'none';
            document.getElementById("save_query_popup_form").style.display = 'block';
            document.getElementById('modal_save_query').style.display = 'block';
            $('#save_query_modal').modal();
        });
});

$(document).ready(function() {
        $("#modal_save_query").on('click', function(event) {
            $('#id_query_name').val($('#modal_query_name').val());
            $('#id_description').val($('#modal_query_description').val());
            $.ajax({ data: $('#query-form').serialize(),
                    type: 'post',
                    url: $(this).attr('action'),
                    success: function(response) {
                        //console.log(response);
                        if(response['success'] == true){
                            $('#modal_query_name').val('');
                            $('#modal_query_description').val('');
                            $('#save_success_message').html(response['message']);
                            document.getElementById('save_failure_message').style.display = 'none';
                            document.getElementById('save_success_message').style.display = 'block';
                            document.getElementById('save_query_popup_form').style.display = 'none';
                            document.getElementById('modal_save_query').style.display = 'none';
                        }
                        else{
                            $('#save_failure_message').html(response['message']);
                            document.getElementById('save_failure_message').style.display = 'block';
                        }
                    },
                    error: function (request, status, error) {
                         console.log(request.responseText);
                    }
           });
        });
});