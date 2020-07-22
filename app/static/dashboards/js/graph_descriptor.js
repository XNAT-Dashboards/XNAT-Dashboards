function descriptor(json, descriptor_values){

    var graph_name = "";
    var graph_id = "";

    for (var g_name in json){
        graph_name = g_name;
        graph_info = json[g_name];
        graph_id = graph_info['id'];
    }

    value = descriptor_values[graph_name];
    generate_text( graph_id, value);
}

function generate_text(g_id, g_value){
    $('#info_text_id'+g_id).text(g_value);
}