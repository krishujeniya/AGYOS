//! AGYOS Worker: Hosted Worker Daemon in Rust.

use std::env;
use std::process;

const VERSION: &str = "0.1.0-bootstrap";

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.contains(&"--version".to_string()) || args.contains(&"version".to_string()) {
        println!("agyos-worker {}", VERSION);
        process::exit(0);
    }

    println!("AGYOS Hosted Worker daemon started (version: {})", VERSION);
    println!("Worker bounded pool initialized with 0 active tasks.");
}
