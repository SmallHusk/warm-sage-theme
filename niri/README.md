# Warm Sage for niri

The working Fedora 44 desktop configuration: translucent brown backgrounds,
cream text, and sage accents. Files under `home/` mirror their locations in the
user's home directory and retain executable permissions for the helper scripts.

## Included

| Component | Configuration |
| --- | --- |
| Niri | Window layout, focus borders, rounded corners, shortcuts |
| Waybar | Bar layout, styles, media controls, notifications, weather |
| Alacritty and Fuzzel | Terminal, application launcher, clipboard and session menus |
| swaync | Notification popups, history panel, do not disturb |
| SwayOSD | Volume, microphone, brightness, and playback overlays |
| Blueman | GTK 3 theme, application launcher, and service theme override |
| Weather | Rome icon and forecast panel, Open-Meteo client, offline cache logic |
| Swaylock and Swayidle | Themed locking, display power management, wallpaper integration |
| Satty | Screenshot and clipboard image annotation |
| systemd user units | Desktop startup, clipboard history, authorization dialogs, wallpaper rotation |

The desktop operation guide is [home/.config/niri/README.md](home/.config/niri/README.md).
It also records the original machine's backup locations.

## Install

This is a snapshot of a configured laptop. Review the defaults below and back up
the corresponding existing files before copying them. Run from this directory:

```sh
cp -a home/. "$HOME/"
systemctl --user daemon-reload
systemctl --user enable niri-desktop.target
systemctl --user mask --now mako.service
```

Log into a niri session to start its desktop components. From an existing niri
session, `systemctl --user start niri-desktop.target` starts the bundle immediately.
The mask prevents mako from competing with swaync for notifications.

The core packages used by this setup are niri, Waybar, Fuzzel, Alacritty,
SwayNotificationCenter, SwayOSD, swaybg, swaylock, swayidle, cliphist,
wl-clipboard, Satty, playerctl, brightnessctl, Blueman, pavucontrol,
network-manager-applet, mate-polkit, libnotify, and fd-find. The weather panel
also needs Python 3, python3-requests, python3-gobject, gtk4, and gtk4-layer-shell
with its introspection bindings. Fonts are Adwaita Sans, Adwaita Mono, and
Font Awesome 6 Free, including the Solid face.

The niri session also uses xwayland-satellite, xdg-desktop-portal-gtk,
xdg-desktop-portal-gnome, gnome-keyring, and Nautilus. Package availability and
third-party repository configuration depend on the Fedora release. SwayOSD's
optional system input backend is not needed by this setup's key bindings.

## Machine defaults

- Niri's laptop output is `eDP-1`, at 1920×1200 and 125% scaling.
- The brightness device is `amdgpu_bl1`; Waybar uses battery `BAT1`.
- The authorization agent path is `/usr/libexec/polkit-mate-authentication-agent-1`.
- Wallpaper images come from `~/Pictures/wallpapers` and rotate every 30 minutes.
- Weather uses Rome, Italy, Celsius, and km/h. Edit
  [home/.config/niri/weather.json](home/.config/niri/weather.json) for another location.
- Three captured files contain `/home/lorenzo`: SwayOSD's CSS path, the wallpaper
  helper's image folder, and the Satty Clipboard desktop launcher's executable.
  Update these paths if installing under another username.
- Niri's `Mod` shortcuts use the existing keyboard layout; punctuation shortcuts
  were configured with an Italian layout.

Desktop panels, the launcher, and the terminal have transparent backgrounds;
normal application windows retain their own rendering. The Blueman GTK theme
is applied through its launcher and user-service override.

## Update the snapshot

After editing the live desktop, run from the repository root:

```sh
python3 niri/sync.py
python3 niri/sync.py --check
git diff -- niri/
```

[files.txt](files.txt) is the explicit list of files to capture. Add new desktop
components there before syncing. The sync command preserves the current file
contents and executable bits; it does not install configs or change services.
Desktop files are maintained in their native formats and are separate from the
editor/browser theme generator.

Only the listed configuration and helper files are included. Weather responses,
clipboard history, wallpapers, local backup archives, runtime state, and service
enablement symlinks are not part of the snapshot. Installation recreates the
target enablement and mako mask with systemctl.

## Weather controls

The condition icon and temperature sit beside the clock. Click to toggle the
forecast panel; right-click to refresh. The panel shows current conditions,
six upcoming hours, and five forecast days. Escape or its close button dismisses
it. Data from [Open-Meteo](https://open-meteo.com/) refreshes every ten minutes,
and saved forecasts remain available offline with a cached-data indication.
The panel's appearance is in `home/.config/niri/weather.css`.
