// jQuery to collapse the navbar on scroll
$(window).scroll(function() {
    if ($(".navbar").offset().top > 50) {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
    } else {
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
    }
});

// jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});

// Closes the Responsive Menu on Menu Item Click
$('.navbar-collapse ul li a').click(function() {
    $('.navbar-toggle:visible').click();
});

function createImage(userName){
    $.ajax({
       type: "GET",
       url: "http://radio.rrampt.com/api/create/" + userName,
       success: function(msg){
         alert( "Data Saved: " + msg );
       }
     });
}

function pollTaskId(taskId, userName) {

    $.ajax({
        type: "GET",
        url: "http://rradio.rrampt.com/api/status/" + userName + "/" +taskId ,
        success: function(msg) {
            if ( msg.result == "SUCCESS" ){
                alert( "job is finished." );
                return;
            }
        }
    });

    setTimeout("pollTaskId", 5000);
}

$("#create-collage").click(function() {
  
    // ensure the text field contains any value 
    if ( !$("#discogs-username").val() ) {
        $("#alert").html("<p class=\"text-danger\"><strong>Please specify a Discogs username.</strong></p>");
        return;
    }

    // attempt to perform a regex match on input field
    var match = $("#discogs-username").val().match(/^([A-Za-z0-9\-\_\.]+)$/);

    // bail if there are no matches.
    if (! match) { 
        $("#alert").html("<p class=\"text-danger\"><strong>Invalid Discogs username.Discogs supports letters, numbers, commas, underscores and hyphens only.</strong></p>");
       return; 
    }

    var userName = match[1];
    //$(document).scrollTop( $("#about").offset().top );
    $("#create-collage").hide()
    $("#discogs-username").hide()

    $("#alert").html("<p class=\"text-info\"><strong>Generating your collage. Please be patient</strong></p>");

    var taskId = createImage(userName);

    if ( ! taskId ) {
        return;
    }
    pollTaskId(taskId, userName);
    
});
