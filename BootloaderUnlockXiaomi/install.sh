#!/data/data/com.termux/files/usr/bin/bash

clear

echo "Mi Community Bootloader Unlock Installer"

pkg update -y > /dev/null 2>&1
pkg install python curl -y > /dev/null 2>&1

mkdir -p $HOME/.miunlock

curl -L https://tft.rf.gd/miunlock.py 
-o $HOME/.miunlock/miunlock.py

cat > $PREFIX/bin/@miunlock << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
python $HOME/.miunlock/miunlock.py
EOF

chmod +x $PREFIX/bin/@miunlock

echo ""
echo "INSTALL COMPLETE"
echo ""
echo "Run command:"
echo "@miunlock"
