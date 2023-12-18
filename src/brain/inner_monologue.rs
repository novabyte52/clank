use rust_bert::{
    gpt_neo::{
        GptNeoConfigResources, GptNeoMergesResources, GptNeoModelResources, GptNeoVocabResources,
    },
    pipelines::{
        common::{ModelResource, ModelType},
        text_generation::{TextGenerationConfig, TextGenerationModel},
    },
    resources::RemoteResource,
};
use tch::Device;

pub fn soliloquy(directive: &str) {
    //    Set-up model resources
    let config_resource = Box::new(RemoteResource::from_pretrained(
        GptNeoConfigResources::GPT_NEO_2_7B,
    ));
    let vocab_resource = Box::new(RemoteResource::from_pretrained(
        GptNeoVocabResources::GPT_NEO_2_7B,
    ));
    let merges_resource = Box::new(RemoteResource::from_pretrained(
        GptNeoMergesResources::GPT_NEO_2_7B,
    ));
    let model_resource = Box::new(RemoteResource::from_pretrained(
        GptNeoModelResources::GPT_NEO_2_7B,
    ));

    let generate_config = TextGenerationConfig {
        model_type: ModelType::GPTNeo,
        model_resource: ModelResource::Torch(model_resource),
        config_resource,
        vocab_resource,
        merges_resource: Some(merges_resource),
        min_length: 1,
        max_length: Some(1),
        // early_stopping: true,
        num_beams: 5,
        no_repeat_ngram_size: 2,
        num_return_sequences: 1,
        device: Device::Cpu,
        ..Default::default()
    };

    let model = TextGenerationModel::new(generate_config).unwrap();

    let mut line = String::new();
    // let input = ["The dog"];
    loop {
        println!("listening...");
        std::io::stdin().read_line(&mut line).unwrap();
        // let split = line.split('/').collect::<Vec<&str>>();
        // let slc = split.as_slice();
        println!("generating...");
        let output = model.generate(&[&line], None);
        for sentence in output {
            println!("[Clank] {}", sentence);
        }
    }
}
