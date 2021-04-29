$(document).ready(function() {

    $('input[name=selected_pipeline]').on('click', function(event){
        var element = $(this).parent().parent().children()[0];
        var status = element.querySelector(".active").textContent;
        var button = document.querySelector('#activate_pipeline_button');
        button.style.display = "inline-block";
        if(status === "Inactive"){
            button.textContent = "Activate";
            button.style.color = "#5cb85c";
            setUpModal(true);
        }
        else{
            button.textContent = "Deactivate";
            button.style.color = "#d9534f";
            setUpModal(false)
        }
    });

    function setUpModal(status){
        $('#escape_activate_popup').html("Cancel");
        if(status){
            $('#confirm_activate_message').html("<h6>Are you sure you wish to activate the pipeline?</h6>");
            document.querySelector('#final_activate_button').setAttribute('class','btn btn-primary')
            document.querySelector('#final_activate_button').textContent = "Activate";
        }
        else{
            $('#confirm_activate_message').html("<h6>Are you sure you wish to deactivate the pipeline?</h6>");
            document.querySelector('#final_activate_button').setAttribute('class','btn btn-danger')
            document.querySelector('#final_activate_button').textContent = "Deactivate";
        }
    }

    $("#activate_pipeline_button").on('click', function(event) {
        $('#activate_modal').modal();
    });

    $("#final_activate_button").on('click', function(event) {
            var form = '#select_pipeline_form';
            var url = '/pipeline/update_pipeline_stage/';
            var menu = '#pipeline_menu';
            var confirmation_message = document.querySelector('#confirm_activate_message').textContent;
            var activated = true;
            if(confirmation_message.includes("deactivate")){
                console.log(confirmation_message);
                activated = false;
            }
            $.ajax({ data: $(form).serialize(),
                type: 'post',
                url: url,
                success: function(response) {
                    if(response['success']){
                        $(menu).html(response['html']);
                        document.querySelector('#escape_activate_popup').style.display = 'none';
                        document.querySelector('#activate_pipeline_button').style.display = 'none';
                        document.getElementById('final_activate_button').style.display = 'none';
                        if(activated){
                            $('#confirm_activate_message').html("<div class='alert alert-success'>Successfully Activated.</div>");
                        }
                        else{
                            $('#confirm_activate_message').html("<div class='alert alert-success'>Successfully Deactivated.</div>");

                        }
                        window.setTimeout(function() {
                                location.reload();
                            }, 1000);
                    }
                    else{
                        //this case should be impossible unless caching is involved
                        document.getElementById('final_activate_button').style.display = 'none';
                        $('#confirm_activate_message').html("<div class='alert alert-danger'>There was an error - could not be changed.</div>");
                    }
                },
                error: function (request, status, error) {
                     console.log(request.responseText);
                }
           });
    });
});
