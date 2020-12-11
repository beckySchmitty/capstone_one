$(function() {
    console.log( "working!" );
});


// ALERT FLASHER
$(document).ready(function() {
  setTimeout(function() {
      $('.alert').fadeOut('slow');
  }, 2000);



  // add pop up for demo 
  // add notificaiton about when data is updated 