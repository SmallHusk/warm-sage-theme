# Warm Sage for Firefox

A dark Firefox theme with muted brown surfaces, cream text, and sage accents.
Coordinates tabs, the toolbar and address bar, menus, the sidebar, and the new-tab
page with the matching Zed and VS Code themes. Uses Firefox's dark color scheme.

This is a static theme with no scripts, browser permissions, or data collection.
It styles browser UI; individual websites control their own colors.

## Try locally

1. Open `about:debugging#/runtime/this-firefox` in Firefox 100 or newer.
2. Choose **Load Temporary Add-on…** and select this directory's `manifest.json`.
3. If needed, open `about:addons`, choose **Themes**, and enable **Warm Sage**.

Temporary installation lasts until Firefox restarts. After changing the palette,
run `npm run build` from the repository root and reload the theme in
`about:debugging`.

## Install permanently

Once published on [Firefox Add-ons](https://addons.mozilla.org/), install
**Warm Sage** by **smallhusk** there. For a self-distributed release, open
`about:addons`, choose the gear menu's **Install Add-on From File…**, and select
the Mozilla-signed `.xpi`.

`npm run package` creates `dist/warm-sage-firefox-1.0.0.zip` for submission to
Mozilla. This local ZIP is unsigned; normal Firefox releases require Mozilla
signing for permanent installation. See [Mozilla's signing guide](https://extensionworkshop.com/documentation/publish/signing-and-distribution-overview/).

## Source and feedback

The shared palette, editor themes, and build tools live in the
[Warm Sage repository](https://github.com/SmallHusk/warm-sage-theme).
Please report problems through its issue tracker, including your Firefox version
and a screenshot when possible.

## License

MIT. Copyright (c) 2026 smallhusk.
