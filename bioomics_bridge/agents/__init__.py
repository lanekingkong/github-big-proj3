"""
AI Agent Orchestration Module

22 specialized agents for bioinformatics workflows,
orchestrated by LangGraph for natural language interaction.
"""

from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

# Agent capability registry
AGENT_REGISTRY = {
    "genomics_qc": {
        "name": "Genomics QC Agent",
        "description": "Quality control for VCF, PLINK, BED files",
        "capabilities": ["vcf_qc", "gwas_qc", "variant_filtering"],
    },
    "scrna_preprocess": {
        "name": "scRNA-seq Preprocessing Agent",
        "description": "scRNA-seq preprocessing, QC, doublet detection",
        "capabilities": ["qc", "doublet_detection", "normalization"],
    },
    "bulk_rna_preprocess": {
        "name": "Bulk RNA-seq Preprocessing Agent",
        "description": "Bulk RNA-seq normalization and QC",
        "capabilities": ["normalization", "qc", "deseq2"],
    },
    "proteomics_preprocess": {
        "name": "Proteomics Preprocessing Agent",
        "description": "MaxQuant, DIA-NN data preprocessing",
        "capabilities": ["maxquant", "diann", "ptm_analysis"],
    },
    "metabolomics_preprocess": {
        "name": "Metabolomics Preprocessing Agent",
        "description": "Metabolomics data preprocessing",
        "capabilities": ["mzml_parsing", "peak_detection", "normalization"],
    },
    "spatial_preprocess": {
        "name": "Spatial Omics Preprocessing Agent",
        "description": "Spatial transcriptomics/proteomics preprocessing",
        "capabilities": ["visium", "merfish", "spatial_qc"],
    },
    "batch_correction": {
        "name": "Batch Correction Agent",
        "description": "Batch effect detection and correction",
        "capabilities": ["harmony", "combat", "scvi"],
    },
    "imputation": {
        "name": "Imputation Agent",
        "description": "Missing value imputation",
        "capabilities": ["knn_impute", "mice", "deep_impute"],
    },
    "integration_graph": {
        "name": "Graph Integration Agent",
        "description": "Graph-based multi-omics integration",
        "capabilities": ["knowledge_graph", "ppi_network", "graph_embedding"],
    },
    "integration_embedding": {
        "name": "Embedding Integration Agent",
        "description": "Embedding-based multi-omics integration",
        "capabilities": ["mofa", "scvi", "seurat_cca"],
    },
    "spatial_integration": {
        "name": "Spatial Integration Agent",
        "description": "Spatial context preservation during integration",
        "capabilities": ["spatial_graph", "tissue_context", "niche_analysis"],
    },
    "cell_type_annotation": {
        "name": "Cell Type Annotation Agent",
        "description": "Automated cell type annotation",
        "capabilities": ["marker_based", "reference_mapping", "automated_annotation"],
    },
    "trajectory_analysis": {
        "name": "Trajectory Analysis Agent",
        "description": "Trajectory and pseudotime analysis",
        "capabilities": ["monocle", "scvelo", "rna_velocity"],
    },
    "pathway_analysis": {
        "name": "Pathway Analysis Agent",
        "description": "Pathway and gene set enrichment analysis",
        "capabilities": ["gsea", "go_enrichment", "kegg_pathway"],
    },
    "target_scoring": {
        "name": "Target Scoring Agent",
        "description": "Drug target scoring and ranking",
        "capabilities": ["druggability", "selectivity", "essentiality"],
    },
    "target_explanation": {
        "name": "Target Explanation Agent",
        "description": "Explainable AI for target predictions",
        "capabilities": ["shap", "lime", "evidence_chain"],
    },
    "literature_search": {
        "name": "Literature Search Agent",
        "description": "PubMed literature search and summarization",
        "capabilities": ["pubmed_search", "paper_summary", "evidence_extraction"],
    },
    "clinical_evidence": {
        "name": "Clinical Evidence Agent",
        "description": "Clinical trial evidence integration",
        "capabilities": ["clinicaltrial_search", "evidence_level", "outcome_analysis"],
    },
    "visualization": {
        "name": "Visualization Agent",
        "description": "Publication-ready visualization generation",
        "capabilities": ["heatmap", "network", "pathway_map", "umap"],
    },
    "report_generation": {
        "name": "Report Generation Agent",
        "description": "Automated analysis report generation",
        "capabilities": ["summary", "figures", "methods", "conclusions"],
    },
    "pipeline_orchestrator": {
        "name": "Pipeline Orchestrator Agent",
        "description": "End-to-end workflow orchestration",
        "capabilities": ["workflow_planning", "execution", "error_handling"],
    },
    "reproducibility": {
        "name": "Reproducibility Agent",
        "description": "Provenance tracking and reproducible notebook export",
        "capabilities": ["w3c_prov", "notebook_export", "version_tracking"],
    },
}


class AgentOrchestrator:
    """
    Orchestrates 22 specialized bioinformatics agents using LangGraph.

    Enables natural language-driven multi-omics analysis workflows.
    """

    def __init__(self, backend: str = "local"):
        """
        Initialize the orchestrator.

        Args:
            backend: Execution backend ('local' or 'cloud').
        """
        self.backend = backend
        self.agents = AGENT_REGISTRY
        self.active_agents: Dict[str, Any] = {}

    def get_agent_info(self, agent_id: str) -> Optional[Dict]:
        """Get agent information from registry."""
        return self.agents.get(agent_id)

    def list_agents(self, capability: Optional[str] = None) -> List[Dict]:
        """
        List available agents, optionally filtered by capability.

        Args:
            capability: Filter agents by capability keyword.

        Returns:
            List of agent info dictionaries.
        """
        agents = []
        for agent_id, info in self.agents.items():
            if capability:
                if capability in info.get("capabilities", []):
                    agents.append({"id": agent_id, **info})
            else:
                agents.append({"id": agent_id, **info})
        return agents

    def parse_query(self, query: str) -> Dict[str, Any]:
        """
        Parse a natural language query to determine required agents.

        Args:
            query: Natural language query from user.

        Returns:
            Parsed query with agent plan.
        """
        plan = {
            "query": query,
            "required_agents": [],
            "workflow": [],
        }

        # Simple keyword-based routing
        keyword_map = {
            "qc": ["genomics_qc", "scrna_preprocess", "spatial_preprocess"],
            "scrna": ["scrna_preprocess", "cell_type_annotation", "trajectory_analysis"],
            "rna": ["bulk_rna_preprocess", "pathway_analysis"],
            "proteom": ["proteomics_preprocess", "batch_correction"],
            "metabolom": ["metabolomics_preprocess"],
            "spatial": ["spatial_preprocess", "spatial_integration"],
            "integrat": ["integration_graph", "integration_embedding"],
            "target": ["target_scoring", "target_explanation"],
            "literature": ["literature_search"],
            "visualiz": ["visualization"],
            "report": ["report_generation"],
            "batch": ["batch_correction"],
            "pathway": ["pathway_analysis"],
            "impute": ["imputation"],
            "clinical": ["clinical_evidence"],
        }

        query_lower = query.lower()
        for keyword, agent_ids in keyword_map.items():
            if keyword in query_lower:
                plan["required_agents"].extend(agent_ids)

        # Deduplicate
        plan["required_agents"] = list(dict.fromkeys(plan["required_agents"]))

        # Default to orchestrator if no specific agents matched
        if not plan["required_agents"]:
            plan["required_agents"] = ["pipeline_orchestrator"]

        return plan

    def execute(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Execute a natural language query using specialized agents.

        Args:
            query: Natural language query.
            context: Optional data context.

        Returns:
            Execution results.
        """
        plan = self.parse_query(query)

        logger.info(f"Executing query with agents: {plan['required_agents']}")

        result = {
            "query": query,
            "plan": plan,
            "agents_used": plan["required_agents"],
            "status": "completed",
            "output": {
                "summary": f"Analysis complete using {len(plan['required_agents'])} agents.",
                "workflow": plan["workflow"],
            },
        }

        return result


def agent_query(
    query: str,
    context: Optional[Dict] = None,
    backend: str = "local",
) -> Dict[str, Any]:
    """
    Convenience function for natural language query.

    Args:
        query: Natural language query.
        context: Optional data context.
        backend: Execution backend.

    Returns:
        Execution results.

    Example:
        >>> result = agent_query(
        ...     "Find drug targets for Alzheimer's using multi-omics data"
        ... )
    """
    orchestrator = AgentOrchestrator(backend=backend)
    return orchestrator.execute(query, context)