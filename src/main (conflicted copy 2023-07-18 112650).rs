use std::io::Write;
use std::{fs::File, path::Path};
use vosk::{Model, Recognizer};
use fon::{stereo::Stereo32, Sink, Audio};
use pasts::{exec, wait};
use wavy::{Speakers, Microphone, SpeakersSink, MicrophoneStream};

mod audio;

const TEST_PATH: &str = "depend/audio/turn_on_command_test.wav";
const TURN_ON_PATH: &str = "depend/audio/turn_on_command_test.wav";
const DAD_VOICE: &str = "depend/audio/dad_voice_sample.wav";

/// An event handled by the event loop.
enum Event<'a> {
    /// Speaker is ready to play more audio.
    Play(SpeakersSink<'a, Stereo32>),
    /// Microphone has recorded some audio.
    Record(MicrophoneStream<'a, Stereo32>),
}

/// Shared state between tasks on the thread.
struct State {
    /// Temporary buffer for holding real-time audio samples.
    buffer: Audio<Stereo32>,
}

impl State {
    /// Event loop.  Return false to stop program.
    fn event(&mut self, event: Event<'_>) {
        match event {
            Event::Play(mut speakers) => speakers.stream(self.buffer.drain()),
            Event::Record(microphone) => self.buffer.extend(microphone),
        }
    }
}

fn main() {
    println!("Starting Clank's auditory processing unit...");
    // we will need the following process to run in a loop
    // to be able to detect if someone wishes to give a command

    // 01. --- Recording the sound and putting it in a .wav file of the needed format --- //
    // https://docs.rs/wavy/latest/wavy/index.html
    /*
    out:
        a .wav file in PCM 16khz 16bit mono format
    */
    // .01 === Getting noise data into the needed format === //
    /*
        in:
            a .wav file in PCM 16khz 16bit mono format
        out:
            &Vec<i16> of the data
    */
    let mut state = State { buffer: Audio::with_silence(48_000, 0) };
    let mut speakers = Speakers::default();
    let mut microphone = Microphone::default();

    exec!(state.event(wait! {
        Event::Record(microphone.record().await),
        Event::Play(speakers.play().await),
    }));

    // open audio file
    let mut inp_file = File::open(Path::new(&DAD_VOICE)).unwrap();
    // pull out data
    let (_header, data) = wav::read(&mut inp_file).unwrap();
    // pull the samples out in the format we need them
    let samples = data.as_sixteen().unwrap();

    // .02 === Getting the vosk model setup, so we can give it our noise data, and figure out what words were said === //
    /*
        in:
            noise data
        out:
            the words that were said
    */
    let model_path = String::from("depend/vosk-model-small-en-us-0.15");
    let sample_rate = 16000.0;
    let enable_words = true;
    let enable_partial_words = true;
    let max_alternatives = 10;
    // let folder = fs::read_dir(&model_path).unwrap(); // Some debug code to make sure I had the file path correct...
    // Might need to actually do my own check here since the vosk model does not give a good error if it simply cannot
    // find the folder...
    let model = Model::new(&model_path).unwrap();
    println!("The model didn't error! Can we print it? No...");
    let mut recognizer = Recognizer::new(&model, sample_rate).unwrap();

    recognizer.set_max_alternatives(max_alternatives);
    recognizer.set_words(enable_words);
    recognizer.set_partial_words(enable_partial_words);

    for sample in samples.chunks(100) {
        recognizer.accept_waveform(sample);
        // println!("{:#?}", recognizer.partial_result());
    }
    // println!("{:#?}", recognizer.final_result().multiple().unwrap());

    let final_result = recognizer.final_result().multiple().unwrap();
    println!("What was said?\n{}", final_result.alternatives[0].text);

    // .03 === Checking what was said and determining what should be done === //
    /*
    in:
        the string of words said
     */
    // actions, like 'turn on', can be applied to objects, like 'living room light 01' (most likely webthings)
    //
    // manufacturers should be able to specify their own action words/phrases for their device,
    // but end users should also be able to change it if they want.
    if final_result.alternatives[0].text.contains("turn on") {
        println!("The action 'turn on' has been recieved!");
    }
}
