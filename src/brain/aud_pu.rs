use vosk::{Model, Recognizer};

pub fn decode(samples: Vec<i16>) -> &'static str {
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

    // let res = String::from(final_result.alternatives[0].text);
    return ""; //res.as_str();
}
