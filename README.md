# Warm Sage

A matching pair of dark themes for **Zed** and **Visual Studio Code**.
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
themes include coordinated UI, diagnostics, Git decorations, and sixteen ANSI
terminal colors. VS Code includes TextMate and semantic-token highlighting.

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

## Build and package

Requires Python 3.11+ and Node.js 22+ for the official VS Code packager.

```sh
npm ci --ignore-scripts
npm run build
npm run check
npm run package
```

The `dist` directory contains the VSIX, Zed extension ZIP, source ZIP, and
SHA-256 checksums. The packaging script creates local files only.

`palette.json` contains the shared colors; `release.json` contains the author,
publisher ID, repository URL, license, and version. Edit these source files and
rebuild instead of changing generated theme files directly.

Rendered PNG artwork is included. Its SVG sources and the optional
`scripts/render-assets.py` renderer are included too; the renderer requires
PyGObject, librsvg, and pycairo. It is not required for normal packaging.

## Publish

See [PUBLISHING.md](PUBLISHING.md) for Marketplace and Zed submission steps.
Repository links target `https://github.com/SmallHusk/warm-sage-theme`; the
repository must be created and made public before submitting the Zed extension.

## License

MIT. Copyright (c) 2026 smallhusk.
