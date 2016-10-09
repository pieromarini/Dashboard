///////////////////////////////////////////////
//        Dropzone.js + Bootstrap            //
//        Piero Marini                       //
///////////////////////////////////////////////

// Get csrf_token
function getCookie(name){
  var cookieValue = null;
  if(document.cookie && document.cookie !== ''){
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++){
      var cookie = jQuery.trim(cookies[i]);
      if(cookie.substring(0, name.length + 1) === (name + '=')){
        cookieValue =  decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method){
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings){
    if(!csrfSafeMethod(settings.type) && !this.crossDomain){
      xhr.setRequestHandler("X-CSRFToken", csrftoken);
    }
  }
});

//Listen to change in the "Publicos" checkbox.
$('#is_public_all').change(function(){
  $("[id=is_public][type=checkbox]").each(function(){
    $(this).prop('checked', $("#is_public_all").is(":checked"));
  });
});


$(function() {
  var previewNode = document.querySelector("#template");
  previewNode.id = "";
  var previewTemplate = previewNode.parentNode.innerHTML;
  previewNode.parentNode.removeChild(previewNode);
  
  var myDropzone = new Dropzone(document.querySelector("#container-dropzone") , {
    url: "/dashby/files/add/",
    maxFilesize: 10,
    thumbnailWidth: 80,
    thumbnailHeight: 80,
    parallelUploads: 20,
    previewTemplate: previewTemplate,
    autoQueue: false,
    previewsContainer: "#previews",
    clickable: ".file-input-button",
    headers: {
      'X-CSRFToken': csrftoken
    }
  });

  myDropzone.on("addedfile", function(file){
    file.previewElement.querySelector(".start").onclick = function(){
      myDropzone.enqueueFile(file);
      };
  });
  
  myDropzone.on("totaluploadprogress", function(progress){
    document.querySelector("#total-progress .progress-bar").style.width = progress + "%";
  });

  myDropzone.on("sending", function(file, xhr, formData){
    // Show total progress on start and disable START button.
    document.querySelector("#total-progress").style.opacity = "1";
    file.previewElement.querySelector(".start").setAttribute("disabled", "disabled");
    // Add "is_public" data to the POST.
    var is_public = $('#is_public').is(':checked')
    $('#is_public').remove();
    if (!is_public){
      $("label[for='is_public']").text("Not Public");
    }
    formData.append('is_public', is_public);
  });
  
  // Hide progress bar when complete.
  myDropzone.on("queuecomplete", function(progress){
    document.querySelector("#total-progress").style.opacity = "0";
  });

  // Setup buttons for every file.
  document.querySelector("#actions .start").onclick = function(){
    myDropzone.enqueueFiles(myDropzone.getFilesWithStatus(Dropzone.ADDED));
  };
  document.querySelector("#actions .cancel").onclick = function(){
    myDropzone.removeAllFiles(true);
  };
});
