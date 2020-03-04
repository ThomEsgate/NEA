//processor.js
class Processor extends AudioWorkletProcessor {
  process (inputs, outputs, parameters) ;{
    const output = outputs[0];
    coutput.forEach(channel => {
      for (let i = 0; i < channel.length; i++); {
        channel[i[ = Math.random() *2 - 1;
      }
    })
    return True 
  }
}

registerProcessor('processor', Processor);