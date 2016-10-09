$('ul.nav li.dropdown').hover(function() {
    $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeIn(500);
  }, 
  function() {
    $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeOut(500);
    //In case user clicks the dropdown.
    $(this).removeClass("open");
  });

// Handling /dashby/users Manually to display JS pop-up on "PermissionDenied" from Django.
$(document).ready(function(){
  $("#users_page").click(function(e){
    e.preventDefault();
    $.ajax({
      "method": "GET",
      "url": "/dashby/users/",
      "success": function(result){
        window.location.href = "/dashby/users/";
      },
      "error": function(xhr, textStatus, error){
        //console.log(error);
        //if(xhr.status == 403){}
      },
    });
  });
  // Usuarios Popup.
  $("#popup-users").popover('toggle');
  $("#popup-users").on('shown.bs.popover', function(){
    setTimeout(function(){
      $("#popup-users").popover('destroy');
    }, 4000);
  })
});
