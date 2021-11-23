$(document).ready(function() {
  // Removes preloader after all files loaded
  $(window).on('load', function() {
    $(".preloader").remove();
  });

  $(document).on('click', '.mega-dropdown', function(e) {
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

  // Card hover animation for adding shadow
  $(".card").hover(
    function() {
      $(this).addClass('shadow-lg').css('cursor', 'pointer');
    },
    function() {
      $(this).removeClass('shadow-lg');
    }
  );

  // Add hide and show logic for project list, project list owned, collab or member and overview dashboards
  $(".project_part").addClass("hide");
  $("#overview").addClass("highlight");

  $("#overview").click(function() {
    $(".project_part").addClass("hide");
    $(".overview_part").removeClass("hide");
    $("#overview").addClass("highlight");
    $("#projects").removeClass("highlight");
  });
  $("#projects").click(function() {
    $(".project_part").removeClass("hide");
    $(".overview_part").addClass("hide");
    $("#projects").addClass("highlight");
    $("#overview").removeClass("highlight");
  });


  // Delete data added to modal after hiding the modal
  $('#drillDown').on('hidden.bs.modal', function(e) {
    $('#modalBodyDrillDown').empty();
    $('#drillDownTitle').empty();
  });
});
