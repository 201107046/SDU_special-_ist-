

function getDataAsJson(){ 
	var data_cousine = document.getElementById("data_cousine").value // getting data from DOM element
	var data_options = document.getElementById("data_options").value
	var data_price = document.getElementById("data_price").value
	
	eel.getDataFromPy(data_cousine,data_options,data_price)(function(ret){ // calling getDataFromPy() from back, and expecting response 
		console.log('this is ret',ret)
		tableFromJson(ret) // calling tableFromJson() fucntion
	})
}

function tableFromJson(data_json) {	// forming table and adding data to it 

	console.log(data_json);

	var col = [];
	for (var i = 0; i < data_json.length ; i++) { // deleting unnecessary data
		delete data_json[i]["cuisine_simmilarity"]; 
		delete data_json[i]["common_extra_types"];
		delete data_json[i]["extra_simmilarity"];
		delete data_json[i]['common_cuisine_types'];
		delete data_json[i]['euclidian_distance'];
		delete data_json[i]['price_class'];
		delete data_json[i]['Reservation'];
		delete data_json[i]['Number of reviews'];
		for (var key in data_json[i]) {
			if (col.indexOf(key) === -1) {
				col.push(key);
			}
		}
	
	}

	// Create a table.
	var table = document.createElement("table");

	// Creating table header row using the extracted headers above.
	var tr = table.insertRow(-1);                   // table row.

	for (var i = 0; i < col.length; i++) {
		var th = document.createElement("th");      // table header.
		th.innerHTML = col[i];
		tr.appendChild(th);
	}

	// adding json data to the table as rows.
	for (var i = 0; i < data_json.length; i++) {

		tr = table.insertRow(-1);

		for (var j = 0; j < col.length; j++) {
			var tabCell = tr.insertCell(-1);
			tabCell.innerHTML = data_json[i][col[j]];
		}
	}

	// Adding the newly created table with json data, to a container.
	var divShowData = document.getElementById('showData');
	divShowData.innerHTML = "";
	divShowData.appendChild(table);
	
}

