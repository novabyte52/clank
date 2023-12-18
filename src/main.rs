pub mod brain;
pub mod senses;

use std::io::{self, BufRead};

use crate::brain::inner_monologue::soliloquy;

// const TEST_PATH: &str = "depend/audio/turn_on_command_test.wav";
// const TURN_ON_PATH: &str = "depend/audio/turn_on_command_test.wav";
const DAD_VOICE: &str = "depend/audio/dad_voice_sample.wav";

fn main() {
    println!("running clank...");
    soliloquy(
        "your name is clank. my name is evan. i respect you, and would like for you to assist me.",
    );
    // we will need the following process to run in a loop
    // to be able to detect if someone wishes to give a command

    // 01 === Recording the sound and putting it in a .wav file of the needed format === //
    /*
    out:
        a .wav file in PCM 16khz 16bit mono format
    */

    // 02 === Getting noise data into the needed format === //
    /*
        in:
            a .wav file in PCM 16khz 16bit mono format
        out:
            &Vec<i16> of the data
    */
    // ===== //
    // open audio file
    // let mut inp_file = File::open(Path::new(&DAD_VOICE)).unwrap();
    // pull out data
    // let (_header, data) = wav::read(&mut inp_file).unwrap();
    // pull the samples out in the format we need them
    // let samples = data.as_sixteen().unwrap();
    // ===== //

    // 03 === Getting the vosk model setup, so we can give it our noise data, and figure out what words were said === //
    /*
        in:
            noise data
        out:
            the words that were said
    */

    // 04 === Checking what was said and determining what should be done === //
    /*
    in:
        the string of words said
      */
    // actions, like 'turn on', can be applied to objects, like 'living room light 01' (most likely webthings)
    //
    // manufacturers should be able to specify their own action words/phrases for their device,
    // but end users should also be able to change it if they want.
    // if final_result.alternatives[0].text.contains("turn on") {
    // println!("The action 'turn on' has been recieved!");
    // }
}
