//function to pause the program for n milliseconds
function sleep(milliseconds) {
	let startTime = new Date().getTime();
	while (true)   {
		let timePassed = new Date().getTime() - startTime
		if (timePassed > milliseconds)
		break;
	}
}

function metronomeCountIn(bpm, timeBetweenSamples) {
	console.log("start");
	
	/*
	counter = 0;
	function funcName(){
		alert("Hello");
		counter++;
		if (counter == 3) {
			clearInterval(run); //stop executing
		}
	}
	
	var func = funcName;
	var run = setInterval(func, 1000);
	
	*/
	
	beat = document.getElementById("beatAudio");
	samples_per_beat = (1000/timeBetweenSamples)*(120/bpm)
	i = 0;
	console.log("here");
	var interval = setTimeout( beatIt(), 250 /*samples_per_beat * timeBetweenSamples*/ );
	function beatIt() {console.log(i + " and a");
		beat.play;
		console.log("inside");
		sleep(samples_per_beat * timeBetweenSamples);
		beat.pause();
		beat.currentTime = 0;
		++i;
		if (i > 4) {clearInterval(interval);}	
		}	
	
	console.log("there");	
}

function getNote(bufferLength, analyser, context, notesArray, timeBetweenSamples, sampleNo) {
		
	switch(songID) {
			case 01:
		 //Astral Alley - 4/4 time sig., 100bpm, in A Minor
			var songArray = [["Astral Alley", 100], ["C", 1], ["A", 6], ["C", 0.5], ["D", 0.5], //bar 1-2 //["C", 1] = Play C note for 1/8th of a 2 bar phrase 1/8 = Crotchet, 0.5/8 = Quaver
												    ["C", 1], ["A", 6], ["C", 0.5], ["D", 0.5], //bar 3-4
													["E", 2], ["D", 2], ["A", 3], ["C", 0.5], ["D", 0.5], //...
													["C", 1], ["A", 6]];
			var bpm = 110;
			break;
			case 02:
			var songArray =[["Lost Woods", "130"],  ["F", 0.5], ["A", 0.5], ["B", 1], ["F", 0.5], ["A", 0.5], ["B", 1], 
													["F", 0.5], ["A", 0.5], ["B", 0.5], ["E", 0.5], ["D", 1], ["B", 0.5], ["C", 0.5],
													["B", 0.5], ["G", 0.5], ["E", 2.5], ["D", 0.5],											
													["E", 0.5], ["G", 0.5], ["E", 3]];
			var bpm = 130;
			break;
		}
		
		var recording = true;

		
		var silenceTime = 1;
		var currentNote = 1;
		var noteSampleNo = 1;
		var noteSampleIncorrect = 0		
		
		while (recording) {
			//create a new array and use the analyser to fill it with byte frequency data   // start and stop buttoons
			var dataArray = new Uint8Array(bufferLength);
			// array to store Frequency values	
			analyser.getByteFrequencyData(dataArray);
			
			var i = 0;	//goes through entire dataArray of dB values and finds the loudest one (the actual frequency being played, ignoring background noise)
			var highestdB = 0;
			var highesti = 0;
			while(i < analyser.frequencyBinCount) {
				//console.log((dataArray[i])); //display all values in array for debugging
				++i;
				if (highestdB < dataArray[i]) {
					highestdB = dataArray[i];
					highesti = i;
				}
			}
			
			//find frequency by finding the loudest played frequency
			var freq = (context.sampleRate / analyser.fftSize) * highesti
			
			//convert frequency to a note on a keyboard
			var notePosOnKeyboard = Math.round(12 * (Math.log(freq / 440)/Math.log(2)) + 69); //A is 69th key on a keyboard
			var note = notesArray[notePosOnKeyboard % 12]; // % is modulus
			var octaveNo = Math.floor(notePosOnKeyboard / 12);
			
		//PLAYING ALONG* - Astral Alley: 100 bpm - 1 sample per 50 milliseconds = 20 samples/second = 24 samples per beat
		
			++sampleNo; // a sample has been taken
			var samples_per_beat = 0.5 * (1000/timeBetweenSamples)*(120/bpm);
			var beatNo = Math.floor(sampleNo/samples_per_beat) + 1;
			
			var dummyVar;
			if ((songID == 01) || (songID == 02)) {var playingSong = true};
			//console.log(dummyVar = ((songID == 01) || (songID == 02)) ? "Playing a song " + songID:"No Song");
			
			if (playingSong) {
				if (sampleNo == 1) { console.log(songArray[0][0]); //song name
									console.log(songArray[0][1]); //bpm
									metronomeCountIn(bpm, timeBetweenSamples);}
								
				//SEEING IF THE NOTE FITS THE SONG
				samples_for_note = (samples_per_beat * songArray[currentNote][1]); //e.g. total samples for a 0.5 beat note is samples per beat
				if (noteSampleNo < samples_for_note) { //if still sampling one beat
					++noteSampleNo
					if (note !== songArray[currentNote][0]){ //wrong note
						++noteSampleIncorrect;
					} 
				}
				
				else { //finished sampling beat
					if ((noteSampleIncorrect/noteSampleNo) > 0.25) {// if more than 25% incorrect, keep waiting for user to play correct note
						console.log("Wrong! Play a " + songArray[currentNote][0])
					}
					else { //correct note
						console.log(songArray[currentNote][0] + " done! Now play " + songArray[currentNote + 1][0]);
						++currentNote; //next note in songArray	
					}
					if (songArray.length <= currentNote + 1) { //if reached the end of the song
						console.log("End of song reached");
						recording = false;
						break; 
					}
				
					noteSampleNo = 0;
					noteSampleIncorrect = 0;
				}
					
			}
			//if the microphone hears nothing then
			if (note == undefined) {
				console.log("Undefined note (too quiet?)");
				++silenceTime;}
			else {
				notesource = "../static/images/" + note + ".png";
				showImage(notesource,
						  note +" Image");
				document.getElementById("noteId").value = note;
				
				if (!(playingSong)) {console.log(note.concat(octaveNo))}; //if not playing a song (free mode), show individual notes being played
				silenceTime = 0;}
				
				
		
			document.getElementById("noteId").innerHTML = note; // .innerHTML allows js code to manipulate website being displayed
			sleep (timeBetweenSamples);
			if (silenceTime > 19) {recording = false}; //stops recording after 20 samples of hearing 
			//console.log(silenceTime);
			document.getElementById("buttonStop").onclick = function(){recording = false};
		}	

		return sampleNo;
}

function showImage(src1, alt1) {
	var myimage = new Image(src1, alt1);
	myimage.src = src1;
	myimage.width = 64;
	myimage.height = 64;
	myimage.alt = alt1;
	document.body.appendChild(myimage); //adds image to <body>
}
     
    
function Initialise(songID) {
if (navigator.mediaDevices) {
	
	function noUserMedia(){
		console.warn('getUserMedia is NOT supported :(');
		document.getElementById("noteId").innerHTML = 'GetUserMedia not supported :(';
	}			
	
    //getUserMedia takes 3 arguments
    //1. constraints 
    navigator.getUserMedia ({audio: true}, //only uses audio
     
    //2. successCallback
    function(stream){
		console.log('getUserMedia is supported');
		
		var notesArray = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
		
		var context = new AudioContext(); // controls creation of audio nodes and contains execution of audio processing
		var source = context.createMediaStreamSource(stream); // sets source of data to be input from microphone
		var analyser = context.createAnalyser(); //analyser can be used to find the frequency of a buffer
		var track = stream.getTracks()[0]; //gets the single audio track as a variable to stop recording
		
		analyser.minDecibels = -60;
		//analyser.maxDecibels = -10;
		//analyser.smoothingTimeConstant = 0.8;
		context.sampleRate = 48000
      
		source.connect(analyser);
		//source.connect(context.destination);	//allows for playback of microphone data through speakers
      
		analyser.fftSize = 16384 //fast fourier transform size - 16384 is best
      
		var bufferLength = analyser.frequencyBinCount;
		
		//Astral Alley: 100 bpm - 1 sample per 50 milliseconds = 20 samples/second = 24 samples per beat
		var timeBetweenSamples = 50; // in milliseconds
		var sampleNo = 0;
											
		//getNote repeats while recording, and will exit the function when the user wants recording to stop
		getNote(bufferLength, analyser, context, notesArray, timeBetweenSamples, sampleNo);
		
		//setInterval( function() {getNote(bufferLength, analyser, context, notesArray, timeBetweenSamples)}, 250 )	//STREAM ISN'T THERE NOTHING ON PLAYBACK WHY DOESN'T THIS WORK :(
		track.stop(); //stops recording																							
	
    },//3. errorCallback - 
    
    function(err){noUserMedia()});
	return
  };//end of getting user media
  
  console.log("navigator.mediaDevices error");
};//initialise end

function checkType(input){
	if(typeof input !== "undefined") {
		console.log("SongId = "+ input);
		clearInterval(run_checkType); //stop executing
		return;
	}
	else {console.log("undefined songId");}
}
//var run_checkType = setInterval(checkType, 1000);

notesource = "../static/images/quarter.png";
var run_showImage = setInterval(showImage(notesource, notesource), 500);


/*var counter = 0;
function sayHello(){
	alert("Hello");
	counter++;
	if (counter == 2) {
		clearInterval(run_sayHello); //stop executing
	}
}
var run_sayHello = setInterval(sayHello, 750); */
	

//onmouseup ="getNote()"
//type = "audio/mpeg"
