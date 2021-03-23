$(document).ready(function() {
        $("#delete_query_button").on('click', function(event){
            updateConfirmDeleteMessage('query');
        });
});

function updateConfirmDeleteMessage(type){
    var selection = $('input[name=selected_'+type+']:checked', '#select_query_form').val();
    if(selection){
        $('#confirm_delete_message').html("<h6>Are you sure you want to delete " + type + " '" + selection + "'?</h6>");
        document.getElementById('final_delete_button').style.display = 'block';
        $('#escape_popup').html("Cancel");
    }
    else{
        $('#confirm_delete_message').html("<h6>No "+ type +" selected.</h6>");
        document.getElementById('final_delete_button').style.display = 'none';
        $('#escape_popup').html("Close");
    }
    $('#delete_modal').modal();
}

$(document).ready(function() {
        $("#final_delete_button").on('click', function(event) {
            console.log('here');
            console.log($('#select_query_form').serialize());
            $.ajax({ data: $('#select_query_form').serialize(),
                    type: 'post',
                    url: $(this).attr('action'),
                    success: function(response) {
                        console.log(response['html']);
                        $('#escape_popup').html("Close");
                        if(response['success']){
                            $('#saved_query_menu').html(response['html']);
                            document.getElementById('final_delete_button').style.display = 'none';
                            $('#confirm_delete_message').html("<div class='alert alert-success'>Successfully deleted.</div>");
                        }
                        else{
                            //this case should be impossible unless caching is involved
                            document.getElementById('final_delete_button').style.display = 'none';
                            $('#confirm_delete_message').html("<div class='alert alert-danger'>There was an error - item not deleted.</div>");
                        }
                    },
                    error: function (request, status, error) {
                         console.log(request.responseText);
                    }
           });
        });
});
