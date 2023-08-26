use wavy::{Speakers, Microphone, SpeakersSink, MicrophoneStream};
use fon::{stereo::Stereo32, Sink, Audio};

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
            Event::Record(microphone) => {
                self.buffer.extend(microphone)
                // TODO: look at buffer and determine if the "attention" phrase has been said
                // if attention phrase, listen for and determine command
            },
        }
    }
}