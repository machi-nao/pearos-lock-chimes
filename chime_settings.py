#!/usr/bin/env python3
"""
pearOS チャイム設定アプリ (v3: 複数音源フォルダ対応)
Lock In / Lock Out それぞれのチャイム音と音量を設定する。

音源は以下の2箇所を自動的にまとめて読み込む:
  - システム側(自作した合成音など): /usr/local/share/sounds/pearos-chimes/{lock-in,lock-out}
  - ユーザー側(録音した生の音源など、sudo不要): ~/Music/pearos-chimes/{lock-in,lock-out}

必要パッケージ: python-pyside6 (pacman -S pyside6)
設定保存先: ~/.config/pearos-chimesrc (kwriteconfig6/kreadconfig6 経由)
  -> Sound には音源ファイルの「フルパス」を保存する(どちらのフォルダの
     ものでも区別なく扱えるようにするため)
"""

import sys
import os
import subprocess

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGroupBox, QFormLayout,
    QComboBox, QSlider, QPushButton, QHBoxLayout, QLabel, QMessageBox
)
from PySide6.QtCore import Qt

SOUND_DIRS = [
    "/usr/local/share/sounds/pearos-chimes",
    os.path.expanduser("~/Music/pearos-chimes"),
]
SUPPORTED_EXT = (".wav", ".ogg", ".flac")
CONFIG_FILE = "pearos-chimesrc"


def list_sounds(kind):
    """kind: 'lock-in' or 'lock-out' -> [(表示名, フルパス), ...] の一覧
    (システム側・ユーザー側の両フォルダをまとめる)"""
    results = []
    for base in SOUND_DIRS:
        d = os.path.join(base, kind)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.lower().endswith(SUPPORTED_EXT):
                full_path = os.path.join(d, f)
                # ユーザー音源はどこの音か分かるように印を付けて表示
                label = f if base == SOUND_DIRS[0] else f"{f}  (自分の音源)"
                results.append((label, full_path))
    return results


def read_config(group, key, default):
    try:
        r = subprocess.run(
            ["kreadconfig6", "--file", CONFIG_FILE, "--group", group, "--key", key],
            capture_output=True, text=True, timeout=5
        )
        val = r.stdout.strip()
        return val if val else default
    except Exception:
        return default


def write_config(group, key, value):
    subprocess.run(
        ["kwriteconfig6", "--file", CONFIG_FILE, "--group", group, "--key", key, str(value)],
        timeout=5
    )


def play_preview(path, volume):
    if not path or not os.path.isfile(path):
        return
    vol_raw = int(65536 * volume / 100)
    subprocess.Popen(["paplay", "--volume", str(vol_raw), path])


class ChimeSection(QGroupBox):
    def __init__(self, title, folder, group):
        super().__init__(title)
        self.folder = folder  # 'lock-in' or 'lock-out'
        self.group = group    # 'LockIn' or 'LockOut'
        layout = QFormLayout()

        self.combo = QComboBox()
        sounds = list_sounds(self.folder)
        for label, path in sounds:
            self.combo.addItem(label, userData=path)

        saved_path = read_config(self.group, "Sound", "")
        if saved_path:
            idx = self.combo.findData(saved_path)
            if idx >= 0:
                self.combo.setCurrentIndex(idx)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(int(read_config(self.group, "Volume", "100")))

        self.volume_label = QLabel(f"{self.slider.value()}%")
        self.slider.valueChanged.connect(
            lambda v: self.volume_label.setText(f"{v}%")
        )

        preview_btn = QPushButton("▶ 試聴")
        preview_btn.clicked.connect(self.preview)

        sound_row = QHBoxLayout()
        sound_row.addWidget(self.combo)
        sound_row.addWidget(preview_btn)

        volume_row = QHBoxLayout()
        volume_row.addWidget(self.slider)
        volume_row.addWidget(self.volume_label)

        layout.addRow("サウンド:", sound_row)
        layout.addRow("音量:", volume_row)
        self.setLayout(layout)

        if not sounds:
            self.combo.setEnabled(False)
            preview_btn.setEnabled(False)
            self.setTitle(f"{title} (音源が見つかりません)")

    def preview(self):
        path = self.combo.currentData()
        play_preview(path, self.slider.value())

    def save(self):
        path = self.combo.currentData()
        if path:
            write_config(self.group, "Sound", path)
        write_config(self.group, "Volume", self.slider.value())


class ChimeSettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("チャイム設定")
        self.lock_in = ChimeSection("Lock In(画面ロック時・施錠)", "lock-in", "LockIn")
        self.lock_out = ChimeSection("Lock Out(ロック解除時)", "lock-out", "LockOut")

        save_btn = QPushButton("保存")
        save_btn.clicked.connect(self.save_all)

        layout = QVBoxLayout()
        layout.addWidget(self.lock_in)
        layout.addWidget(self.lock_out)
        layout.addWidget(save_btn)
        self.setLayout(layout)

    def save_all(self):
        self.lock_in.save()
        self.lock_out.save()
        QMessageBox.information(self, "保存完了", "設定を保存しました。\n次回のロック/解除から反映されます。")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ChimeSettingsWindow()
    win.resize(420, 300)
    win.show()
    sys.exit(app.exec())
