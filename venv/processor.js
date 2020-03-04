//processor.js
class TestProcessor extends AudioWorkletProcessor {
  constructor () {
    super()
    // current sample-frame and time at the moment of instantiation
    // to see values change, you can put these two lines in process method
    console.log(currentFrame)
    console.log(currentTime)
  }
  // the process method is required - simply output silence
  process (inputs, outputs, parameters) {
    return true
  }
}

// the sample rate is not going to change ever,
// because it's a read-only property of a BaseAudioContext
// and is set only during its instantiation
console.log(sampleRate)

// you can declare any variables and use them in you processors
// for example it may be an ArrayBuffer with a wavetable
const usefulVariable = 42
console.log(usefulVariable)

registerProcessor('test-processor', TestProcessor)