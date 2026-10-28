# Warm Sage tray icons

Discord (including Vesktop), Slack, and Bluetooth use sage-green (`#b7c99a`)
symbols in Waybar. The `tray.icons` map in `config.jsonc` matches the messaging
apps' StatusNotifier IDs. Blueman uses its native symbolic status icons, colored
by `#tray` in `style.css` so its Bluetooth state changes remain visible.
The SVGs are in `~/.local/share/icons/hicolor/scalable/apps/` and are named
`warm-sage-discord`, `warm-sage-slack`, and `warm-sage-bluetooth`.
The Bluetooth SVG is also available for optional static overrides.
The same rune is installed as `hicolor/scalable/status/blueman-tray-symbolic.svg`
for Blueman's normal symbolic state; other Bluetooth state names remain native.

After copying the icons, rebuild the user's icon cache:

```sh
gtk-update-icon-cache --force --ignore-theme-index "$HOME/.local/share/icons/hicolor"
gsettings set org.blueman.general symbolic-status-icons true
systemctl --user restart waybar.service
```

These SVG documents were rendered from the Discord (U+F392), Slack (U+F198),
and Bluetooth B (U+F294) glyphs of Font Awesome Free 6 Brands by Fonticons, Inc.
The artwork was centered in 24×24 view boxes and given a fixed sage fill.
The source font is licensed under SIL Open Font License 1.1; the complete
upstream license and attribution notice is included in `FONT-AWESOME-LICENSE.txt`.
See https://fontawesome.com/license/free for Font Awesome's licensing details.
Brand marks represent their respective applications and belong to their owners.

The messaging icons are fixed. Notification badges drawn into an application's
original icon bitmap can be hidden by the replacement. App notifications still
arrive in swaync. Remove an app's `tray.icons` entry to restore its supplied icon.
