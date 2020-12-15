$(function() {
    console.log( "working!" );
});


// ALERT FLASHER


  $( "#email-icon" ).mouseenter(function() {
    $( this ).removeClass( "fas fa-envelope fa-5x" ).addClass( "fas fa-envelope-open fa-5x btn-r-2");
  })
  .mouseleave(function() {
    $( this ).removeClass( "fas fa-envelope-open fa-5x btn-r-2" ).addClass( "fas fa-envelope fa-5x");
  });



  $("footer").css("bottom", "0")
