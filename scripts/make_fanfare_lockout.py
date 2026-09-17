#!/usr/bin/env python3
"""
Lock Out 用チャイム: オーケストラ風ファンファーレ(F長調の和音)
仕様(経過報告書 4-1節より):
  - Fメジャーの和音 (F2, F3, A3, C4, F4, A4, C5, F5)
  - 鋭いアタック(0.004秒間隔で一斉に鳴らす)
  - 速い減衰(オーケストラのファンファーレ風)
  - 全長 約2.5秒
  - 生成後、音量を1.15倍に増幅し、単純クリップ(-0.98, 0.98)で音割れ防止
"""

import numpy as np
from scipy.io import wavfile

SR = 44100

# F長調の和音を構成する音(音名, 周波数Hz)
NOTES = {
    "F2": 87.31,
    "F3": 174.61,
    "A3": 220.00,
    "C4": 261.63,
    "F4": 349.23,
    "A4": 440.00,
    "C5": 523.25,
    "F5": 698.46,
}


def fanfare(duration=2.5):
    t = np.arange(int(SR * duration)) / SR
    wave = np.zeros_like(t)

    # 各音を0.004秒(約176サンプル)ずつずらして重ねることで
    # 完全に同時ではない、自然な「一斉に鳴る」感じのアタックを作る
    stagger = 0.004
    decay_rate = 2.8  # 速い減衰(オーケストラのファンファーレらしいキレを出す)

    for i, (name, freq) in enumerate(NOTES.items()):
        delay = i * stagger
        note_t = t - delay
        note_t = np.clip(note_t, 0, None)
        env = np.exp(-decay_rate * note_t)
        # 開始前は無音にする(delay以前をゼロにする)
        env[t < delay] = 0
        wave += env * np.sin(2 * np.pi * freq * note_t)

    peak = np.max(np.abs(wave))
    if peak > 0:
        wave /= peak
    return wave


def main():
    wave = fanfare(2.5)

    # 音量を15%増幅、単純クリップ(tanhソフトクリップは音質変化が大きいため不採用)
    wave = wave * 1.15
    wave = np.clip(wave, -0.98, 0.98)

    wavfile.write("fanfare.wav", SR, (wave * 32767).astype(np.int16))
    print("fanfare.wav を生成しました (約", len(wave) / SR, "秒)")


if __name__ == "__main__":
    main()
