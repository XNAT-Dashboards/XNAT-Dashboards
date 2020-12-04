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
function getRandomColor() {

    min = Math.ceil(0);
    max = Math.floor(255);

    r = Math.floor(Math.random() * (max - min + 1)) + min;
    g = Math.floor(Math.random() * (max - min + 1)) + min;
    b = Math.floor(Math.random() * (max - min + 1)) + min;

    color = 'rgb('+r+','+g+','+b+')';
    return color;
}

// Code for barchart
function barchart_generator(graph_name, graph_info, id, color, id_type){

        if(graph_name == "Age Range"){
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

        updatemenus= [{
            y: 1.3,
            yanchor: 'top',
            x:0,
            xanchor:"left",
            pad:{"r": 10, "t": 10},
            buttons: [{
                method: 'relayout',
                args: [{"yaxis.type": "linear"}],
                label: 'Linear'
            },{
                method: 'relayout',
                args: [{"yaxis.type": "log"}],
                label: 'Log'
            }]
        }]
    
        var layout = {
                title: graph_name,
                updatemenus:updatemenus,
                barmode:'stack'
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
        color = getRandomColor();
        trace = {
            x: x_axis,
            y: y_axis,
            name: differ_keys[i],
            type: 'bar',
            marker: {
            color: color // Adding color values
            }
        };
        data.push(trace);
    }


    updatemenus= [{
        y: 1.3,
        yanchor: 'top',
        x:0,
        xanchor:"left",
        pad:{"r": 10, "t": 10},
        buttons: [{
            method: 'relayout',
            args: [{"yaxis.type": "linear"}],
            label: 'Linear'
        },{
            method: 'relayout',
            args: [{"yaxis.type": "log"}],
            label: 'Log'
        }]
    }]

    var layout = {
            title: graph_name,
            updatemenus:updatemenus,
            barmode:'stack'
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
          marker: {
            color: color // Adding color values
          }
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
    
    colors_num = x_axis.length;
    colors_list = []

    // Generating color values
    for( i=0; i<colors_num; i++ ){
        
        color = getRandomColor();
        while(colors_list.indexOf(color) != -1){
            color = getRandomColor();
        }
        colors_list.push(color);
    }

    var data = [
        {
          values: y_axis,
          labels: x_axis,
          type: 'pie',
          marker: {
            colors: colors_list // Adding color for each part of pie
          }
        }
      ];

      var layout = {
        title: graph_name
    };

    var config = {responsive: true}
    
    Plotly.newPlot('graph_body'+id, data, layout, config);
    myDiv = document.getElementById('graph_body'+id);

    drill_down_pie(myDiv, graph_info, graph_name, id_type);
}

// Code for linechart
function linechart_generator(graph_name, graph_info, id, color, id_type){

    xy_axis = generate_x_y_axis(graph_info['count']);
    x_axis = xy_axis[0];
    y_axis = xy_axis[1];

    var data = [
        {
          x: x_axis,
          y: y_axis,
          type: 'scatter',
          marker: {
            color: color // Adding random color values
          }
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
