/* homepage.html */
// Recorder
const startButton = document.querySelector('#start');
const stopButton = document.querySelector('#stop');
const displayBlink = document.querySelector('#blink');
const displayTimer = document.querySelector('#timer');
const displayHours = document.querySelector('#hours'); 
const displayMinutes = document.querySelector('#minutes'); 
const displaySeconds = document.querySelector('#seconds');
const displayToast = document.querySelector('#toast');

const width = displayBlink.width = window.innerWidth;
const height = displayBlink.height = window.innerHeight;
const ctx = displayBlink.getContext('2d');

function blinking_circle()
{
 displayBlink.style.visibility !== 'hidden' ? displayBlink.style.visibility = 'hidden' : displayBlink.style.visibility = 'visible';
}

let timer , timerBlink , timerStop;
let secondsCount = 0;

function timer_count() 
{
 let hours = Math.floor(secondsCount/3600);
 let minutes = Math.floor((secondsCount % 3600)/60);
 let seconds = Math.floor(secondsCount % 60)
 displayHours.textContent = (hours < 10) ? '0' + hours : hours;
 displayMinutes.textContent = (minutes < 10) ? '0' + minutes : minutes;
 displaySeconds.textContent = (seconds < 10) ? '0' + seconds : seconds;
 secondsCount++;
}

function blinking_timer()
{
 displayTimer.style.visibility !== 'hidden' ? displayTimer.style.visibility = 'hidden' : displayTimer.style.visibility = 'visible';
}

let timeStamp;

function time_stamp()
{
 let today = new Date();
 let date = today.getFullYear()+("0"+(today.getMonth()+1)).slice(-2)+("0"+today.getDate()).slice(-2);
 let time = ("0"+today.getHours()).slice(-2)+""+("0"+today.getMinutes()).slice(-2)+""+("0"+today.getSeconds()).slice(-2);
 let dateTime = date+"_"+time;
 return dateTime;
}

function getCookie(name) 
{
 let cookieValue = null;
 if (document.cookie && document.cookie !== '') 
 {
  let cookies = document.cookie.split(';');
  for (var i = 0; i < cookies.length; i++) 
  {
   let cookie = cookies[i].trim();
   // Does this cookie string begin with the name we want?
   if (cookie.substring(0, name.length + 1) === (name + '=')) 
   {
    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
    break;
   }
  }
 }
 return cookieValue;
}

let csrftoken, request, blinking, recordingName;

function recorder() 
{
 startButton.addEventListener('click', function() 
 {
  navigator.mediaDevices.getUserMedia({ audio: true, video: false }).then(function(stream)
  {
   const options = {mimeType: 'audio/webm;codecs:opus'};
   const mediaRecorder = new MediaRecorder(stream, options);
   const audioChunks = [];
   mediaRecorder.addEventListener("dataavailable", function(event)
   {
    audioChunks.push(event.data);
   });
   mediaRecorder.start();
   blinking = setInterval(blinking_circle, 500);
   timer = setInterval(timer_count, 1000);
   startButton.disabled = true;
   displayToast.textContent = "Recording has been started";
   displayToast.className = "show";
   setTimeout(function() { displayToast.className = displayToast.className.replace("show", ""); }, 1000);
   if(mediaRecorder.state === 'recording')
   {
    stopButton.addEventListener('click', function()
    {
     mediaRecorder.stop();
     timeStamp = time_stamp();
     recordingName = "Audio_"+timeStamp+".webm";
     stream.getTracks().forEach(function(track)
     {
      track.stop();
     });
     if(startButton.disabled === true)
     {
      clearInterval(blinking);
      displayBlink.style.visibility = 'visible';
      clearInterval(timer);
      timerBlink = setInterval(blinking_timer, 500);
      startButton.disabled = false;
      secondsCount = 0;
      stopButton.disabled = true;
      timerStop = setTimeout(function()
      {
       clearInterval(timerBlink);
       displayTimer.style.visibility = 'visible';
       timer_count();
       stopButton.disabled = false;
      }, 3500);
     }
     mediaRecorder.addEventListener('stop', function()
     {
      const recordingAudio = new Blob(audioChunks);
      let formData = new FormData();
      formData.append('audio_recording', recordingAudio, recordingName);
      let request = new XMLHttpRequest();
      csrftoken = getCookie('csrftoken');
      request.open('POST', 'saveRecording', true);
      request.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
      request.setRequestHeader('X-CSRFToken', csrftoken);
      request.onload = function(e) 
      {
       if (this.readyState === 4) 
       {
        displayToast.textContent = e.target.responseText;
        displayToast.className = "show";
        setTimeout(function() { displayToast.className = displayToast.className.replace("show", ""); }, 3000);
       }
      };
      request.send(formData);
     });
    });
   }
  });
 });
}

recorder();

// Audio to Text
const convertButton = document.querySelector('#convert');
const recordingText = document.querySelector('#text');
const loadingCircle1 = document.querySelector('#loader1');

convertButton.addEventListener('click', function()
{
 loader1.style.visibility = 'visible'; 
 let request = new XMLHttpRequest();
 request.open('POST', 'speechToText', true);
 request.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
 request.onload = function(e) 
 {
  if (this.readyState === 4) 
  {
   recordingText.textContent = e.target.responseText
   loader1.style.visibility = '';
  }
 };
 request.send(recordingName);
});


// Find emotion(s)
const findButton = document.querySelector('#find');
const emotions = document.querySelector('#emotions');
const loadingCircle2 = document.querySelector('#loader2');

findButton.addEventListener('click', function()
{
 loader2.style.visibility = 'visible'; 
 let request = new XMLHttpRequest();
 request.open('POST', 'findEmotions', true);
 request.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
 request.onload = function(e) 
 {
  if (this.readyState === 4) 
  {
   emotions.textContent = e.target.responseText
   loader2.style.visibility = '';
  }
 };
 request.send(recordingName);
});