function test(){

	var fso = new ActiveXObject("Scripting.FileSystemObject");
	fileExist = fso.FileExists(cmdline);

	if (!fileExist) {
    	alert("The requested application is not installed.");
  	}else {
	
		var shell = new ActiveXObject( "WScript.Shell" )

		shell.Run('"' + "C:\\Windows\\System32\\notepad.exe" + '"');


		alert("hello");
	}
	

	return false;
}