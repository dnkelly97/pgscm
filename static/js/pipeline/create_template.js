$(document).ready(function() {
        $(".dropdown-item").on('click', function(event) {
            event.preventDefault();
            var full_text = ($(this).val());
            var name = $(this).text()
            var text = full_text.split('+++')[0];
            var id = full_text.split('+++')[1];
            var stage_number = $(this).closest('div').prop('id').replace('Stage_','').replace('_dropdown','');
            var words = text.split(" ");
            var placeholder_found = false;

            document.getElementById("Stage_"+stage_number+"_template").innerHTML = "";
            document.getElementById("Stage_"+stage_number+"_template").appendChild(appendHeader(name));
            for (var i = 0; i < words.length; i += 1) {
                //console.log(words[i]);
                if(words[i].includes("@placeholder")){
                    placeholder_found = true;
                }
                else if(placeholder_found && words[i].includes("name=")){
                    var name = words[i].replace("name=", "").replace(/['"]+/g, '');
                    placeholder_found = false;
                    var form_div = createFormElementLabel(name);
                    form_div.appendChild(createTextArea(name,stage_number,id));
                    form_div.style.marginBottom = "16px";
                    document.getElementById("Stage_"+stage_number+"_template").appendChild(form_div);
                }
            }
            document.getElementById("Stage_"+stage_number+"_template").appendChild(appendDivider());
        });

        function appendHeader(name){
            var header = document.createElement('h6');
                header.setAttribute('class','card-header');
            var header_content = document.createElement('b');
                header_content.textContent=name
            header.appendChild(header_content);
            header.style.marginBottom="8px";
            return header
        }

        function appendDivider(){
            var outer_div = document.createElement('div');
                outer_div.setAttribute('class','dropdown-divider');
            return outer_div
        }

        function createFormElementLabel(label){
            var outer_div = document.createElement('div');
                outer_div.setAttribute('class','input-group');

            var innner_div = document.createElement('div');
                innner_div.setAttribute('class','input-group-prepend');

            var div_label = document.createElement('span');
                div_label.setAttribute('class','input-group-text');
                div_label.textContent=label;
            console.log(div_label.textContent);

            innner_div.appendChild(div_label);
            outer_div.appendChild(innner_div);
            return outer_div
        }

        function createTextArea(label,stage_number,id){
            var text_area = document.createElement('textarea');
                text_area.setAttribute('class','form-control');
                text_area.setAttribute('aria-label',label);
                text_area.setAttribute('name', stage_number+'_'+label+'_'+id);
            return text_area;
        }
});