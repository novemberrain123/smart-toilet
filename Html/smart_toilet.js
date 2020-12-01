
$(document).ready(function () {
    $(document).on("click", "#stats", function () {
    // hide main and results pages + hide input form
    $("#image").hide();
    // display the charts
    $("#chartContainer").attr("style", "display:block");
  });
});

var config = {
  apiKey: "AIzaSyAH0JTJqYZaKiO-GssnbO9lIW_Z9-HMu0c",
  authDomain: "smart-toilet-adc07.firebaseapp.com",
  databaseURL: "https://smart-toilet-adc07.firebaseio.com",
  projectId: "smart-toilet-adc07",
  storageBucket: "smart-toilet-adc07.appspot.com",
  messagingSenderId: "957295405488",
  // appId: "1:957295405488:web:e1ef9592e182de5c670e75",
  // measurementId: "G-H534KJ3HY5"
};
firebase.initializeApp(config);

document.getElementById("stats").onclick = function() {

var dps = []; // dataPoints
var chart = new CanvasJS.Chart("chartContainer", {
title :{
  text: "Ultrasonic sensor value"
},
data: [{
  type: "line",
  dataPoints: dps
}]
});

var xVal = 0;
var yVal = 0;
var updateInterval = 1000;
var dataLength = 20; // number of dataPoints visible at any point
var path;
var nextPath;
var key;

var updateChart = function (count) {

count = count || 1;

for (var j = 0; j < count; j++) {
  

  var query = firebase.database().ref("users/00").orderByKey();
  query.once("value").then(function(snapshot) {
  for (var x in snapshot.val())
    {
      key = x;
    }
  path = parseInt(key);
  
  if(path>=1000)
  {
    nextPath=toString(path);
  }
  else if(path>=100)
  {
    nextPath="0"+path.toString();
  }
  else if(path>=10)
  {
    nextPath="00"+path.toString();
  }
  else
  {
    nextPath="000"+path.toString();
  }
  
  firebase.database().ref('users/00/'+nextPath).on('value',function(valSnapshot){
          yVal= valSnapshot.val().a;
        
      });
    
});


  
  dps.push({

    x: xVal,
    y: yVal
  });

  xVal+=1;
  
  
}

if (dps.length > dataLength) {
  dps.shift();
}

chart.render();
};

updateChart(dataLength);
setInterval(function(){updateChart()}, updateInterval);

}

