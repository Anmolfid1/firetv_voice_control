# Fire TV Voice Control for Termux

This script allows you to control your Amazon Fire TV Stick with voice commands from your Android phone using Termux.

## Requirements

- An Android phone with [Termux](https://f-droid.org/en/packages/com.termux/) installed
- [Termux:API](https://f-droid.org/en/packages/com.termux.api/) app installed
- Amazon Fire TV Stick on the same network as your phone
- ADB debugging enabled on your Fire TV Stick

## Setup Instructions

### 1. Install Required Apps

1. Install Termux from F-Droid: https://f-droid.org/en/packages/com.termux/
2. Install Termux:API from F-Droid: https://f-droid.org/en/packages/com.termux.api/

### 2. Enable ADB on Fire TV

1. On your Fire TV, go to Settings → My Fire TV → Developer Options
2. Enable "ADB debugging"
3. Enable "Apps from Unknown Sources"
4. Make note of your Fire TV's IP address (Settings → My Fire TV → About → Network)

### 3. Setup Termux

1. Open Termux and run the following commands:

   ```
   pkg update
   pkg upgrade
   pkg install termux-api python python-pip android-tools
   pip install SpeechRecognition
   ```

2. Download the script to your phone and move it to Termux's home directory
   ```
   chmod +x firetv_voice_control.py
   ```

## Using the Script

1. Run the script:

   ```
   python firetv_voice_control.py
   ```

2. On first run, you'll be asked to enter your Fire TV's IP address

3. Say any of the following voice commands:

   - "up", "down", "left", "right" (for navigation)
   - "select" (for OK/Enter)
   - "play", "pause", "play pause" (media controls)
   - "back", "home", "menu" (system navigation)
   - "help" (shows all commands)
   - "exit" (quits the program)

4. The script also recognizes many alternative words (aliases) for each command:

   - For "up": "cup", "app", "hop", "top"
   - For "down": "dumb", "town", "don", "crown", "brown"
   - For "left": "laugh", "lift"
   - For "right": "write", "bright", "light"
   - For "select": "ok", "okay", "enter", "click"
   - And many more...

5. **Hindi commands are now supported!**

   - "oopar" / "upar" / "ooper" → up
   - "neeche" / "neche" / "niche" → down
   - "bayen" / "baye" → left
   - "dayen" / "daye" / "daine" → right
   - "select karo" / "ok karo" → select
   - "chalaao" / "chalao" / "play karo" → play
   - "roko" / "rukjaao" / "pause karo" → pause
   - "peeche" / "wapas" → back
   - "home jaao" → home
   - "menu dikhaao" / "menu dikhao" → menu

6. Some Spanish and French commands are also included

   - "arriba" → up, "abajo" → down (Spanish)
   - "izquierda" → left, "derecha" → right (Spanish)
   - "gauche" → left, "droite" → right (French)

7. If voice recognition fails, the script will automatically switch to a number-based input method:
   - 1: UP
   - 2: DOWN
   - 3: LEFT
   - 4: RIGHT
   - 5: SELECT
   - 6: PLAY
   - 7: PAUSE
   - 8: BACK
   - 9: HOME
   - 0: MENU
   - E: EXIT

## Troubleshooting

- If the script says "Command not found", make sure you have installed all required packages
- If ADB can't connect, verify:
  1. Your Fire TV and phone are on the same network
  2. ADB debugging is enabled on your Fire TV
  3. The IP address is correct
- If voice recognition consistently fails:
  1. Ensure Termux has microphone permissions
  2. Try speaking more clearly and slowly
  3. Use the number-based fallback method instead
  4. Try adding your own command aliases to the COMMAND_ALIASES dictionary in the script

## Customizing

You can easily customize the script for your own needs:

1. **Adding your own language commands**:

   - Edit the `COMMAND_ALIASES` dictionary in the script
   - Add new entries for words in your language
   - Example format: `"your_word": "command"`
   - Where "command" must be one of: up, down, left, right, select, play, pause, play pause, back, home, menu

2. **Adding new commands**:
   - Add new entries to the `COMMANDS` dictionary
   - You'll need to use the correct Android keycode values for each command

## Notes

- The script requires internet for voice recognition
- Your Fire TV IP might change if you restart your router (DHCP)
- For better results, speak clearly and in a quiet environment
- You can add your own command aliases by editing the COMMAND_ALIASES dictionary in the script
