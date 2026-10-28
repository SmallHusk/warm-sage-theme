# Warm Sage Niri desktop

Muted taupe-brown backgrounds and cream text with sage focus and moss selections.
The laptop panel uses its native 1920×1200 resolution at 125% scaling.

## Colors

The same color roles are used by Niri, Waybar, Alacritty, Fuzzel (including
clipboard and session menus), swaync, SwayOSD, Blueman, and Swaylock.

| Role | Color | Use |
| --- | --- | --- |
| Backdrop | `#29231f` | Overview, lock screen, wallpaper fallback |
| Workspace | `#51483f` | Niri workspace background beneath the wallpaper |
| Background | `#352e29` | Terminal, bar, launcher, notifications |
| Surface | `#403831` | Hover backgrounds, terminal black |
| Outline | `#65594e` | Inactive borders and idle lock indicator |
| Text | `#e8dfd1` | Cream foreground |
| Muted | `#b2a496` | Secondary labels and inactive controls |
| Sage | `#b7c99a` | Focus, matching text, cursor, enabled controls |
| Selection | `#3f4938` | Selected workspace, launcher row, terminal selection |
| Warning | `#d4b477` | Low battery, terminal yellow |
| Error | `#d98478` | Critical battery, urgent notifications, failed unlock |

Terminal blue, magenta, and cyan retain distinct colors for readable command output.
The palette is stored directly in each application's native config format.

Desktop surfaces use subtle transparency: Alacritty's background is 88% opaque,
Waybar and Fuzzel are 90%, and swaync's panel and notification cards are 92%.
Text, icons, and focus accents stay opaque. Adjust `window.opacity` in Alacritty,
the `panel` color in Waybar, the background alpha in Fuzzel, or `--cc-bg` and
`--noti-bg-alpha` in swaync to tune the effect. Niri's Alacritty rule prevents
the focus ring from filling the area behind its transparent background.

Blueman uses the GTK 3 theme in `~/.local/share/themes/Warm-Sage/gtk-3.0/`.
Its application launcher and the `blueman-manager.service` user override both
set `GTK_THEME=Warm-Sage`, including when it is opened from the Bluetooth tray.

Before the brown background adjustment, configs were backed up to
`~/.local/state/niri-backups/20261026-014412-brown/`.
Run `python3 ~/.local/state/niri-backups/20261026-014412-brown/restore.py`
to undo it, then reload the affected desktop components.

## Keyboard shortcuts

`Super` is the Windows key. Punctuation bindings use the Italian layout.

| Shortcut | Action |
| --- | --- |
| Super+S / Super+F1 | Show shortcuts |
| Super+D | Applications |
| Super+Alt+V | Clipboard history |
| Super+T / Super+Enter | Alacritty terminal |
| Super+E | Files |
| Super+P | Session and power menu |
| Super+Alt+L | Lock |
| Super+N | Toggle notification center |
| Super+Shift+N | Hide notification popups (keep in center) |
| Super+Ctrl+N | Toggle do not disturb |
| Super+Shift+S | Screenshot, then annotate in Satty |
| Super+Alt+A | Annotate a copied image in Satty |
| Super+Tab | Previous workspace |
| Super+1…9 | Workspace by number |
| Super+arrows / H J K L | Focus windows |
| Super+Ctrl+arrows | Move windows/columns |
| Super+Alt+Left/Right | Move window into/out of adjacent column |
| Super+plus/minus | Adjust column width |
| Super+Shift+plus/minus | Adjust window height |
| Super+R | Cycle column widths |
| Super+F / Super+Shift+F | Maximize column / fullscreen |
| Super+V | Toggle floating |
| Super+W | Toggle tabbed column |

## Bar controls

The bar has three floating groups: workspaces and current media on the left,
the clock in the center, and system controls on the right. The current window
title is shortened to keep space for music. The media widget follows the active
MPRIS player (including supported browsers), hides when no player is available,
and dims when paused. Click it to play/pause, right-click for the next track,
or middle-click for the previous track. Hover for the full title and artist.

The previous bar layout is backed up in
`~/.local/state/niri-backups/20261026-020547-bar-layout/`.

- Circle: applications. Workspace numbers: switch workspace.
- Discord/Vesktop and Slack use sage icons from
  `~/.local/share/icons/hicolor/scalable/apps/`, mapped by Waybar's `tray.icons`.
  Blueman uses its native symbolic icons, colored sage by the tray CSS.
  Messaging icon replacements can hide embedded badges; notifications remain
  available in swaync. See `~/.config/waybar/WARM-SAGE-ICONS.md` for setup details.
- Eye: keep awake; inhibits idle timeouts while enabled.
- Bell: open notification center. Right-click: toggle do not disturb. Middle-click: hide popups.
- Network: open connection settings.
- Brightness: scroll to adjust in 5% steps, with a minimum of one backlight unit.
- Volume: click for sound settings; right-click to mute; scroll to adjust.
- Battery: click for remaining time, battery health, power draw, and power profiles.
- Clock: click to toggle the month calendar; hover for the full date.
- Weather beside the clock: click for Rome's forecast; right-click to refresh.
- Lock and power icons: lock or open the session menu.

## Desktop services

`niri-desktop.target` starts the bar, notifications, on-screen indicators, background, idle manager,
authorization agent, and clipboard history with Niri. It is enabled only for the Niri session.
Screen locking occurs after 10 idle minutes, display power-off after 15.
Suspend locks first. Restart and power-off require confirmation in the menu.

Inspect: `systemctl --user status niri-desktop.target niri-*.service waybar.service`

Restart the bar: `systemctl --user restart waybar.service`

Reload notifications: `systemctl --user reload swaync.service`

The Waybar bell opens the swaync notification center. Right-click toggles do not disturb;
middle-click hides popups while keeping them in the center.

Swaync's Warm Sage theme is in `~/.config/swaync/style.css`; panel dimensions,
spacing, and notification timeouts are in `~/.config/swaync/config.json`.
The theme imports swaync's default layout and overrides its colors and controls.
After editing either file, use the reload command above.

SwayOSD displays volume, microphone mute, brightness, and playback indicators
through the media keys. Its translucent Warm Sage style and behavior are in
`~/.config/swayosd/`. Restart it with `systemctl --user restart niri-osd.service`.
Volume keys use 10% steps with a 100% cap; laptop brightness keys use 5% steps
with a 1% minimum. The optional system-wide libinput backend is not used.

The battery popup uses UPower and Fedora's existing TuneD/PPD power-profile API.
It offers Power Saver, Balanced, and Performance when supported. Profile changes
happen only when selected in the panel. Click the battery again, Escape, or the
close button to dismiss it. Styling is in `~/.config/niri/power.css`.
`niri-battery.service` sends low-battery notifications at 20% and critical
notifications at 10%, once per level until charging or recovery above 25%.
Thresholds and polling are in `~/.config/niri/power.json`; the helper is
`~/.config/niri/scripts/power-panel`. Existing system critical-power actions and
idle/locking policies are managed by UPower and swayidle respectively.

Click the clock to toggle a Warm Sage calendar with Monday-first weeks,
ISO week numbers, month navigation, and a highlight for today. Select a day
to see its details; the copy button copies it as YYYY-MM-DD. Today or Home
returns to the current date; Page Up/Down changes month; Escape closes the panel.
Its script is `~/.config/niri/scripts/calendar-panel`, and its styling is in
`~/.config/niri/calendar.css`. Opening calendar or weather closes the other panel.

The weather icon shows Rome's current conditions and temperature in Celsius.
Click it to toggle a Warm Sage panel with current conditions, six upcoming hours,
and a five-day forecast. Escape or the close button dismisses the panel.
Data from Open-Meteo refreshes every ten minutes and is cached for offline use;
old data is marked as cached. The city and coordinates are in `~/.config/niri/weather.json`,
the panel styling is in `~/.config/niri/weather.css`, and the integration is
`~/.config/niri/scripts/weather`. Wind speed is shown in km/h.

Niri reloads its config automatically. New app windows pick up decoration changes.
The Alacritty theme is in `~/.config/alacritty/alacritty.toml`.
Launcher, lock, and idle settings are in `~/.config/fuzzel`, `~/.config/swaylock`,
and `~/.config/swayidle`.

## Lock screen wallpaper

The lock screen uses the current desktop wallpaper, with the same fill scaling.
Super+Alt+L, the bar lock button, the session menu, idle locking, and locking
before suspend all use `~/.config/niri/scripts/lock-screen`. It reads the image
recorded by the wallpaper rotator each time you lock, so future wallpaper
changes apply automatically. If the record or image is missing, the lock screen
uses its muted brown background. The cream and sage unlock indicator is retained.

The previous lock setup is backed up in
`~/.local/state/niri-backups/20261026-020910-lock-wallpaper/`.

## Restore

The previous configuration is backed up in:

`~/.local/state/niri-backups/20261025-182150/`

Run its `restore.py` from a terminal to restore the previous configuration.
Installed packages are retained.

## Clipboard history

Super+Alt+V opens the themed clipboard picker. Choose an item and press Enter,
then paste normally. Escape leaves the current clipboard unchanged.
The Niri clipboard service stores up to 250 copied items, including images.
It starts with the Niri session. Existing GNOME clipboard history is separate.

## Satty image annotation

Niri screenshots open automatically in Satty after capture. Cancelling the
screenshot picker does not open an editor. Print, Ctrl+Print, and Alt+Print
keep their screenshot actions and also open Satty after capture.

For an image copied from another app, press Super+Alt+A, or launch
"Satty Clipboard" from the application launcher. For an older image,
choose it from Super+Alt+V clipboard history, then press Super+Alt+A.

In Satty, Enter copies the edited image and closes. Escape exits without
copying changes. Ctrl+S saves an annotated PNG in ~/Pictures/Screenshots
with a separate filename, preserving the original screenshot.

Screenshot integration is managed by niri-satty.service.

## Wallpaper rotation

Images are selected randomly from ~/Pictures/wallpapers (including subfolders).
A wallpaper is chosen at Niri startup and then every 30 minutes. The previous
image is avoided when multiple images are available. Images fill the screen.
With one image it stays selected; an empty or missing folder uses the brown
background. Add PNG, JPEG, WebP, GIF, BMP, TIFF, or SVG files to the folder.

Change now: `systemctl --user start niri-wallpaper-rotate.service`

Adjust the interval in ~/.config/systemd/user/niri-wallpaper-rotate.timer,
then run `systemctl --user daemon-reload` and
`systemctl --user restart niri-wallpaper-rotate.timer`.

See the next change: `systemctl --user list-timers niri-wallpaper-rotate.timer`
