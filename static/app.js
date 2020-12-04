$(function() {
    console.log( "working!" );
});


// WELCOME
let $welcomePage = $("#welcome")

if ($welcomePage) {
  $("body").css("background-color", "white");
}


// BUTTONS
$( "#us-daily-btn" ).click(function() {
    $( "#current-hospital-graph" ).hide();
    $( "#death-daily-graph" ).hide();
    $( "#us-daily-graph" ).show();
  });

$( "#current-hospital-btn" ).click(function() {
        $( "#us-daily-graph" ).hide();
        $( "#death-daily-graph" ).hide();
        $( "#current-hospital-graph" ).show();
  });  

  $( "#death-daily-btn" ).click(function() {
    $( "#us-daily-graph" ).hide();
    $( "#current-hospital-graph" ).hide();
    $( "#death-daily-graph" ).show();
});  


