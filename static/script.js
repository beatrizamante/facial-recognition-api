const IMAGE_INTERVAL_MS = 42;

const drawFaceRectangles = (video, canvas, faces) => {
  const ctx = canvas.getContext('2d');

  ctx.width = video.videoWidth;
  ctx.height = video.videoHeight;

  ctx.clearRect(0, 0, ctx.width, ctx.height);
  
  if (!faces.facesList || faces.facesList.length === 0) {
    return;    
  }
  ctx.beginPath();

  for (const face of faces.facesList) { 
    const { x, y, width, height, label } = face; 
    ctx.strokeStyle = "#005D54";
    ctx.lineWidth = 4
    ctx.beginPath();
    ctx.rect(x, y, width, height);
    ctx.stroke();

    const labelHeight = 20; 
    ctx.fillStyle = "#005D54"; 
    ctx.fillRect(x, y + height, width, labelHeight);

    ctx.fillStyle = "#FFFFFF"; 
    ctx.font = "16px Sans"; 
    ctx.textBaseline = "top";
    ctx.fillText(label, x + 5, y + height + 2); 
  }
};

const startFaceDetection = (video, canvas, deviceId) => {
  const socket = new WebSocket('wss://172.16.3.21:8000/face-detection');
  let intervalId;

  // Connection opened
  socket.addEventListener('open', function () {

    // Start reading video from device
    navigator.mediaDevices.getUserMedia({
      audio: false,
      video: {
        deviceId,
        width: { max: 640 },
        height: { max: 480 },
      },
    }).then(function (stream) {
      video.srcObject = stream;
      video.play().then(() => {
        // Adapt overlay canvas size to the video size
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Send an image in the WebSocket every 42 ms
        intervalId = setInterval(() => {

          // Create a virtual canvas to draw current video image
          const canvas = document.createElement('canvas');
          const ctx = canvas.getContext('2d');
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          ctx.drawImage(video, 0, 0);

          // Convert it to JPEG and send it to the WebSocket
          canvas.toBlob((blob) => socket.send(blob), 'image/jpeg');
        }, IMAGE_INTERVAL_MS);
      });
    });
  });

  // Listen for messages
  socket.addEventListener('message', function (event) {
    drawFaceRectangles(video, canvas, JSON.parse(event.data));
  });

  // Stop the interval and video reading on close
  socket.addEventListener('close', function () {
    window.clearInterval(intervalId);
    video.pause();
  });

  return socket;
};

window.addEventListener('DOMContentLoaded', (event) => {
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  const cameraSelect = document.getElementById('camera-select');
  let socket;

  // List available cameras and fill select
  navigator.mediaDevices.enumerateDevices().then((devices) => {
    for (const device of devices) {
      if (device.kind === 'videoinput' && device.deviceId) {
        const deviceOption = document.createElement('option');
        deviceOption.value = device.deviceId;
        deviceOption.innerText = device.label;
        cameraSelect.appendChild(deviceOption);
      }
    }
  });

  // Start face detection on the selected camera on submit
  document.getElementById('form-connect').addEventListener('submit', (event) => {
    event.preventDefault();

    // Close previous socket is there is one
    if (socket) {
      socket.close();
    }

    const deviceId = cameraSelect.selectedOptions[0].value;
    socket = startFaceDetection(video, canvas, deviceId);
  });

});