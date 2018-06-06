function loadModel(params){
	cont =0;    
	insertLayer("capaEntrada", 5, null, cont++);
	insertLayer("capaOculta", 3, null, cont++);
	insertLayer("capaOculta", 4, null, cont++);
	insertLayer("capaSalida", 3, null, cont++);
      
	return false;
}

function insertLayer(type, neurons, activation, cont){
	var divOriginal = document.getElementById(type);
	var clone = divOriginal.cloneNode(true);

	clone.id = type + String(cont);

	clone.children[0].value = neurons;

	if(activation!=null){
		alert("Tiene activacion")
	}

	/*Ajustes esteticos*/
	switch(type){
		case "capaEntrada":
			clone.children[0].style.left = 255+'px';/*Ajuste para que la caja de num neurones aparezca centrada a pesar del resize*/
		break;

		case "capaOculta":
			clone.children[0].style.left = 130+'px';/*Ajuste para que la caja de num neurones aparezca centrada a pesar del resize*/
            /*Overlap de capas para que si ensamblen*/
            if(document.getElementById('bottom').lastChild.className=='capaEntrada')
                clone.style.marginTop = -34 +'px';
            else
                clone.style.marginTop = -64 +'px';
		break;

		case "capaSalida":
			clone.children[0].style.left = 255+'px';/*Ajuste para que la caja de num neurones aparezca centrada a pesar del resize*/
            clone.style.marginTop = -64 +'px';/*Overlap de capas para que si ensamblen*/
		break;
	}

	document.getElementById('bottom').appendChild(clone);
}