function deleteStudent(email){
    $('#confirm_student_delete_message').html("<h6>Are you sure you want to delete: " + email + "?</h6>");
    document.getElementById('final_student_delete_button').style.display = 'block';
    $('#escape_student_popup').html("Cancel");
    $('#delete_student_modal').modal();
}

$(document).ready(function() {
     $("#final_student_delete_button").on('click', function(event) {

            var url = '/student/delete_student/';
            var form = '#delete_student_form';

            $.ajax({
                    data: $(form).serialize(),
                    type: 'post',
                    url: url,
                    success: function(response) {
                        console.log("MATHEW");
                        if(response['success']){
                            document.getElementById('escape_student_popup').style.display = 'none';
                            document.getElementById('final_student_delete_button').style.display = 'none';
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
