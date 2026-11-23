# pearOS Lock Chime Settings (Unofficial Customization)

*For Linux fans who are curious about macOS and want to enjoy pearOS, the "Mac-like OS."*

**This is not an official pearOS tool. It's an unofficial customization made by an individual user.**


## Background

On real macOS machines with Apple Silicon, opening the lid plays a startup chime — but that depends on hardware only Apple chips have, so it can't happen on a regular PC running pearOS.

As a substitute, I set up a chime that plays when the screen **unlocks (Lock Out)**. I then extended it further so a chime also plays when the screen **locks (Lock In)**, with the sound and volume configurable independently for each.

## Features

- Choose any chime sound for Lock In (screen locks) and Lock Out (screen unlocks) independently
- Set the volume independently for Lock In and Lock Out
- Configured through a small standalone GUI app, launched from the App Launcher — pick a sound, preview it, adjust volume, save
- Add your own chimes by generating them yourself with Python (NumPy/SciPy), or simply drop in any downloaded `.wav` / `.ogg` / `.flac` file

## Installation

```bash
git clone https://github.com/machi-nao/pearos-lock-chimes.git
cd pearos-lock-chimes
chmod +x install.sh
./install.sh
```

Then start the watcher (it will also auto-start on future logins):

```bash
python3 ~/lock-chime-watcher.py & disown
```

## File structure

pearos-lock-chimes/
├── install.sh Install script
├── chime_settings.py Settings app (PySide6)
├── lock-chime-watcher.py Background watcher that plays chimes on lock/unlock
├── icons/
│ └── chime-settings-icon.svg App icon
├── desktop/
│ └── pearos-chime-settings.desktop App Launcher entry
├── sounds/
│ ├── lock-in/
│ │ └── suzumushi.wav Japanese bell-cricket chirp (default Lock In sound)
│ └── lock-out/
│ └── fanfare.wav Orchestral-style fanfare (default Lock Out sound)
└── scripts/
├── make_suzumushi_lockin.py Generates the bell-cricket sound
└── make_fanfare_lockout.py Generates the fanfare sound


## Usage

1. Open "Chime Settings" from the App Launcher
2. Pick a sound for Lock In / Lock Out from the dropdowns (preview button included)
3. Adjust volume with the sliders
4. Click "Save" — it takes effect on the next lock/unlock

To add your own sounds, just drop `.wav` / `.ogg` / `.flac` files into these folders — they show up automatically in the app's dropdowns, no reinstall needed:

~/Music/pearos-chimes/lock-in/
~/Music/pearos-chimes/lock-out/


## Credits

Built together with [Claude AI](https://claude.ai).

## License

MIT License (see LICENSE file)

---

*Mulțumesc pearOS pentru un sistem de operare atât de distractiv de personalizat! 🍐*
