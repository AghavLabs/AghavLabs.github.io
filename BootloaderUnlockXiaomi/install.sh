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
mkdir -p $HOME/.miunlock

echo "[•] Downloading unlock tool..."

curl -fsSL https://aghavlabs.github.io/BootloaderUnlockXiaomi/unlock.py -o $HOME/.miunlock/unlock.py

if [ ! -f "$HOME/.miunlock/unlock.py" ]; then
echo "[✗] Download failed"
exit 1
fi

echo "[•] Creating command..."

cat > $PREFIX/bin/@miunlock << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
python $HOME/.miunlock/unlock.py "$@"
EOF

chmod +x $PREFIX/bin/@miunlock

echo ""
echo "====================================="
echo " Install Complete"
echo "====================================="
echo ""
echo "Run tool:"
echo "@miunlock"
