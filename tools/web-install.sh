echo "Installing required packages...";
python3 -m pip install distro nuitka;

echo "Downloading Germanium...";
git clone https://github.com/Froggo8311/Germanium.git;

echo "Running install script...";
cd Germanium;
python3 tools/install_src.py;
