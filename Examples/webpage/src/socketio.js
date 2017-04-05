/**
 * Created by Tyler Narmore on 4/4/2017.
 */
$(document).ready(function() {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on("sensor added", function(sensor) {
       console.log("Sensor added " + sensor);
    });

    socket.on("update relationship", function(data){
       console.log("Updataing relationship \n" +
                    "Sensor_x: "+ data.sensor_x +"\n" +
                    "Sensor_y: "+ data.sensor_y +"\n" +
                    "Value: " + data.value);
    });
});