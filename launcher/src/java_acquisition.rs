//! Java Edition acquisition providers.
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

    fn acquire(&self, request: &Request<'_>, log: &dyn Fn(String)) -> Result<Outcome, String>;
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
