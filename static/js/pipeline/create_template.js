$(document).ready(function() {
        $(".dropdown-item").on('click', function(event) {
            var text = ($(this).val());
            var words = text.split(" ");
            console.log(words);
            var placeholder_found = false;
            for (var i = 0; i < words.length; i += 1) {
                //console.log(words[i]);
                if(words[i].includes("@placeholder")){
                    placeholder_found = true;
                }
                else if(placeholder_found && words[i].includes("name=")){
                    var name = words[i].replace("name=", "").replace(/['"]+/g, '');
                    placeholder_found = false;
                    var form_div = createFormElementLabel(name);
                    form_div.appendChild(createTextArea(name));
                    form_div.style.marginBottom = "16px";
                    document.getElementById("placeholders").appendChild(form_div);
                }
            }
        });
});

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

function createTextArea(label){
    var text_area = document.createElement('textarea');
        text_area.setAttribute('class','form-control');
        text_area.setAttribute('aria-label',label);
    return text_area;
}