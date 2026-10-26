# Publishing Warm Sage

The packages are prepared for the **smallhusk** author and VS Code publisher ID,
under the **MIT** license. No registry upload or Git push is performed by the
build scripts.

## Release metadata

The intended repository is `https://github.com/SmallHusk/warm-sage-theme`.
Confirm that you own this repository and the Marketplace publisher ID
`smallhusk` before publishing. If either differs, edit `release.json`, update
the corresponding README links, and rebuild. All package manifests are generated
from that metadata.

## Build the release

```sh
npm ci --ignore-scripts
npm run build
npm run check
npm run package
```

Outputs in `dist/`:

- `warm-sage-1.0.0.vsix`: official `@vscode/vsce` package.
- `warm-sage-zed-1.0.0.zip`: Zed extension directory with `extension.toml`.
- `warm-sage-source-1.0.0.zip`: clean, portable source tree.
- `SHA256SUMS`: integrity hashes for those three files.

Before release, install the VSIX in a clean VS Code profile and install the Zed
directory as a dev extension. Inspect code in languages you use, selections,
diagnostics, search, diffs, and terminals. Zed requires manually testing the
specific repository commit submitted to the registry.

For an additional check against Zed's official schema, download
`https://zed.dev/schema/themes/v0.2.0.json`, install Python's `jsonschema` package,
and run `python3 scripts/check.py --zed-schema /path/to/schema.json`.

## VS Code Marketplace

1. Create or select the **smallhusk** publisher in the
   [Marketplace publisher dashboard](https://marketplace.visualstudio.com/manage).
2. Add a new extension and upload `dist/warm-sage-1.0.0.vsix`.
3. Review the displayed publisher, theme name, license, icon, preview, and links,
   then submit it through the dashboard.

The package contains theme data and artwork; it has no executable extension entry
point. Authentication is handled by the publisher dashboard. Never put account
tokens into this repository.

Alternatively, use the official `vsce` publishing workflow after configuring
authentication as described in Microsoft's documentation. `npm run package` never
calls `vsce publish`.

## Zed extension registry

Zed publishes from a public Git repository, rather than a ZIP upload. The ZIP is
useful for distributing and inspecting the exact extension directory.

1. Create the intended public repository, commit this source tree on `main`,
   and push it using the personal Git identity configured for your workspace.
2. Install the repository's `zed` directory as a dev extension and manually test
   the exact commit you will submit.
3. Fork and clone `zed-industries/extensions`.
4. Add the repository as an HTTPS submodule and register the extension:

```sh
git submodule add https://github.com/SmallHusk/warm-sage-theme.git extensions/warm-sage-theme
```

Add this entry to the registry repository's `extensions.toml`:

```toml
[warm-sage-theme]
submodule = "extensions/warm-sage-theme"
path = "zed"
version = "1.0.0"
```

5. Run `pnpm sort-extensions` in that registry checkout.
6. Open a pull request adding this one extension. Zed publishes it after review
   and merge. Its submodule must point to a commit available on a public branch.

The Zed extension ID is `warm-sage-theme`, satisfying the theme-specific naming
rule. The MIT license is present inside `zed/`, as required for a monorepo
subdirectory extension. This package needs no Rust or WebAssembly code.

## Future releases

Update `version` in `release.json` and `package.json`, document the changes in
`CHANGELOG.md`, and rebuild. The builder synchronizes both extension versions and
copies the changelog and license into each package. Use a new version for each
public release. Attach the packages and checksums to the matching GitHub release.

## Official references

- [Microsoft's extension publishing guide](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
- [Zed publishing prerequisites](https://zed.dev/docs/extensions/publishing/prerequisites)
- [Zed publishing guide](https://zed.dev/docs/extensions/publishing/publishing-guide)
- [Zed license requirements](https://zed.dev/docs/extensions/publishing/license-requirements)
