"""Export installed native binaries without a build toolchain."""
import argparse

from . import NativeArtifactError, export_artifacts, export_rust_component


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m sorust")
    commands = parser.add_subparsers(dest="command", required=True)
    export = commands.add_parser("export", help="export verified binaries to a new directory")
    export.add_argument("destination", help="new directory under an existing parent")
    export.add_argument("--package-dir", help="package containing sorust-artifacts.json; defaults to Sorust")
    component = commands.add_parser("export-component", help="export a pinned installed Rust-only component")
    component.add_argument("destination", help="new directory under an existing parent")
    component.add_argument("--distribution", required=True, help="installed component distribution")
    component.add_argument("--version", required=True, help="exact installed component version")
    component.add_argument("--package", required=True, help="artifact package recorded in the manifest")
    component.add_argument("--manifest-sha256", required=True, help="SHA-256 of exact manifest bytes")
    component.add_argument("--rust-library", required=True, help="Rust library identity without prefix or suffix")
    args = parser.parse_args(argv)
    try:
        if args.command == "export-component":
            destination = export_rust_component(args.destination, distribution=args.distribution,
                version=args.version, package=args.package, manifest_sha256=args.manifest_sha256,
                rust_library=args.rust_library)
        else:
            destination = export_artifacts(args.destination, package_dir=args.package_dir)
    except (NativeArtifactError, OSError) as error:
        parser.exit(1, f"sorust: {error}\n")
    print(destination)


if __name__ == "__main__":
    main()
