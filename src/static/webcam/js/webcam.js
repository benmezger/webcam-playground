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
            audio: false,
            image: true,
            video: false,
            maxLength: 10,
            debug: true
        }
      }
};

function clearphoto() {
  var context = canvas.getContext('2d');
  context.fillStyle = "#FF9500";
  context.fillRect(0, 0, canvas.width, canvas.height);

  var data = canvas.toDataURL('image/png');
  photo.setAttribute('src', data);
}

var player = videojs('webcam', options, function() {
    // print version information at startup
    var msg = 'Using video.js ' + videojs.VERSION +
        ' with videojs-record ' + videojs.getPluginVersion('record');
    videojs.log(msg);
  canvas = document.getElementById('canvas');
  clearphoto();

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

function b64toBlob(dataURI) {

    var byteString = atob(dataURI.split(',')[1]);
    var ab = new ArrayBuffer(byteString.length);
    var ia = new Uint8Array(ab);

    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], { type: 'image/jpeg' });
}

async function upload(blob) {
  var serverUrl = '/';
  var formData = new FormData();
  formData.append('image', b64toBlob(blob), "image.png");

  const response = await fetch(serverUrl, {
    method: 'POST',
    headers: {'X-CSRFToken': getCookie('csrftoken')},
    body: formData
  });

  const result = await response.json();
  var canvas = document.getElementById('canvas');
  canvas.width = 600;
  canvas.height = 524;

  photo = document.getElementById('photo');
  photo.setAttribute('src', result.image);
}
