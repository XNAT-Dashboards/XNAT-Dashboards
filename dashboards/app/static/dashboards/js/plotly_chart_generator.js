// Generate Charts using the json provided from html jinja

function chart_generator(json){

    /* 
    JSON structure: 
    {
        'graph_name' : {
            'x1':'y1',
            'x2':'y2',
            'x3':'y3',
            'graph_type':'bar'
            'graph_id':'1'
        }
    }
    */

    var graph_name = "";
    var graph_info = {};
    var graph_type = "";

    for (var g_name in json){
        graph_name = g_name;
        graph_info = json[g_name];
        graph_type = graph_info['graph_type'];
        id = graph_info['id'];
        description = graph_info['graph descriptor'];
        color = graph_info['color'];
        id_type = ''

        if('id_type' in graph_info){
            id_type = graph_info['id_type'];
            delete graph_info['id_type'];
        }

        delete graph_info['color'];
        delete graph_info['graph descriptor'];
        delete graph_info['graph_type'];
        delete graph_info['id'];
    }

    generate_text(id, description);

    // Checks the type of chart to be prepared
    if(graph_type == "pie"){
        piechart_generator(graph_name, graph_info, id, id_type);
    }else if(graph_type == 'scatter'){
        scatterchart_generator(graph_name, graph_info, id, color, id_type);
    }else if(graph_type == 'bar'){
        barchart_generator(graph_name, graph_info, id, color, id_type);
    }else if(graph_type == 'line'){
        linechart_generator(graph_name, graph_info, id, color, id_type);
    }else if(graph_type == 'stacked_bar'){
        stacked_barchart_generator(graph_name, graph_info, id, color, id_type);
    }
    
}  

// Code for generating random values for RGB
function getRandomColor(n) {

    color_list = ["#00b33c","#c299ff", "#660066"]
    //c = color_list.slice(0, n)
    c = color_list[Math.floor(Math.random() * color_list.length)];
    return c;
}

// Code for barchart
function barchart_generator(graph_name, graph_info, id, color, id_type){

        if((graph_name == "Dates difference (Acquisition date - Insertion date)") || (graph_name == 'Scans per session')){
            x_axis = []
            y_axis = []

            for (x in graph_info['count']){
                console.log(x);
                x_axis.push(x);
                y_axis.push(graph_info['count'][x]);
            }
    
        }else{
            xy_axis = generate_x_y_axis(graph_info['count']);
            x_axis = xy_axis[0];
            y_axis = xy_axis[1];
        }

        var data = [
            {
              x: x_axis,
              y: y_axis,
              type: 'bar',
              marker: {
                color: color // Adding color values
              }
            }
          ];
          var layout = {
                title: graph_name,
                  margin: {
                    l: 100,
                    r: 100,
                    b: 100,
                    t: 100,
                },
        };
    
        var config = {responsive: true}
    
        Plotly.newPlot('graph_body'+id, data, layout, config);
        myDiv = document.getElementById('graph_body'+id);


    drill_down(myDiv, graph_info, graph_name, id_type);

}

function stacked_barchart_generator(graph_name, graph_info, id, color, id_type){

    data = []

    x_axis = []
    for(x in graph_info['count']){
        x_axis.push(x);
    }

    differ_keys = []

    for(x in graph_info['count']){
        for(y in graph_info['count'][x]){
            if(differ_keys.includes(y)){
                continue;
            }else{
                differ_keys.push(y);
            }
        }
    }

    for(i=0; i<differ_keys.length; i++){
        y_axis = []
        for(x in graph_info['count']){
            if(differ_keys[i] in graph_info['count'][x]){
                y_axis.push(graph_info['count'][x][differ_keys[i]]);
            }else{
                y_axis.push(0);
            }
        }

        trace = {};
        trace = {
            x: x_axis,
            y: y_axis,
            name: differ_keys[i],
            type: 'bar',
        };
        data.push(trace);
    }
     if (data.length > color.length) {
            n = data.length - color.length;
            new_color = getRandomColor(n)
            color = color.concat(new_color);
     }

    var layout = {
            title: graph_name,
            colorway: color,
            barmode:'stack',
            "xaxis": {"categoryorder": "total ascending"},
            margin: {
                l: 100,
                r: 100,
                b: 100,
                t: 100,
            },
    };

    var config = {responsive: true}

    Plotly.newPlot('graph_body'+id, data, layout, config);
    myDiv = document.getElementById('graph_body'+id);

    drill_down_stacked(myDiv, graph_info, graph_name, id_type);

}


// Code for scatterchart
function scatterchart_generator(graph_name, graph_info, id, color, id_type){

    xy_axis = generate_x_y_axis(graph_info['count']);
    x_axis = xy_axis[0];
    y_axis = xy_axis[1];

    var data = [
        {
          x: x_axis,
          y: y_axis,
          mode: 'markers',
          type: 'scatter',
        }
      ];

      var layout = {
        title: graph_name
    };

    var config = {responsive: true}
    
    Plotly.newPlot('graph_body'+id, data, layout, config);
    myDiv = document.getElementById('graph_body'+id);

    drill_down(myDiv, graph_info, graph_name, id_type);
}

// Code for piechart
function piechart_generator(graph_name, graph_info){
    x_axis = [];
    y_axis = [];

    for (x in graph_info['count']){

            x_axis.push(x);
            y_axis.push(graph_info['count'][x]);
        
    }

    var data = [
        {
          values: y_axis,
          labels: x_axis,
          type: 'pie',
        }
      ];
      if (x_axis.length > color.length) {
            n = x_axis.length - color.length;
            new_color = getRandomColor(n)
            color = color.concat(new_color);
      }
      var layout = {
        title: graph_name,
        colorway: color
    };

    var config = {responsive: true}
    
    Plotly.newPlot('graph_body'+id, data, layout, config);
    myDiv = document.getElementById('graph_body'+id);

    drill_down_pie(myDiv, graph_info, graph_name, id_type);
}

// Code for linechart
function linechart_generator(graph_name, graph_info, id, color, id_type){

    data = []

    n_res = []
    for(r in graph_info['count']){
        n_res.push(r);
    }
    var arrayLength = n_res.length;

    for (var i = 0; i < arrayLength; i++){
        x_axis = []
        y_axis = []
        for(x in graph_info['count'][n_res[i]]){
            x_axis.push(x);
            y_axis.push(graph_info['count'][n_res[i]][x]);
        }
        trace = {};
        trace = {
            x: x_axis,
            y: y_axis,
            name: n_res[i],
            type: 'scatter',
        };
        data.push(trace);
    }
    if (data.length > color.length) {
            n = data.length - color.length;
            new_color = getRandomColor(n)
            color = color.concat(new_color);
    }

    var layout = {
        title: graph_name,
        colorway: color
    };

    var config = {responsive: true}

    Plotly.newPlot('graph_body'+id, data, layout, config);
    myDiv = document.getElementById('graph_body'+id);

    drill_down(myDiv, graph_info, graph_name, id_type);
}

// Generate x and y axis
function generate_x_y_axis(graph_info){

    x_axis = [];
    y_axis = [];

    var sortable = [];
    for (var x in graph_info) {
        sortable.push([x, graph_info[x]]);
    }

    sortable.sort(function(a, b) {
        return a[1] - b[1];
    });

    var objSorted = {}
    sortable.forEach(function(item){
        objSorted[item[0]]=item[1]
    });

    for (x in objSorted){
        
            x_axis.push(x);
            y_axis.push(objSorted[x]);
    }

    return [x_axis, y_axis];
}

/*
Drill down functionality
*/

a_end_e = '</a>'
a_pro = '<a href="'+ server_o + '/data/projects/'
a_sub = '<a href="'+ server_o + '/data/subjects/'
a_exp = '<a href="'+ server_o + '/data/experiments/'
a_end_s = '?format=html" target="_blank">'

function drill_down(myDiv, graph_info, graph_name, id_type){

    myDiv.on('plotly_click', function(data){
        if('list' in graph_info){
            
            $('#drillDown').modal('toggle');
            lists_output = graph_info['list'][data['points'][0]['x']];
            html_output = '';

            for (output in lists_output){

                if(id_type == 'experiment'){
                    html_output = html_output + '<center>'+a_exp+lists_output[output].split('/')[0]+a_end_s+lists_output[output]+a_end_e+'</center><br/>';
                }else if(id_type == 'subject'){
                    html_output = html_output + '<center>'+a_sub+lists_output[output].split('/')[0]+a_end_s+lists_output[output]+a_end_e+'</center><br/>';
                }else if(id_type == 'project'){
                    html_output = html_output + '<center>'+a_pro+lists_output[output].split('/')[0]+a_end_s+lists_output[output]+a_end_e+'</center><br/>';
                }else{
                    html_output = html_output + '<center>'+lists_output[output]+'</center><br/>';
                }

            }

            $('#drillDownTitle').append(graph_name+': '+data['points'][0]['x']);
            $('#modalBodyDrillDown').append(html_output);
            html_output='';

        }
    });
}

function drill_down_stacked(myDiv, graph_info, graph_name){

    myDiv.on('plotly_click', function(data){
        if('list' in graph_info){

            html_output = '';
            title = '';

            lists_output = graph_info['list'][data['points'][0]['x']];

            $('#drillDown').modal('toggle');

            for(i in lists_output){
                html_output = html_output + '<center><b>'+i+'</b></center><br/>'
                for(x in lists_output[i]){
                    if(id_type == 'experiment'){
                        html_output = html_output + '<center>'+a_exp+lists_output[i][x].split('/')[0]+a_end_s+lists_output[i][x]+a_end_e+'</center><br/>';
                    }else if(id_type == 'subject'){
                        html_output = html_output + '<center>'+a_sub+lists_output[i][x].split('/')[0]+a_end_s+lists_output[i][x]+a_end_e+'</center><br/>';
                    }else if(id_type == 'project'){
                        html_output = html_output + '<center>'+a_pro+lists_output[i][x].split('/')[0]+a_end_s+lists_output[i][x]+a_end_e+'</center><br/>';
                    }else{
                        html_output = html_output + '<center>'+lists_output[i][x]+'</center><br/>';
                    }
                }
            }
            
            $('#drillDownTitle').append(graph_name+': '+data['points'][0]['x']);
            $('#modalBodyDrillDown').append(html_output);
            html_output='';

        }
    });
}

function drill_down_pie(myDiv, graph_info, graph_name, id_type){

    myDiv.on('plotly_click', function(data){
        if('list' in graph_info){

            $('#drillDown').modal('toggle');
            lists_output = graph_info['list'][data['points'][0]['label']];
            html_output = '';
            for (output in lists_output){
                if(id_type == 'experiment'){
                    html_output = html_output + '<center>'+a_exp+lists_output[output].split('/')[0]+a_end_s+lists_output[output]+a_end_e+'</center><br/>';
                }else if(id_type == 'subject'){
                    html_output = html_output + '<center>'+a_sub+lists_output[output].split('/')[0]+a_end_s+lists_output[output]+a_end_e+'</center><br/>';
                }else if(id_type == 'project'){
                    html_output = html_output + '<center>'+a_pro+lists_output[output].split('/')[0]+a_end_s+lists_output[output]+a_end_e+'</center><br/>';
                }else{
                    html_output = html_output + '<center>'+lists_output[output]+'</center><br/>';
                }
            }
            $('#drillDownTitle').append(graph_name+': '+data['points'][0]['label']);
            $('#modalBodyDrillDown').append(html_output);
            html_output='';

        }
    });
}

function generate_text(g_id, g_value){
    $('#info_text_id'+g_id).text(g_value);
}
