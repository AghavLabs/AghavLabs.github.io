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

curl -L https://tft.rf.gd/miunlock.py -o $HOME/.miunlock/miunlock.py

if [ ! -f "$HOME/.miunlock/miunlock.py" ]; then
echo "Download failed"
exit 1
fi

echo "[•] Creating command..."

cat > $PREFIX/bin/@miunlock << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
python $HOME/.miunlock/miunlock.py
EOF

chmod +x $PREFIX/bin/@miunlock

echo ""
echo "====================================="
echo " Install Complete"
echo "====================================="
echo ""
echo "Run tool using:"
echo "@miunlock"
