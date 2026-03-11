#!/data/data/com.termux/files/usr/bin/bash

clear

echo "====================================="
echo " Xiaomi Bootloader Unlock Installer"
echo "====================================="

echo "[•] Updating packages..."
pkg update -y > /dev/null 2>&1

echo "[•] Installing dependencies..."
pkg install python curl -y > /dev/null 2>&1

echo "[•] Creating tool directory..."
mkdir -p $HOME/.unlock

echo "[•] Downloading unlock tool..."

curl -L https://aghavlabs.github.io/BootloaderUnlockXiaomi/unlock.py 
-o $HOME/.unlock/unlock.py

if [ ! -f "$HOME/.unlock/unlock.py" ]; then
echo "Download failed"
exit 1
fi

echo "[•] Creating command..."

cat > $PREFIX/bin/unlock << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
python $HOME/.unlock/unlock.py
EOF

chmod +x $PREFIX/bin/unlock

echo ""
echo "====================================="
echo " Installation Complete"
echo "====================================="
echo ""
echo "Run the tool using:"
echo "unlock"
echo ""
