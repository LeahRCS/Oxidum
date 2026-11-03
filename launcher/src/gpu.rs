//! Linux graphics-adapter discovery and PRIME selection for Oxidum.
//!
//! The user-facing choice is a stable PCI id such as pci:0000:01:00.0 rather than "GPU 1":
//! DRM card numbers can change across boots. Friendly names come from udev's PCI database when
//! available; the PCI id and driver remain enough to identify a card when that database is absent.
//!
//! Rust game instances also receive HORIZON_GPU. The Horizon renderer matches that id against
//! wgpu's adapter PCI bus id, so the game does not have to rely on PRIME ordering alone.

use std::process::Command;

/// The adapter id the Rust client reads when it chooses its wgpu adapter.
pub const HORIZON_GPU: &str = "HORIZON_GPU";
/// Friendly adapter name passed beside the PCI id as a fallback for backends that do not expose
/// a PCI bus id through wgpu.
pub const HORIZON_GPU_NAME: &str = "HORIZON_GPU_NAME";

/// Environment variables used by Mesa/NVIDIA PRIME offload.
pub const PRIME_ENV: [&str; 4] = [
    "DRI_PRIME",
    "__NV_PRIME_RENDER_OFFLOAD",
    "__VK_LAYER_NV_optimus",
    "__GLX_VENDOR_LIBRARY_NAME",
];

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Gpu {
    /// Stable choice written to settings: pci:<domain>:<bus>:<device>.<function>.
    pub id: String,
    /// Human-readable adapter name, e.g. NVIDIA GeForce GTX 1660 Ti Mobile.
    pub name: String,
    /// PCI slot without the pci: prefix.
    pub pci_slot: String,
    pub vendor: u16,
    pub device: u16,
    /// Kernel driver, e.g. nvidia, amdgpu, i915.
    pub driver: String,
    /// The display/default VGA device according to sysfs.
    pub boot_vga: bool,
}

impl Gpu {
    /// Mesa's stable PCI selector for DRI_PRIME.
    pub fn dri_prime(&self) -> String {
        format!("pci-{}", self.pci_slot.replace(':', "_").replace('.', "_"))
    }

    fn proprietary_nvidia(&self) -> bool {
        self.vendor == 0x10de && self.driver.starts_with("nvidia")
    }
}

/// Physical DRM GPUs visible on this Linux system, default/display adapter first.
pub fn list() -> Vec<Gpu> {
    #[cfg(target_os = "linux")]
    {
        linux_gpus()
    }
    #[cfg(not(target_os = "linux"))]
    {
        Vec::new()
    }
}

pub fn find(id: &str) -> Option<Gpu> {
    list().into_iter().find(|gpu| gpu.id == id)
}

pub fn name(id: &str) -> String {
    find(id).map_or_else(|| id.to_string(), |gpu| gpu.name)
}

/// Apply an explicit physical GPU to a child process. None means inherit the process environment.
///
/// rust_game also pins Horizon's own wgpu adapter by PCI id. PRIME remains useful for the
/// window-system/driver side and for wrappers around the game.
pub fn apply_to_command(cmd: &mut Command, gpu_id: Option<&str>, rust_game: bool) {
    let Some(gpu_id) = gpu_id else {
        return;
    };
    let Some(gpu) = find(gpu_id) else {
        return;
    };
    for key in PRIME_ENV {
        cmd.env_remove(key);
    }
    if rust_game {
        cmd.env(HORIZON_GPU, &gpu.id);
        cmd.env(HORIZON_GPU_NAME, &gpu.name);
    }
    for (key, value) in prime_env(&gpu) {
        cmd.env(key, value);
    }
}

/// Apply the launcher's saved GPU before GPUI/wgpu starts.
///
/// This is only called during process startup, before the GUI creates worker threads. None means
/// preserve the environment exactly as Oxidum was started, including an external prime-run.
#[cfg(target_os = "linux")]
pub fn apply_to_current_process(gpu_id: Option<&str>) {
    let Some(gpu_id) = gpu_id else {
        return;
    };
    let gpus = list();
    let Some(gpu) = gpus.iter().find(|gpu| gpu.id == gpu_id) else {
        return;
    };
    let has_proprietary_nvidia = gpus.iter().any(Gpu::proprietary_nvidia);
    for key in PRIME_ENV {
        std::env::remove_var(key);
    }
    for (key, value) in launcher_env(gpu, has_proprietary_nvidia) {
        std::env::set_var(key, value);
    }
}

/// PRIME variables for a child whose renderer can also select its exact wgpu adapter.
fn prime_env(gpu: &Gpu) -> Vec<(&'static str, String)> {
    if gpu.proprietary_nvidia() {
        vec![
            ("__NV_PRIME_RENDER_OFFLOAD", "1".into()),
            ("__VK_LAYER_NV_optimus", "NVIDIA_only".into()),
            ("__GLX_VENDOR_LIBRARY_NAME", "nvidia".into()),
        ]
    } else {
        vec![("DRI_PRIME", gpu.dri_prime())]
    }
}

/// GPUI chooses its adapter internally, so an explicit launcher choice must constrain what Vulkan
/// can see instead of relying on its HighPerformance preference. Mesa's trailing ! exposes only
/// the selected device to Vulkan. NVIDIA's implicit Optimus layer can likewise hide NVIDIA when
/// a non-NVIDIA adapter was chosen on a proprietary-NVIDIA hybrid system.
fn launcher_env(gpu: &Gpu, has_proprietary_nvidia: bool) -> Vec<(&'static str, String)> {
    if gpu.proprietary_nvidia() {
        return prime_env(gpu);
    }
    let mut env = vec![("DRI_PRIME", format!("{}!", gpu.dri_prime()))];
    if has_proprietary_nvidia && gpu.vendor != 0x10de {
        env.push(("__NV_PRIME_RENDER_OFFLOAD", "1".into()));
        env.push(("__VK_LAYER_NV_optimus", "non_NVIDIA_only".into()));
    }
    env
}

#[cfg(target_os = "linux")]
fn linux_gpus() -> Vec<Gpu> {
    use std::collections::BTreeSet;
    use std::fs;

    let Ok(entries) = fs::read_dir("/sys/class/drm") else {
        return Vec::new();
    };
    let mut seen = BTreeSet::new();
    let mut out = Vec::new();

    for entry in entries.flatten() {
        let card = entry.file_name().to_string_lossy().into_owned();
        let Some(number) = card.strip_prefix("card") else {
            continue;
        };
        if number.is_empty() || !number.chars().all(|c| c.is_ascii_digit()) {
            continue;
        }
        let Ok(device_path) = fs::canonicalize(entry.path().join("device")) else {
            continue;
        };
        let Some(slot) = device_path.file_name().and_then(|s| s.to_str()) else {
            continue;
        };
        // Oxidum's Linux AppImage is x86_64; the physical GPUs we select are PCI devices.
        if !slot.contains(':') || !slot.contains('.') || !seen.insert(slot.to_string()) {
            continue;
        }

        let vendor = read_hex(&device_path.join("vendor")).unwrap_or(0);
        let device = read_hex(&device_path.join("device")).unwrap_or(0);
        let driver = fs::canonicalize(device_path.join("driver"))
            .ok()
            .and_then(|p| p.file_name().map(|n| n.to_string_lossy().into_owned()))
            .unwrap_or_default();
        let boot_vga = fs::read_to_string(device_path.join("boot_vga"))
            .ok()
            .is_some_and(|v| v.trim() == "1");
        let name = gpu_name(slot, vendor, device);
        out.push(Gpu {
            id: format!("pci:{slot}"),
            name,
            pci_slot: slot.to_string(),
            vendor,
            device,
            driver,
            boot_vga,
        });
    }

    out.sort_by_key(|gpu| (!gpu.boot_vga, gpu.pci_slot.clone()));
    out
}

#[cfg(target_os = "linux")]
fn read_hex(path: &std::path::Path) -> Option<u16> {
    let text = std::fs::read_to_string(path).ok()?;
    u16::from_str_radix(text.trim().trim_start_matches("0x"), 16).ok()
}

#[cfg(target_os = "linux")]
fn gpu_name(slot: &str, vendor: u16, device: u16) -> String {
    let model = udev_property(slot, "ID_MODEL_FROM_DATABASE")
        .map(|m| bracket_name(&m).to_string())
        .filter(|m| !m.trim().is_empty());
    let vendor_name = match vendor {
        0x10de => "NVIDIA".to_string(),
        0x8086 => "Intel".to_string(),
        0x1002 => "AMD".to_string(),
        _ => udev_property(slot, "ID_VENDOR_FROM_DATABASE")
            .unwrap_or_else(|| format!("{vendor:04x}")),
    };

    match model {
        Some(model)
            if model
                .to_ascii_lowercase()
                .starts_with(&vendor_name.to_ascii_lowercase()) =>
        {
            model
        }
        Some(model) => format!("{vendor_name} {model}"),
        None => format!("{vendor_name} GPU [{vendor:04x}:{device:04x}]"),
    }
}

#[cfg(target_os = "linux")]
fn bracket_name(model: &str) -> &str {
    match (model.find('['), model.rfind(']')) {
        (Some(left), Some(right)) if left + 1 < right => &model[left + 1..right],
        _ => model,
    }
}

#[cfg(target_os = "linux")]
fn udev_property(slot: &str, key: &str) -> Option<String> {
    let text = std::fs::read_to_string(format!("/run/udev/data/+pci:{slot}")).ok()?;
    let prefix = format!("E:{key}=");
    text.lines()
        .find_map(|line| line.strip_prefix(&prefix))
        .map(str::to_string)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn mesa_selector_uses_the_stable_pci_slot() {
        let gpu = Gpu {
            id: "pci:0000:03:00.0".into(),
            name: "AMD Radeon".into(),
            pci_slot: "0000:03:00.0".into(),
            vendor: 0x1002,
            device: 0,
            driver: "amdgpu".into(),
            boot_vga: false,
        };
        assert_eq!(gpu.dri_prime(), "pci-0000_03_00_0");
    }

    #[test]
    fn prime_environment_follows_the_selected_driver() {
        let mut gpu = Gpu {
            id: "pci:0000:03:00.0".into(),
            name: "AMD Radeon".into(),
            pci_slot: "0000:03:00.0".into(),
            vendor: 0x1002,
            device: 0,
            driver: "amdgpu".into(),
            boot_vga: false,
        };
        assert_eq!(prime_env(&gpu), [("DRI_PRIME", "pci-0000_03_00_0".into())]);

        gpu.vendor = 0x10de;
        gpu.driver = "nvidia".into();
        assert_eq!(
            prime_env(&gpu),
            [
                ("__NV_PRIME_RENDER_OFFLOAD", "1".into()),
                ("__VK_LAYER_NV_optimus", "NVIDIA_only".into()),
                ("__GLX_VENDOR_LIBRARY_NAME", "nvidia".into()),
            ]
        );

        gpu.boot_vga = true;
        assert_eq!(
            prime_env(&gpu),
            [
                ("__NV_PRIME_RENDER_OFFLOAD", "1".into()),
                ("__VK_LAYER_NV_optimus", "NVIDIA_only".into()),
                ("__GLX_VENDOR_LIBRARY_NAME", "nvidia".into()),
            ]
        );
    }

    #[test]
    fn launcher_environment_forces_the_named_mesa_adapter() {
        let gpu = Gpu {
            id: "pci:0000:00:02.0".into(),
            name: "Intel Graphics".into(),
            pci_slot: "0000:00:02.0".into(),
            vendor: 0x8086,
            device: 0,
            driver: "i915".into(),
            boot_vga: true,
        };
        assert_eq!(
            launcher_env(&gpu, true),
            [
                ("DRI_PRIME", "pci-0000_00_02_0!".into()),
                ("__NV_PRIME_RENDER_OFFLOAD", "1".into()),
                ("__VK_LAYER_NV_optimus", "non_NVIDIA_only".into()),
            ]
        );
        assert_eq!(
            launcher_env(&gpu, false),
            [("DRI_PRIME", "pci-0000_00_02_0!".into())]
        );
    }

    #[cfg(target_os = "linux")]
    #[test]
    fn database_names_prefer_the_model_in_brackets() {
        assert_eq!(
            bracket_name("TU116M [GeForce GTX 1660 Ti Mobile]"),
            "GeForce GTX 1660 Ti Mobile"
        );
        assert_eq!(bracket_name("Iris Xe Graphics"), "Iris Xe Graphics");
    }
}
