use std::process::{Command, Stdio};
use std::{env, path::PathBuf};

/// Run a python script from rust file
pub fn run_python(script_path: &str) {
    // Determine the Python executable based on OS
    let python_exe = if cfg!(target_os = "windows") {
        "python"
    } else {
        "python3"
    };

    // Get current executable directory
    let exe_path: PathBuf = env::current_exe().expect("Failed to get current exe path");
    let script_dir = exe_path.parent().expect("Failed to get parent dir");

    println!("=== Running Python script {} ===", script_path);

    let output = Command::new(python_exe)
        .arg(script_path)
        .current_dir(script_dir) // ensures relative paths work
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .expect("Failed to spawn python process")
        .wait_with_output()
        .expect("Failed to wait on python process");

    println!("{}", String::from_utf8_lossy(&output.stdout));
    if !output.stderr.is_empty() {
        eprintln!("Error: {}", String::from_utf8_lossy(&output.stderr));
    }
}

fn main() {
    let python_script = "../../runAquaQ.py";
    run_python(python_script);
}