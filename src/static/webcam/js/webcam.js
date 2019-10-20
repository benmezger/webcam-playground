function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var options = {
    controls: true,
    width: 320,
    height: 240,
    fluid: true,
    plugins: {
        record: {
            audio: true,
            video: true,
            maxLength: 10,
            debug: true
        }
      }
};

var player = videojs('webcam', options, function() {
    // print version information at startup
    var msg = 'Using video.js ' + videojs.VERSION +
        ' with videojs-record ' + videojs.getPluginVersion('record');
    videojs.log(msg);
});

player.on('deviceError', function() {
    console.log('device error:', player.deviceErrorCode);
});
player.on('error', function(element, error) {
    console.error(error);
});
// user clicked the record button and started recording
player.on('startRecord', function() {
    console.log('started recording!');
});
// user completed recording and stream is available
player.on('finishRecord', function() {
    // the blob object contains the recorded data that
    // can be downloaded by the user, stored on server etc.
    upload(player.recordedData);
    // player.record().saveAs({'video': 'my-video-file-name.webm'});
});

function upload(blob) {
  var serverUrl = '/';
  var formData = new FormData();
  formData.append('video', blob, blob.name);

  fetch(serverUrl, {
    method: 'POST',
    headers: {'X-CSRFToken': getCookie('csrftoken')},
    body: formData
  }).then(
      success => console.log('recording upload complete.')
  ).catch(
      error => console.error('an upload error occurred!')
  );
}
