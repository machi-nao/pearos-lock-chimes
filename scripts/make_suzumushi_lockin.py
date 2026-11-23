#!/usr/bin/env python3
"""
Lock In 用チャイム: 鈴虫(すずむし)の鳴き声
仕様(経過報告書 4-1節より):
  - 基音3200Hz、単純な正弦波+振幅トレモロのみ
    (倍音やノイズを足すとかえって金属的になるため、シンプルな構成が正解)
  - リズム構成: 3.5秒鳴く(フェードアウト0.35秒) -> 0.9秒無音
             -> 2.6秒鳴く(フェードアウト0.35秒) -> 0.9秒無音
             -> 7秒鳴く(フェードアウト2.6秒)
    全長 約15秒("長短長"のパターン)
  - 音量は0.8倍(80%)に調整
"""

import numpy as np
from scipy.io import wavfile

SR = 44100
BASE_FREQ = 3200.0


def suzumushi_phrase(duration):
    t = np.arange(int(SR * duration)) / SR

    # 基音(単純な正弦波)
    tone = np.sin(2 * np.pi * BASE_FREQ * t)

    # 振幅トレモロ(鈴虫特有の細かい震え)
    tremolo_rate = 22.0  # トレモロの速さ(Hz)
    tremolo = 0.5 + 0.5 * np.sin(2 * np.pi * tremolo_rate * t)

    wave = tone * tremolo

    peak = np.max(np.abs(wave))
    if peak > 0:
        wave /= peak
    return wave


def apply_fadeout(wave, fade_sec):
    n = int(SR * fade_sec)
    if 0 < n < len(wave):
        fade = np.linspace(1, 0, n)
        wave[-n:] *= fade
    return wave


def silence(duration):
    return np.zeros(int(SR * duration))


def main():
    phrase1 = apply_fadeout(suzumushi_phrase(3.5), 0.35)
    gap1 = silence(0.9)
    phrase2 = apply_fadeout(suzumushi_phrase(2.6), 0.35)
    gap2 = silence(0.9)
    phrase3 = apply_fadeout(suzumushi_phrase(7.0), 2.6)

    full = np.concatenate([phrase1, gap1, phrase2, gap2, phrase3])

    full = full * 0.8
    full = np.clip(full, -0.98, 0.98)

    wavfile.write("suzumushi.wav", SR, (full * 32767).astype(np.int16))
    print("suzumushi.wav を生成しました (約", len(full) / SR, "秒)")


if __name__ == "__main__":
    main()
