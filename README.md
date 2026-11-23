# pearOS Lock Chime Settings (非公式カスタマイズ)

**これはpearOS公式のツールではありません。個人ユーザーによる非公式カスタマイズです。**

## きっかけ

本来のmacOSはApple Silicon搭載機の上蓋(ディスプレイ)を開けたときに「ジャーン」というチャイムが鳴りますが、これはMacチップ独自のハードウェア機能に依存しているため、pearOSをインストールした一般的なPCでは再現できません。

その代わりとして、**画面ロックの解除(Lock Out)時にチャイムが鳴る**ように設定しました。さらに発展させて、**画面がロックされる(Lock In)ときにもチャイムが鳴る**ようにし、それぞれ好きな音・好きな音量を個別に設定できるようにしています。

## できること

- Lock In(画面ロック時)/ Lock Out(ロック解除時)、それぞれに好きなチャイム音を設定できる
- 音量もLock In / Lock Outで個別に調整できる
- 設定は専用アプリ(アプリランチャーから起動)で行える。GUIでサウンドを選んで、試聴して、保存するだけ
- 好みのチャイムは自分でPython(NumPy/SciPy)を使って音を合成して作ることもできるし、どこかからダウンロードしてきた音源ファイル(wav/ogg/flac)を追加することもできる

## インストール

```bash
git clone https://github.com/yourname/pearos-lock-chimes.git
cd pearos-lock-chimes
chmod +x install.sh
./install.sh
```

インストール後、watcherを起動します(次回ログイン時からは自動起動します)。

```bash
python3 ~/lock-chime-watcher.py & disown
```

## ファイル構成

```
pearos-lock-chimes/
├── install.sh                    インストールスクリプト
├── chime_settings.py             チャイム設定アプリ本体(PySide6)
├── lock-chime-watcher.py         画面ロック/解除を監視して音を鳴らす常駐スクリプト
├── icons/
│   └── chime-settings-icon.svg   設定アプリのアイコン
├── desktop/
│   └── pearos-chime-settings.desktop  アプリランチャー登録用
├── sounds/
│   ├── lock-in/
│   │   └── suzumushi.wav         鈴虫の音(デフォルトのLock In用)
│   └── lock-out/
│       └── fanfare.wav           オーケストラ風ファンファーレ(デフォルトのLock Out用)
└── scripts/
    ├── make_suzumushi_lockin.py  鈴虫の音の生成スクリプト
    └── make_fanfare_lockout.py   ファンファーレの生成スクリプト
```

## 使い方

1. アプリランチャーから「チャイム設定」を起動
2. Lock In / Lock Outそれぞれのプルダウンから好きな音を選ぶ(試聴ボタンあり)
3. 音量スライダーで音量を調整
4. 「保存」を押せば、次回のロック/解除から反映される

音源を自分で追加したい場合は、以下のフォルダに `.wav` / `.ogg` / `.flac` ファイルを置くだけで、アプリのプルダウンに自動的に反映されます。

```
~/Music/pearos-chimes/lock-in/
~/Music/pearos-chimes/lock-out/
```

## クレジット

このツールの設計・実装は [Claude AI](https://claude.ai) と一緒に作りました。

## ライセンス

MIT License(LICENSEファイル参照)
