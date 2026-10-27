# Warm Sage

Matching dark themes for **Zed**, **Visual Studio Code**, **Firefox**, and a
coordinated **niri desktop**.
Muted brown surfaces, cream text, sage accents, and soft syntax colors.

![Warm Sage palette and syntax preview](assets/preview.png)

This preview illustrates the palette and syntax colors, rather than showing an
editor screenshot. Actual token assignments depend on the language grammar and
language server.

## Palette

| Role | Color |
| --- | --- |
| Editor background | `#352e29` |
| Sidebar and title bar | `#29231f` |
| Raised surfaces | `#403831` |
| Cream text | `#e8dfd1` |
| Muted text and comments | `#b2a496` |
| Sage accents, strings, and functions | `#b7c99a` |
| Mauve keywords | `#ceb2c1` |
| Dusty blue types | `#91a7b0` |
| Amber numbers and warnings | `#d4b477` |
| Terracotta diagnostics | `#c09086` |

Syntax colors have at least 4.5:1 contrast against the editor background. Both
editor themes include coordinated UI, diagnostics, Git decorations, and sixteen ANSI
terminal colors. VS Code includes TextMate and semantic-token highlighting.
Firefox coordinates tabs, toolbars, address fields, menus, the sidebar, and the
new-tab page using the same palette and a dark color scheme.

## Install

### Visual Studio Code

Download the release's `.vsix`, run **Extensions: Install from VSIX...**, and
select it. Then choose **Warm Sage** in **Preferences: Color Theme**.

Once published on the Marketplace, search for **Warm Sage** by **smallhusk**.

### Zed

Copy `zed/themes/warm-sage.json` into `~/.config/zed/themes/`, restart Zed,
and select **Warm Sage** using **theme selector: toggle**.

To test the extension manifest, use **Install Dev Extension** in Zed's Extensions
view and select the `zed` directory. Once accepted into Zed's extension registry,
it will also be installable from the Extensions view.

### Firefox

Open `about:debugging#/runtime/this-firefox`, choose **Load Temporary Add-on…**,
and select `firefox/manifest.json`. This works in Firefox 100 or newer and lasts
until Firefox restarts. If needed, enable **Warm Sage** under **Themes** in
`about:addons`.

Permanent installation requires Mozilla signing. Once published, install it
from Firefox Add-ons, or use **Install Add-on From File…** in `about:addons`
with a signed `.xpi`. The ZIP built here is unsigned and intended for submission.
See [firefox/README.md](firefox/README.md) for details.

### Niri desktop

The [niri bundle](niri/README.md) contains the current Fedora desktop configs,
including Waybar, Alacritty, Fuzzel, swaync, SwayOSD, Blueman, weather, locking,
wallpaper rotation, screenshot tools, and supporting user services. Its `home/`
tree mirrors the installation paths. See the bundle's installation notes for
hardware defaults and `python3 niri/sync.py` to capture later desktop changes.

## Build and package

Requires Python 3.11+ and Node.js 22+ for the official VS Code packager.

```sh
npm ci --ignore-scripts
npm run build
npm run check
npm run package
```

The `dist` directory contains the VSIX, Zed extension ZIP, Firefox theme ZIP,
source ZIP, and SHA-256 checksums. The packaging script creates local files only.

For the generated editor and browser themes, `palette.json` contains the shared colors;
`release.json` contains the author,
publisher ID, repository URL, license, and version. Edit these source files and
rebuild instead of changing generated theme files directly.

Rendered PNG artwork is included. Its SVG sources and the optional
`scripts/render-assets.py` renderer are included too; the renderer requires
PyGObject, librsvg, and pycairo. It is not required for normal packaging.

## Publish

See [PUBLISHING.md](PUBLISHING.md) for Marketplace, Zed, and Firefox Add-ons
submission steps.
Repository links target `https://github.com/SmallHusk/warm-sage-theme`; the
repository must be created and made public before submitting the Zed extension.

## License

MIT. Copyright (c) 2026 smallhusk.
