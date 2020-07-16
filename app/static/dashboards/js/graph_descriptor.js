var descriptor_values = {
    "Imaging Sessions": "Total number different types of session visible",
    "Projects Visibility": "Total project visible and their visiblity type",
    "Sessions types/Project": "Number of scans for each visible project",
    "Subjects/Project": "Number of Subjects or patient in each visible project",
    "Age Range": "Age distribution of patients or subjects",
    "Gender": "Gender distribution of patients",
    "Handedness": "Number of patients with their dominant hand count",
    "Experiments/Subject": "Number of sessions for each patient",
    "Experiment Types": "Different types of Sessions",
    "Experiments/Project": "Number of sessions for each project visible",
    "Scans Quality": "How many scans are of usable quality",
    "Scan Types": "Different scan types present and there count",
    "XSI Scan Types": "Different XSI types of scans",
    "Scans/Project": "Number of scans present in each project",
    "Scans/Subject": "Number of scans for each patient",
    "Resources/Project": "Number of resources present in each project",
    "Resource Types": "Different type of resources present",
    "Resources/Session":"Number of resources present for each session",
    "UsableT1": "Number of usable and non usable T1 for each session done on patient",
    "Archiving Validator": "Number of session which have archiving validator",
    "Version Distribution": "Different versions of Archiving validator for each sessions",
    "BBRC validator": "BBRC validator present in resources for each session"
  }

function descriptor(json){
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