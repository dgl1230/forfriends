
  $("#email_login").click(function() {
    $("#register").fadeIn("slow", "linear");
    });

  $("#email_login2").click(function() {
    $("#register").fadeIn("slow", "linear");
    });

    jQuery('.postwords').addClass("hidden2").viewportChecker({
      classToAdd:'visible animated fadeIn',
      offset: 300
    });
 
    jQuery('#bottom_buttons').addClass("hidden2").viewportChecker({
      classToAdd:'visible animated fadeInUp',
      offset: 100
    });
 
    jQuery('#user_1').addClass("hidden2").viewportChecker({
      classToAdd:'visible animated rollIn',
      offset: 100
    });
 
    jQuery('#user_2').addClass("hidden2").viewportChecker({
      classToAdd:'visible animated rollIn',
      offset: 100
    });
 
    jQuery('#match').viewportChecker({
      classToAdd:'visible animated tada',
      offset: 100
    });