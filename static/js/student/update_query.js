$(document).ready(function() {
        $("#edit_query_button").on('click', function(event){
            console.log("edit query button clicked");
            event.preventDefault();
            var selection = $('input[name=selected_query]:checked', '#select_query_form').val();
            if(selection){
                $('input[name="csrfmiddlewaretoken"]', '#select_query_form').remove();
                console.log($('input[name="csrfmiddlewaretoken"]', '#select_query_form').val());
                setTimeout(() => {  console.log("World!"); }, 2000);
//                $('#select_query_form').attr('action', "/student/update_query/" + selection).submit();
            }
        });
});