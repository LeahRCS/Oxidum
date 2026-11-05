# Java Edition acquisition providers

Oxidum keeps Java Edition acquisition behind one explicit extension point:

`launcher/src/java_acquisition.rs`.

The rest of the launcher does not need to know where the vanilla files came from.

## Flow

1. Oxidum first looks for a complete local Java installation it can reuse.
2. If the requested vanilla version is still missing from Oxidum's own data root, it builds a
   `java_acquisition::Request`.
3. Registered acquisition providers are tried in order.
4. A provider may populate Oxidum's destination and return `Outcome::Acquired`.
5. Oxidum validates the minimum launcher layout.
6. If every provider returns `NotHandled`, the existing built-in official download path runs.
7. Java runtime selection, loader installation, instance configuration and launch continue in
   Oxidum regardless of which acquisition provider supplied the vanilla files.

This means adding a new acquisition implementation does **not** require editing
`backend::java_game`, the loader code or the UI.

## Request contract

A provider receives:

- `minecraft`: the requested Minecraft version;
- `manifest_sha1`: the manifest hash already resolved by Oxidum;
- `destination`: Oxidum's own Minecraft data root.

Before returning `Acquired`, the provider must leave at least:

```text
<destination>/
├── assets/
├── libraries/
└── versions/
    └── <version>/
        ├── <version>.json
        └── <version>.jar
```

The provider is responsible for making sure the files it supplies are complete and that its source
is appropriate for the user's use. Oxidum deliberately keeps acquisition separate from account,
runtime, loader and launch logic.

## Adding a provider

Implement the trait in `launcher/src/java_acquisition.rs` or another launcher module:

```rust
struct MyProvider;

impl Provider for MyProvider {
    fn id(&self) -> &'static str {
        "my-provider"
    }

    fn acquire(
        &self,
        request: &Request<'_>,
        log: &dyn Fn(String),
    ) -> Result<Outcome, String> {
        // Populate request.destination here when this provider handles the request.
        // Use request.minecraft and request.manifest_sha1 as the resolved version identity.
        log(format!("Checking {}", request.minecraft));

        Ok(Outcome::NotHandled)
    }
}
```

Then register it in the single provider list:

```rust
fn providers() -> Vec<Box<dyn Provider>> {
    vec![
        Box::new(MyProvider),
    ]
}
```

Returning `NotHandled` preserves the normal Oxidum fallback. Returning `Acquired` hands control
back to Oxidum, which validates the layout and then continues with Java/runtime/loader handling.

## Why this exists

Freesm, Halky and Prism discovery remains optional interoperability. It is not the architecture of
the Java path. The provider API is the point where Oxidum can grow independent acquisition
strategies without making the rest of the launcher depend on another installed launcher.
