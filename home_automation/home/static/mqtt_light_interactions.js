const light_button = document.getElementById("lightButton");
const color_input = document.getElementById("rgbColorInput");
const brightness_input = document.getElementById("brightnessInput");
const alarm_button = document.getElementById("alarmButton");
const alarm_time_input = document.getElementById("alarmTimeInput");
const socket = io();
var button_on = false;

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}
  
function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

$(document).ready(function() {
    console.log("trying to emit");
    socket.emit("connection", "high there!");
    socket.on(
        "connection", function(msg) {
            console.log("connection confirmed");
            console.log(msg);
        }
    );
    socket.on(
        "bedroom_light_message", function(msg) {
            console.log("Received light message: ", msg);
            var parsed_message = JSON.parse(msg);
            var state = parsed_message["on_status"];
            var rgb_hex = rgbToHex(parsed_message["red"], parsed_message["green"], parsed_message["blue"]);
            var brightness_value = parsed_message["white"]
            color_input.value = rgb_hex;
            brightness_input.value = brightness_value;
            light_button.innerHTML = "Lights: " + state[0].toUpperCase() + state.substring(1);
        }
    );
    socket.on(
        "alarm_message", function(msg) {
            console.log("Received alarm message: ", msg);
            var parsed_message = JSON.parse(msg);
            var state = parsed_message["alarm_status"];
            var time = parsed_message["alarm_time"];
            alarm_time_input.value = time;
            alarm_button.innerHTML = "Alarm: " + state[0].toUpperCase() + state.substring(1);
        }
    );
});

function bedroomLightsInput(store=false) {
    var rgb_vals = hexToRgb(color_input.value);
    var brightness_value = brightness_input.value;
    var state = light_button.innerHTML.split(" ").pop().toLowerCase();
    var message = JSON.stringify(
        {
            "red" : rgb_vals.r,
            "green" : rgb_vals.g,
            "blue": rgb_vals.b,
            "white": brightness_value,
            "on_status": state,
            "store": store
        }
    );
    console.log("Emitting message: ", message);
    socket.emit("bedroom_light_message", message);
}

function bedroomLightsChange() {
    console.log("This was a change and should be stored")
    bedroomLightsInput(store=true);
}

function lightButtonClick() {
    var state = light_button.innerHTML.split(" ").pop();
    if (state == "On") {
        light_button.innerHTML = "Lights: Off";
    } else {
        light_button.innerHTML = "Lights: On";
    }
    bedroomLightsChange();
}

function alarmTimeChange() {
    var time = alarm_time_input.value;
    var state = alarm_button.innerHTML.split(" ").pop().toLowerCase();
    var message = JSON.stringify(
        {
            "alarm_time": time,
            "alarm_status": state
        }
    );
    console.log("Emitting message: ", message);
    socket.emit("alarm_message", message);
}

function alarmButtonClick() {
    var state = alarm_button.innerHTML.split(" ").pop();
    if (state == "On") {
        alarm_button.innerHTML = "Lights: Off";
    } else {
        alarm_button.innerHTML = "Lights: On";
    }
    alarmTimeChange();
}
