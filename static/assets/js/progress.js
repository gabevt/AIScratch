function updateProgress(error, accuracy){
	var accuracyBar = document.getElementById('progressAccuracy');
	var errorBar = document.getElementById('progressError');

	if(accuracy>100){
		accuracyBar.style.height = 100+'%';
	}else{
		accuracyBar.style.height = accuracy+'%';
	}

	if(error>100){
		errorBar.style.height = 100+'%';	
	}else{
		errorBar.style.height = error+'%';
	}

	return false;
}