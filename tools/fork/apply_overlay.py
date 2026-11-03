#!/usr/bin/env python3
from pathlib import Path

def replace(path, old, new):
    p = Path(path)
    text = p.read_text()
    if old not in text:
        raise SystemExit(f"overlay: expected text not found in {path}: {old!r}")
    p.write_text(text.replace(old, new))

replace("launcher/src/backend.rs",
        'pub const LAUNCHER_REPO: &str = "0CYBER/horizon-free";',
        'pub const LAUNCHER_REPO: &str = "LeahRCS/horizon-free";')
replace("launcher/src/main.rs",
        '"https://github.com/0CYBER/horizon-free".to_string()',
        '"https://github.com/LeahRCS/horizon-free".to_string()')
replace("README.md",
        "https://github.com/0CYBER/horizon-free/releases/latest",
        "https://github.com/LeahRCS/horizon-free/releases")
replace("packaging/linux/horizon-launcher.desktop",
        "Icon=horizon",
        "Icon=horizon-free")

p = Path("packaging/linux/appimage.sh")
text = p.read_text()
text = text.replace(
    'cp "$here/../icons/hicolor/512x512/apps/horizon.png" "$appdir/horizon.png"\nln -s horizon.png "$appdir/.DirIcon"',
    'cp "$here/../icons/hicolor/scalable/apps/horizon-free.svg" "$appdir/horizon-free.svg"\nln -s horizon-free.svg "$appdir/.DirIcon"')
if "horizon-free.svg" not in text:
    raise SystemExit("overlay: AppImage icon block changed upstream")
p.write_text(text)

p = Path("launcher/src/desktop.rs")
text = p.read_text()
start = text.find("/// The icon theme sizes")
end = text.find("const LAUNCHER_ENTRY")
if start < 0 or end < 0:
    raise SystemExit("overlay: desktop icon block changed upstream")
block = '''/// The Horizon-Free launcher icon installed in the user's hicolor theme.
const ICONS: [(&str, &[u8]); 1] = [(
    "scalable",
    include_bytes!("../../packaging/icons/hicolor/scalable/apps/horizon-free.svg"),
)];

'''
text = text[:start] + block + text[end:]
text = text.replace("Icon=horizon\\n\\", "Icon=horizon-free\\n\\")
text = text.replace('            "horizon.svg"', '            "horizon-free.svg"')
text = text.replace('            "horizon.png"', '            "horizon-free.png"')
text = text.replace('assert!(entry.contains("Icon=horizon\\n"));',
                    'assert!(entry.contains("Icon=horizon-free\\n"));')
text = text.replace('let png = data.join("icons/hicolor/48x48/apps/horizon.png");',
                    'let svg = data.join("icons/hicolor/scalable/apps/horizon-free.svg");')
text = text.replace('assert!(fs::read(&png).unwrap().starts_with(b"\\x89PNG"));\n        assert!(data\n            .join("icons/hicolor/scalable/apps/horizon.svg")\n            .exists());',
                    'assert!(fs::read_to_string(&svg).unwrap().starts_with("<svg"));')
text = text.replace('assert!(!png.exists());', 'assert!(!svg.exists());')
p.write_text(text)
