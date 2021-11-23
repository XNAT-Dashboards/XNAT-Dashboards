// Code for filtering version
function filterVersion() {
  var input = document.getElementById("version_list");
  filter = input.value;
  console.log(filter);
  if (filter == 'All') {
    var rows = $('#tests_table tbody tr');
    rows.show();
  } else {
    $("#tests_table tbody tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(filter) > -1)
    });
  }
}

$(document).ready(function() {

  // Download data as excel from table

  $("#btnExport").click(function() {
    let table = document.getElementsByTagName("table");
    TableToExcel.convert(table[1], { // html code may contain multiple tables so here we are referring to 1st table tag
      name: project_id + `_export.xlsx`, // fileName you could use any name
      sheet: {
        name: 'Sheet 1' // sheetName
      }
    });
  })

  // Code for hiding and displaying test grid in per project view
  $(".tests_grid_part").addClass("hide");
  $(".p_project_part").removeClass("hide");
  $("#project").addClass("highlight");

  $("#project").click(function() {
    $(".tests_grid_part").addClass("hide");
    $(".p_project_part").removeClass("hide");
    $("#project").addClass("highlight");
    $("#tests_grid").removeClass("highlight");
  });
  $("#tests_grid").click(function() {
    $(".tests_grid_part").removeClass("hide");
    $(".p_project_part").addClass("hide");
    $("#project").removeClass("highlight");
    $("#tests_grid").addClass("highlight");
  });

  // Delete data added to modal after hiding the modal tests
  $('#test').on('hidden.bs.modal', function(e) {
    $('#modalTest').empty();
    $('#testTitle').empty();
  });


  // Code for showing information regarding failed test
  $('#tests_table tbody td').on('click', function() {
    data = $(this).children().html();
    if (data != '' && data != [] && data != 'undefined') {
      $('#test').modal('toggle');
      $('#testTitle').append("Status");
      $('#modalTest').append(data);
    }
  });

});
