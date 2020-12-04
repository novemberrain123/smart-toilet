$(document).ready(function () {
  $(document).on("click", "#ult1", function () {
    // hide main and results pages + hide input form
    $("#image").hide();
    // display the charts
    $("#chartContainer").attr("style", "display:block");

  });
});

$(document).ready(function () {
  $(document).on("click", "#ult2", function () {
    // hide main and results pages + hide input form
    $("#image").hide();
    // display the charts
    $("#chartContainer").attr("style", "display:block");

  });
});

$(document).ready(function () {
  $(document).on("click", "#light", function () {
    // hide main and results pages + hide input form
    $("#image").hide();
    // display the charts
    $("#chartContainer").attr("style", "display:block");

  });
});

$(document).ready(function () {
  $(document).on("click", "#sound", function () {
    // hide main and results pages + hide input form
    $("#image").hide();
    // display the charts
    $("#chartContainer").attr("style", "display:block");
    

  });
});

$(document).ready(function () {
  $(document).on("click", "#retrieve", function () {
    // hide main and results pages + hide input form
    $("#image").hide();
    $("#chartContainer").hide();
    // display the charts
    $("#picture").attr("style", "display:block");
    $("#picture").css("margin-top","-370px");
  });
});

$(document).ready(function () {
  $(document).on("click", "#home", function () {
    // hide main and results pages + hide input form
    $("#picture").hide();
    $("#chartContainer").hide();
    // display the charts
    // $("#graph").attr("style", "display:inline");
    $("#image").attr("style", "display:block");
    $("#image").attr("border","11","solid");
    $("#image").css("margin-left","-100px");

  });
});

function eraseText() {
  document.getElementById("console").value = "";
}

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

// capture image
document.getElementById("retrieve").onclick = function () {
  var picName; 
  firebase
    .database()
    .ref("main/LatestPic") 
    .on("value", function (valSnapshot) {
      picName = valSnapshot.val();
      firebase
        .storage()
        .ref("main/" + picName)
        .getDownloadURL()
        .then(function (url) {
          var img = document.getElementById("img");
          img.src = url;
        })
        .catch(function (error) {
          console.log("Error occurred");
        });
    });

  firebase
    .storage()
    .ref("main/" + picName)
    .getDownloadURL()
    .then(function (url) {
      var img = document.getElementById("img");
      img.src = url;
    })
    .catch(function (error) {
      console.log("Error occurred");
    });
};


// //Display graphs
document.getElementById("ult1").onclick = function() 
{graphDisplay("ultra1")};

document.getElementById("ult2").onclick = function() 
{graphDisplay("ultra2")};

document.getElementById("sound").onclick = function() 
{graphDisplay("sound")};

document.getElementById("light").onclick = function() 
{graphDisplay("light")};


function graphDisplay(sensor_type) 
{
  var sensorName=sensor_type.toString();
  var dps = []; // dataPoints
  var chart = new CanvasJS.Chart("chartContainer", {
    title: {
      text: sensorName+" sensor value",
    },
    data: [
      {
        type: "line",
        dataPoints: dps,
      },
    ],
  });

  var xVal = 0;
  var yVal = 0;
  var updateInterval = 1000;
  var dataLength = 20; // number of dataPoints visible at any point
  var path;
  var nextPath;
  var key;

  var updateChart2 = function (count) {
    count = count || 1;

    for (var j = 0; j < count; j++) {
      var sensorName=sensor_type.toString();
      var date = new Date();
      var year = (date.getFullYear()).toString();
      var month = (date.getMonth() + 1).toString();
      var day = (date.getDate()).toString();
      var days;
      if (parseInt(day) < 10) {
        days = ("0" + day).toString();
      } else {
        days = day.toString();
      }
      var set=year.concat(month).concat(days);
      var query = firebase
        .database()
        .ref("main/"+set)
        .orderByKey();
      query.once("value").then(function (snapshot) {
        for (var x in snapshot.val()) {
          key = x;
        }
        path = parseInt(key);

        if (path >= 1000) {
          nextPath = path.toString();
        } else if (path >= 100) {
          nextPath =path.toString();
        } else if (path >= 10) {
          nextPath =path.toString();
        } else {
          nextPath = "0" + path.toString();
        }
      
        firebase
          .database()
          .ref("main/"+set+"/"+nextPath)
          .on("value", function (valSnapshot) {

            if(sensorName=="ultra1")
            {
              yVal = valSnapshot.val().ultra1;
            }
            else if(sensorName=="ultra2")
            {
              yVal = valSnapshot.val().ultra2;
            }
            else if(sensorName=="sound")
            {
              yVal = valSnapshot.val().sound;
            }
            else if(sensorName=="light")
            {
              yVal = valSnapshot.val().led;
            }
            else
            {
              yVal=null;
            }
            
          });
        });
      

      var yValue = parseInt(yVal);

      dps.push({
        x: xVal,
        y: yValue,
      });

      xVal += 1;
    }

    if (dps.length > dataLength) {
      dps.shift();
    }

    chart.render();
  };
  updateChart2(dataLength);
  setInterval(function () {
    updateChart2();
  }, updateInterval);
};

var consoleText = ""
//For console output 
firebase.database().ref("main/console").on("value", function(valSnapshot){
    consoleText = consoleText.concat(valSnapshot.val(),"\n")
    document.getElementById("console").value = consoleText;
});