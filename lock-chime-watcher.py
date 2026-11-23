#!/usr/bin/env python3
import subprocess
import os
from dbus.mainloop.glib import DBusGMainLoop
import dbus
from gi.repository import GLib

CONFIG_FILE = "pearos-chimesrc"

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

def play_chime(group):
    path = read_config(group, "Sound", "")
    volume = int(read_config(group, "Volume", "100"))
    if not path or not os.path.isfile(path):
        return
    vol_raw = int(65536 * volume / 100)
    subprocess.Popen(["paplay", "--volume", str(vol_raw), path])

def on_active_changed(locked):
    if locked:
        play_chime("LockIn")
    else:
        play_chime("LockOut")

DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
bus.add_signal_receiver(
    on_active_changed,
    dbus_interface="org.freedesktop.ScreenSaver",
    signal_name="ActiveChanged"
)

loop = GLib.MainLoop()
loop.run()
