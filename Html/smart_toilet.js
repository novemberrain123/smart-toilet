import firebase from 'firebase';

document.getElementById("myBtn").addEventListener("click", display);

(function display(){
    // Initialize Firebase
    var config = {
    apiKey: "AIzaSyAH0JTJqYZaKiO-GssnbO9lIW_Z9-HMu0c",
    authDomain: "smart-toilet-adc07.firebaseapp.com",
    databaseURL: "https://smart-toilet-adc07.firebaseio.com/",
    storageBucket: "smart-toilet-adc07.appspot.com",
    projectId: "smart-toilet-adc07",
    };

    firebase.initializeApp(config);
    
    var userDataRef = firebase.database().ref("users").ref("00").oderByKey().userDataRef.once("value").then(function(snapshot) {
        snapshot.forEach(function(childSnapshot) {
          var key = childSnapshot.key;
          var childData = childSnapshot.val();              // childData will be the actual contents of the child
    
          var name_val = childSnapshot.val().a;          
          $("#NAME").append(name_val);
          document.write(name_val);

      });
     });
    }());

