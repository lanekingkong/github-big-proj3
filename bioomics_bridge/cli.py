"""
BioOmicsBridge Command Line Interface
"""

import argparse
import sys
from pathlib import Path

from bioomics_bridge import (
    __version__,
    load_multiomics,
    harmonize,
    integrate,
    discover_targets,
    agent_query,
)


def cmd_version(args):
    """Print version info."""
    print(f"BioOmicsBridge v{__version__}")


def cmd_ingest(args):
    """Ingest multi-omics data."""
    print(f"Ingesting data from: {args.data_dir}")
    dataset = load_multiomics(
        genomics=args.genomics,
        transcriptomics=args.transcriptomics,
        proteomics=args.proteomics,
        metabolomics=args.metabolomics,
        spatial=args.spatial,
    )
    print(dataset.get_summary())


def cmd_harmonize(args):
    """Harmonize data."""
    print("Harmonizing data...")
    dataset = load_multiomics(
        genomics=args.genomics,
        transcriptomics=args.transcriptomics,
        proteomics=args.proteomics,
    )
    result = harmonize(dataset, method=args.method)
    print(f"Harmonized {len(result)} omics types.")


def cmd_integrate(args):
    """Integrate multi-omics data."""
    print("Integrating multi-omics data...")
    dataset = load_multiomics(
        genomics=args.genomics,
        transcriptomics=args.transcriptomics,
        proteomics=args.proteomics,
    )
    harm_data = harmonize(dataset)
    result = integrate(harm_data, method=args.method)
    print(f"Integration complete: {result['n_omics_types']} omics types.")


def cmd_discover(args):
    """Discover drug targets."""
    print(f"Discovering targets for: {args.disease}")
    dataset = load_multiomics(
        genomics=args.genomics,
        transcriptomics=args.transcriptomics,
        proteomics=args.proteomics,
    )
    harm_data = harmonize(dataset)
    int_result = integrate(harm_data)
    result = discover_targets(
        int_result,
        disease=args.disease,
        min_confidence=args.min_confidence,
    )
    if not result["targets"].empty:
        print(f"Found {len(result['targets'])} targets.")
        print(result["targets"][["rank", "target_name", "confidence"]].to_string())
    else:
        print("No targets found above threshold.")


def cmd_query(args):
    """Natural language query."""
    print(f"Query: {args.query}")
    result = agent_query(args.query)
    print(f"Used agents: {result['agents_used']}")
    print(result["output"]["summary"])


def cmd_dashboard(args):
    """Launch dashboard."""
    print("Launching BioOmicsBridge Dashboard...")
    print("Dashboard is a web application.")
    print("Run: cd dashboard && npm run dev")
    print("Then open http://localhost:3000 in your browser.")


def main():
    parser = argparse.ArgumentParser(
        description="BioOmicsBridge - AI-Powered Multi-Omics Data Integration Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="Show version"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest multi-omics data")
    ingest_parser.add_argument("--genomics", help="Genomics data file")
    ingest_parser.add_argument("--transcriptomics", help="Transcriptomics data file")
    ingest_parser.add_argument("--proteomics", help="Proteomics data file")
    ingest_parser.add_argument("--metabolomics", help="Metabolomics data file")
    ingest_parser.add_argument("--spatial", help="Spatial omics data file")
    ingest_parser.add_argument("--data-dir", default=".", help="Base data directory")

    # harmonize command
    harm_parser = subparsers.add_parser("harmonize", help="Harmonize data")
    harm_parser.add_argument("--genomics", help="Genomics data file")
    harm_parser.add_argument("--transcriptomics", help="Transcriptomics data file")
    harm_parser.add_argument("--proteomics", help="Proteomics data file")
    harm_parser.add_argument("--method", default="auto", help="Harmonization method")

    # integrate command
    int_parser = subparsers.add_parser("integrate", help="Integrate data")
    int_parser.add_argument("--genomics", help="Genomics data file")
    int_parser.add_argument("--transcriptomics", help="Transcriptomics data file")
    int_parser.add_argument("--proteomics", help="Proteomics data file")
    int_parser.add_argument("--method", default="graph", help="Integration method")

    # discover command
    disc_parser = subparsers.add_parser("discover", help="Discover drug targets")
    disc_parser.add_argument("--disease", default="cancer", help="Disease context")
    disc_parser.add_argument("--genomics", help="Genomics data file")
    disc_parser.add_argument("--transcriptomics", help="Transcriptomics data file")
    disc_parser.add_argument("--proteomics", help="Proteomics data file")
    disc_parser.add_argument(
        "--min-confidence", type=float, default=0.8, help="Minimum confidence"
    )

    # query command
    query_parser = subparsers.add_parser("query", help="Natural language query")
    query_parser.add_argument("query", help="Query text")

    # dashboard command
    subparsers.add_parser("dashboard", help="Launch web dashboard")

    args = parser.parse_args()

    if args.version:
        cmd_version(args)
        return

    command_map = {
        "ingest": cmd_ingest,
        "harmonize": cmd_harmonize,
        "integrate": cmd_integrate,
        "discover": cmd_discover,
        "query": cmd_query,
        "dashboard": cmd_dashboard,
    }

    if args.command in command_map:
        command_map[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()