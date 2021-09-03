//directory selection
//document.getElementById("folder").addEventListener("change", function(event) {
//  var output = document.querySelector("ul");
//  var files = event.target.files;
//
//  for (var i=0; i<files.length; i++) {
//    var item = document.createElement("li");
//    item.innerHTML = files[i].webkitRelativePath;
//    output.appendChild(item);
//  };
//}, false);


//Get data button
$(document).ready(function() {
    $(document.getElementById("getData")).click(function(){
        clr_table()
        var measurePoint = document.getElementById("measurePoint").value
        var currentType = document.getElementById("currentType").value
        measureSocket.send(JSON.stringify({"command": "start_measures", "current_type": currentType, "measure_point": measurePoint}))
    });
});

// submit customer button click
$(document).ready(function() {
    $(document.getElementById("submitCustomer")).click(function(){
        var customerName = document.getElementById("customerName").value
        var deviceType = document.getElementById("deviceType").value
        var deviceNumber = document.getElementById("deviceNumber").value
        measureSocket.send(JSON.stringify({"command": "save_customer", "customer_name": customerName, "device_type": deviceType, "device_number": deviceNumber}))
    });
});

// save data button
$(document).ready(function() {
    $(document.getElementById("saveData")).click(function(){
        measureSocket.send(JSON.stringify({"command": "save_data"}))
    });
});


// generate report
$(document).ready(function() {
    $(document.getElementById("saveOnServer")).click(function(){
        measureSocket.send(JSON.stringify({"command": "generate_report"}))
    });
});

//new device
$(document).ready(function() {
    $(document.getElementById("newDevice")).click(function(){
        clr_table()
        document.getElementById("customerName").value = ""
        document.getElementById("deviceType").value = ""
        document.getElementById("deviceNumber").value = ""
        document.getElementById("measurePoint").value = ""

        measureSocket.send(JSON.stringify({"command": "new_device"}))
    });
});


//clear table button
$(document).ready(function() {
    $(document.getElementById("clearTable")).click(function(){
        clr_table();
    });
});


// socket activation
var measureSocket = new WebSocket('ws://' + window.location.host + "/")
measureSocket.onmessage = function (event) {
    console.log(event.data);
    var table = document.getElementById("data");

    var data = JSON.parse(event.data)

    var curr_row = table.insertRow(-1);

    var cell0 = curr_row.insertCell(0);
    cell0.innerText = data["ACV"];

    var cell1 = curr_row.insertCell(1);
    cell1.innerText = data["FR"];

    var cell2 = curr_row.insertCell(2);
    cell2.innerText = data["DCV"];

    var cell3 = curr_row.insertCell(3);
    cell3.innerText = data["PKPK"];

    var cell4 = curr_row.insertCell(4);
    cell4.innerText = data["CF"];
}

function clr_table() {
        var table = document.getElementById("data");
        var t_size = table.rows.length - 1
        for (i=t_size; i>0; i--) {
            table.deleteRow(i)
        }
        measureSocket.send(JSON.stringify({"command": "clear_table"}))
}

