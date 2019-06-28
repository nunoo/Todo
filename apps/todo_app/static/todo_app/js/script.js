$(function(){
    //Getting values from session and saving in javascript variable.
    // But this will be executed only at document.ready.
    var firstName = '<%= Session["First_Name"] ?? "" %>';
    var lastName = '<%= Session["Last_Name"] ?? "" %>';
 
    $("#first_name").val(firstName);
    $("#last_name").val(lastName);
 
    $('#fb-btn').click(function(){
      //Posting values to save in session
      $.post(document.URL+'?mode=ajax', 
      {'first_name':$("#first_name").val(),
      'last_name':$("#last_name").val()
      } );
    });
 
  });