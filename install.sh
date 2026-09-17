#!/bin/bash
# pearOS Lock Chime Settings - インストールスクリプト
# このリポジトリを一式、pearOS機に配置する

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SOUND_DIR="/usr/local/share/sounds/pearos-chimes"

echo "=== システム側の音源フォルダを作成 ==="
sudo mkdir -p "$SOUND_DIR/lock-in" "$SOUND_DIR/lock-out"
sudo cp "$REPO_DIR/sounds/lock-in/suzumushi.wav" "$SOUND_DIR/lock-in/"
sudo cp "$REPO_DIR/sounds/lock-out/fanfare.wav" "$SOUND_DIR/lock-out/"
sudo chmod -R a+rX "$SOUND_DIR"

echo "=== ユーザー音源フォルダを作成(sudo不要で自分の音源を追加できる場所) ==="
mkdir -p ~/Music/pearos-chimes/lock-in
mkdir -p ~/Music/pearos-chimes/lock-out

echo "=== 設定アプリを配置 ==="
mkdir -p ~/.local/share/pearos-chime-settings
cp "$REPO_DIR/chime_settings.py" ~/.local/share/pearos-chime-settings/

echo "=== アイコンを配置 ==="
mkdir -p ~/.local/share/icons/hicolor/scalable/apps
cp "$REPO_DIR/icons/chime-settings-icon.svg" ~/.local/share/icons/hicolor/scalable/apps/pearos-chime-settings.svg

echo "=== アプリランチャー用の.desktopファイルを配置 ==="
mkdir -p ~/.local/share/applications
cp "$REPO_DIR/desktop/pearos-chime-settings.desktop" ~/.local/share/applications/
chmod +x ~/.local/share/applications/pearos-chime-settings.desktop

echo "=== 常駐watcherを配置 ==="
cp "$REPO_DIR/lock-chime-watcher.py" ~/lock-chime-watcher.py

echo "=== ログイン時にwatcherを自動起動する設定 ==="
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/lock-chime-watcher.desktop << EOF
[Desktop Entry]
Type=Application
Exec=python3 $HOME/lock-chime-watcher.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Lock Chime Watcher
EOF

echo "=== アイコン・メニューキャッシュを更新 ==="
gtk-update-icon-cache ~/.local/share/icons/hicolor 2>/dev/null || true
kbuildsycoca6 --noincremental

echo ""
echo "インストール完了です。"
echo "watcherを今すぐ起動するには:"
echo "  python3 ~/lock-chime-watcher.py & disown"
echo "(次回ログイン時からは自動で起動します)"
echo ""
echo "アプリランチャーから「チャイム設定」を開いて、好きな音・音量を選んでください。"
