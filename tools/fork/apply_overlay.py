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
    ('"HORIZON".chars().enumerate()', '"OXIDUM".chars().enumerate()'),
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

# Glass UI has separate branding surfaces from the legacy frame.
p = Path("launcher/src/frame.rs")
text = p.read_text()
text = text.replace(
    '"horizon-free",\n                "Horizon-Free",\n                "globe-02",\n                "https://github.com/0CYBER/horizon-free".to_string(),',
    '"oxidum",\n                "Oxidum",\n                "globe-02",\n                "https://github.com/LeahRCS/Oxidum".to_string(),',
)
p.write_text(text)

p = Path("launcher/src/glass_settings.rs")
text = p.read_text()
# Older layouts pass a bare string; newer Glass About tiles call .into().
text = text.replace('                "Horizon",', '                "Oxidum",')
text = text.replace('                "Horizon".into(),', '                "Oxidum".into(),')
text = text.replace(
    "Horizon and its icon are in your desktop's menu.",
    "Oxidum and its icon are in your desktop's menu.",
)
p.write_text(text)

p = Path("launcher/src/glass_ui.rs")
text = p.read_text()
start = text.find("/// Horizon's mark on its dark tile")
end = text.find("/// A big square button", start)
if start >= 0 and end >= 0:
    glass_mark = """/// Oxidum's fixed brand mark on its dark tile, matching the app icon's copper-to-patina oxidation.
pub fn mark_tile(size: f32, _accent_soft: u32) -> Div {
    let inner = size * 0.64;
    let u = inner / 16.;
    let bar = |x: f32, y: f32, w: f32, h: f32, c: Hsla| {
        div()
            .absolute()
            .left(px(x * u))
            .top(px(y * u))
            .w(px(w * u))
            .h(px(h * u))
            .bg(c)
    };
    div()
        .flex()
        .flex_none()
        .items_center()
        .justify_center()
        .size(px(size))
        .rounded(px((size * 0.26).round()))
        .bg(color(0x181a22))
        .child(
            div()
                .relative()
                .size(px(inner))
                .child(bar(5., 2., 6., 2., color(0xeb9655)))
                .child(bar(3., 4., 2., 3., color(0xb85b29)))
                .child(bar(11., 4., 2., 3., color(0xb85b29)))
                .child(bar(3., 8., 2., 3., color(0x71866b)))
                .child(bar(11., 8., 2., 3., color(0x55ad93)))
                .child(bar(5., 11., 6., 2., color(0x55ad93)))
                .child(bar(1., 7., 6., 1., color(0xeb9655)))
                .child(bar(7., 7., 3., 1., color(0x71866b)))
                .child(bar(10., 7., 5., 1., color(0x55ad93))),
        )
}

"""
    p.write_text(text[:start] + glass_mark + text[end:])
else:
    # Newer upstream moved the default-instance brand mark to a packaged PNG.
    p = Path("launcher/src/instance_icons.rs")
    text = p.read_text()
    old = 'const MARK: &[u8] = include_bytes!("../../packaging/icons/hicolor/256x256/apps/horizon.png");'
    new = 'const MARK: &[u8] = include_bytes!("../../packaging/icons/hicolor/256x256/apps/oxidum.png");'
    if old not in text:
        raise SystemExit("Oxidum overlay: could not find either Glass mark implementation")
    p.write_text(text.replace(old, new))

# Glass defaults come from the Oxidum icon instead of Horizon's violet.
p = Path("crates/horizon-theme/src/glass.rs")
text = p.read_text()
for old, new in [
    ("pub const ACCENT: u32 = 0x6b4bff;", "pub const ACCENT: u32 = 0xb85b29;"),
    ("pub const PAGE: u32 = 0x0a0919;", "pub const PAGE: u32 = 0x181a22;"),
    ("pub const LIVE: u32 = 0x4ade80;", "pub const LIVE: u32 = 0x55ad93;"),
    ("pub const WARN: u32 = 0xf2c46b;", "pub const WARN: u32 = 0xeb9655;"),
    ("/// A dark violet from the accent: what the plates are tinted with.", "/// A dark charcoal/copper mix from the accent: what the plates are tinted with."),
    ("/// `--base: color-mix(in oklab, accent 10%, #14111d)`, and `.hzl-glass`'s background", "/// `--base: color-mix(in oklab, accent 10%, #181a22)`, and `.hzl-glass`'s background"),
    ("let base = mix_oklab(accent, 0x14111d, 0.10);", "let base = mix_oklab(accent, 0x181a22, 0.10);"),
    ("[0.772018, 0.0291158, -0.12693]", "[0.7793512, 0.0488354, 0.0508413]"),
    ("close(g.accent_soft, 0xa9a9ff)", "close(g.accent_soft, 0xdeaa91)"),
    ('assert!(close(g.base, 0x1b1830), "base {:06x}", g.base);', 'assert!(close(g.base, 0x272125), "base {:06x}", g.base);'),
    ('assert!(close(g.plate, 0x4e4c5f), "plate {:06x}", g.plate);', 'assert!(close(g.plate, 0x585356), "plate {:06x}", g.plate);'),
]:
    text = text.replace(old, new)
p.write_text(text)

# GPU selectors live in fast-moving launcher UI files. Apply them semantically instead of
# carrying fragile line-based hunks in gpu-selection.patch.
p = Path("launcher/src/glass_settings.rs")
text = p.read_text()
if "fn launcher_gpu_row" not in text:
    anchor = "    /// The Game card's Native mods row."
    if anchor not in text:
        raise SystemExit("Oxidum overlay: glass Settings GPU anchor changed upstream")
    rows = r'''    /// Linux: the physical GPU the launcher window itself uses on its next start.
    pub(super) fn launcher_gpu_row(&mut self, cx: &mut Context<Self>) -> Option<Div> {
        if !cfg!(target_os = "linux") {
            return None;
        }
        let gpus = horizon_launcher::gpu::list();
        if gpus.is_empty() {
            return None;
        }
        let t = self.theme;
        let current = self.settings.launcher_gpu.clone();
        let mut choices = div().flex().flex_col().items_stretch().gap(px(6.));
        choices = choices.child(
            button(
                "launcher-gpu-system",
                "Automatic / system",
                if current.is_none() {
                    Kind::Primary
                } else {
                    Kind::Secondary
                },
                &t,
            )
            .on_click(cx.listener(|this, _: &ClickEvent, _, cx| {
                this.settings.launcher_gpu = None;
                this.save_settings();
                cx.notify();
            })),
        );
        for (index, gpu) in gpus.into_iter().enumerate() {
            let id = gpu.id.clone();
            let selected = current.as_deref() == Some(id.as_str());
            let label = match gpu.boot_vga {
                true => trf("{gpu} (system default)", &[("gpu", &gpu.name)]),
                false => gpu.name.clone(),
            };
            choices = choices.child(
                button(
                    SharedString::from(format!("launcher-gpu-{index}")),
                    label,
                    if selected {
                        Kind::Primary
                    } else {
                        Kind::Secondary
                    },
                    &t,
                )
                .on_click(cx.listener(move |this, _: &ClickEvent, _, cx| {
                    this.settings.launcher_gpu = Some(id.clone());
                    this.save_settings();
                    cx.notify();
                })),
            );
        }
        Some(index_row(
            0,
            tr("Launcher graphics card"),
            note("Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens."),
            Some(choices.into_any_element()),
            &t,
        ))
    }

    /// Linux: the physical GPU Rust Minecraft instances use unless an instance overrides it.
    pub(super) fn rust_game_gpu_row(&mut self, cx: &mut Context<Self>) -> Option<Div> {
        if !cfg!(target_os = "linux") {
            return None;
        }
        let gpus = horizon_launcher::gpu::list();
        if gpus.is_empty() {
            return None;
        }
        let t = self.theme;
        let current = self.settings.rust_game_gpu.clone();
        let mut choices = div().flex().flex_col().items_stretch().gap(px(6.));
        choices = choices.child(
            button(
                "rust-game-gpu-system",
                "Automatic / system",
                if current.is_none() {
                    Kind::Primary
                } else {
                    Kind::Secondary
                },
                &t,
            )
            .on_click(cx.listener(|this, _: &ClickEvent, _, cx| {
                this.settings.rust_game_gpu = None;
                this.save_settings();
                cx.notify();
            })),
        );
        for (index, gpu) in gpus.into_iter().enumerate() {
            let id = gpu.id.clone();
            let selected = current.as_deref() == Some(id.as_str());
            let label = match gpu.boot_vga {
                true => trf("{gpu} (system default)", &[("gpu", &gpu.name)]),
                false => gpu.name.clone(),
            };
            choices = choices.child(
                button(
                    SharedString::from(format!("rust-game-gpu-{index}")),
                    label,
                    if selected {
                        Kind::Primary
                    } else {
                        Kind::Secondary
                    },
                    &t,
                )
                .on_click(cx.listener(move |this, _: &ClickEvent, _, cx| {
                    this.settings.rust_game_gpu = Some(id.clone());
                    this.save_settings();
                    cx.notify();
                })),
            );
        }
        Some(index_row(
            0,
            tr("Rust Minecraft graphics card"),
            note("Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings."),
            Some(choices.into_any_element()),
            &t,
        ))
    }

'''
    text = text.replace(anchor, rows + anchor, 1)

if ".children(self.launcher_gpu_row(cx))" not in text:
    anchor = "            .child(self.glass_accent_row(cx))\n"
    if anchor not in text:
        raise SystemExit("Oxidum overlay: launcher GPU row placement changed upstream")
    text = text.replace(anchor, anchor + "            .children(self.launcher_gpu_row(cx))\n", 1)

if ".children(self.rust_game_gpu_row(cx))" not in text:
    anchor = "        let game = card()\n"
    if anchor not in text:
        raise SystemExit("Oxidum overlay: game Settings card changed upstream")
    text = text.replace(anchor, anchor + "            .children(self.rust_game_gpu_row(cx))\n", 1)
p.write_text(text)

p = Path("launcher/src/launch_page.rs")
text = p.read_text()
if "fn pick_instance_gpu" not in text:
    anchor = "    /// The instance the memory row sets:"
    if anchor not in text:
        raise SystemExit("Oxidum overlay: instance GPU save anchor changed upstream")
    helper = r'''    /// Picks a physical GPU for a Rust instance. None means inherit the Settings default.
    /// Choosing through the new list also retires the old boolean dedicated-GPU switch for it.
    fn pick_instance_gpu(&mut self, gpu: Option<String>) {
        let Some(panel) = &mut self.launch else {
            return;
        };
        let saved = instances::edit(&panel.instance, |m| {
            m.launch.gpu = gpu.clone();
            m.launch.dedicated_gpu = false;
        });
        panel.saved = Some(saved.map(|i| i.launch.summary()));
        self.reload_instances();
    }

'''
    text = text.replace(anchor, helper + anchor, 1)

start = text.find("    /// The Linux switches this computer can use:")
end = text.find("    /// The panel under the Instance row", start)
if start < 0 or end < 0:
    raise SystemExit("Oxidum overlay: Linux launch switches changed upstream")
linux = r'''    /// Linux launch helpers: GameMode and MangoHud, plus a physical GPU picker for Rust
    /// instances. Java instances keep the older dedicated-GPU switch unchanged.
    fn linux_switches(&self, cx: &mut Context<Self>) -> Option<Div> {
        let t = self.theme;
        let found = self.launch.as_ref()?.found;
        let instance = self.selected_instance()?.clone();
        let now = instance.launch.clone();
        let mut list = div().flex().flex_col().gap(px(10.));

        for (toggle, shown, on, label, about) in [
            (
                Toggle::GameMode,
                found.gamemode,
                now.gamemode,
                "GameMode",
                "Feral's gamemoderun: CPU and scheduler tuned while you play.",
            ),
            (
                Toggle::MangoHud,
                found.mangohud,
                now.mangohud,
                "MangoHud",
                "The frame time, CPU and GPU overlay.",
            ),
        ] {
            if !shown {
                continue;
            }
            list = list.child(
                div()
                    .id(SharedString::from(format!("launch-switch-{label}")))
                    .flex()
                    .items_center()
                    .gap(px(10.))
                    .cursor_pointer()
                    .child(switch(
                        SharedString::from(format!("launch-switch-{label}-s")),
                        on,
                        &t,
                    ))
                    .child(text(theme::LABEL).text_color(t.ink_soft).child(tr(label)))
                    .child(text(theme::CAPTION).text_color(t.muted).child(tr(about)))
                    .on_click(cx.listener(move |this, _: &ClickEvent, _, cx| {
                        this.flip(toggle);
                        cx.notify();
                    })),
            );
        }

        if instance.java.is_some() {
            if found.two_gpus {
                let gpu_about = match found.nvidia {
                    true => "NVIDIA render offload for this Java instance.",
                    false => "Mesa PRIME render offload for this Java instance.",
                };
                list = list.child(
                    div()
                        .id("launch-switch-Dedicated-gpu")
                        .flex()
                        .items_center()
                        .gap(px(10.))
                        .cursor_pointer()
                        .child(switch(
                            "launch-switch-Dedicated-gpu-s",
                            now.dedicated_gpu,
                            &t,
                        ))
                        .child(
                            text(theme::LABEL)
                                .text_color(t.ink_soft)
                                .child(tr("Dedicated graphics card")),
                        )
                        .child(
                            text(theme::CAPTION)
                                .text_color(t.muted)
                                .child(tr(gpu_about)),
                        )
                        .on_click(cx.listener(|this, _: &ClickEvent, _, cx| {
                            this.flip(Toggle::Gpu);
                            cx.notify();
                        })),
                );
            }
        } else {
            let gpus = horizon_launcher::gpu::list();
            if gpus.len() > 1 {
                let legacy = if now.dedicated_gpu {
                    gpus.iter()
                        .find(|gpu| !gpu.boot_vga)
                        .map(|gpu| gpu.id.clone())
                } else {
                    None
                };
                let current = now.gpu.clone().or(legacy);
                let default_label = self.settings.rust_game_gpu.as_deref().map_or_else(
                    || tr("Use Settings default (automatic)").to_string(),
                    |id| {
                        let name = horizon_launcher::gpu::name(id);
                        trf("Use Settings default ({gpu})", &[("gpu", &name)])
                    },
                );
                let mut choices = div().flex().flex_col().items_stretch().gap(px(6.));
                choices = choices.child(
                    button(
                        "instance-gpu-system",
                        default_label,
                        if current.is_none() {
                            Kind::Primary
                        } else {
                            Kind::Secondary
                        },
                        &t,
                    )
                    .on_click(cx.listener(|this, _: &ClickEvent, _, cx| {
                        this.pick_instance_gpu(None);
                        cx.notify();
                    })),
                );
                for (index, gpu) in gpus.into_iter().enumerate() {
                    let id = gpu.id.clone();
                    let selected = current.as_deref() == Some(id.as_str());
                    let label = match gpu.boot_vga {
                        true => trf("{gpu} (system default)", &[("gpu", &gpu.name)]),
                        false => gpu.name.clone(),
                    };
                    choices = choices.child(
                        button(
                            SharedString::from(format!("instance-gpu-{index}")),
                            label,
                            if selected {
                                Kind::Primary
                            } else {
                                Kind::Secondary
                            },
                            &t,
                        )
                        .on_click(cx.listener(
                            move |this, _: &ClickEvent, _, cx| {
                                this.pick_instance_gpu(Some(id.clone()));
                                cx.notify();
                            },
                        )),
                    );
                }
                list = list.child(
                    div()
                        .flex()
                        .flex_col()
                        .gap(px(8.))
                        .child(caps(tr("Graphics card")).text_color(t.muted))
                        .child(choices)
                        .child(
                            text(theme::CAPTION)
                                .text_color(t.muted)
                                .child(tr("Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.")),
                        ),
                );
            }
        }

        let any = found.gamemode
            || found.mangohud
            || (instance.java.is_some() && found.two_gpus)
            || (instance.java.is_none() && horizon_launcher::gpu::list().len() > 1);
        any.then(|| {
            div()
                .flex()
                .flex_col()
                .gap(px(8.))
                .child(caps(tr("On this computer")).text_color(t.muted))
                .child(list)
        })
    }

'''
text = text[:start] + linux + text[end:]
p.write_text(text)

# Oxidum Home treats Rust Edition and Java Edition as real switchable launch targets.
p = Path("launcher/src/glass_home.rs")
text = p.read_text()
text = text.replace(".child(self.edition_tabs(java.is_some()))", ".child(self.edition_tabs(java.is_some(), cx))")
start = text.find("    /// The edition tabs")
end = text.find("    /// The instance's icon and its name", start)
if start < 0 or end < 0:
    raise SystemExit("Oxidum overlay: Home edition tabs changed upstream")
edition = r'''    /// The edition tabs switch between Rust Edition and Java Edition instances.
    fn edition_tabs(&mut self, java: bool, cx: &mut Context<Self>) -> Div {
        let grass = self.vanilla_icon().and_then(|path| {
            self.icon_image("mark:grass".into(), 18., false, move || {
                std::fs::read(&path).ok()
            })
        });
        let tab = |label: &'static str, icon: AnyElement, open: bool| {
            let d = div()
                .flex()
                .flex_none()
                .items_center()
                .gap(px(6.))
                .h(px(32.))
                .px(px(12.))
                .rounded(px(radius::CONTROL))
                .font_family(horizon_theme::glass::FONT)
                .text_size(px(13.))
                .line_height(px(18.))
                .child(icon)
                .child(tr(label));
            if open {
                d.bg(white(fill::ACTIVE))
                    .font_weight(FontWeight::MEDIUM)
                    .text_color(white(ink::FULL))
            } else {
                d.text_color(white(ink::BODY))
            }
        };
        let java_icon = match grass {
            Some(image) => gpui::img(image)
                .flex_none()
                .size(px(18.))
                .rounded(px(5.))
                .into_any_element(),
            None => div().into_any_element(),
        };
        let rust = tab(
            "Rust Edition",
            ui::mark_tile(18., self.look.accent_soft).into_any_element(),
            !java,
        )
        .id("edition-rust")
        .cursor_pointer()
        .hover(|s| s.bg(white(fill::ACTIVE)))
        .on_click(cx.listener(|this, _: &ClickEvent, _, cx| {
            this.switch_edition(false, cx);
            cx.notify();
        }));
        let java = tab("Java Edition", java_icon, java)
            .id("edition-java")
            .cursor_pointer()
            .hover(|s| s.bg(white(fill::ACTIVE)))
            .on_click(cx.listener(|this, _: &ClickEvent, _, cx| {
                this.switch_edition(true, cx);
                cx.notify();
            }));
        div()
            .flex()
            .items_center()
            .gap(px(4.))
            .child(rust)
            .child(java)
    }

    fn switch_edition(&mut self, java: bool, cx: &mut Context<Self>) {
        if self
            .selected_instance()
            .is_some_and(|instance| instance.java.is_some() == java)
        {
            return;
        }
        self.home_menu = HomeMenu::None;
        self.picker_open = false;
        let existing = self
            .instances
            .list
            .iter()
            .find(|instance| {
                matches!(
                    instance.kind,
                    horizon_launcher::instances::Kind::Default
                        | horizon_launcher::instances::Kind::Own
                ) && instance.java.is_some() == java
            })
            .cloned();
        if let Some(instance) = existing {
            self.select_instance(&instance);
            self.go(Page::Play);
            return;
        }
        self.open_instance_dialog(None);
        self.pick_kind(
            if java {
                new_instance::NewKind::Vanilla
            } else {
                new_instance::NewKind::Horizon
            },
            cx,
        );
    }

'''
text = text[:start] + edition + text[end:]
p.write_text(text)

# Java Edition can launch locally/offline from already-present files without importing secrets.
p = Path("launcher/src/account.rs")
text = p.read_text()
if "pub fn java_local_player()" not in text:
    needle = "pub fn java_player() -> Result<crate::java_launch::Player, String> {"
    if needle not in text:
        raise SystemExit("Oxidum overlay: java_player changed upstream")
    local_player = r'''/// A local/offline Java player for an already-installed game.
pub fn java_local_player() -> crate::java_launch::Player {
    use sha1::{Digest, Sha1};

    let accounts = Accounts::load();
    let name = accounts
        .offline_selected
        .clone()
        .or_else(|| accounts.selected().map(|a| a.name.clone()))
        .or_else(|| accounts.offline.first().cloned())
        .unwrap_or_else(|| "Player".into());
    let digest = Sha1::digest(format!("OxidumOffline:{name}").as_bytes());
    let uuid = digest[..16]
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect::<String>();
    crate::java_launch::Player {
        name,
        uuid,
        token: "0".into(),
        xuid: String::new(),
    }
}

'''
    text = text.replace(needle, local_player + needle, 1)
p.write_text(text)

# One explicit extension point for Java Edition acquisition. Providers populate Oxidum's own
# Minecraft root; runtime, loaders and launch stay inside Oxidum.
p = Path("launcher/src/lib.rs")
text = p.read_text()
if "pub mod java_acquisition;" not in text:
    needle = "pub mod java;\n"
    if needle not in text:
        raise SystemExit("Oxidum overlay: Java module list changed upstream")
    text = text.replace(needle, needle + "pub mod java_acquisition;\n", 1)
p.write_text(text)

Path("launcher/src/java_acquisition.rs").write_text(r'''//! Java Edition acquisition providers.
//!
//! This module is the single extension point between "the requested Java version is not present
//! locally" and Oxidum's built-in official download fallback. A provider may populate Oxidum's own
//! Minecraft root from any source it is allowed to use, then report `Acquired`. Runtime selection,
//! loader installation and launching stay in Oxidum.
//!
//! To add another provider, implement [`Provider`] and register it in [`providers`]. The backend
//! does not need to change.

use crate::mojang;
use std::path::Path;

/// Everything a Java acquisition provider needs to prepare one vanilla Minecraft version.
///
/// Providers write into `destination`, which is Oxidum's own Minecraft root. They do not need to
/// install Fabric/Quilt/Forge/NeoForge or a Java runtime; Oxidum does those after acquisition.
pub struct Request<'a> {
    pub minecraft: &'a str,
    pub manifest_sha1: &'a str,
    pub destination: &'a Path,
}

/// Whether a provider handled this request.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Outcome {
    /// This provider does not handle the request; Oxidum tries the next one.
    NotHandled,
    /// The provider populated `Request::destination` with the requested vanilla game files.
    Acquired,
}

/// A pluggable source for Java Edition game files.
///
/// A provider owns only acquisition. It should return `Acquired` after the requested version has
/// been fully written to Oxidum's destination root, and `NotHandled` when another provider or the
/// built-in fallback should be tried.
pub trait Provider {
    /// Stable diagnostic name shown in the launch log.
    fn id(&self) -> &'static str;

    fn acquire(
        &self,
        request: &Request<'_>,
        log: &dyn Fn(String),
    ) -> Result<Outcome, String>;
}

/// Provider registry.
///
/// Extension point: add `Box::new(YourProvider)` here. Keeping this list in one module means a
/// custom acquisition implementation never has to patch `backend::java_game`.
fn providers() -> Vec<Box<dyn Provider>> {
    vec![]
}

/// Gives every registered provider one chance to prepare the requested Java version.
///
/// Returns `true` only after a provider reports success and Oxidum verifies the minimum launcher
/// layout it needs. `false` tells the caller to use the existing built-in fallback.
pub fn acquire(request: &Request<'_>, log: &dyn Fn(String)) -> Result<bool, String> {
    for provider in providers() {
        match provider.acquire(request, log)? {
            Outcome::NotHandled => continue,
            Outcome::Acquired => {
                validate_layout(request)?;
                log(format!(
                    "Java Edition {} acquired by provider {}",
                    request.minecraft,
                    provider.id()
                ));
                return Ok(true);
            }
        }
    }
    Ok(false)
}

fn validate_layout(request: &Request<'_>) -> Result<(), String> {
    let version = mojang::relative(request.minecraft)?;
    let version_dir = request.destination.join("versions").join(version);
    let version_json = version_dir.join(format!("{}.json", request.minecraft));
    let client_jar = version_dir.join(format!("{}.jar", request.minecraft));

    for (path, label) in [
        (request.destination.join("assets"), "assets"),
        (request.destination.join("libraries"), "libraries"),
        (version_json, "version JSON"),
        (client_jar, "client jar"),
    ] {
        let present = if label == "assets" || label == "libraries" {
            path.is_dir()
        } else {
            path.is_file()
        };
        if !present {
            return Err(format!(
                "Java acquisition provider reported success, but {label} is missing at {}",
                path.display()
            ));
        }
    }
    Ok(())
}
''')

p = Path("launcher/src/backend.rs")
text = p.read_text()
if "fn prism_java_roots()" not in text:
    doc = "/// The command that starts a Java instance's Minecraft, for an account that owns the game: its"
    at = text.find(doc)
    if at < 0:
        raise SystemExit("Oxidum overlay: java_game documentation changed upstream")
    helpers = r'''/// Roots from Prism-family launchers whose public game files Oxidum can reuse.
fn prism_java_roots() -> Vec<PathBuf> {
    let Some(home) = std::env::var_os("HOME").map(PathBuf::from) else {
        return Vec::new();
    };
    let data = std::env::var_os("XDG_DATA_HOME")
        .map(PathBuf::from)
        .unwrap_or_else(|| home.join(".local/share"));
    [
        data.join("HalkyLauncher"),
        data.join("FreesmLauncher"),
        data.join("PrismLauncher"),
        home.join(".var/app/org.HalkyLauncher.HalkyLauncher/data/HalkyLauncher"),
        home.join(".var/app/org.freesmlauncher.FreesmLauncher/data/FreesmLauncher"),
        home.join(".var/app/org.prismlauncher.PrismLauncher/data/PrismLauncher"),
    ]
    .into_iter()
    .filter(|path| path.is_dir())
    .collect()
}

fn reusable_java_root(root: &Path, minecraft: &str, start_id: &str) -> bool {
    let Ok(game) = mojang::relative(minecraft) else {
        return false;
    };
    let Ok(start) = mojang::relative(start_id) else {
        return false;
    };
    let base = root
        .join("versions")
        .join(&game)
        .join(format!("{minecraft}.json"));
    let profile = root
        .join("versions")
        .join(&start)
        .join(format!("{start_id}.json"));
    root.join("assets").is_dir()
        && root.join("libraries").is_dir()
        && base.is_file()
        && profile.is_file()
}

fn java_minecraft_root(minecraft: &str, start: &str) -> (PathBuf, bool) {
    let own = data_dir().join("minecraft");
    if reusable_java_root(&own, minecraft, start) {
        return (own, true);
    }
    if let Some(root) = prism_java_roots()
        .into_iter()
        .find(|root| reusable_java_root(root, minecraft, start))
    {
        return (root, true);
    }
    (own, false)
}

fn acquire_java_version(
    id: &str,
    manifest_sha1: &str,
    log: &dyn Fn(String),
) -> Result<(), String> {
    let destination = data_dir().join("minecraft");
    let request = crate::java_acquisition::Request {
        minecraft: id,
        manifest_sha1,
        destination: &destination,
    };
    if crate::java_acquisition::acquire(&request, log)? {
        return Ok(());
    }
    download_version_for_owner(id, manifest_sha1, log).map(|_| ())
}

'''
    text = text[:at] + helpers + text[at:]

start = text.find("pub fn java_game(")
end = text.find("\n/// What [", start)
if start < 0 or end < 0:
    raise SystemExit("Oxidum overlay: java_game changed upstream")
java_game = r'''pub fn java_game(
    instance: &crate::instances::Instance,
    server: Option<&str>,
    log: &dyn Fn(String),
) -> Result<Command, String> {
    let game = instance.java.as_ref().ok_or_else(|| {
        format!(
            "{} plays Oxidum's Rust Edition, not Minecraft: Java Edition",
            instance.name
        )
    })?;

    let mut start = game.minecraft.clone();
    if let Some(loader) = &game.loader {
        start = loader.kind.profile_id(&loader.version, &game.minecraft);
    }

    let (minecraft, mut local_files) = java_minecraft_root(&game.minecraft, &start);
    let id = mojang::relative(&game.minecraft)?;
    let downloaded = |root: &Path, id: &str| -> Result<PathBuf, String> {
        Ok(root
            .join("versions")
            .join(mojang::relative(id)?)
            .join(".downloaded"))
    };

    if !local_files {
        let marker = downloaded(&minecraft, &game.minecraft)?;
        if !marker.is_file() {
            let listed = crate::minecraft_versions::load()?;
            let version = listed.find(&game.minecraft)?;
            acquire_java_version(&version.id, &version.sha1, log)?;
            fs::write(&marker, "").map_err(|e| format!("{}: {e}", marker.display()))?;
        }
        local_files = true;
    } else if minecraft != data_dir().join("minecraft") {
        log(format!(
            "Reusing Minecraft {} files from {}",
            game.minecraft,
            minecraft.display()
        ));
    }

    // Select Java from the vanilla profile before installing a loader. Newer Horizon-Free
    // loaders use this runtime for Forge/NeoForge installers.
    let base_file = minecraft
        .join("versions")
        .join(mojang::relative(&game.minecraft)?)
        .join(format!("{}.json", game.minecraft));
    let vanilla = crate::java_launch::read(&base_file)?;
    let base_version = crate::java_launch::resolve(vanilla, &minecraft)?;
    let need = crate::java::Need::of(&base_version);
    let found = crate::java::pick(
        &need,
        game.home.as_deref(),
        &crate::java::mojang_runtimes(&crate::java::runtimes_dir()),
        &crate::java::installed(),
    )?;
    let runtime = match found {
        Some(runtime) => runtime,
        None => {
            log(format!("Downloading Java {} from Mojang", need.major));
            crate::java::install(&need, log)?
        }
    };

    if let Some(loader) = &game.loader {
        let profile = minecraft
            .join("versions")
            .join(mojang::relative(&start)?)
            .join(format!("{start}.json"));
        if !profile.is_file() {
            start = __OXIDUM_LOADER_INSTALL__;
            fs::write(downloaded(&minecraft, &start)?, "").map_err(|e| e.to_string())?;
        }
    }

    let natives = minecraft.join("natives").join(&id);
    let file = minecraft
        .join("versions")
        .join(mojang::relative(&start)?)
        .join(format!("{start}.json"));
    let version = crate::java_launch::resolve(crate::java_launch::read(&file)?, &minecraft)?;

    let player = if OFFLINE_PLAY && local_files {
        account::java_local_player()
    } else {
        account::java_player()?
    };
    let jvm_args: Vec<String> = game.jvm_args.split_whitespace().map(String::from).collect();
    fs::create_dir_all(&instance.home).map_err(|e| format!("{}: {e}", instance.home.display()))?;
    crate::java_launch::command(
        &version,
        &crate::java_launch::Launch {
            minecraft: &minecraft,
            game_dir: &instance.home,
            natives: &natives,
            java: &runtime.java(),
            memory_mb: game
                .memory_mb
                .unwrap_or(crate::instances::DEFAULT_MEMORY_MB),
            jvm_args: &jvm_args,
            player: &player,
            os: crate::java_launch::os_name(),
            window: game.window,
            server,
        },
    )
}
'''
loaders_source = Path("launcher/src/loaders.rs").read_text()
if "    java: &Path," in loaders_source:
    loader_install = """crate::loaders::install(
                loader,
                &game.minecraft,
                &minecraft,
                &runtime.java(),
                &get_bytes,
                log,
            )?"""
else:
    loader_install = """crate::loaders::install(
                loader,
                &game.minecraft,
                &minecraft,
                &get_bytes,
                log,
            )?"""
java_game = java_game.replace("__OXIDUM_LOADER_INSTALL__", loader_install)
text = text[:start] + java_game + text[end:]
p.write_text(text)

p = Path("launcher/src/main.rs")
text = p.read_text()
text = text.replace(
    "Minecraft {version} (Java Edition). Play downloads it from Mojang for your account the first time, with the Java it needs.",
    "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.",
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
    'const NAMES: [&str; 8] = [\n    "oxidum", "violet", "blue", "teal", "green", "amber", "red", "pink",\n];',
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
text = text.replace(
    'self.field(Field::AccentHex, "#6b4bff", 96., cx)',
    'self.field(Field::AccentHex, "#b85b29", 96., cx)',
)
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
for old, new in [
    ("--glass-accent: #6b4bff;", "--glass-accent: #b85b29;"),
    ("--glass-accent-soft: #a9a9ff;", "--glass-accent-soft: #deaa91;"),
    ("--glass-base: #1b1830;", "--glass-base: #272125;"),
    ("--glass-page: #0a0919;", "--glass-page: #181a22;"),
    ("--glass-live: #4ade80;", "--glass-live: #55ad93;"),
    ("--glass-warn: #f2c46b;", "--glass-warn: #eb9655;"),
    ("--glass-plate: rgba(78, 76, 95, 0.267);", "--glass-plate: rgba(88, 83, 86, 0.267);"),
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
    "Horizon and its icon are in your desktop's menu.": "Oxidum and its icon are in your desktop's menu.",
}
gpu_translation_keys = {
    "ar": {
        "Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.": "اختر بطاقة رسوميات بديلة لهذه النسخة من Minecraft المكتوبة بـ Rust، أو استخدم الإعداد الافتراضي من الإعدادات. يضبط Oxidum تقنية PRIME تلقائيًا.",
        "Graphics card": "بطاقة الرسوميات",
        "Automatic / system": "تلقائي / النظام",
        "Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens.": "اختر بطاقة الرسوميات التي تعرض Oxidum. يحافظ الوضع التلقائي على طريقة تشغيل Oxidum كما هي؛ ويتم تطبيق بطاقة محددة عند فتح Oxidum في المرة التالية.",
        "Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings.": "بطاقة الرسوميات الافتراضية لنسخ Minecraft المكتوبة بـ Rust. يمكن لكل نسخة تجاوز هذا الإعداد من إعدادات التشغيل الخاصة بها.",
        "Launcher graphics card": "بطاقة رسوميات المشغّل",
        "Rust Minecraft graphics card": "بطاقة رسوميات Minecraft بلغة Rust",
        "Use Settings default (automatic)": "استخدام الإعداد الافتراضي من الإعدادات (تلقائي)",
        "Use Settings default ({gpu})": "استخدام الإعداد الافتراضي من الإعدادات ({gpu})",
        "on {gpu}": "على {gpu}",
        "{gpu} (system default)": "{gpu} (إعداد النظام الافتراضي)"
    },
    "de": {
        "Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.": "Wähle für diese Rust-Minecraft-Instanz eine abweichende GPU oder verwende den Standard aus den Einstellungen. Oxidum konfiguriert PRIME automatisch.",
        "Graphics card": "Grafikkarte",
        "Automatic / system": "Automatisch / System",
        "Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens.": "Wähle die GPU, die Oxidum rendert. Automatisch behält bei, wie Oxidum gestartet wurde; eine bestimmte Karte wird beim nächsten Start von Oxidum verwendet.",
        "Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings.": "Standard-GPU für Rust-Minecraft-Instanzen. Eine einzelne Instanz kann dies in ihren Starteinstellungen überschreiben.",
        "Launcher graphics card": "Grafikkarte des Launchers",
        "Rust Minecraft graphics card": "Grafikkarte für Rust-Minecraft",
        "Use Settings default (automatic)": "Standard aus den Einstellungen verwenden (automatisch)",
        "Use Settings default ({gpu})": "Standard aus den Einstellungen verwenden ({gpu})",
        "on {gpu}": "auf {gpu}",
        "{gpu} (system default)": "{gpu} (Systemstandard)"
    },
    "es": {
        "Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.": "Elige una GPU distinta para esta instancia de Minecraft en Rust o usa la predeterminada de Ajustes. Oxidum configura PRIME automáticamente.",
        "Graphics card": "Tarjeta gráfica",
        "Automatic / system": "Automático / sistema",
        "Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens.": "Elige la GPU que renderiza Oxidum. Automático conserva la forma en que se inició Oxidum; una tarjeta específica se aplicará la próxima vez que se abra Oxidum.",
        "Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings.": "GPU predeterminada para las instancias de Minecraft en Rust. Cada instancia puede anularla en sus ajustes de inicio.",
        "Launcher graphics card": "Tarjeta gráfica del launcher",
        "Rust Minecraft graphics card": "Tarjeta gráfica de Minecraft en Rust",
        "Use Settings default (automatic)": "Usar predeterminada de Ajustes (automático)",
        "Use Settings default ({gpu})": "Usar predeterminada de Ajustes ({gpu})",
        "on {gpu}": "en {gpu}",
        "{gpu} (system default)": "{gpu} (predeterminada del sistema)"
    },
    "fr": {
        "Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.": "Choisis un GPU différent pour cette instance Minecraft Rust, ou utilise celui par défaut des paramètres. Oxidum configure PRIME automatiquement.",
        "Graphics card": "Carte graphique",
        "Automatic / system": "Automatique / système",
        "Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens.": "Choisis le GPU qui affiche Oxidum. Automatique conserve la façon dont Oxidum a été lancé ; une carte précise sera utilisée au prochain démarrage d’Oxidum.",
        "Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings.": "GPU par défaut pour les instances Minecraft Rust. Chaque instance peut le remplacer dans ses paramètres de lancement.",
        "Launcher graphics card": "Carte graphique du launcher",
        "Rust Minecraft graphics card": "Carte graphique de Minecraft Rust",
        "Use Settings default (automatic)": "Utiliser le choix par défaut des paramètres (automatique)",
        "Use Settings default ({gpu})": "Utiliser le choix par défaut des paramètres ({gpu})",
        "on {gpu}": "sur {gpu}",
        "{gpu} (system default)": "{gpu} (choix par défaut du système)"
    },
    "hi": {
        "Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.": "इस Rust Minecraft इंस्टेंस के लिए कोई अलग GPU चुनें, या Settings का डिफ़ॉल्ट इस्तेमाल करें। Oxidum PRIME को अपने आप कॉन्फ़िगर करता है।",
        "Graphics card": "ग्राफ़िक्स कार्ड",
        "Automatic / system": "स्वचालित / सिस्टम",
        "Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens.": "Oxidum को रेंडर करने वाला GPU चुनें। स्वचालित मोड Oxidum को शुरू करने के मौजूदा तरीके को बनाए रखता है; चुना गया कार्ड अगली बार Oxidum खुलने पर लागू होगा।",
        "Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings.": "Rust Minecraft इंस्टेंस के लिए डिफ़ॉल्ट GPU। हर इंस्टेंस अपनी लॉन्च सेटिंग में इसे बदल सकता है।",
        "Launcher graphics card": "लॉन्चर ग्राफ़िक्स कार्ड",
        "Rust Minecraft graphics card": "Rust Minecraft ग्राफ़िक्स कार्ड",
        "Use Settings default (automatic)": "Settings का डिफ़ॉल्ट इस्तेमाल करें (स्वचालित)",
        "Use Settings default ({gpu})": "Settings का डिफ़ॉल्ट इस्तेमाल करें ({gpu})",
        "on {gpu}": "{gpu} पर",
        "{gpu} (system default)": "{gpu} (सिस्टम डिफ़ॉल्ट)"
    },
    "hr": {
        "Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.": "Odaberi drugu grafičku karticu za ovu Rust Minecraft instancu ili koristi zadanu iz postavki. Oxidum automatski podešava PRIME.",
        "Graphics card": "Grafička kartica",
        "Automatic / system": "Automatski / sustav",
        "Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens.": "Odaberi GPU koji prikazuje Oxidum. Automatski način zadržava način na koji je Oxidum pokrenut; određena kartica primjenjuje se pri sljedećem pokretanju Oxiduma.",
        "Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings.": "Zadani GPU za Rust Minecraft instance. Pojedina instanca može ga nadjačati u svojim postavkama pokretanja.",
        "Launcher graphics card": "Grafička kartica pokretača",
        "Rust Minecraft graphics card": "Grafička kartica za Rust Minecraft",
        "Use Settings default (automatic)": "Koristi zadano iz postavki (automatski)",
        "Use Settings default ({gpu})": "Koristi zadano iz postavki ({gpu})",
        "on {gpu}": "na {gpu}",
        "{gpu} (system default)": "{gpu} (zadano sustavom)"
    },
    "id": {
        "Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.": "Pilih GPU khusus untuk instans Minecraft Rust ini, atau gunakan default dari Pengaturan. Oxidum mengatur PRIME secara otomatis.",
        "Graphics card": "Kartu grafis",
        "Automatic / system": "Otomatis / sistem",
        "Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens.": "Pilih GPU yang merender Oxidum. Otomatis mempertahankan cara Oxidum dijalankan; kartu tertentu diterapkan saat Oxidum dibuka berikutnya.",
        "Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings.": "GPU default untuk instans Minecraft Rust. Setiap instans dapat menggantinya di pengaturan peluncurannya.",
        "Launcher graphics card": "Kartu grafis launcher",
        "Rust Minecraft graphics card": "Kartu grafis Minecraft Rust",
        "Use Settings default (automatic)": "Gunakan default Pengaturan (otomatis)",
        "Use Settings default ({gpu})": "Gunakan default Pengaturan ({gpu})",
        "on {gpu}": "di {gpu}",
        "{gpu} (system default)": "{gpu} (default sistem)"
    },
    "ja": {
        "Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.": "このRust Minecraftインスタンス用に別のGPUを選ぶか、設定のデフォルトを使用します。OxidumがPRIMEを自動で設定します。",
        "Graphics card": "グラフィックカード",
        "Automatic / system": "自動 / システム",
        "Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens.": "Oxidum の描画に使う GPU を選択します。自動では Oxidum の起動方法をそのまま使用し、特定のカードを選ぶと次回 Oxidum 起動時に適用されます。",
        "Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings.": "Rust Minecraft インスタンスの既定 GPU です。各インスタンスの起動設定で上書きできます。",
        "Launcher graphics card": "ランチャーのグラフィックカード",
        "Rust Minecraft graphics card": "Rust Minecraftのグラフィックカード",
        "Use Settings default (automatic)": "設定のデフォルトを使用（自動）",
        "Use Settings default ({gpu})": "設定のデフォルトを使用（{gpu}）",
        "on {gpu}": "{gpu} で実行",
        "{gpu} (system default)": "{gpu}（システム既定）"
    },
    "ko": {
        "Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.": "이 Rust Minecraft 인스턴스에 사용할 GPU를 따로 선택하거나 설정의 기본값을 사용하세요. Oxidum이 PRIME을 자동으로 구성합니다.",
        "Graphics card": "그래픽 카드",
        "Automatic / system": "자동 / 시스템",
        "Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens.": "Oxidum을 렌더링할 GPU를 선택하세요. 자동은 Oxidum이 시작된 방식을 그대로 유지하며, 특정 카드를 선택하면 다음에 Oxidum을 열 때 적용됩니다.",
        "Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings.": "Rust Minecraft 인스턴스의 기본 GPU입니다. 각 인스턴스의 실행 설정에서 재정의할 수 있습니다.",
        "Launcher graphics card": "런처 그래픽 카드",
        "Rust Minecraft graphics card": "Rust Minecraft 그래픽 카드",
        "Use Settings default (automatic)": "설정 기본값 사용 (자동)",
        "Use Settings default ({gpu})": "설정 기본값 사용 ({gpu})",
        "on {gpu}": "{gpu}에서",
        "{gpu} (system default)": "{gpu} (시스템 기본값)"
    },
    "pl": {
        "Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.": "Wybierz inną kartę graficzną dla tej instancji Minecrafta w Rust albo użyj domyślnej z ustawień. Oxidum automatycznie skonfiguruje PRIME.",
        "Graphics card": "Karta graficzna",
        "Automatic / system": "Automatycznie / system",
        "Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens.": "Wybierz GPU renderujący Oxidum. Tryb automatyczny zachowuje sposób uruchomienia Oxidum; wybrana karta zostanie użyta przy następnym uruchomieniu Oxidum.",
        "Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings.": "Domyślny GPU dla instancji Minecrafta w Rust. Każda instancja może go zastąpić w swoich ustawieniach uruchamiania.",
        "Launcher graphics card": "Karta graficzna launchera",
        "Rust Minecraft graphics card": "Karta graficzna Minecrafta w Rust",
        "Use Settings default (automatic)": "Użyj domyślnej z ustawień (automatycznie)",
        "Use Settings default ({gpu})": "Użyj domyślnej z ustawień ({gpu})",
        "on {gpu}": "na {gpu}",
        "{gpu} (system default)": "{gpu} (domyślna systemowa)"
    },
    "pt-br": {
        "Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.": "Escolha uma placa de vídeo específica para esta instância do Minecraft em Rust ou use o padrão das Configurações. O Oxidum configura o PRIME automaticamente.",
        "Graphics card": "Placa de vídeo",
        "Automatic / system": "Automático / sistema",
        "Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens.": "Escolha a GPU que renderiza o Oxidum. Automático mantém exatamente a forma como o Oxidum foi iniciado; uma placa específica será aplicada na próxima vez que o Oxidum abrir.",
        "Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings.": "GPU padrão para instâncias do Minecraft em Rust. Cada instância pode substituir esse padrão nas próprias configurações de inicialização.",
        "Launcher graphics card": "Placa de vídeo do launcher",
        "Rust Minecraft graphics card": "Placa de vídeo do Minecraft em Rust",
        "Use Settings default (automatic)": "Usar padrão das Configurações (automático)",
        "Use Settings default ({gpu})": "Usar padrão das Configurações ({gpu})",
        "on {gpu}": "na {gpu}",
        "{gpu} (system default)": "{gpu} (padrão do sistema)"
    },
    "pt": {
        "Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.": "Escolha uma placa gráfica específica para esta instância do Minecraft em Rust ou use a predefinição das Definições. O Oxidum configura o PRIME automaticamente.",
        "Graphics card": "Placa gráfica",
        "Automatic / system": "Automático / sistema",
        "Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens.": "Escolha a GPU que renderiza o Oxidum. Automático mantém a forma como o Oxidum foi iniciado; uma placa específica será aplicada da próxima vez que o Oxidum abrir.",
        "Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings.": "GPU predefinida para instâncias do Minecraft em Rust. Cada instância pode substituí-la nas respetivas definições de arranque.",
        "Launcher graphics card": "Placa gráfica do launcher",
        "Rust Minecraft graphics card": "Placa gráfica do Minecraft em Rust",
        "Use Settings default (automatic)": "Usar predefinição das Definições (automático)",
        "Use Settings default ({gpu})": "Usar predefinição das Definições ({gpu})",
        "on {gpu}": "na {gpu}",
        "{gpu} (system default)": "{gpu} (predefinição do sistema)"
    },
    "ru": {
        "Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.": "Выберите видеокарту для этого экземпляра Minecraft на Rust или используйте значение по умолчанию из настроек. Oxidum настроит PRIME автоматически.",
        "Graphics card": "Видеокарта",
        "Automatic / system": "Автоматически / система",
        "Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens.": "Выберите GPU для отрисовки Oxidum. Автоматический режим сохраняет способ запуска Oxidum; выбранная видеокарта будет применена при следующем запуске Oxidum.",
        "Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings.": "GPU по умолчанию для экземпляров Minecraft на Rust. Для каждого экземпляра его можно переопределить в настройках запуска.",
        "Launcher graphics card": "Видеокарта лаунчера",
        "Rust Minecraft graphics card": "Видеокарта Minecraft на Rust",
        "Use Settings default (automatic)": "Использовать значение из настроек (автоматически)",
        "Use Settings default ({gpu})": "Использовать значение из настроек ({gpu})",
        "on {gpu}": "на {gpu}",
        "{gpu} (system default)": "{gpu} (системная по умолчанию)"
    },
    "tr": {
        "Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.": "Bu Rust Minecraft örneği için bir ekran kartı seçin veya Ayarlar'daki varsayılanı kullanın. Oxidum PRIME yapılandırmasını otomatik olarak yapar.",
        "Graphics card": "Ekran kartı",
        "Automatic / system": "Otomatik / sistem",
        "Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens.": "Oxidum'u işleyen GPU'yu seçin. Otomatik seçenek, Oxidum'un başlatılma biçimini korur; belirli bir kart seçerseniz bir sonraki Oxidum açılışında uygulanır.",
        "Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings.": "Rust Minecraft örnekleri için varsayılan GPU. Her örnek bunu kendi başlatma ayarlarında geçersiz kılabilir.",
        "Launcher graphics card": "Başlatıcının ekran kartı",
        "Rust Minecraft graphics card": "Rust Minecraft ekran kartı",
        "Use Settings default (automatic)": "Ayarlar varsayılanını kullan (otomatik)",
        "Use Settings default ({gpu})": "Ayarlar varsayılanını kullan ({gpu})",
        "on {gpu}": "{gpu} üzerinde",
        "{gpu} (system default)": "{gpu} (sistem varsayılanı)"
    },
    "uk": {
        "Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.": "Виберіть відеокарту для цього екземпляра Minecraft на Rust або використайте типове значення з Налаштувань. Oxidum налаштує PRIME автоматично.",
        "Graphics card": "Відеокарта",
        "Automatic / system": "Автоматично / система",
        "Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens.": "Виберіть GPU для відтворення Oxidum. Автоматичний режим зберігає спосіб запуску Oxidum; вибрана відеокарта буде застосована під час наступного запуску Oxidum.",
        "Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings.": "Типовий GPU для екземплярів Minecraft на Rust. Кожен екземпляр може перевизначити його у своїх налаштуваннях запуску.",
        "Launcher graphics card": "Відеокарта лаунчера",
        "Rust Minecraft graphics card": "Відеокарта Minecraft на Rust",
        "Use Settings default (automatic)": "Використати типове з Налаштувань (автоматично)",
        "Use Settings default ({gpu})": "Використати типове з Налаштувань ({gpu})",
        "on {gpu}": "на {gpu}",
        "{gpu} (system default)": "{gpu} (системна за замовчуванням)"
    },
    "zh": {
        "Choose an override for this Rust Minecraft instance, or use the default from Settings. Oxidum configures PRIME automatically.": "为这个 Rust Minecraft 实例选择显卡，或使用“设置”中的默认值。Oxidum 会自动配置 PRIME。",
        "Graphics card": "显卡",
        "Automatic / system": "自动 / 系统",
        "Choose the GPU that renders Oxidum. Automatic keeps the way Oxidum was started; a specific card is applied the next time Oxidum opens.": "选择用于渲染 Oxidum 的 GPU。自动模式会保持 Oxidum 当前的启动方式；选择特定显卡后，将在下次打开 Oxidum 时生效。",
        "Default GPU for Rust Minecraft instances. An individual instance can override this in its launch settings.": "Rust Minecraft 实例的默认 GPU。单个实例可在其启动设置中覆盖此默认值。",
        "Launcher graphics card": "启动器显卡",
        "Rust Minecraft graphics card": "Rust Minecraft 显卡",
        "Use Settings default (automatic)": "使用设置默认值（自动）",
        "Use Settings default ({gpu})": "使用设置默认值（{gpu}）",
        "on {gpu}": "使用 {gpu}",
        "{gpu} (system default)": "{gpu}（系统默认）"
    }
}

java_translation_keys = {
    "ar": {
        "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.": "Minecraft {version} (إصدار Java). يعيد Oxidum استخدام ملفات Freesm أو Halky أو Prism المتوافقة عندما تكون مثبتة بالفعل؛ وإلا فسيقوم التشغيل بتنزيل اللعبة من Mojang باستخدام حساب يملكها."
    },
    "de": {
        "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.": "Minecraft {version} (Java Edition). Oxidum verwendet kompatible Freesm-, Halky- oder Prism-Dateien wieder, wenn sie bereits installiert sind; andernfalls lädt Spielen das Spiel von Mojang für ein Konto herunter, dem es gehört."
    },
    "es": {
        "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.": "Minecraft {version} (Java Edition). Oxidum reutiliza archivos compatibles de Freesm, Halky o Prism cuando ya están instalados; de lo contrario, Jugar descarga el juego desde Mojang para una cuenta que lo posea."
    },
    "fr": {
        "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.": "Minecraft {version} (édition Java). Oxidum réutilise les fichiers compatibles de Freesm, Halky ou Prism lorsqu’ils sont déjà installés ; sinon, Jouer télécharge le jeu depuis Mojang pour un compte qui le possède."
    },
    "hi": {
        "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.": "Minecraft {version} (Java Edition)। यदि संगत Freesm, Halky या Prism फ़ाइलें पहले से इंस्टॉल हैं, तो Oxidum उनका पुनः उपयोग करता है; अन्यथा Play स्वामित्व वाले खाते के लिए Mojang से गेम डाउनलोड करता है।"
    },
    "hr": {
        "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.": "Minecraft {version} (Java Edition). Oxidum ponovno koristi kompatibilne datoteke iz Freesma, Halkyja ili Prisma ako su već instalirane; u suprotnom Play preuzima igru s Mojanga za račun koji je posjeduje."
    },
    "id": {
        "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.": "Minecraft {version} (Java Edition). Oxidum menggunakan kembali berkas Freesm, Halky, atau Prism yang kompatibel jika sudah terpasang; jika tidak, Play mengunduh game dari Mojang untuk akun yang memilikinya."
    },
    "ja": {
        "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.": "Minecraft {version} (Java Edition)。互換性のある Freesm、Halky、Prism のファイルがすでにインストールされている場合、Oxidum はそれらを再利用します。それ以外の場合は、所有権のあるアカウントで Mojang からゲームをダウンロードします。"
    },
    "ko": {
        "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.": "Minecraft {version} (Java Edition). 호환되는 Freesm, Halky 또는 Prism 파일이 이미 설치되어 있으면 Oxidum이 이를 재사용합니다. 그렇지 않으면 소유 계정으로 Mojang에서 게임을 다운로드합니다."
    },
    "pl": {
        "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.": "Minecraft {version} (Java Edition). Oxidum ponownie wykorzystuje zgodne pliki Freesm, Halky lub Prism, jeśli są już zainstalowane; w przeciwnym razie Play pobiera grę z Mojang dla konta, które ją posiada."
    },
    "pt-br": {
        "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.": "Minecraft {version} (Java Edition). O Oxidum reutiliza arquivos compatíveis do Freesm, Halky ou Prism quando já estão instalados; caso contrário, Jogar baixa o jogo da Mojang para uma conta que o possua."
    },
    "pt": {
        "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.": "Minecraft {version} (Java Edition). O Oxidum reutiliza ficheiros compatíveis do Freesm, Halky ou Prism quando já estão instalados; caso contrário, Jogar transfere o jogo da Mojang para uma conta que o possua."
    },
    "ru": {
        "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.": "Minecraft {version} (Java Edition). Oxidum повторно использует совместимые файлы Freesm, Halky или Prism, если они уже установлены; иначе «Играть» загружает игру с Mojang для учётной записи, которой она принадлежит."
    },
    "tr": {
        "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.": "Minecraft {version} (Java Edition). Oxidum, uyumlu Freesm, Halky veya Prism dosyaları zaten kuruluysa bunları yeniden kullanır; aksi takdirde Oyna, oyuna sahip bir hesap için oyunu Mojang’dan indirir."
    },
    "uk": {
        "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.": "Minecraft {version} (Java Edition). Oxidum повторно використовує сумісні файли Freesm, Halky або Prism, якщо вони вже встановлені; інакше «Грати» завантажує гру з Mojang для облікового запису, якому вона належить."
    },
    "zh": {
        "Minecraft {version} (Java Edition). Oxidum reuses compatible Freesm, Halky or Prism files when they are already installed; otherwise Play downloads the game from Mojang for an owning account.": "Minecraft {version}（Java 版）。如果已安装兼容的 Freesm、Halky 或 Prism 文件，Oxidum 会直接复用；否则，“游玩”会通过拥有该游戏的账户从 Mojang 下载游戏。"
    }
}
obsolete_java_translation_keys = {
    "Minecraft {version} (Java Edition). Play downloads it from Mojang for your account the first time, with the Java it needs.",
}

obsolete_gpu_translation_keys = {
    "Mesa's DRI_PRIME=1, so Vulkan picks the other card.",
    "NVIDIA render offload: __NV_PRIME_RENDER_OFFLOAD and its Vulkan layer.",
}

for lang in Path("launcher/lang").glob("*.json"):
    original = json.loads(lang.read_text())
    branded = {}
    for key, value in original.items():
        new_key = translation_keys.get(key, key)
        if key in translation_keys and isinstance(value, str):
            value = value.replace("Horizon", "Oxidum")
        branded[new_key] = value
    for key in obsolete_gpu_translation_keys:
        branded.pop(key, None)
    for key in obsolete_java_translation_keys:
        branded.pop(key, None)
    branded.update(gpu_translation_keys.get(lang.stem, {}))
    branded.update(java_translation_keys.get(lang.stem, {}))
    lang.write_text(json.dumps(branded, ensure_ascii=False, indent=2) + "\n")
