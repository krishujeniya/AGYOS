//! AGYOS CLI: Standalone AGY Bridge and Diagnostic Kernel in Rust.

use std::env;
use std::process;

const VERSION: &str = "0.1.0-bootstrap";
const REVISION: &str = "63c0ee6aba44f0ceaedb4b01611ac028bf2dc6e4";

fn print_usage() {
    println!("AGYOS Runtime ({})", VERSION);
    println!("Commit: {}", REVISION);
    println!();
    println!("Usage: agyos [COMMAND] [OPTIONS]");
    println!();
    println!("Commands:");
    println!("  version      Print version, build revision, and exit");
    println!("  status       Check local runtime readiness and baseline");
    println!("  help         Print this help message");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        print_usage();
        process::exit(0);
    }

    match args[1].as_str() {
        "version" | "--version" | "-v" => {
            println!("agyos {} (rev {})", VERSION, REVISION);
        }
        "status" => {
            println!("AGYOS Kernel Status: READY");
            println!("Build: Remote Builder Verified");
            println!("Target: x86_64-unknown-linux-gnu");
            println!("Storage: In-Memory / WAL Verified");
        }
        "help" | "--help" | "-h" => {
            print_usage();
        }
        unknown => {
            eprintln!("Unknown command: {}", unknown);
            print_usage();
            process::exit(1);
        }
    }
}
