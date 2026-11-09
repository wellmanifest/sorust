"""Export installed native binaries without a build toolchain."""
import argparse

from . import NativeArtifactError, export_artifacts


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m sorust")
    commands = parser.add_subparsers(dest="command", required=True)
    export = commands.add_parser("export", help="export verified binaries to a new directory")
    export.add_argument("destination", help="new directory under an existing parent")
    export.add_argument("--package-dir", help="package containing sorust-artifacts.json; defaults to Sorust")
    args = parser.parse_args(argv)
    try:
        destination = export_artifacts(args.destination, package_dir=args.package_dir)
    except (NativeArtifactError, OSError) as error:
        parser.exit(1, f"sorust: {error}\n")
    print(destination)


if __name__ == "__main__":
    main()
