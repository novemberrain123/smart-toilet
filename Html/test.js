
$(document).ready(function () {
    $(document).on("click", "#stats", function () {
    // hide main and results pages + hide input form
    $("#image").hide();
    // display the charts
    $("#user-stats").attr("style", "display:block");
  });
});

var config = {
      apiKey: "AIzaSyAH0JTJqYZaKiO-GssnbO9lIW_Z9-HMu0c",
      authDomain: "smart-toilet-adc07.firebaseapp.com",
      databaseURL: "https://smart-toilet-adc07.firebaseio.com",
      projectId: "smart-toilet-adc07",
      storageBucket: "smart-toilet-adc07.appspot.com",
      messagingSenderId: "957295405488",
      appId: "1:957295405488:web:e1ef9592e182de5c670e75",
      measurementId: "G-H534KJ3HY5"
};
firebase.initializeApp(config);