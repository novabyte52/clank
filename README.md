# Dependencies
## Vosk
The voice to text recognition library being used.

## wav
A crate to parse wav files

# Setup for development
## Vosk
CAVEATS:
- I have the path that the lib files are copied from hardcoded in the `Makefile.rs` (`"/usr/lib/vosk-linux-x86-0.3.43/."`), that will need to at least be standardized and specified in this `README` at some point, but just noting it here to not forget.
- You will want to adopt the same standard above for the `build.rs` file, too.

The vosk crate page states the following:
____
### Compilation

The Vosk-API dynamic libraries have to be discoverable by the rust linker (static libraries are not available). Download the zip file for your platform [here](https://github.com/alphacep/vosk-api/releases) and:

**Windows and Linux (Recommended)** *--- I did this one and created a build script. I have a folder `depend/` where I have the lib files and can put any other 3rd party dependencies.*

Do either of the following:

- Use the [`RUSTFLAGS` environment variable](https://doc.rust-lang.org/cargo/reference/environment-variables.html) to provide the path to the variables like so: `RUSTFLAGS=-L/path/to/the/libraries`
- Create a [build script](https://doc.rust-lang.org/cargo/reference/build-scripts.html) and provide cargo with the path to the libraries with `cargo:rustc-link-search` or `cargo:rustc-link-lib`.

Although both approaches are equivalent, the latter is more practical as it does not require the developer to remember a terminal command.

**Windows-only**

- Move the libraries to a directory in your PATH environment variable.

**Linux-only** *--- this one*

Do either of the following:

- Move them to `/usr/local/lib` or `/usr/lib`.
- Set the `LIBRARY_PATH` environment variable to the directory containing the libraries.

### Execution

The libraries also have to be discoverable by the executable at runtime. You will have to follow one of the approaches in the same section you chose in compilation.

**Windows and Linux (Recommended)** *--- this one*

For both approaches, you will need to copy the libraries to the root of the executable (target/<cargo profile name> by default). It is recommended that you use a tool such as cargo-make to automate moving the libraries from another, more practical, directory to the destination during build.

**Windows-only**

If you added your libraries to a directory in your PATH, no extra steps are needed as long as that is also the case for the target machine.

**Linux-only** *--- and this one*

- **If you followed option 1 in the compilation section:** No extra steps are needed as long as the target machine also has the libraries in one of the mentioned directories.
- **If you followed option 2:** You will need to add the directory containing the libraries to the LD_LIBRARY_PATH environment variable. Note that this directory does not have to be the same added to LIBRARY_PATH in the compilation step.
