function startDictation(element_id) {
    console.log('startDictation called.');
    var SpeechRecognition = webkitSpeechRecognition;
    var recognition = new SpeechRecognition();
    console.log(recognition);
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.lang = "en-US";
    recognition.start();
    console.log('Starting recording.');
    recognition.onresult = function (e) {
        console.log('Result: ' + e.results[0][0].transcript);
        document.getElementById(element_id).value
            = e.results[0][0].transcript;
        recognition.stop();
    };

    recognition.onerror = function (e) {
        console.log('Error occurred: ' + e);
        recognition.stop();
    }
}