$(document).ready(function() {
        $("#edit_pipeline_button").on('click', function(event){
            event.preventDefault();
            var selection = $('input[name=selected_pipeline]:checked', '#select_pipeline_form').val();
            if(selection){
                $('input[name="csrfmiddlewaretoken"]', '#select_pipeline_form').remove();
                $('#select_pipeline_form').attr('action', "/pipeline/edit_pipeline/" + selection).submit();
            }
        });
});