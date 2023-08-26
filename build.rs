fn main() {
    println!("cargo:rerun-if-changed=depend/vosk-linux-x86_64-0.3.43");
    println!("cargo:rustc-link-search=depend/vosk-linux-x86_64-0.3.43");
}
// depend/vosk-linux-x86_64-0.3.43/libvosk.so
