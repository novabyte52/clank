fn main() {
    println!("cargo:rerun-if-changed=vosk");
    println!("cargo:rustc-link-lib=vosk");
}
// depend/vosk-linux-x86_64-0.3.45/libvosk.so
