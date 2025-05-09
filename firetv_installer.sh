#!/bin/bash
# Fire TV Voice Control Installer/Updater for Termux
# This script downloads the latest version from GitHub and sets up all dependencies

# Terminal colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Fire TV Voice Control Installer/Updater ===${NC}"
echo -e "This will download/update the Fire TV voice control script and set up dependencies."

# Create a directory for the app if it doesn't exist
APP_DIR="$HOME/firetv_voice_control"
if [ ! -d "$APP_DIR" ]; then
    echo -e "\n${YELLOW}Creating app directory...${NC}"
    mkdir -p "$APP_DIR"
fi

# Change to the app directory
cd "$APP_DIR"

# Check for required packages and install if missing
echo -e "\n${YELLOW}Checking and installing required packages...${NC}"

# Function to check if a package is installed
is_package_installed() {
    dpkg -s "$1" &> /dev/null
    return $?
}

# Install necessary packages
packages=("python" "python-pip" "termux-api" "android-tools")
for pkg in "${packages[@]}"; do
    if ! is_package_installed "$pkg"; then
        echo -e "Installing $pkg..."
        pkg install -y "$pkg"
    else
        echo -e "$pkg is already installed."
    fi
done

# Install Python dependencies
echo -e "\n${YELLOW}Installing Python dependencies...${NC}"
pip install SpeechRecognition

# GitHub URLs for the script and readme
SCRIPT_URL="https://raw.githubusercontent.com/Anmolfid1/firetv_voice_control/main/firetv_voice_control.py"
README_URL="https://raw.githubusercontent.com/Anmolfid1/firetv_voice_control/main/firetv_voice_control_readme.md"

# For now, we'll create a placeholder for the URL
# In the future, you'd replace YOUR_USERNAME with your actual GitHub username
echo -e "\n${YELLOW}Downloading latest version from GitHub...${NC}"
echo -e "${RED}NOTE: You need to upload this to GitHub and update the URLs in this installer script!${NC}"
echo -e "For now, we'll copy from your local files."

# Copy files from local storage for now
if [ -f "$HOME/firetv_voice_control.py" ]; then
    cp "$HOME/firetv_voice_control.py" "$APP_DIR/firetv_voice_control.py"
    echo -e "${GREEN}Script copied successfully!${NC}"
else
    echo -e "${RED}Local script not found. Please upload to GitHub and update this installer.${NC}"
    
    # This is what the actual download would look like once you've uploaded to GitHub
    # echo -e "Downloading from GitHub..."
    # curl -s -o firetv_voice_control.py "$SCRIPT_URL"
    # curl -s -o README.md "$README_URL"
fi

# Make the script executable
chmod +x firetv_voice_control.py

# Create a launcher script
echo -e "\n${YELLOW}Creating launcher...${NC}"
cat > "$HOME/../usr/bin/firetv" << 'EOL'
#!/bin/bash
cd $HOME/firetv_voice_control
python firetv_voice_control.py "$@"
EOL

chmod +x "$HOME/../usr/bin/firetv"

echo -e "\n${GREEN}Installation complete!${NC}"
echo -e "${BLUE}=== Usage ===${NC}"
echo -e "1. Run the script by typing: ${YELLOW}firetv${NC}"
echo -e "2. To update in the future, run this installer again."
echo -e "3. Make sure your Fire TV and phone are on the same network."
echo -e "\nEnjoy controlling your Fire TV with voice commands!" 
