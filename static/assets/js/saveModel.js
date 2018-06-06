function saveModel(){
	var drawArea = document.getElementById('bottom');
	var nodes = drawArea.childNodes;
	var sendString = new Array();

	for(var i=0;i<nodes.length;i++){
		//Capa entrada
		if(i==0){
			sendString.push(nodes[i].children[0].value);
			continue;
		}

		//Capa salida
		if(i==nodes.length-1){
			sendString.push(nodes[i].children[0].value);
			break;
		}

		//Capa oculta n
		sendString.push(nodes[i].children[0].value + ':' + nodes[i].children[1].className)		
	}

	for(var i=0; i<sendString.length;i++){
		alert(sendString[i]);
	}

	return false;
}

/*
function saveModel(){
	alert("Hello");
	var MongoClient = require('mongodb').MongoClient;
	var url = "mongodb+srv://Usuario:12345@clusteria-higk8.mongodb.net/";

	MongoClient.connect(url, function(err, db) {
	  if (err) throw err;
	  var dbo = db.db("AISCRATCH");
	  var myobj = { NAME_MODEL: "TEST1", CONFIG_MODEL:["2","5:sigmoid","1"] };
	  dbo.collection("MODELS").insertOne(myobj, function(err, res) {
	    if (err) throw err;
	    alert("Insert completed");
	    db.close();
	  });
	});

}*/
