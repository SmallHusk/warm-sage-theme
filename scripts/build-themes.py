#!/usr/bin/env python3
"""Build matching editor themes and public extension manifests."""
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
M = json.loads((ROOT / "release.json").read_text())
P = json.loads((ROOT / 'palette.json').read_text())
base, surface, backdrop = P['base'], P['surface'], P['backdrop']
text, muted, outline = P['text'], P['muted'], P['outline']
sage, red, amber = P['sage'], P['red'], P['warning']
blue, mauve, cyan = P['ansi']['normal']['blue'], P['ansi']['bright']['magenta'], P['ansi']['bright']['cyan']
selection = P['selection'] + '80'


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


z = {
    'background': base, 'background.appearance': 'opaque',
    'surface.background': surface, 'elevated_surface.background': surface,
    'border': outline, 'border.variant': surface, 'border.focused': sage,
    'border.selected': sage, 'border.transparent': '#00000000', 'border.disabled': surface,
    'text': text, 'text.muted': muted, 'text.placeholder': muted,
    'text.disabled': P['ansi']['bright']['black'], 'text.accent': sage,
    'icon': P['icon'], 'icon.muted': muted, 'icon.placeholder': muted,
    'icon.disabled': P['ansi']['bright']['black'], 'icon.accent': sage,
    'element.background': surface, 'element.hover': outline + '60',
    'element.active': P['selection_solid'], 'element.selected': P['selection_solid'],
    'element.disabled': backdrop,
    'ghost_element.background': '#00000000', 'ghost_element.hover': surface,
    'ghost_element.active': P['selection_solid'], 'ghost_element.selected': P['selection_solid'],
    'ghost_element.disabled': backdrop, 'drop_target.background': sage + '25',
    'title_bar.background': backdrop, 'title_bar.inactive_background': backdrop,
    'toolbar.background': base, 'status_bar.background': backdrop,
    'tab_bar.background': backdrop, 'tab.active_background': base,
    'tab.inactive_background': backdrop, 'panel.background': backdrop,
    'panel.focused_border': sage, 'panel.indent_guide': outline + '80',
    'panel.indent_guide_active': sage + '80', 'panel.indent_guide_hover': outline,
    'pane.focused_border': sage, 'pane_group.border': outline,
    'editor.foreground': text, 'editor.background': base, 'editor.gutter.background': base,
    'editor.subheader.background': surface, 'editor.active_line.background': surface,
    'editor.highlighted_line.background': sage + '18',
    'editor.line_number': P['ansi']['bright']['black'], 'editor.active_line_number': sage,
    'editor.invisible': outline, 'editor.wrap_guide': outline + '70',
    'editor.active_wrap_guide': outline, 'editor.indent_guide': outline + '80',
    'editor.indent_guide_active': sage + '80',
    'editor.document_highlight.read_background': sage + '20',
    'editor.document_highlight.write_background': amber + '25',
    'editor.document_highlight.bracket_background': sage + '30',
    'scrollbar.thumb.background': outline + 'a0', 'scrollbar.thumb.hover_background': outline,
    'scrollbar.thumb.border': '#00000000', 'scrollbar.track.background': '#00000000',
    'scrollbar.track.border': '#00000000', 'search.match_background': amber + '40',
    'link_text.hover': sage, 'terminal.background': base, 'terminal.foreground': text,
    'terminal.bright_foreground': P['ansi']['bright']['white'], 'terminal.dim_foreground': muted,
    'terminal.ansi.background': base,
    'accents': [sage, blue, amber, mauve, cyan, red],
    'players': [{'cursor': sage, 'background': sage, 'selection': selection}],
}
for role, color in {
    'error': red, 'warning': amber, 'info': blue, 'hint': muted, 'success': sage,
    'created': sage, 'modified': amber, 'deleted': red, 'renamed': cyan,
    'conflict': mauve, 'hidden': muted, 'ignored': muted, 'unreachable': muted,
    'predictive': muted,
}.items():
    z.update({role: color, role + '.background': color + '18', role + '.border': color + '80'})
for name, color in P['ansi']['normal'].items():
    z['terminal.ansi.' + name] = color
for name, color in P['ansi']['bright'].items():
    z['terminal.ansi.bright_' + name] = color

syntax = {
    'attribute': amber, 'boolean': amber, 'comment': muted, 'comment.doc': muted,
    'constant': amber, 'constructor': blue, 'embedded': text, 'emphasis': text,
    'emphasis.strong': text, 'enum': blue, 'function': sage, 'function.builtin': sage,
    'function.method': sage, 'function.macro': cyan, 'hint': muted, 'keyword': mauve,
    'keyword.control': mauve, 'keyword.function': mauve, 'keyword.operator': cyan,
    'keyword.return': mauve, 'label': amber, 'link_text': sage, 'link_uri': blue,
    'namespace': blue, 'number': amber, 'operator': cyan, 'parameter': P['icon'],
    'preproc': mauve, 'property': P['icon'], 'punctuation': muted,
    'punctuation.bracket': text, 'punctuation.delimiter': muted,
    'punctuation.list_marker': sage, 'punctuation.special': cyan,
    'string': sage, 'string.escape': cyan, 'string.regex': amber,
    'string.special': cyan, 'string.special.symbol': amber, 'tag': sage,
    'text.literal': sage, 'title': sage, 'type': blue, 'type.builtin': blue,
    'variable': text, 'variable.builtin': mauve, 'variable.special': mauve,
    'variant': blue,
}
z['syntax'] = {name: {'color': color} for name, color in syntax.items()}
for name in ['comment', 'comment.doc', 'emphasis']:
    z['syntax'][name]['font_style'] = 'italic'
for name in ['emphasis.strong', 'title']:
    z['syntax'][name]['font_weight'] = 700
write_json(ROOT / 'zed/themes/warm-sage.json', {
    '$schema': 'https://zed.dev/schema/themes/v0.2.0.json',
    'name': 'Warm Sage', 'author': M['author'],
    'themes': [{'name': 'Warm Sage', 'appearance': 'dark', 'style': z}],
})

v = {
    'foreground': text, 'descriptionForeground': muted, 'disabledForeground': muted,
    'errorForeground': red, 'focusBorder': sage, 'icon.foreground': P['icon'],
    'selection.background': selection, 'widget.border': outline,
    'widget.shadow': '#00000050',
    'textLink.foreground': sage, 'textLink.activeForeground': P['ansi']['bright']['green'],
    'textBlockQuote.background': surface, 'textBlockQuote.border': sage,
    'textCodeBlock.background': backdrop, 'textPreformat.foreground': sage,
    'textPreformat.background': surface, 'textSeparator.foreground': outline,
    'button.background': sage, 'button.foreground': base,
    'button.hoverBackground': P['ansi']['bright']['green'],
    'button.secondaryBackground': surface, 'button.secondaryForeground': text,
    'button.secondaryHoverBackground': outline,
    'badge.background': P['selection_solid'], 'badge.foreground': text,
    'progressBar.background': sage,
    'input.background': backdrop, 'input.foreground': text,
    'input.border': outline, 'input.placeholderForeground': muted,
    'inputOption.activeBackground': P['selection_solid'],
    'inputOption.activeBorder': sage, 'inputOption.activeForeground': text,
    'dropdown.background': surface, 'dropdown.foreground': text,
    'dropdown.border': outline, 'dropdown.listBackground': surface,
    'list.activeSelectionBackground': P['selection_solid'], 'list.activeSelectionForeground': text,
    'list.activeSelectionIconForeground': sage,
    'list.inactiveSelectionBackground': surface, 'list.inactiveSelectionForeground': text,
    'list.hoverBackground': surface, 'list.hoverForeground': text,
    'list.focusBackground': P['selection_solid'], 'list.focusForeground': text,
    'list.focusOutline': sage, 'list.highlightForeground': sage,
    'list.focusHighlightForeground': P['ansi']['bright']['green'],
    'list.errorForeground': red, 'list.warningForeground': amber,
    'tree.indentGuidesStroke': outline, 'tree.inactiveIndentGuidesStroke': outline + '80',
    'activityBar.background': backdrop, 'activityBar.foreground': sage,
    'activityBar.inactiveForeground': muted, 'activityBar.border': outline,
    'activityBar.activeBorder': sage, 'activityBarBadge.background': sage,
    'activityBarBadge.foreground': base, 'activityBarTop.foreground': sage,
    'activityBarTop.inactiveForeground': muted, 'activityBarTop.activeBorder': sage,
    'sideBar.background': backdrop, 'sideBar.foreground': text,
    'sideBar.border': outline, 'sideBarTitle.foreground': text,
    'sideBarSectionHeader.background': surface, 'sideBarSectionHeader.foreground': text,
    'sideBarSectionHeader.border': outline,
    'titleBar.activeBackground': backdrop, 'titleBar.activeForeground': text,
    'titleBar.inactiveBackground': backdrop, 'titleBar.inactiveForeground': muted,
    'titleBar.border': outline, 'commandCenter.background': surface,
    'commandCenter.foreground': muted, 'commandCenter.border': outline,
    'editorGroupHeader.tabsBackground': backdrop, 'editorGroupHeader.tabsBorder': outline,
    'editorGroup.border': outline, 'editorGroup.dropBackground': sage + '25',
    'tab.activeBackground': base, 'tab.activeForeground': text,
    'tab.activeBorderTop': sage, 'tab.activeBorder': base,
    'tab.inactiveBackground': backdrop, 'tab.inactiveForeground': muted,
    'tab.unfocusedActiveBackground': base, 'tab.unfocusedActiveForeground': muted,
    'tab.border': backdrop, 'tab.hoverBackground': surface,
    'tab.unfocusedHoverBackground': surface,
    'editor.background': base, 'editor.foreground': text,
    'editorCursor.foreground': sage, 'editorCursor.background': base,
    'editorLineNumber.foreground': P['ansi']['bright']['black'],
    'editorLineNumber.activeForeground': sage,
    'editor.lineHighlightBackground': surface, 'editor.lineHighlightBorder': '#00000000',
    'editor.selectionBackground': selection, 'editor.selectionForeground': text,
    'editor.inactiveSelectionBackground': P['selection'] + '50',
    'editor.selectionHighlightBackground': sage + '20',
    'editor.wordHighlightBackground': sage + '20',
    'editor.wordHighlightStrongBackground': amber + '25',
    'editor.findMatchBackground': amber + '50', 'editor.findMatchBorder': amber,
    'editor.findMatchHighlightBackground': amber + '25',
    'editor.findRangeHighlightBackground': sage + '15',
    'editorWhitespace.foreground': outline, 'editorRuler.foreground': outline + '80',
    'editorIndentGuide.background1': outline + '80', 'editorIndentGuide.activeBackground1': sage + '80',
    'editorBracketMatch.background': sage + '25', 'editorBracketMatch.border': sage,
    'editorBracketHighlight.foreground1': sage, 'editorBracketHighlight.foreground2': blue,
    'editorBracketHighlight.foreground3': amber, 'editorBracketHighlight.foreground4': mauve,
    'editorBracketHighlight.foreground5': cyan, 'editorBracketHighlight.foreground6': P['icon'],
    'editorBracketHighlight.unexpectedBracket.foreground': red,
    'editorError.foreground': red, 'editorWarning.foreground': amber,
    'editorInfo.foreground': blue, 'editorHint.foreground': muted,
    'editorGutter.background': base, 'editorGutter.addedBackground': sage,
    'editorGutter.modifiedBackground': amber, 'editorGutter.deletedBackground': red,
    'diffEditor.insertedTextBackground': sage + '20', 'diffEditor.removedTextBackground': red + '20',
    'diffEditor.insertedLineBackground': sage + '10', 'diffEditor.removedLineBackground': red + '10',
    'editorWidget.background': surface, 'editorWidget.foreground': text,
    'editorWidget.border': outline, 'editorSuggestWidget.background': surface,
    'editorSuggestWidget.foreground': text, 'editorSuggestWidget.border': outline,
    'editorSuggestWidget.selectedBackground': P['selection_solid'],
    'editorSuggestWidget.selectedForeground': text, 'editorSuggestWidget.highlightForeground': sage,
    'editorHoverWidget.background': surface, 'editorHoverWidget.foreground': text,
    'editorHoverWidget.border': outline, 'editorHoverWidget.statusBarBackground': backdrop,
    'editorGhostText.foreground': muted + 'a0',
    'editorInlayHint.background': surface, 'editorInlayHint.foreground': muted,
    'peekView.border': sage, 'peekViewEditor.background': base,
    'peekViewResult.background': backdrop, 'peekViewTitle.background': surface,
    'peekViewTitleLabel.foreground': text, 'peekViewTitleDescription.foreground': muted,
    'panel.background': backdrop, 'panel.border': outline,
    'panelTitle.activeForeground': sage, 'panelTitle.activeBorder': sage,
    'panelTitle.inactiveForeground': muted,
    'statusBar.background': backdrop, 'statusBar.foreground': text,
    'statusBar.border': outline, 'statusBar.noFolderBackground': backdrop,
    'statusBar.noFolderForeground': text, 'statusBar.debuggingBackground': P['selection_solid'],
    'statusBar.debuggingForeground': text, 'statusBarItem.hoverBackground': surface,
    'statusBarItem.remoteBackground': P['selection_solid'], 'statusBarItem.remoteForeground': text,
    'statusBarItem.prominentBackground': surface, 'statusBarItem.prominentForeground': sage,
    'terminal.background': base, 'terminal.foreground': text,
    'terminalCursor.foreground': sage, 'terminalCursor.background': base,
    'terminal.selectionBackground': P['selection_solid'], 'terminal.selectionForeground': text,
    'terminal.border': outline, 'terminalCommandDecoration.successBackground': sage,
    'terminalCommandDecoration.errorBackground': red,
    'scrollbarSlider.background': outline + '80', 'scrollbarSlider.hoverBackground': outline + 'c0',
    'scrollbarSlider.activeBackground': muted + '90',
    'minimap.selectionHighlight': sage + '70', 'minimap.findMatchHighlight': amber,
    'minimap.errorHighlight': red, 'minimap.warningHighlight': amber,
    'notifications.background': surface, 'notifications.foreground': text,
    'notifications.border': outline, 'notificationCenterHeader.background': backdrop,
    'notificationCenterHeader.foreground': text, 'notificationLink.foreground': sage,
    'notificationsErrorIcon.foreground': red, 'notificationsWarningIcon.foreground': amber,
    'notificationsInfoIcon.foreground': blue,
    'menu.background': surface, 'menu.foreground': text, 'menu.border': outline,
    'menu.selectionBackground': P['selection_solid'], 'menu.selectionForeground': text,
    'menu.separatorBackground': outline,
    'quickInput.background': surface, 'quickInput.foreground': text,
    'quickInputTitle.background': backdrop,
    'pickerGroup.foreground': sage, 'pickerGroup.border': outline,
    'breadcrumb.foreground': muted, 'breadcrumb.focusForeground': sage,
    'breadcrumb.activeSelectionForeground': text, 'breadcrumb.background': base,
    'breadcrumbPicker.background': surface,
    'gitDecoration.addedResourceForeground': sage, 'gitDecoration.modifiedResourceForeground': amber,
    'gitDecoration.deletedResourceForeground': red, 'gitDecoration.renamedResourceForeground': cyan,
    'gitDecoration.untrackedResourceForeground': sage, 'gitDecoration.ignoredResourceForeground': muted,
    'gitDecoration.conflictingResourceForeground': mauve,
    'gitDecoration.stageModifiedResourceForeground': amber,
    'gitDecoration.stageDeletedResourceForeground': red,
    'settings.headerForeground': sage, 'settings.modifiedItemIndicator': amber,
    'settings.dropdownBackground': surface, 'settings.textInputBackground': backdrop,
    'settings.numberInputBackground': backdrop,
    'debugToolBar.background': surface, 'debugToolBar.border': outline,
    'welcomePage.background': base, 'welcomePage.tileBackground': surface,
    'welcomePage.tileHoverBackground': outline,
    'chat.requestBackground': surface, 'chat.requestBorder': outline,
    'chat.slashCommandForeground': sage, 'chat.slashCommandBackground': sage + '20',
}
for family, prefix in [('normal', 'ansi'), ('bright', 'ansiBright')]:
    for name, color in P['ansi'][family].items():
        v['terminal.' + prefix + name.capitalize()] = color
for role, color in [('error', red), ('warning', amber), ('info', blue)]:
    v[f'inputValidation.{role}Background'] = surface
    v[f'inputValidation.{role}Border'] = color
    v[f'inputValidation.{role}Foreground'] = text

rules = []


def token(name, scopes, color, style=None):
    settings = {'foreground': color}
    if style is not None:
        settings['fontStyle'] = style
    rules.append({'name': name, 'scope': scopes, 'settings': settings})


token('Comments', ['comment', 'punctuation.definition.comment'], muted, 'italic')
token('Keywords and storage', ['keyword', 'storage.type', 'storage.modifier'], mauve)
token('Operators', ['keyword.operator'], cyan)
token('Strings', ['string'], sage)
token('Escapes and interpolation delimiters', ['constant.character.escape', 'punctuation.section.interpolation'], cyan)
token('Numbers, booleans and constants', ['constant.numeric', 'constant.language', 'constant.other', 'variable.other.constant', 'support.constant'], amber)
token('Functions and methods', ['entity.name.function', 'support.function', 'variable.function'], sage)
token('Types, classes and namespaces', ['entity.name.type', 'entity.name.class', 'entity.name.namespace', 'support.type', 'support.class'], blue)
token('Variables', ['variable', 'meta.definition.variable.name'], text)
token('Parameters and properties', ['variable.parameter', 'variable.other.property', 'support.variable.property'], P['icon'])
token('Language variables', ['variable.language'], mauve)
token('Attributes and annotations', ['entity.other.attribute-name', 'meta.annotation', 'entity.name.function.decorator'], amber)
token('Tags', ['entity.name.tag'], sage)
token('Punctuation', ['punctuation'], muted)
token('Brackets', ['punctuation.section', 'punctuation.definition.tag'], text)
token('Regex', ['string.regexp'], amber)
token('JSON object keys', ['support.type.property-name.json', 'support.type.property-name.jsonc'], P['icon'])
token('Markup headings', ['markup.heading', 'entity.name.section'], sage, 'bold')
token('Markup emphasis', ['markup.italic'], text, 'italic')
token('Markup strong', ['markup.bold'], text, 'bold')
token('Markup links', ['markup.underline.link', 'string.other.link'], blue)
token('Markup code', ['markup.inline.raw', 'markup.raw'], sage)
token('Diff additions', ['markup.inserted'], sage)
token('Diff deletions', ['markup.deleted'], red)
token('Diff changes', ['markup.changed'], amber)
token('Invalid syntax', ['invalid', 'invalid.illegal'], red)

semantic = {
    'namespace': blue, 'type': blue, 'class': blue, 'enum': blue,
    'interface': blue, 'struct': blue, 'typeParameter': blue,
    'parameter': P['icon'], 'variable': text, 'property': P['icon'],
    'enumMember': amber, 'event': sage, 'function': sage, 'method': sage,
    'macro': cyan, 'keyword': mauve, 'modifier': mauve, 'comment': {'foreground': muted, 'italic': True},
    'string': sage, 'number': amber, 'regexp': amber, 'operator': cyan,
    'decorator': amber, '*.readonly': amber, '*.defaultLibrary': blue,
    'function.defaultLibrary': sage, 'method.defaultLibrary': sage,
}
write_json(ROOT / 'vscode/themes/warm-sage-color-theme.json', {
    '$schema': 'vscode://schemas/color-theme', 'name': 'Warm Sage', 'type': 'dark',
    'semanticHighlighting': True, 'colors': v, 'tokenColors': rules, 'semanticTokenColors': semantic,
})

write_json(ROOT / 'vscode/package.json', {
    'name': M['name'], 'displayName': M['displayName'], 'version': M['version'],
    'description': 'Muted brown surfaces, cream text, and sage accents for a warm, readable editor.',
    'publisher': M['publisher'], 'author': {'name': M['author']},
    'engines': {'vscode': '^1.95.0'}, 'categories': ['Themes'],
    'keywords': ['brown', 'sage', 'warm', 'dark', 'muted', 'earthy'],
    'license': M['license'], 'extensionKind': ['ui'], 'pricing': 'Free',
    'icon': 'assets/icon.png', 'galleryBanner': {'color': base, 'theme': 'dark'},
    'repository': {'type': 'git', 'url': M['repository'] + '.git', 'directory': 'vscode'},
    'homepage': M['repository'] + '#readme', 'bugs': {'url': M['repository'] + '/issues'},
    'contributes': {'themes': [{'label': M['displayName'], 'uiTheme': 'vs-dark', 'path': './themes/warm-sage-color-theme.json'}]},
})

(ROOT / 'zed/extension.toml').write_text('\n'.join([
    f'id = {json.dumps(M["zedId"])}', f'name = {json.dumps(M["displayName"])}',
    f'version = {json.dumps(M["version"])}', 'schema_version = 1',
    f'authors = [{json.dumps(M["author"])}]',
    'description = "Muted brown surfaces, cream text, and sage accents."',
    f'repository = {json.dumps(M["repository"])}', '',
]))
for package in ['vscode', 'zed']:
    for name in ['LICENSE', 'CHANGELOG.md']:
        shutil.copy2(ROOT / name, ROOT / package / name)
    assets = ROOT / package / 'assets'
    assets.mkdir(exist_ok=True)
    for name in ['icon.png', 'preview.png']:
        shutil.copy2(ROOT / 'assets' / name, assets / name)
print('Built Zed and VS Code themes and synchronized release metadata.')
