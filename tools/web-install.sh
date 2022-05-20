echo "Installing required packages..."
python3 -m pip install --quiet distro nuitka > germanium_pip_install.log
rm germanium_pip_install.log

echo "Downloading Germanium..."
touch Germanium
cd Germanium
git clone --quiet https://github.com/Froggo8311/Germanium.git > germanium_git_clone.log
rm germanium_git_clone.log

echo "Running install script..."
python3 tools/install.py
