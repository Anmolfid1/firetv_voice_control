#!/bin/bash
# One-line installer for Fire TV Voice Control

# Setup colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Fire TV Voice Control Quick Installer ===${NC}"

# Install base packages
echo -e "\n${YELLOW}Installing required packages...${NC}"
pkg update -y
pkg install -y python python-pip termux-api android-tools curl

# Install Python dependencies
echo -e "\n${YELLOW}Installing Python dependencies...${NC}"
pip install SpeechRecognition

# Create app directory
APP_DIR="$HOME/firetv_voice_control"
mkdir -p "$APP_DIR"
cd "$APP_DIR"

# Download the script from GitHub
echo -e "\n${YELLOW}Downloading latest version...${NC}"
# Replace YOUR_USERNAME with your actual GitHub username once you've created the repo
curl -s -o firetv_voice_control.py "https://raw.githubusercontent.com/Anmolfid1/firetv_voice_control/main/firetv_voice_control.py"

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to download script. Please check your internet connection.${NC}"
    exit 1
fi

# Make the script executable
chmod +x firetv_voice_control.py

# Create launcher
echo -e "\n${YELLOW}Creating launcher...${NC}"
mkdir -p "$HOME/../usr/bin"
cat > "$HOME/../usr/bin/firetv" << 'EOL'
#!/bin/bash
cd $HOME/firetv_voice_control
python firetv_voice_control.py "$@"
EOL

chmod +x "$HOME/../usr/bin/firetv"

echo -e "\n${GREEN}Installation complete!${NC}"
echo -e "${BLUE}=== Usage ===${NC}"
echo -e "Simply type ${YELLOW}firetv${NC} to run the voice control app"
echo -e "\nTo update in the future, run this command again:"
echo -e "${YELLOW}curl -s https://raw.githubusercontent.com/Anmolfid1/firetv_voice_control/main/firetv_direct_installer.sh | bash${NC}" 
