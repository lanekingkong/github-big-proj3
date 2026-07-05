"""
BioOmicsBridge - AI-Powered Multi-Omics Data Integration Platform

Core package initialization and public API.
"""

__version__ = "1.0.0"
__author__ = "BioOmicsBridge Team"
__license__ = "MIT"

from bioomics_bridge.ingest import load_multiomics, DataIngestor
from bioomics_bridge.harmonize import harmonize, DataHarmonizer
from bioomics_bridge.integrate import integrate, MultiOmicsIntegrator
from bioomics_bridge.discover import discover_targets, TargetDiscoverer
from bioomics_bridge.agents import agent_query, AgentOrchestrator

__all__ = [
    "load_multiomics",
    "DataIngestor",
    "harmonize",
    "DataHarmonizer",
    "integrate",
    "MultiOmicsIntegrator",
    "discover_targets",
    "TargetDiscoverer",
    "agent_query",
    "AgentOrchestrator",
    "__version__",
]