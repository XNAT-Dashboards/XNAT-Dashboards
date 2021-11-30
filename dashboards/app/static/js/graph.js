function show_graphs(graphs) {

  html = '<div class="row">'
  for (id = 0; id < graphs.length; id++) {
    html = html + `<div class="col-lg-6"><div class="card">
                  <div class="card-body" id="graph_id` + id + `">
                      <i id="info_id' + id + '" class="fa fa-info wrapper_tooltip" aria-hidden="true" >
                              <div id="info_text_id` + id + `" class="tooltip"></div>
                      </i>
                      <div id="graph_body` + id + `"></div>
                  </div></div></div>`
    if (id % 2 != 0) {
      html = html + '</div><div class="row">'
    }
  }

  $("#graphs").html(html)


  function make_drill(drill) {
    is_array = Array.isArray(drill);
    console.log(is_array)

    if (is_array) {
      item = drill[0];
    } else {
      k = Object.keys(drill)[0];
      item = drill[k][0][0]
    }

    if (item.split('_')[1][0] == 'E')
      id_type = 'experiment'
    else if (item.split('_')[1][0] == 'S')
      id_type = 'subject'
    else
      id_type = 'project'


    html = ''
    for (i in drill) {
      item = drill[i];
      if (is_array) {
        html += '<center><a href="' + server + '/data/' + id_type + 's/' + item.split('/')[0] + '?format=html" target="_blank">' + item + '</a></center><br/>'
      } else {
        html = html + '<center><b>' + i + '</b></center><br/>'
        for (x in item[0]) {
          html += '<center><a href="' + server + '/data/' + id_type + 's/' + item[0][x].split('/')[0] + '?format=html" target="_blank">' + item[0][x] + '</a></center><br/>'
        }
      }
    }
    return html;
  }

  for (i in graphs) {
    graph = graphs[i];
    id = graph[0];
    data = graph[1];
    layout = graph[2];
    layout['font'] = {
      family: 'Poppins, sans-serif'
    }
    desc = graph[3];
    name = graph[4];
    drill = graph[5];
    type = graph[6];
    Plotly.newPlot('graph_body' + id, data, layout, {
      responsive: true
    });
    $('#info_text_id' + id).text(desc);
    document.getElementById('graph_body' + id).on('plotly_click', function(data) {
      pn = data.points[0].label;

      $('#drillDown').modal('toggle');
      id = $(data.event.target).closest('div.card-body').attr('id');
      id = parseInt(id.slice('graph_id'.length))
      graph = graphs[id]
      name = graph[4];
      drill = graph[5];
      type = graph[6];
      $('#drillDownTitle').append(name + ': ' + pn);

      if (drill != undefined) {
        drill = graph[5][pn];
        $('#modalBodyDrillDown').append(make_drill(drill));
      }
    })

  }
}
