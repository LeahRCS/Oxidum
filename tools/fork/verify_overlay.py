#!/usr/bin/env python3
"""Fail with a precise message when an Oxidum overlay invariant is missing."""

from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
failures: list[str] = []


def read(path: str) -> str:
    file = root / path
    if not file.is_file():
        failures.append(f"{path}: file is missing")
        return ""
    return file.read_text(errors="replace")


def require(path: str, needle: str, label: str) -> None:
    if needle not in read(path):
        failures.append(f"{label}: {path} is missing {needle!r}")
    else:
        print(f"[ok] {label}")


def forbid(path: str, needle: str, label: str) -> None:
    if needle in read(path):
        failures.append(f"{label}: {path} still contains {needle!r}")
    else:
        print(f"[ok] {label}")


require("launcher/src/backend.rs", 'LAUNCHER_REPO: &str = "LeahRCS/Oxidum"', "Oxidum update channel")
require("launcher/src/backend.rs", "oxidum-linux-x86_64.AppImage", "Oxidum AppImage asset")
require("launcher/src/lib.rs", "pub mod gpu;", "GPU module exported")
require("crates/horizon-client-render/src/gfx.rs", "HORIZON_GPU", "Rust renderer GPU selector")
require(
    "crates/horizon-client-render/src/gfx.rs",
    "device_pci_bus_id.eq_ignore_ascii_case(wanted)",
    "physical GPU selection prefers PCI identity",
)
require("launcher/src/titlebar.rs", 'title: Some("Oxidum".into())', "window title branding")
require("packaging/linux/horizon-launcher.desktop", "Icon=oxidum", "desktop icon branding")
require("launcher/src/main.rs", '"OXIDUM".chars().enumerate()', "opening wordmark")
require("launcher/src/frame.rs", '"Oxidum"', "Glass sidebar branding")
require("launcher/src/frame.rs", "https://github.com/LeahRCS/Oxidum", "Glass sidebar repository link")
forbid("launcher/src/frame.rs", '"Horizon-Free"', "old sidebar brand removed")
require("launcher/src/glass_settings.rs", '"Oxidum"', "Glass settings branding")
forbid(
    "launcher/src/glass_settings.rs",
    "Horizon and its icon are in your desktop",
    "old applications-menu brand removed",
)
require("launcher/src/glass_settings.rs", "fn launcher_gpu_row", "launcher GPU picker")
require("launcher/src/glass_settings.rs", "fn rust_game_gpu_row", "Rust default GPU picker")
require("launcher/src/launch_page.rs", "fn pick_instance_gpu", "per-instance GPU persistence")
require("launcher/src/launch_page.rs", "instance-gpu-system", "per-instance GPU selector UI")
require("crates/horizon-theme/src/night.rs", "accent: 0xb85b29", "copper Night accent")
require("crates/horizon-theme/src/glass.rs", "pub const ACCENT: u32 = 0xb85b29;", "copper Glass accent")
require("crates/horizon-theme/src/glass.rs", "pub const LIVE: u32 = 0x55ad93;", "patina live/success")
require("crates/horizon-theme/src/glass.rs", "pub const PAGE: u32 = 0x181a22;", "charcoal Glass base")
require("packaging/icons/hicolor/scalable/apps/oxidum.svg", "#B85B29", "Oxidum SVG copper")
require("packaging/icons/hicolor/scalable/apps/oxidum.svg", "#55AD93", "Oxidum SVG patina")

glass_ui = read("launcher/src/glass_ui.rs")
if "pub fn mark_tile" in glass_ui:
    require("launcher/src/glass_ui.rs", "0xb85b29", "legacy Glass Oxidum mark")
else:
    require("launcher/src/instance_icons.rs", "oxidum.png", "new upstream Oxidum mark asset")
    if not (root / "packaging/icons/hicolor/256x256/apps/oxidum.png").is_file():
        failures.append("new upstream Oxidum mark asset: oxidum.png is missing")
    else:
        print("[ok] packaged Oxidum PNG exists")

if failures:
    print("\nOxidum overlay verification failed:", file=sys.stderr)
    for failure in failures:
        print(f"  - {failure}", file=sys.stderr)
    raise SystemExit(1)

print("\nOxidum overlay verification passed.")
