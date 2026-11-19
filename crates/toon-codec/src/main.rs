//! TOON CLI utility for fast conversion and minification.

use std::env;
use std::fs;
use std::io::{self, Read};
use std::process;

use toon_codec::{decode_records, encode_json_array, minify_toon};

fn print_usage() {
    eprintln!(
        "Usage: toon <command> [options]\n\n\
        Commands:\n  \
          encode <json_file> [--key <name>]   Encode JSON array of objects to TOON\n  \
          decode <toon_file>                 Decode TOON tabular block to JSON\n  \
          minify <toon_file>                 Minify TOON file stripping excess whitespace\n\n\
        Options:\n  \
          --help, -h                         Show help\n  \
          --key, -k                          Key name for array (default: items)\n"
    );
}

fn read_input(path_or_dash: Option<&str>) -> io::Result<String> {
    match path_or_dash {
        None | Some("-") => {
            let mut buffer = String::new();
            io::stdin().read_to_string(&mut buffer)?;
            Ok(buffer)
        }
        Some(path) => fs::read_to_string(path),
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        print_usage();
        process::exit(1);
    }

    let command = args[1].as_str();
    match command {
        "encode" => {
            let file_arg = args.get(2).map(|s| s.as_str());
            let mut key_name = "items";
            for i in 2..args.len() {
                if (args[i] == "--key" || args[i] == "-k") && i + 1 < args.len() {
                    key_name = &args[i + 1];
                }
            }

            let input = match read_input(file_arg) {
                Ok(s) => s,
                Err(e) => {
                    eprintln!("Error reading input: {}", e);
                    process::exit(1);
                }
            };

            let json_val: serde_json::Value = match serde_json::from_str(&input) {
                Ok(v) => v,
                Err(e) => {
                    eprintln!("Invalid JSON input: {}", e);
                    process::exit(1);
                }
            };

            let array = match json_val.as_array() {
                Some(arr) => arr,
                None => {
                    eprintln!("Error: Root JSON value must be an array of objects");
                    process::exit(1);
                }
            };

            match encode_json_array(array, key_name) {
                Ok(toon) => println!("{}", toon),
                Err(e) => {
                    eprintln!("Encoding error: {}", e);
                    process::exit(1);
                }
            }
        }
        "decode" => {
            let file_arg = args.get(2).map(|s| s.as_str());
            let input = match read_input(file_arg) {
                Ok(s) => s,
                Err(e) => {
                    eprintln!("Error reading input: {}", e);
                    process::exit(1);
                }
            };

            match decode_records(&input) {
                Ok(records) => {
                    let json_out = serde_json::to_string_pretty(&records).unwrap();
                    println!("{}", json_out);
                }
                Err(e) => {
                    eprintln!("Decoding error: {}", e);
                    process::exit(1);
                }
            }
        }
        "minify" => {
            let file_arg = args.get(2).map(|s| s.as_str());
            let input = match read_input(file_arg) {
                Ok(s) => s,
                Err(e) => {
                    eprintln!("Error reading input: {}", e);
                    process::exit(1);
                }
            };

            println!("{}", minify_toon(&input));
        }
        "--help" | "-h" | "help" => {
            print_usage();
        }
        unknown => {
            eprintln!("Unknown command: {}", unknown);
            print_usage();
            process::exit(1);
        }
    }
}
