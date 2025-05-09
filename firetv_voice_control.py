#!/usr/bin/env python3
# Voice-controlled ADB script for Fire TV Stick
# For use in Termux on Android

import os
import subprocess
import time
import json
import threading
from datetime import datetime

# Check for required packages
try:
    import speech_recognition as sr
except ImportError:
    print("Installing required packages...")
    os.system("pkg install python python-pip")
    os.system("pip install SpeechRecognition")
    os.system("pkg install termux-api")
    os.system("pkg install android-tools")  # For ADB
    print("Please run the script again after installation completes.")
    exit(1)

# Configuration
DEVICE_IP = None  # Will be set during setup
COMMANDS = {
    "up": "KEYCODE_DPAD_UP",
    "down": "KEYCODE_DPAD_DOWN",
    "left": "KEYCODE_DPAD_LEFT", 
    "right": "KEYCODE_DPAD_RIGHT",
    "select": "KEYCODE_ENTER",
    "play": "KEYCODE_MEDIA_PLAY",
    "pause": "KEYCODE_MEDIA_PAUSE",
    "play pause": "KEYCODE_MEDIA_PLAY_PAUSE",
    "back": "KEYCODE_BACK",
    "home": "KEYCODE_HOME",
    "menu": "KEYCODE_MENU"
}

# Add command aliases to improve recognition
COMMAND_ALIASES = {
    # English alternatives
    "cup": "up",
    "app": "up",
    "hop": "up",
    "top": "up",
    "dumb": "down",
    "town": "down",
    "don": "down",
    "crown": "down",
    "brown": "down",
    "laugh": "left",
    "lift": "left",
    "write": "right",
    "bright": "right",
    "light": "right",
    "ok": "select",
    "okay": "select",
    "enter": "select",
    "click": "select",
    "plate": "play",
    "stop": "pause",
    "boss": "pause",
    "return": "back",
    "go back": "back",
    "start": "home",
    "options": "menu",
    
    # Hindi commands
    "oopar": "up",
    "upar": "up",
    "ooper": "up",
    "neeche": "down",
    "neche": "down",
    "niche": "down",
    "bayen": "left",
    "baye": "left",
    "dayen": "right",
    "daye": "right",
    "daine": "right",
    "dahiney": "right",
    "select karo": "select",
    "ok karo": "select",
    "chalaao": "play",
    "chalao": "play",
    "play karo": "play",
    "roko": "pause",
    "rukjaao": "pause",
    "pause karo": "pause",
    "peeche": "back",
    "wapas": "back",
    "home jaao": "home",
    "menu dikhaao": "menu",
    "menu dikhao": "menu",
    
    # Other common misspellings and languages
    "arriba": "up",      # Spanish
    "abajo": "down",     # Spanish
    "izquierda": "left", # Spanish
    "derecha": "right",  # Spanish
    "aage": "up",        # Alternate Hindi
    "peeche": "down",    # Alternate Hindi
    "forward": "up",
    "backward": "down",
    "gauche": "left",    # French
    "droite": "right"    # French
}

def save_config(ip):
    """Save Fire TV IP address to config file"""
    config = {"device_ip": ip}
    with open("firetv_config.json", "w") as f:
        json.dump(config, f)

def load_config():
    """Load Fire TV IP address from config file"""
    global DEVICE_IP
    try:
        with open("firetv_config.json", "r") as f:
            config = json.load(f)
            DEVICE_IP = config.get("device_ip")
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def setup():
    """Initial setup to connect to Fire TV"""
    global DEVICE_IP
    
    print("\n==== Fire TV Voice Control Setup ====")
    
    # Try to load existing config
    load_config()
    
    if DEVICE_IP:
        print(f"Found saved Fire TV IP: {DEVICE_IP}")
        change = input("Change IP? (y/n): ").lower()
        if change != 'y':
            return
    
    # Get new IP
    DEVICE_IP = input("Enter your Fire TV Stick's IP address: ")
    save_config(DEVICE_IP)
    
    # Connect ADB
    print(f"Connecting to Fire TV at {DEVICE_IP}...")
    result = subprocess.run(f"adb connect {DEVICE_IP}", shell=True, capture_output=True, text=True)
    
    if "connected" in result.stdout.lower():
        print("Successfully connected to Fire TV!")
    else:
        print("Failed to connect. Please check:")
        print("1. Fire TV and phone are on the same network")
        print("2. ADB debugging is enabled on your Fire TV")
        print("3. IP address is correct")
        print("\nError:", result.stdout)
        retry = input("Retry? (y/n): ").lower()
        if retry == 'y':
            setup()

def send_command(command):
    """Send ADB command to Fire TV"""
    if not DEVICE_IP:
        print("Device not configured. Run setup first.")
        return False

    # Check if it's an alias and convert to main command
    if command in COMMAND_ALIASES:
        print(f"Recognized '{command}' as '{COMMAND_ALIASES[command]}'")
        command = COMMAND_ALIASES[command]

    if command in COMMANDS:
        keycode = COMMANDS[command]
        print(f"Sending {command} ({keycode})...")
        cmd = f"adb shell input keyevent {keycode}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Command sent successfully: {command}")
            return True
        else:
            print(f"Error sending command: {result.stderr}")
            return False
    else:
        print(f"Unknown command: {command}")
        print("Try saying: up, down, left, right, select, play, pause, back, home, menu")
        return False

def listen_for_command():
    """Use Termux API to capture voice and convert to text"""
    print("\nListening for command... (say 'exit' to quit)")
    
    # Use Termux API for speech recognition
    try:
        # First attempt with termux-speech-to-text
        result = subprocess.run(
            "termux-speech-to-text", 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=10  # Add timeout to prevent hanging
        )
        
        if result.returncode == 0:
            command = result.stdout.strip().lower()
            if command:
                print(f"I heard: {command}")
                return command
            else:
                print("Could not understand. Please try again.")
                return None
        else:
            print("Error with speech recognition. Trying alternative method...")
            return try_alternative_recognition()
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Trying alternative method...")
        return try_alternative_recognition()

def try_alternative_recognition():
    """Alternative method if termux-speech-to-text fails"""
    try:
        # Method 1: Use number input as fallback
        print("\nVoice recognition failed. Use numbers instead:")
        print("1: UP    2: DOWN    3: LEFT    4: RIGHT")
        print("5: SELECT    6: PLAY    7: PAUSE    8: BACK")
        print("9: HOME    0: MENU    E: EXIT")
        
        choice = input("Enter option: ").strip().lower()
        
        if choice == "1":
            return "up"
        elif choice == "2":
            return "down"
        elif choice == "3":
            return "left"
        elif choice == "4":
            return "right"
        elif choice == "5":
            return "select"
        elif choice == "6":
            return "play"
        elif choice == "7":
            return "pause"
        elif choice == "8":
            return "back"
        elif choice == "9":
            return "home"
        elif choice == "0":
            return "menu"
        elif choice == "e":
            return "exit"
        else:
            print("Invalid option")
            return None
    except Exception as e:
        print(f"Error with alternative method: {str(e)}")
        return None

def show_help():
    """Display available commands"""
    print("\n==== Available Voice Commands ====")
    for cmd in COMMANDS:
        print(f"• {cmd}")
    print("\n==== Command Aliases ====")
    for alias, cmd in COMMAND_ALIASES.items():
        print(f"• {alias} → {cmd}")
    print("\n• exit (quits the program)")
    print("• help (shows this menu)")

def main():
    print("\n==== Fire TV Voice Control ====")
    print("This script lets you control your Fire TV Stick with voice commands.")
    print("Works with English, Hindi, and some other languages.")
    
    if not DEVICE_IP:
        setup()
    
    show_help()
    
    while True:
        command = listen_for_command()
        
        if not command:
            continue
            
        if command == "exit":
            print("Exiting program.")
            break
        elif command == "help":
            show_help()
        else:
            send_command(command)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.") 