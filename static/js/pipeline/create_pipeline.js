$(document).ready(function() {
        $("#create_pipeline_submit_button").on('click', function(event) {
            event.preventDefault();
            $.ajax({ data: $('#create_pipeline_form').serialize(),
                    type: 'post',
                    url: '/pipeline/create/',
                    success: function(response) {
                        console.log(response['success']);
                        if(!response['success']){
                            $('#message').html(response['message']);
                            document.getElementById('message').style = 'display: block;';
                            $('html, body').animate({ scrollTop: 0 }, 'slow');
                        }
                        else{
                            document.getElementById('id_dashboard').click();
                        }
                    },
                    error: function (request, status, error) {
                         console.log(request.responseText);
                    }
            });
        });
});

$(document).ready(function() {
  $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
});

$(document).ready(function() {
        $("#id_num_stages").on('change', function(event) {
            event.preventDefault();
            var num_stages = $('#id_num_stages');
            if(parseInt(num_stages.val()) > 0){
                document.getElementById("message").style = "display: none;";
                $.ajax({ data: num_stages.serialize(),
                    type: 'get',
                    url: '/pipeline/get_stages/',
                    success: function(response) {
                        $("#define_stages").html(response['html']);
                        document.getElementById("define_stages").style = "display: block;";
                        document.getElementById("create_pipeline_submit_button").style = "display: block;";
                        console.log('ready freddy');
                        var form_selects = document.evaluate("//select[@name='advancement_condition']", document, null, XPathResult.ANY_TYPE, null);
                        var node = null;
                        while(node = form_selects.iterateNext()) {
                            console.log('woof');
                            console.log(node);
                            node.addEventListener('change', showForm);
                        }
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

function showForm(event){
    if(event.target.value == 'FR'){
        event.target.parentNode.nextElementSibling.style = 'display: block;';
    }
    else{
        event.target.parentNode.nextElementSibling.childNodes[3].value = "None";
        event.target.parentNode.nextElementSibling.style = 'display: none;';
    }
}