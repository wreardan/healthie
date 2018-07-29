// Drag and drop functionality for Records page
function dropHandler(ev) {
  console.log('File(s) dropped');

  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();

  if (ev.dataTransfer.items) {
    // Use DataTransferItemList interface to access the file(s)
    for (var i = 0; i < ev.dataTransfer.items.length; i++) {
      // If dropped items aren't files, reject them
      if (ev.dataTransfer.items[i].kind === 'file') {
        var file = ev.dataTransfer.items[i].getAsFile();
        console.log('... file[' + i + '].name = ' + file.name);
        addFile(file);

      }
    }
  } else {
    // Use DataTransfer interface to access the file(s)
    for (var i = 0; i < ev.dataTransfer.files.length; i++) {
      var file = ev.dataTransfer.files[i];
      console.log('... file[' + i + '].name = ' + ev.dataTransfer.files[i].name);
      addFile(file);
    }
  } 
  
  // Pass event to removeDragData for cleanup
  removeDragData(ev)
}

function addFile(file) {
  var name = file.name;
  $(".record-table tbody").append("<tr><td>" + name + "</td><td>7/28/18</td><td>San Francisco General</td></tr>");

  var form_data = new FormData();
  form_data.append("attachment", file);
  $.ajax({
      type: 'POST',
      url: '/attachment',
      data: form_data,
      contentType: file.type,
      cache: false,
      processData: false,
      async: false,
      success: function(data) {
          console.log('Success!');
      },
  });
}

function dragOverHandler(ev) {
  console.log('File(s) in drop zone'); 

  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();
}

function removeDragData(ev) {
  console.log('Removing drag data')

  if (ev.dataTransfer.items) {
    // Use DataTransferItemList interface to remove the drag data
    ev.dataTransfer.items.clear();
  } else {
    // Use DataTransfer interface to remove the drag data
    ev.dataTransfer.clearData();
  }
}

// function setupDrop() {
//   $(window).load(function() {
//     $content = $(".app-content");
//     var height = $content.height();
//     if(height < window.innerHeight) {
//       $content.css("min-height", height);
//     }
//   });
// }
