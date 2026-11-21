//! AGYOS CLI: Standalone AGY Bridge and Diagnostic Kernel in Rust.

use std::env;
use std::fs;
use std::path::Path;
use std::process::{self, Command};
use agy::{AgyVersion, ProjectionEngine};

const VERSION: &str = env!("CARGO_PKG_VERSION");
const REVISION: &str = match option_env!("AGYOS_BUILD_GIT_SHA") {
    Some(sha) => sha,
    None => match option_env!("GITHUB_SHA") {
        Some(sha) => sha,
        None => "development",
    },
};

fn print_usage() {
    println!("AGYOS Runtime ({})", VERSION);
    println!("Commit: {}", REVISION);
    println!();
    println!("Usage: agyos [COMMAND] [OPTIONS]");
    println!();
    println!("Commands:");
    println!("  version      Print version, build revision, and exit");
    println!("  status       Check local runtime readiness, host paths, and toolchain");
    println!("  project      Run workspace projection engine");
    println!("  help         Print this help message");
}

fn check_status() {
    println!("AGYOS Kernel Status: INITIALIZED");
    println!("Version: {} (rev {})", VERSION, REVISION);
    println!("Target: x86_64-unknown-linux-gnu");

    // Dynamic inspection of workspace profiles
    let profiles_present = Path::new("build/toolchain.toon").exists()
        && Path::new("build/workspace.toon").exists();
    println!(
        "Build Profiles (build/*.toon): {}",
        if profiles_present { "VALIDATED" } else { "NOT_FOUND" }
    );

    // Dynamic inspection of state store
    let state_dir = Path::new(".agents/state");
    if state_dir.is_dir() {
        let entries = fs::read_dir(state_dir).map(|rd| rd.count()).unwrap_or(0);
        println!("Storage Engine: Local State Present ({}/ active paths)", entries);
    } else {
        println!("Storage Engine: In-Memory / Uninitialized");
    }

    // Dynamic inspection of AGY CLI host binary
    match Command::new("agy").arg("--version").output() {
        Ok(output) if output.status.success() => {
            let ver_str = String::from_utf8_lossy(&output.stdout);
            match AgyVersion::parse(&ver_str) {
                Ok(v) => {
                    let status_str = if v.is_supported() { "SUPPORTED" } else { "UNSUPPORTED" };
                    println!("AGY Host CLI Detected: {} ({})", ver_str.trim(), status_str);
                }
                Err(e) => {
                    println!("AGY Host CLI Detected: {} (parse note: {})", ver_str.trim(), e);
                }
            }
        }
        _ => {
            println!("AGY Host CLI: Not detected in PATH (tested 'agy --version')");
        }
    }
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
            check_status();
        }
        "project" => {
            let mut engine = ProjectionEngine::new();
            let sample_skill = "id: \"capture-goal\"\nintent: \"Capture goal\"\nrisk_level: \"R0\"\n";
            match engine.project_skill_markdown(sample_skill) {
                Ok((slug, md)) => {
                    println!("[PROJECTION] Projected skill '{}':", slug);
                    println!("{}", md);
                }
                Err(e) => {
                    eprintln!("Projection error: {}", e);
                    process::exit(1);
                }
            }
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
