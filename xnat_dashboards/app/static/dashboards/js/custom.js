// Removes preloader after all files loaded
$(window).on('load', function () {
    $(".preloader").remove();
});

$(function() {

    jQuery(document).on('click', '.mega-dropdown', function(e) {
        e.stopPropagation()
    }); 

    // Top header part and sidebar par

    var set = function() {
        var width = (window.innerWidth > 0) ? window.innerWidth : this.screen.width;
        var topOffset = 75;
        if (width < 1170) {
            $("body").addClass("mini-sidebar");
            $('.navbar-brand span').hide();
        } else {
            $("body").removeClass("mini-sidebar");
            $('.navbar-brand span').show();
        }
        var height = ((window.innerHeight > 0) ? window.innerHeight : this.screen.height) - 1;
        height = height - topOffset;
        if (height < 1) height = 1;
        if (height > topOffset) {
            $(".page-wrapper").css("min-height", (height) + "px");
        }
    };

    // nav bar icon toggler

    $(".nav-toggler").on('click', function() {
        $("body").toggleClass("show-sidebar");

    });
    $(window).ready(set);
    $(window).on("resize", set);   
    $(".sidebartoggler").on('click', function() {
        $("body").toggleClass("mini-sidebar");

    });

    $("body, .page-wrapper").trigger("resize");

    $('a[data-action="collapse"]').on('click', function(e) {
        e.preventDefault();
        $(this).closest('.card').find('[data-action="collapse"] i').toggleClass('ti-minus ti-plus');
        $(this).closest('.card').children('.card-body').collapse('toggle');
    });
    // Toggle fullscreen
    $('a[data-action="expand"]').on('click', function(e) {
        e.preventDefault();
        $(this).closest('.card').find('[data-action="expand"] i').toggleClass('mdi-arrow-expand mdi-arrow-compress');
        $(this).closest('.card').toggleClass('card-fullscreen');
    });
    // Close Card
    $('a[data-action="close"]').on('click', function() {
        $(this).closest('.card').removeClass().slideUp('fast');
    });

});


// Card hover animation for adding shadow
$( ".card" ).hover(
    function() {
      $(this).addClass('shadow-lg').css('cursor', 'pointer'); 
    }, function() {
      $(this).removeClass('shadow-lg');
    }
  );

// Add hide and show logic for project list, project list owned, collab or member and overview dashboards

$(".project_part").addClass("hide");
$(".project_part_ow_co_me").addClass("hide");
$("#overview").addClass("highlight");
$(".longitudinal_part").addClass("hide");

$("#overview").click(function(){
    $(".project_part").addClass("hide");
    $(".project_part_ow_co_me").addClass("hide");
    $(".overview_part").removeClass("hide");
    $("#overview").addClass("highlight");
    $(".longitudinal_part").addClass("hide");
    $("#longitudinal").removeClass("highlight");
    $("#projects").removeClass("highlight");
    $("#projects_ow_co_me").removeClass("highlight");
});
$("#projects").click(function(){
    $(".project_part").removeClass("hide");
    $(".project_part_ow_co_me").addClass("hide");
    $(".overview_part").addClass("hide");
    $(".longitudinal_part").addClass("hide");
    $("#longitudinal").removeClass("highlight");
    $("#projects").addClass("highlight");
    $("#overview").removeClass("highlight");
    $("#projects_ow_co_me").removeClass("highlight");
});
$("#projects_ow_co_me").click(function(){
    $(".project_part_ow_co_me").removeClass("hide");
    $(".project_part").addClass("hide");
    $(".overview_part").addClass("hide");
    $(".longitudinal_part").addClass("hide");
    $("#longitudinal").removeClass("highlight");
    $("#projects").removeClass("highlight");
    $("#overview").removeClass("highlight");
    $("#projects_ow_co_me").addClass("highlight");
});
$("#longitudinal").click(function(){
    $(".longitudinal_part").removeClass("hide");
    $(".project_part_ow_co_me").addClass("hide");
    $(".project_part").addClass("hide");
    $(".overview_part").addClass("hide");
    $("#longitudinal").addClass("highlight");
    $("#projects").removeClass("highlight");
    $("#overview").removeClass("highlight");
    $("#projects_ow_co_me").removeClass("highlight");
});

// Counter js for counting animation

(function ($) {
	$.fn.countTo = function (options) {
		options = options || {};
		
		return $(this).each(function () {
			// set options for current element
			var settings = $.extend({}, $.fn.countTo.defaults, {
				from:            $(this).data('from'),
				to:              $(this).data('to'),
				speed:           $(this).data('speed'),
				refreshInterval: $(this).data('refresh-interval'),
				decimals:        $(this).data('decimals')
			}, options);
			
			// how many times to update the value, and how much to increment the value on each update
			var loops = Math.ceil(settings.speed / settings.refreshInterval),
				increment = (settings.to - settings.from) / loops;
			
			// references & variables that will change with each update
			var self = this,
				$self = $(this),
				loopCount = 0,
				value = settings.from,
				data = $self.data('countTo') || {};
			
			$self.data('countTo', data);
			
			// if an existing interval can be found, clear it first
			if (data.interval) {
				clearInterval(data.interval);
			}
			data.interval = setInterval(updateTimer, settings.refreshInterval);
			
			// initialize the element with the starting value
			render(value);
			
			function updateTimer() {
				value += increment;
				loopCount++;
				
				render(value);
				
				if (typeof(settings.onUpdate) == 'function') {
					settings.onUpdate.call(self, value);
				}
				
				if (loopCount >= loops) {
					// remove the interval
					$self.removeData('countTo');
					clearInterval(data.interval);
					value = settings.to;
					
					if (typeof(settings.onComplete) == 'function') {
						settings.onComplete.call(self, value);
					}
				}
			}
			
			function render(value) {
				var formattedValue = settings.formatter.call(self, value, settings);
				$self.html(formattedValue);
			}
		});
	};
	
	$.fn.countTo.defaults = {
		from: 0,               // the number the element should start at
		to: 0,                 // the number the element should end at
		speed: 1000,           // how long it should take to count between the target numbers
		refreshInterval: 100,  // how often the element should be updated
		decimals: 0,           // the number of decimal places to show
		formatter: formatter,  // handler for formatting the value before rendering
		onUpdate: null,        // callback method for every time the element is updated
		onComplete: null       // callback method for when the element finishes updating
	};
	
	function formatter(value, settings) {
		return value.toFixed(settings.decimals);
	}
}(jQuery));

jQuery(function ($) {
  // custom formatting example
  $('.count-number').data('countToOptions', {
	formatter: function (value, options) {
	  return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
	}
  });
  
  // start all the timers
  $('.timer').each(count);  
  
  function count(options) {
	var $this = $(this);
	options = $.extend({}, options || {}, $this.data('countToOptions') || {});
	$this.countTo(options);
  }
});

// Delete data added to modal after hiding the modal
$('#drillDown').on('hidden.bs.modal', function (e) {
    $('#modalBodyDrillDown').empty();
    $('#drillDownTitle').empty();
  });


/*
Code for hiding and displaying test grid in per project view
*/


$(".tests_grid_part").addClass("hide");
$(".p_project_part").removeClass("hide");
$("#project").addClass("highlight");

$("#project").click(function(){
    $(".tests_grid_part").addClass("hide");
    $(".p_project_part").removeClass("hide");
    $("#project").addClass("highlight");
    $("#tests_grid").removeClass("highlight");
});
$("#tests_grid").click(function(){
    $(".tests_grid_part").removeClass("hide");
    $(".p_project_part").addClass("hide");
    $("#project").removeClass("highlight");
    $("#tests_grid").addClass("highlight");
});

// Delete data added to modal after hiding the modal tests
$('#test').on('hidden.bs.modal', function (e) {
    $('#modalTest').empty();
    $('#testTitle').empty();
  });


// Code for showing information regarding failed test
$('#tests_table tbody td').on('click', function(){
    data_l = $(this).children().html();

    html_output = '';
    
    if(data_l == '' || data_l == [] || data_l == 'undefined'){

    }else{
        
        html_output = data_l;
            
        $('#test').modal('toggle');
        $('#testTitle').append("Status");
        $('#modalTest').append(html_output);
        html_output = '';
    }
});


// Download data as excel from table

$(document).ready(function(){
    $("#btnExport").click(function() {
        let table = document.getElementsByTagName("table");
        TableToExcel.convert(table[1], { // html code may contain multiple tables so here we are referring to 1st table tag
           name: project_id+`_export.xlsx`, // fileName you could use any name
           sheet: {
              name: 'Sheet 1' // sheetName
           }
        });
    });
});

// Code for filtering version
function filterVersion(){
        var input = document.getElementById("version_list");
        filter = input.value;
        console.log(filter);
        if(filter == 'All'){
            var rows = $('#tests_table tbody tr');
            rows.show();
        }else{
            $("#tests_table tbody tr").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(filter) > -1)
              });
        }
}