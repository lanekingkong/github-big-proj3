# BioOmicsBridge Architecture

## Overview

BioOmicsBridge follows a modular, pipeline-oriented architecture designed for extensibility and reproducibility.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │ Web UI   │  │ CLI      │  │ Python API           │  │
│  │ (Next.js)│  │ (argparse│  │ (bioomics_bridge.*)  │  │
│  └────┬─────┘  └────┬─────┘  └───────────┬──────────┘  │
│       │              │                    │              │
├───────┴──────────────┴────────────────────┴──────────────┤
│                   Agent Orchestration Layer               │
│  ┌───────────────────────────────────────────────────┐  │
│  │          LangGraph Agent Orchestrator              │  │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │  │
│  │  │Agent1│ │Agent2│ │Agent3│ │Agent4│ │AgentN│   │  │
│  │  └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘   │  │
│  └─────┼────────┼────────┼────────┼────────┼─────────┘  │
├────────┼────────┼────────┼────────┼────────┼────────────┤
│                    Core Processing Layer                  │
│  ┌─────┴────────┴────────┴────────┴────────┴─────────┐ │
│  │  ┌────────┐  ┌──────────┐  ┌───────────────────┐  │ │
│  │  │Ingest  │→ │Harmonize │→ │     Integrate     │  │ │
│  │  └────────┘  └──────────┘  └─────────┬─────────┘  │ │
│  │                                      │             │ │
│  │                          ┌───────────┴───────────┐ │ │
│  │                          │     Discover          │ │ │
│  │                          └───────────────────────┘ │ │
│  └────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│                    Data Management Layer                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │ Cache    │  │ Metadata │  │ Provenance           │  │
│  └──────────┘  └──────────┘  └──────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│                 External Dependencies                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │ scverse  │  │ PyTorch  │  │ BioNeMo (optional)   │  │
│  └──────────┘  └──────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Pipeline Stages

### 1. Data Ingestion (`ingest.py`)
- **Input**: Raw omics data files (VCF, h5ad, MaxQuant, mzML, Visium)
- **Process**: Format detection, validation, metadata extraction
- **Output**: Standardized `MultiOmicsDataset` object

### 2. Data Harmonization (`harmonize.py`)
- **Input**: `MultiOmicsDataset` from ingestion
- **Process**: Normalization, batch correction, missing value imputation, QC
- **Output**: Harmonized `MultiOmicsDataset` with QC report

### 3. Multi-Omics Integration (`integrate.py`)
- **Input**: Harmonized data
- **Process**: Knowledge graph construction, embedding learning, graph attention
- **Output**: Unified embedding space and multi-omics graph

### 4. Target Discovery (`discover.py`)
- **Input**: Integrated data
- **Process**: Scoring, ranking, druggability assessment, explainable evidence chains
- **Output**: Ranked target list with full evidence

## Agent System

### Agent Categories

| Category | Agents | Description |
|----------|--------|-------------|
| Preprocessing | genomics_qc, scrna_preprocess, bulk_rna_preprocess, proteomics_preprocess, metabolomics_preprocess, spatial_preprocess | Data QC and preprocessing per omics type |
| Integration | integration_graph, integration_embedding, spatial_integration | Cross-omics integration |
| Analysis | cell_type_annotation, trajectory_analysis, pathway_analysis | Downstream biological analysis |
| Discovery | target_scoring, target_explanation, literature_search, clinical_evidence | Drug target discovery |
| Output | visualization, report_generation | Publication-ready outputs |
| Orchestration | pipeline_orchestrator, reproducibility | Workflow management |

## Data Flow

```
Raw Data → [Ingestion] → Standardized Dataset → [Harmonization] → Clean Dataset
                                                                    ↓
Targets ← [Discovery] ← Integrated Embeddings ← [Integration] ←────┘
   ↓
Explainable AI Evidence Chain → Report Generation
```

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14, React 18, Tailwind CSS, Plotly.js |
| Backend | Python 3.10+, scverse, scikit-learn |
| Agent Framework | LangGraph |
| Deep Learning | PyTorch (optional) |
| Data Format | AnnData (standard) |
| Containerization | Docker |

## Extensibility

### Adding New Omics Types
1. Implement format detection in `ingest.py`
2. Add normalization method in `harmonize.py`
3. Register agent in `agents/__init__.py`

### Adding New Analysis Methods
1. Extend relevant module with new method
2. Add corresponding agent
3. Update documentation