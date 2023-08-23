// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::fs;
use std::io::ErrorKind;
use std::path::Path;
use std::path::PathBuf;

fn get_chat_history_path() -> PathBuf {
    PathBuf::from("/tmp/chat_history.json")
}

#[tauri::command]
fn save_chat_history(data: String) -> Result<String, String> {
    let chat_history_path = get_chat_history_path();
    match fs::write(&chat_history_path, data) {
        Ok(_) => Ok("Chat history saved successfully.".to_string()),
        Err(e) => Err(format!("Failed to save chat history: {}", e)),
    }
}

#[tauri::command]
fn load_chat_history() -> Result<String, String> {
    let chat_history_path = get_chat_history_path();

    match fs::read_to_string(&chat_history_path) {
        Ok(data) => Ok(data),
        Err(e) => {
            if e.kind() == ErrorKind::NotFound {
                Ok("".to_string()) // If file not found, return empty string
            } else {
                Err(format!("Failed to load chat history: {}", e))
            }
        }
    }
}

#[tauri::command]
fn clear_chat_history() -> Result<String, String> {
    let chat_history_path = get_chat_history_path();

    if Path::new(&chat_history_path).exists() {
        match fs::remove_file(&chat_history_path) {
            Ok(_) => Ok("Chat history cleared successfully.".to_string()),
            Err(e) => Err(format!("Failed to clear chat history: {}", e)),
        }
    } else {
        Ok("No chat history found.".to_string())
    }
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            save_chat_history,
            load_chat_history,
            clear_chat_history
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
