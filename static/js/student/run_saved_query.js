$(document).ready(function() {
        $("#run_saved_query_button").on('click', function(event){
            event.preventDefault();
            var selection = $('input[name=selected_query]:checked', '#select_query_form').val();
            if(selection){
                $('input[name="csrfmiddlewaretoken"]', '#select_query_form').remove();
                $('#select_query_form').attr('action', "/student/run_query/" + selection).submit();
            }
        });
});