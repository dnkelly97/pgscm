function deleteAPIKey(name){
    $('#confirm_delete_message').html("<h6>Are you sure you want to delete: " + name + "?</h6>");
    document.getElementById('final_delete_button').style.display = 'block';
    $('#escape_popup').html("Cancel");
    $('#delete_modal').modal();
}

$(document).ready(function() {
     $("#final_delete_button").on('click', function(event) {
            console.log('here');
            console.log('prefix');

            var url = '/apis/delete_api/';
            var form = '#delete_api_form';

            console.log($(form).serialize());

            $.ajax({
                    data: $(form).serialize(),
                    type: 'post',
                    url: url,
                    success: function(response) {
                        $('#escape_popup').html("Close");
                        if(response['success']){
                            //$(menu).html(response['html']);
                            document.getElementById('final_regenerate_button').style.display = 'none';
                            $('#confirm_delete_message').html("<div class='alert alert-success'>Successfully deleted.</div>");
                            window.setTimeout(function() {
                                window.location.href = response['url'];
                            }, 1000);
                        }
                        else{
                            //this case should be impossible unless caching is involved
                            document.getElementById('final_delete_button').style.display = 'none';
                            $('#confirm_delete_message').html("<div class='alert alert-danger'>There was an error - item not regenerated.</div>");
                        }
                    },
                    error: function (request, status, error) {
                         console.log(request.responseText);
                    }
           });
    });
});
