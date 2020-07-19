// Generate Charts using the json provided from html jinja
stack_count = {"Stats": false,
               "Sessions types/Project":true,
               "Imaging Sessions": false,
               "Projects Visibility": false,
               "Subjects/Project": false,
               "Age Range":false,
               "Gender": false,
               "Handedness": false,
               "Experiments/Subject": false,
               "Experiment Types": false,
               "Experiments/Project": false,
               "Scans Quality": false,
               "Scan Types":false,
               "XSI Scan Types": false,
               "Scans/Project": false, 
               "Scans/Subject": false, 
               "Resources/Project": false,
               "Resource Types": false,
               "Resources/Session":false,
               "UsableT1": false,
               "Archiving Validator": false,
               "Version Distribution": false,
               "BBRC validator": false};


function chart_generator(json){

    /* 
    JSON structure: 
    {
        'graph_name' : {
            'x1':'y1',
            'x2':'y2',
            'x3':'y3',
            'graphy_type':'bar'
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
    }

    // Checks the type of chart to be prepared
    if(graph_type == "pie"){
        delete graph_info['graph_type'];
        id = graph_info['id'];
        delete graph_info['id'];
        piechart_generator(graph_name, graph_info, id);
    }else if(graph_type == 'scatter'){
        delete graph_info['graph_type']
        id = graph_info['id'];
        delete graph_info['id'];
        scatterchart_generator(graph_name, graph_info, id);
    }else if(graph_type == 'bar'){
        id = graph_info['id'];
        delete graph_info['graph_type'];
        delete graph_info['id'];
        barchart_generator(graph_name, graph_info, id);
    }else if(graph_type == 'line'){
        id = graph_info['id'];
        delete graph_info['graph_type'];
        delete graph_info['id'];
        linechart_generator(graph_name, graph_info, id);
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
function barchart_generator(graph_name, graph_info, id){

    if(stack_count[graph_name]){
        
        data = [];
        for (gi in graph_info['count']){

            xy_axis = generate_x_y_axis(graph_info['count'][gi]);
            x_axis = xy_axis[0];
            y_axis = xy_axis[1];

            trace = {};
            color = getRandomColor();
            trace = {
                x: x_axis,
                y: y_axis,
                name: gi,
                type: 'bar',
                marker: {
                  color: color // Adding color values
                }
              };
              data.push(trace);
              
        }

    }else{

        xy_axis = generate_x_y_axis(graph_info['count']);
        x_axis = xy_axis[0];
        y_axis = xy_axis[1];

        // Generating color values
        color = getRandomColor();
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

    drill_down(myDiv, graph_info, graph_name);
}


// Code for scatterchart
function scatterchart_generator(graph_name, graph_info){

    xy_axis = generate_x_y_axis(graph_info['count']);
    x_axis = xy_axis[0];
    y_axis = xy_axis[1];

    //Generating color values
    color = getRandomColor()

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

    drill_down(myDiv, graph_info, graph_name);
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

    drill_down_pie(myDiv, graph_info, graph_name);
}

// Code for linechart
function linechart_generator(graph_name, graph_info){

    xy_axis = generate_x_y_axis(graph_info['count']);
    x_axis = xy_axis[0];
    y_axis = xy_axis[1];

    // Generating color values
    color = getRandomColor();
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

    drill_down(myDiv, graph_info, graph_name);
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


function drill_down(myDiv, graph_info, graph_name){

    myDiv.on('plotly_click', function(data){
        if('list' in graph_info){
            
            $('#drillDown').modal('toggle');
            lists_output = graph_info['list'][data['points'][0]['x']];
            html_output = '';
            for (output in lists_output){
                html_output = html_output + '<center>'+lists_output[output]+'</center><br/>';
            }
            $('#drillDownTitle').append(graph_name+': '+data['points'][0]['x']);
            $('#modalBodyDrillDown').append(html_output);
            html_output='';

        }
    });
}

function drill_down_pie(myDiv, graph_info, graph_name){

    myDiv.on('plotly_click', function(data){
        if('list' in graph_info){

            $('#drillDown').modal('toggle');
            lists_output = graph_info['list'][data['points'][0]['label']];
            html_output = '';
            for (output in lists_output){
                html_output = html_output + '<center>'+lists_output[output]+'</center><br/>';
            }
            $('#drillDownTitle').append(graph_name+': '+data['points'][0]['label']);
            $('#modalBodyDrillDown').append(html_output);
            html_output='';

        }
    });
}