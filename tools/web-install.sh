echo "Installing required packages..."
python3 -m pip -q install distro nuitka

echo "Downloading Germanium..."
git clone --quiet https://github.com/Froggo8311/Germanium.git

echo "Running install script..."
cd Germanium
pwd
python3 tools/install_src.py
