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
               "Scans/Subject": false};


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
        id = graph_info['id'];
        description = graph_info['graph descriptor'];
        color = graph_info['color'];

        delete graph_info['color'];
        delete graph_info['graph descriptor'];
        delete graph_info['graph_type'];
        delete graph_info['id'];
    }

    generate_text(id, description);

    // Checks the type of chart to be prepared
    if(graph_type == "pie"){
        piechart_generator(graph_name, graph_info, id);
    }else if(graph_type == 'scatter'){
        scatterchart_generator(graph_name, graph_info, id, color);
    }else if(graph_type == 'bar'){
        barchart_generator(graph_name, graph_info, id, color);
    }else if(graph_type == 'line'){
        linechart_generator(graph_name, graph_info, id, color);
    }
}  

// Code for generating random values for RGB
function getRandomIntInclusive(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Code for barchart
function barchart_generator(graph_name, graph_info, id){
    if(stack_count[graph_name]){
        
        data = [];
        for (gi in graph_info){
            var x_axis = [];
            var y_axis = [];
            for( x in graph_info[gi]){
                if(gi == 'graph_type' || gi == 'id' ){
                    continue;
                }else{
                    console.log(x);
                    console.log(graph_info[gi][x]);
                    x_axis.push(x);
                    y_axis.push(graph_info[gi][x]);
                }
            }
            trace = {};
            r = getRandomIntInclusive(0,254);
            g = getRandomIntInclusive(0,254);
            b = getRandomIntInclusive(0,254);
            trace = {
                x: x_axis,
                y: y_axis,
                name: gi,
                type: 'bar',
                marker: {
                  color: 'rgb('+r+','+g+','+b+')' // Adding color values
                }
              };
              data.push(trace);
        }
    }else{
        x_axis = [];
        y_axis = [];
        for (x in graph_info){
            if(x == 'graph_type' || x == 'id' ){
                continue;
            }else{
                x_axis.push(x);
                y_axis.push(graph_info[x]);
            }
        }

        r = getRandomIntInclusive(0,254);
        g = getRandomIntInclusive(0,254);
        b = getRandomIntInclusive(0,254);
        var data = [
            {
              x: x_axis,
              y: y_axis,
              type: 'bar',
              marker: {
                color: 'rgb('+r+','+g+','+b+')' // Adding color values
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

}

// Code for scatterchart
function scatterchart_generator(graph_name, graph_info, id){
    x_axis = [];
    y_axis = [];
    for (x in graph_info){
            x_axis.push(x);
            y_axis.push(graph_info[x]);
        
    }
    //Generating color values
    r = getRandomIntInclusive(0,254);
    g = getRandomIntInclusive(0,254);
    b = getRandomIntInclusive(0,254);
    var data = [
        {
          x: x_axis,
          y: y_axis,
          mode: 'markers',
          type: 'scatter',
          marker: {
            color: 'rgb('+r+','+g+','+b+')' // Adding color values
          }
        }
      ];

      var layout = {
        title: graph_name
    };

    var config = {responsive: true}
    
    Plotly.newPlot('graph_body'+id, data, layout, config);

}

// Code for piechart
function piechart_generator(graph_name, graph_info, id){
    x_axis = [];
    y_axis = [];

    for (x in graph_info){
        
            x_axis.push(x);
            y_axis.push(graph_info[x]);
        
    }
    colors_num = x_axis.length;
    colors_list = []

    // Generating color values
    for( i=0; i<colors_num; i++ ){
        r = getRandomIntInclusive(0,255);
        g = getRandomIntInclusive(0,255);
        b = getRandomIntInclusive(0,255);
        colors_list.push('rgb('+r+','+g+','+b+')');
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

}

// Code for linechart
function linechart_generator(graph_name, graph_info, id){
    x_axis = [];
    y_axis = [];
    for (x in graph_info){
            x_axis.push(x);
            y_axis.push(graph_info[x]);
        
    }
    // Generating color values
    r = getRandomIntInclusive(0,254);
    g = getRandomIntInclusive(0,254);
    b = getRandomIntInclusive(0,254);
    var data = [
        {
          x: x_axis,
          y: y_axis,
          type: 'scatter',
          marker: {
            color: 'rgb('+r+','+g+','+b+')' // Adding random color values
          }
        }
      ];

      var layout = {
        title: graph_name
    };

    var config = {responsive: true}
    
    Plotly.newPlot('graph_body'+id, data, layout, config);

}


function generate_text(g_id, g_value){
    $('#info_text_id'+g_id).text(g_value);
}