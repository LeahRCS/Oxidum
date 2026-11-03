#!/usr/bin/env python3
from pathlib import Path


def replace(path, old, new):
    p = Path(path)
    text = p.read_text()
    if old not in text:
        raise SystemExit(f"Oxidum overlay: expected text not found in {path}: {old!r}")
    p.write_text(text.replace(old, new))


# Distribution channel and repository-facing links.
replace(
    "launcher/src/backend.rs",
    'pub const LAUNCHER_REPO: &str = "0CYBER/horizon-free";',
    'pub const LAUNCHER_REPO: &str = "LeahRCS/horizon-free";',
)
replace(
    "launcher/src/backend.rs",
    'pub const README_URL: &str = "https://github.com/horizon-rust/horizon/blob/main/launcher/README.md";',
    'pub const README_URL: &str = "https://github.com/LeahRCS/horizon-free";',
)
replace(
    "launcher/src/backend.rs",
    'Some("horizon-launcher-linux-x86_64.AppImage")',
    'Some("oxidum-linux-x86_64.AppImage")',
)

# Visible application brand.
for path in [
    "launcher/src/titlebar.rs",
    "launcher/src/home.rs",
    "launcher/src/setup_page.rs",
]:
    p = Path(path)
    p.write_text(p.read_text().replace("Horizon", "Oxidum"))

p = Path("launcher/src/main.rs")
text = p.read_text()
old_mark = """/// Horizon's mark: two stems, their reflection below, and the horizon across in the accent.
fn mark(size: f32, t: &Theme) -> Div {
    let u = size / 16.;
    let stem = |x: f32, y: f32, color: Hsla| {
        div()
            .absolute()
            .left(px(x * u))
            .top(px(y * u))
            .w(px(2. * u))
            .h(px(4. * u))
            .bg(color)
    };
    div()
        .relative()
        .flex_none()
        .size(px(size))
        .child(stem(4., 3., t.ink))
        .child(stem(10., 3., t.ink))
        .child(stem(4., 8., t.ink.opacity(0.36)))
        .child(stem(10., 8., t.ink.opacity(0.36)))
        .child(
            div()
                .absolute()
                .left(px(u))
                .top(px(7. * u))
                .w(px(14. * u))
                .h(px(u))
                .bg(t.accent),
        )
}"""
new_mark = """/// Oxidum's mark: an O split by the accent line, bright above and reflected below.
fn mark(size: f32, t: &Theme) -> Div {
    let u = size / 16.;
    let bar = |x: f32, y: f32, w: f32, h: f32, color: Hsla| {
        div()
            .absolute()
            .left(px(x * u))
            .top(px(y * u))
            .w(px(w * u))
            .h(px(h * u))
            .bg(color)
    };
    div()
        .relative()
        .flex_none()
        .size(px(size))
        .child(bar(5., 2., 6., 2., t.ink))
        .child(bar(3., 4., 2., 3., t.ink))
        .child(bar(11., 4., 2., 3., t.ink))
        .child(bar(3., 8., 2., 3., t.ink.opacity(0.36)))
        .child(bar(11., 8., 2., 3., t.ink.opacity(0.36)))
        .child(bar(5., 11., 6., 2., t.ink.opacity(0.36)))
        .child(bar(1., 7., 14., 1., t.accent))
}"""
if old_mark not in text:
    raise SystemExit("Oxidum overlay: launcher mark changed upstream")
text = text.replace(old_mark, new_mark)
for old, new in [
    ('"https://github.com/0CYBER/horizon-free".to_string()', '"https://github.com/LeahRCS/horizon-free".to_string()'),
    ('"horizon-free",\n            "Horizon-Free",', '"oxidum",\n            "Oxidum",'),
    ('.child("Horizon"),', '.child("Oxidum"),'),
    ('tr("Horizon crashed")', 'tr("Oxidum crashed")'),
    ('index_row(n + 7, "Horizon",', 'index_row(n + 7, "Oxidum",'),
    ('tr("Horizon and its icon are in your desktop\'s menu.")', 'tr("Oxidum and its icon are in your desktop\'s menu.")'),
    ('"Horizon is built in the open. Sponsors fund the next release."', '"Oxidum is built in the open. Sponsors fund the next release."'),
    ('tr("Install Horizon first.")', 'tr("Install Oxidum first.")'),
    ('"This moves the instance to Horizon {version}. It compiles the game from scratch, so it takes longer than a normal rebuild: up to 30 minutes."', '"This moves the instance to Oxidum {version}. It compiles the game from scratch, so it takes longer than a normal rebuild: up to 30 minutes."'),
    ('tr("These mods were made for different Horizon versions")', 'tr("These mods were made for different Oxidum versions")'),
    ('"Not prepared. Horizon can download Minecraft {version} from Mojang for your account, or use your own install."', '"Not prepared. Oxidum can download Minecraft {version} from Mojang for your account, or use your own install."'),
    ('tr("None needed: Horizon downloads Minecraft from Mojang for your account.")', 'tr("None needed: Oxidum downloads Minecraft from Mojang for your account.")'),
    ('"Horizon and its icon are in your desktop\\'s menu."', '"Oxidum and its icon are in your desktop\\'s menu."'),
    ('"Horizon needs a Microsoft account that owns Minecraft: Java Edition, like other launchers. It also plays online servers with your name and skin."', '"Oxidum needs a Microsoft account that owns Minecraft: Java Edition, like other launchers. It also plays online servers with your name and skin."'),
    ('"Unsigned: you picked these programs yourself, and Horizon can\\'t \\\n                    check where they came from. Updates never replace them."', '"Unsigned: you picked these programs yourself, and Oxidum can\\'t \\\n                    check where they came from. Updates never replace them."'),
    ('name: "Horizon Launcher".into(),', 'name: "Oxidum Launcher".into(),'),
    ('MenuItem::action("Quit Horizon Launcher", Quit)', 'MenuItem::action("Quit Oxidum Launcher", Quit)'),
    ('assert_eq!(menus[0].name, "Horizon Launcher");', 'assert_eq!(menus[0].name, "Oxidum Launcher");'),
    ('if name == "Quit Horizon Launcher"', 'if name == "Quit Oxidum Launcher"'),
]:
    text = text.replace(old, new)
p.write_text(text)

# Linux desktop integration.
p = Path("launcher/src/desktop.rs")
text = p.read_text().replace("Horizon", "Oxidum")
start = text.find("/// The icon theme sizes")
end = text.find("const LAUNCHER_ENTRY")
if start < 0 or end < 0:
    raise SystemExit("Oxidum overlay: desktop icon block changed upstream")
block = """/// The Oxidum launcher icon installed in the user's hicolor theme.
const ICONS: [(&str, &[u8]); 1] = [(
    "scalable",
    include_bytes!("../../packaging/icons/hicolor/scalable/apps/oxidum.svg"),
)];

"""
text = text[:start] + block + text[end:]
text = text.replace("Icon=horizon\\n\\", "Icon=oxidum\\n\\")
text = text.replace('            "horizon.svg"', '            "oxidum.svg"')
text = text.replace('            "horizon.png"', '            "oxidum.png"')
text = text.replace(
    'assert!(entry.contains("Icon=horizon\\n"));',
    'assert!(entry.contains("Icon=oxidum\\n"));',
)
text = text.replace(
    'let png = data.join("icons/hicolor/48x48/apps/horizon.png");',
    'let svg = data.join("icons/hicolor/scalable/apps/oxidum.svg");',
)
old_test = """        assert!(fs::read(&png).unwrap().starts_with(b"\\x89PNG"));
        assert!(data
            .join("icons/hicolor/scalable/apps/horizon.svg")
            .exists());"""
if old_test not in text:
    raise SystemExit("Oxidum overlay: desktop icon test changed upstream")
text = text.replace(
    old_test,
    '        assert!(fs::read_to_string(&svg).unwrap().starts_with("<svg"));',
)
text = text.replace("assert!(!png.exists());", "assert!(!svg.exists());")
p.write_text(text)

replace("packaging/linux/horizon-launcher.desktop", "Name=Horizon", "Name=Oxidum")
replace(
    "packaging/linux/horizon-launcher.desktop",
    "Comment=Install, prepare and play Horizon,",
    "Comment=Install, prepare and play Oxidum,",
)
replace("packaging/linux/horizon-launcher.desktop", "Icon=horizon", "Icon=oxidum")

p = Path("packaging/linux/appimage.sh")
text = p.read_text()
text = text.replace(
    "name=horizon-launcher-linux-x86_64.AppImage",
    "name=oxidum-linux-x86_64.AppImage",
)
text = text.replace(
    'cp "$here/../icons/hicolor/512x512/apps/horizon.png" "$appdir/horizon.png"\nln -s horizon.png "$appdir/.DirIcon"',
    'cp "$here/../icons/hicolor/scalable/apps/oxidum.svg" "$appdir/oxidum.svg"\nln -s oxidum.svg "$appdir/.DirIcon"',
)
if "oxidum.svg" not in text:
    raise SystemExit("Oxidum overlay: AppImage icon block changed upstream")
p.write_text(text)

# Other user-facing launcher surfaces.
p = Path("launcher/src/installer.rs")
text = p.read_text().replace("Horizon Launcher", "Oxidum Launcher")
text = text.replace('const PUBLISHER: &str = "Horizon";', 'const PUBLISHER: &str = "Oxidum";')
text = text.replace('const ABOUT_URL: &str = "https://playhorizon.dev";', 'const ABOUT_URL: &str = "https://github.com/LeahRCS/horizon-free";')
p.write_text(text)

p = Path("launcher/src/cli.rs")
text = p.read_text()
text = text.replace(
    'about = "Installs, prepares and starts Horizon. Without a subcommand, opens the window."',
    'about = "Installs, prepares and starts Oxidum. Without a subcommand, opens the window."',
)
for old, new in [
    ('println!("Removed Horizon from the applications menu.");', 'println!("Removed Oxidum from the applications menu.");'),
    ('println!("Horizon is in the applications menu.");', 'println!("Oxidum is in the applications menu.");'),
    ('None => println!("Horizon: up to date."),', 'None => println!("Oxidum: up to date."),'),
    ('Some(r) if check => println!("Horizon: {} is available.", r.tag),', 'Some(r) if check => println!("Oxidum: {} is available.", r.tag),'),
    ('println!("Horizon: installed {tag}.");', 'println!("Oxidum: installed {tag}.");'),
]:
    text = text.replace(old, new)
p.write_text(text)

# Translation files contain only display strings, so the brand substitution is safe there.
for lang in Path("launcher/lang").glob("*.json"):
    lang.write_text(lang.read_text().replace("Horizon", "Oxidum"))
