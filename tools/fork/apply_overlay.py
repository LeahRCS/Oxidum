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
    'pub const LAUNCHER_REPO: &str = "LeahRCS/Oxidum";',
)
replace(
    "launcher/src/backend.rs",
    'pub const README_URL: &str = "https://github.com/horizon-rust/horizon/blob/main/launcher/README.md";',
    'pub const README_URL: &str = "https://github.com/LeahRCS/Oxidum";',
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
new_mark = """/// Oxidum's mark: copper above the seam, oxidized patina below it.
fn mark(size: f32, _t: &Theme) -> Div {
    let u = size / 16.;
    let copper_hi: Hsla = gpui::rgb(0xeb9655).into();
    let copper: Hsla = gpui::rgb(0xb85b29).into();
    let transition: Hsla = gpui::rgb(0x71866b).into();
    let patina: Hsla = gpui::rgb(0x55ad93).into();
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
        .child(bar(5., 2., 6., 2., copper_hi))
        .child(bar(3., 4., 2., 3., copper))
        .child(bar(11., 4., 2., 3., copper))
        .child(bar(3., 8., 2., 3., transition))
        .child(bar(11., 8., 2., 3., patina))
        .child(bar(5., 11., 6., 2., patina))
        .child(bar(1., 7., 6., 1., copper_hi))
        .child(bar(7., 7., 3., 1., transition))
        .child(bar(10., 7., 5., 1., patina))
}"""
if old_mark not in text:
    raise SystemExit("Oxidum overlay: launcher mark changed upstream")
text = text.replace(old_mark, new_mark)
for old, new in [
    ('"https://github.com/0CYBER/horizon-free".to_string()', '"https://github.com/LeahRCS/Oxidum".to_string()'),
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
    ('''"Horizon and its icon are in your desktop's menu."''', '''"Oxidum and its icon are in your desktop's menu."'''),
    ('"Horizon needs a Microsoft account that owns Minecraft: Java Edition, like other launchers. It also plays online servers with your name and skin."', '"Oxidum needs a Microsoft account that owns Minecraft: Java Edition, like other launchers. It also plays online servers with your name and skin."'),
    ('''"Unsigned: you picked these programs yourself, and Horizon can't \\
                    check where they came from. Updates never replace them."''', '''"Unsigned: you picked these programs yourself, and Oxidum can't \\
                    check where they came from. Updates never replace them."'''),
    ('name: "Horizon Launcher".into(),', 'name: "Oxidum Launcher".into(),'),
    ('MenuItem::action("Quit Horizon Launcher", Quit)', 'MenuItem::action("Quit Oxidum Launcher", Quit)'),
    ('assert_eq!(menus[0].name, "Horizon Launcher");', 'assert_eq!(menus[0].name, "Oxidum Launcher");'),
    ('if name == "Quit Horizon Launcher"', 'if name == "Quit Oxidum Launcher"'),
]:
    text = text.replace(old, new)
# Two user-facing strings contain wrapping that can change upstream; match their stable prefixes.
text = text.replace(
    "Horizon is built in the open. Sponsors fund the next release.",
    "Oxidum is built in the open. Sponsors fund the next release.",
)
text = text.replace(
    "Unsigned: you picked these programs yourself, and Horizon can't",
    "Unsigned: you picked these programs yourself, and Oxidum can't",
)
p.write_text(text)

# Keep the Glass UI branded too; these surfaces live outside main.rs.
for glass_path in [
    "launcher/src/glass_notes.rs",
    "launcher/src/glass_versions.rs",
]:
    p = Path(glass_path)
    text = p.read_text()
    text = text.replace(
        "Horizon is built in the open. Sponsors fund the next release.",
        "Oxidum is built in the open. Sponsors fund the next release.",
    )
    text = text.replace(
        "Unsigned: you picked these programs yourself, and Horizon can't",
        "Unsigned: you picked these programs yourself, and Oxidum can't",
    )
    p.write_text(text)

# Oxidum's default colour language: copper action/focus, patina success.
p = Path("crates/horizon-theme/src/night.rs")
text = p.read_text()
text = text.replace("one violet for the main", "Oxidum copper for the main")
text = text.replace("with the night's violet.", "with Oxidum's copper accent.")
text = text.replace(
    "accent: 0x7656fa,\n    accent_hi: 0xa08cff,\n    on_accent: 0xffffff,\n    success: 0x5fd39a,\n    warn: 0xf5b45a,",
    "accent: 0xb85b29,\n    accent_hi: 0xeb9655,\n    on_accent: 0xffffff,\n    success: 0x55ad93,\n    warn: 0xd9a45c,",
)
text = text.replace(
    "accent: 0x5b3fd6,\n    accent_hi: 0x5333c9,\n    on_accent: 0xffffff,\n    success: 0x136336,\n    warn: 0x7a4f00,",
    "accent: 0x934018,\n    accent_hi: 0x843a16,\n    on_accent: 0xffffff,\n    success: 0x286858,\n    warn: 0x755000,",
)
p.write_text(text)

p = Path("launcher/src/themes.rs")
text = p.read_text()
text = text.replace(
    "An accent is a hue, and the player may pick any of them; seven hues have names, as shortcuts.\n//! Horizon's violet is the default. Another hue turns the violet tokens",
    "An accent is a hue, and the player may pick any of them; eight accents have names, as shortcuts.\n//! Oxidum's copper is the default. Another hue turns the base tokens",
)
text = text.replace(
    "lightness, then darkens or lightens each just enough to read as well as the violet does:",
    "lightness, then darkens or lightens each just enough to preserve the same readability:",
)
text = text.replace(
    "/// An accent: a hue in degrees, or none for Horizon's violet, whose tokens are the palette's own",
    "/// An accent: a hue in degrees, or none for Oxidum's copper, whose tokens are the palette's own",
)
text = text.replace(
    "pub const SWATCHES: [u32; 7] = [\n    0x6b4bff, 0x2563eb, 0x0f766e, 0x15803d, 0xc2410c, 0xdc2626, 0xbe185d,\n];",
    "pub const SWATCHES: [u32; 8] = [\n    0xb85b29, 0x6b4bff, 0x2563eb, 0x0f766e, 0x15803d, 0xc2410c, 0xdc2626, 0xbe185d,\n];",
)
text = text.replace(
    'const NAMES: [&str; 7] = ["violet", "blue", "teal", "green", "amber", "red", "pink"];',
    'const NAMES: [&str; 8] = ["oxidum", "violet", "blue", "teal", "green", "amber", "red", "pink"];',
)
text = text.replace(
    "impl Accent {\n    pub const VIOLET: Accent = Accent {\n        hue: None,\n        rgb: None,\n    };",
    "impl Accent {\n    pub const OXIDUM: Accent = Accent {\n        hue: None,\n        rgb: None,\n    };\n    pub const VIOLET: Accent = Accent {\n        hue: Some(251.),\n        rgb: None,\n    };",
)
text = text.replace(
    "pub const ALL: [Accent; 7] = [\n        Self::VIOLET,",
    "pub const ALL: [Accent; 8] = [\n        Self::OXIDUM,\n        Self::VIOLET,",
)
text = text.replace("/// the violet's saturation and lightness.", "/// the legacy violet's saturation and lightness.")
text = text.replace("let (_, s, l) = hsl(SWATCHES[0]);", "let (_, s, l) = hsl(SWATCHES[1]);")
text = text.replace('None => "violet".to_owned(),', 'None => "oxidum".to_owned(),')
text = text.replace(
    'let name = if name == "purple" || name == "default" {\n            "violet"\n        } else {',
    'let name = if name == "purple" {\n            "violet"\n        } else if name == "default" {\n            "oxidum"\n        } else {',
)
text = text.replace(
    "/// Its hue in degrees; None for the violet, whose tokens stay as they are.",
    "/// Its hue in degrees; None for Oxidum's default copper, whose tokens stay as they are.",
)
p.write_text(text)

p = Path("launcher/src/themes_page.rs")
text = p.read_text()
text = text.replace(
    "Horizon's violet by default. Every colour keeps text as easy to read.",
    "Oxidum copper by default. Every colour keeps text as easy to read.",
)
text = text.replace("its seven swatches", "its eight swatches")
p.write_text(text)

p = Path("launcher/src/themes/tests.rs")
text = p.read_text()
text = text.replace(
    "fn every_accent_reads_as_well_as_the_violet()",
    "fn every_accent_keeps_the_required_contrast()",
)
text = text.replace(
    "let violet = Accent::VIOLET.apply(base);\n        assert_eq!((violet.accent, violet.face), (base.accent, base.face));",
    "let oxidum = Accent::OXIDUM.apply(base);\n        assert_eq!((oxidum.accent, oxidum.face), (base.accent, base.face));",
)
text = text.replace(
    'assert_eq!(Accent::parse("purple"), Some(Accent::VIOLET));',
    'assert_eq!(Accent::parse("purple"), Some(Accent::VIOLET));\n    assert_eq!(Accent::parse("default"), Some(Accent::OXIDUM));',
)
text = text.replace(
    'assert_eq!(Accent::VIOLET.name(), "violet");',
    'assert_eq!(Accent::OXIDUM.name(), "oxidum");\n    assert_eq!(Accent::VIOLET.name(), "violet");',
)
text = text.replace(
    'assert_eq!(Accent::VIOLET.hex(), "#6b4bff");',
    'assert_eq!(Accent::OXIDUM.hex(), "#b85b29");\n    assert_eq!(Accent::VIOLET.hex(), "#6b4bff");',
)
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
replace("packaging/linux/horizon.desktop", "Name=Horizon", "Name=Oxidum")
replace("packaging/linux/horizon.desktop", "Icon=horizon", "Icon=oxidum")

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

# Keep generated web design tokens in sync with the Oxidum NIGHT/DAWN palette.
p = Path("crates/horizon-theme/tokens.css")
text = p.read_text()
for old, new in [
    ("--night-accent: #5b3fd6;", "--night-accent: #934018;"),
    ("--night-accent-hi: #5333c9;", "--night-accent-hi: #843a16;"),
    ("--night-success: #136336;", "--night-success: #286858;"),
    ("--night-warn: #7a4f00;", "--night-warn: #755000;"),
    ("--night-accent: #7656fa;", "--night-accent: #b85b29;"),
    ("--night-accent-hi: #a08cff;", "--night-accent-hi: #eb9655;"),
    ("--night-success: #5fd39a;", "--night-success: #55ad93;"),
    ("--night-warn: #f5b45a;", "--night-warn: #d9a45c;"),
]:
    text = text.replace(old, new)
p.write_text(text)

# Keep launcher tests aligned with Oxidum's distribution defaults.
p = Path("launcher/src/backend.rs")
text = p.read_text()
text = text.replace(
    "fn the_accent_is_violet_unless_picked_and_an_unknown_one_keeps_the_rest()",
    "fn the_accent_is_oxidum_unless_picked_and_an_unknown_one_keeps_the_rest()",
)
text = text.replace(
    'assert_eq!(Settings::parse("{}").accent, Accent::VIOLET);',
    'assert_eq!(Settings::parse("{}").accent, Accent::OXIDUM);',
)
text = text.replace('(Accent::VIOLET, "--x")', '(Accent::OXIDUM, "--x")')
p.write_text(text)

# Horizon-Free/Oxidum deliberately allows local/offline play without a Microsoft owner.
# Keep the integration coverage aligned with that policy when applying the overlay to a fresh
# upstream launcher release.
Path("launcher/tests/owner_gate.rs").write_text(r'''//! Offline-play behavior from the outside: without a Microsoft owner, Oxidum still reaches the
//! normal launch/preparation path instead of stopping at Horizon's owner gate.
use std::io::Write;
use std::path::{Path, PathBuf};
use std::process::{Command, Output, Stdio};

const OWNER_GATE: &str =
    "Sign in with a Microsoft account that owns Minecraft: Java Edition to play.";
const NOT_PREPARED: &str = "is not prepared yet";

/// Fresh homes with one installed (not prepared) version and an offline name.
fn home(name: &str) -> PathBuf {
    let root =
        std::env::temp_dir().join(format!("oxidum-offline-play-{name}-{}", std::process::id()));
    let _ = std::fs::remove_dir_all(&root);
    let version = root.join("launcher/versions/v2026.10.27.01");
    std::fs::create_dir_all(&version).unwrap();
    std::fs::write(version.join(".installed"), "").unwrap();
    std::fs::write(
        root.join("launcher/accounts.json"),
        r#"{"accounts":[],"selected":null,"offline":["Builder_1"],"offline_selected":"Builder_1"}"#,
    )
    .unwrap();
    root
}

fn launcher(root: &Path, args: &[&str]) -> Command {
    let mut cmd = Command::new(env!("CARGO_BIN_EXE_horizon-launcher"));
    cmd.args(args)
        .env("HORIZON_HOME", root.join("game"))
        .env("HORIZON_LAUNCHER_HOME", root.join("launcher"))
        .env("XDG_DATA_HOME", root.join("data"))
        .env("XDG_CONFIG_HOME", root.join("config"))
        .env("HORIZON_LAUNCHER_NO_SELF_UPDATE", "1")
        .env("HORIZON_NO_AUDIO", "1")
        .env("HORIZON_TELEMETRY_URL", "off")
        .env("HORIZON_NO_KEYCHAIN", "1")
        .env("HORIZON_MSA_CLIENT_ID", "test-client");
    cmd
}

fn text(out: &Output) -> String {
    String::from_utf8_lossy(&out.stdout).into_owned() + &String::from_utf8_lossy(&out.stderr)
}

#[test]
fn the_cli_reaches_the_offline_launch_path_without_an_owner() {
    let root = home("cli");
    let out = launcher(&root, &["play"]).output().unwrap();
    let said = text(&out);

    // This fixture is deliberately not prepared, so launch stops there — after the owner gate.
    assert!(!out.status.success(), "{said}");
    assert!(said.contains(NOT_PREPARED), "{said}");
    assert!(!said.contains(OWNER_GATE), "{said}");

    let accounts = std::fs::read_to_string(root.join("launcher/accounts.json")).unwrap();
    assert!(accounts.contains("Builder_1"), "{accounts}");
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn the_mcp_server_reaches_the_offline_launch_path_without_an_owner() {
    let root = home("mcp");
    let mut child = launcher(&root, &["mcp"])
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    let requests = [
        r#"{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}"#,
        r#"{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"play","arguments":{}}}"#,
    ];
    let mut stdin = child.stdin.take().unwrap();
    for r in requests {
        writeln!(stdin, "{r}").unwrap();
    }
    drop(stdin);

    let out = child.wait_with_output().unwrap();
    let reply = String::from_utf8_lossy(&out.stdout)
        .lines()
        .map(|l| serde_json::from_str::<serde_json::Value>(l).unwrap())
        .find(|v| v["id"] == 2)
        .expect("a reply to play");
    assert_eq!(reply["result"]["isError"], true, "{reply}");
    let said = reply["result"]["content"][0]["text"].as_str().unwrap();
    assert!(said.contains(NOT_PREPARED), "{said}");
    assert!(!said.contains(OWNER_GATE), "{said}");

    let _ = std::fs::remove_dir_all(&root);
}
''')

# Other user-facing launcher surfaces.
p = Path("launcher/src/installer.rs")
text = p.read_text().replace("Horizon Launcher", "Oxidum Launcher")
text = text.replace('const PUBLISHER: &str = "Horizon";', 'const PUBLISHER: &str = "Oxidum";')
text = text.replace('const ABOUT_URL: &str = "https://playhorizon.dev";', 'const ABOUT_URL: &str = "https://github.com/LeahRCS/Oxidum";')
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

# Only strings whose source text was rebranded get new translation keys.
import json

translation_keys = {
    "Horizon crashed": "Oxidum crashed",
    "Install Horizon first.": "Install Oxidum first.",
    "This moves the instance to Horizon {version}. It compiles the game from scratch, so it takes longer than a normal rebuild: up to 30 minutes.": "This moves the instance to Oxidum {version}. It compiles the game from scratch, so it takes longer than a normal rebuild: up to 30 minutes.",
    "These mods were made for different Horizon versions": "These mods were made for different Oxidum versions",
    "Not prepared. Horizon can download Minecraft {version} from Mojang for your account, or use your own install.": "Not prepared. Oxidum can download Minecraft {version} from Mojang for your account, or use your own install.",
    "None needed: Horizon downloads Minecraft from Mojang for your account.": "None needed: Oxidum downloads Minecraft from Mojang for your account.",
    "Horizon needs a Microsoft account that owns Minecraft: Java Edition, like other launchers. It also plays online servers with your name and skin.": "Oxidum needs a Microsoft account that owns Minecraft: Java Edition, like other launchers. It also plays online servers with your name and skin.",
    "Unsigned: you picked these programs yourself, and Horizon can't check where they came from. Updates never replace them.": "Unsigned: you picked these programs yourself, and Oxidum can't check where they came from. Updates never replace them.",
    "Horizon is built in the open. Sponsors fund the next release.": "Oxidum is built in the open. Sponsors fund the next release.",
    "Horizon's violet by default. Every colour keeps text as easy to read.": "Oxidum copper by default. Every colour keeps text as easy to read.",
    "Installs Horizon Launcher for this account. No administrator needed.": "Installs Oxidum Launcher for this account. No administrator needed.",
    "Removes Horizon Launcher from this computer. Your worlds and the game's folder stay.": "Removes Oxidum Launcher from this computer. Your worlds and the game's folder stay.",
    "Horizon Launcher is installed.": "Oxidum Launcher is installed.",
    "Horizon Launcher was removed.": "Oxidum Launcher was removed.",
    "Launch Horizon": "Launch Oxidum",
}
for lang in Path("launcher/lang").glob("*.json"):
    original = json.loads(lang.read_text())
    branded = {}
    for key, value in original.items():
        new_key = translation_keys.get(key, key)
        if key in translation_keys and isinstance(value, str):
            value = value.replace("Horizon", "Oxidum")
        branded[new_key] = value
    lang.write_text(json.dumps(branded, ensure_ascii=False, indent=2) + "\n")
