$(function() {
    console.log( "working!" );
});


// WELCOME
let $welcomePage = $("#welcome")

if ($welcomePage) {
  $("body").css("background-image", "https://images.unsplash.com/photo-1585378335564-c220f04a9ad0?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1834&q=80");

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


