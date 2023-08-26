use cpal::{
    traits::{DeviceTrait, HostTrait, StreamTrait},
    Sample, SampleFormat,
};
use std::env;
use std::io::Write;
use std::{fmt::Display, fs::File, path::Path};
use vosk::{Model, Recognizer};

const TEST_PATH: &str = "depend/audio/turn_on_command_test.wav";
const TURN_ON_PATH: &str = "depend/audio/turn_on_command_test.wav";
const DAD_VOICE: &str = "depend/audio/dad_voice_sample.wav";

fn main() {
    println!("Starting Clank's auditory processing unit...");
    // we will need the following process to run in a loop
    // to be able to detect if someone wishes to give a command

    // 01. --- Recording the sound and putting it in a .wav file of the needed format --- //
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
    let host = cpal::default_host();
    let def_device = host
        .default_input_device()
        .expect("No default device found");
    println!("Default Device:");
    // println!("{:#?}", def_device.name());

    let mut supported_configs_range = def_device
        .supported_input_configs()
        .expect("error while querying configs");
    // below is probably where i need to set the sample rate to 16000 (16khz)
    let supported_config = supported_configs_range
        .next()
        .expect("no supported config?!")
        .with_max_sample_rate();

    let err_fn = |err| eprintln!("an error occurred on the input audio stream: {}", err);
    let sample_format = supported_config.sample_format();
    let config = supported_config.into();
    let stream = match sample_format {
        SampleFormat::F32 => def_device.build_input_stream(&config, write_silence::<f32>, err_fn),
        SampleFormat::I16 => def_device.build_input_stream(&config, write_silence::<i16>, err_fn),
        SampleFormat::U16 => def_device.build_input_stream(&config, write_silence::<u16>, err_fn),
    }
    .unwrap();

    fn write_silence<T: Sample>(data: &[T], _: &cpal::InputCallbackInfo) {
        let path = "temp/foo.wav";

        // println!(
        //     "{}",
        //     env::current_dir()
        //         .expect("poop")
        //         .into_os_string()
        //         .into_string()
        //         .expect("msg")
        // );
        let mut output =
            File::create(path).expect(format!("Trouble creating file: {}", path).as_str());
        for sample in data.iter() {
            // println!("{:#?}", sample.to_i16());
            write!(output, "{}", sample.to_i16()).expect("error writing to file");
        }
    }

    stream.play().unwrap();

    // Iterating over all of the devices, but will figure this out later
    // let devices = host.devices().expect("No devices found");
    // println!("All Device:");
    // for device in devices {
    //     let res = device.name();
    //     println!("{:#?}\n____________________", res.expect(""));
    // }

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
