# BioOmicsBridge API Reference

## Main API

### `bioomics_bridge.load_multiomics()`

Load multi-omics data from various file formats.

```python
from bioomics_bridge import load_multiomics

dataset = load_multiomics(
    genomics="path/to/data.vcf",
    transcriptomics="path/to/data.h5ad",
    proteomics="path/to/proteomics/",
    metabolomics="path/to/metabolomics.mzML",
    spatial="path/to/visium/",
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `genomics` | `str` | Path to genomics data file (.vcf, .bed, etc.) |
| `transcriptomics` | `str` | Path to transcriptomics data file (.h5ad, .mtx, etc.) |
| `proteomics` | `str` | Path to proteomics data file or directory |
| `metabolomics` | `str` | Path to metabolomics data file (.mzML, etc.) |
| `spatial` | `str` | Path to spatial omics data directory |

**Returns:** `MultiOmicsDataset`

---

### `bioomics_bridge.harmonize()`

Harmonize multi-omics data: normalize, batch-correct, impute.

```python
from bioomics_bridge import harmonize

harmonized_data = harmonize(
    dataset,
    method="auto",
    batch_correction=True,
    impute_missing=True,
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dataset` | `MultiOmicsDataset` | required | Dataset to harmonize |
| `method` | `str` | `"auto"` | Normalization method |
| `batch_correction` | `bool` | `True` | Apply batch effect correction |
| `impute_missing` | `bool` | `True` | Impute missing values |

**Returns:** `Dict[str, Any]` with harmonized data and QC report

---

### `bioomics_bridge.integrate()`

Integrate multi-omics data into unified representation.

```python
from bioomics_bridge import integrate

result = integrate(
    harmonized_data,
    method="graph",
    n_components=50,
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `harmonized_data` | `Dict` | required | Output from `harmonize()` |
| `method` | `str` | `"graph"` | Integration method (`"graph"`, `"embedding"`, `"spatial"`) |
| `n_components` | `int` | `50` | Number of embedding components |

**Returns:** `Dict[str, Any]` with integrated results

---

### `bioomics_bridge.discover_targets()`

Discover and rank drug targets from integrated multi-omics data.

```python
from bioomics_bridge import discover_targets

targets = discover_targets(
    integrated_result,
    disease="alzheimer",
    min_confidence=0.8,
    top_n=10,
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `integrated_result` | `Dict` | required | Output from `integrate()` |
| `disease` | `str` | required | Disease context |
| `min_confidence` | `float` | `0.8` | Minimum confidence threshold |
| `top_n` | `int` | `10` | Number of top targets to return |

**Returns:** `Dict[str, Any]` with ranked targets

---

### `bioomics_bridge.agent_query()`

Natural language query interface.

```python
from bioomics_bridge import agent_query

result = agent_query(
    "Find drug targets for Alzheimer's disease using multi-omics data"
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Natural language query |
| `context` | `Dict` | `None` | Optional data context |

**Returns:** `Dict[str, Any]`

---

## CLI Reference

```bash
# Version
bioomics-bridge --version

# Ingest data
bioomics-bridge ingest \
    --genomics data/genomics.vcf \
    --transcriptomics data/scrna.h5ad \
    --proteomics data/proteomics/

# Harmonize
bioomics-bridge harmonize \
    --genomics data/genomics.vcf \
    --transcriptomics data/scrna.h5ad \
    --method auto

# Integrate
bioomics-bridge integrate \
    --genomics data/genomics.vcf \
    --transcriptomics data/scrna.h5ad \
    --proteomics data/proteomics/ \
    --method graph

# Discover targets
bioomics-bridge discover \
    --disease alzheimer \
    --genomics data/genomics.vcf \
    --transcriptomics data/scrna.h5ad \
    --proteomics data/proteomics/ \
    --min-confidence 0.8

# Natural language query
bioomics-bridge query "Find drug targets for Alzheimer's"

# Launch dashboard
bioomics-bridge dashboard
```

## MultiOmicsDataset Class

```python
class MultiOmicsDataset:
    attributes:
        data: Dict[str, Any]     # Raw data
        metadata: Dict[str, Dict] # Per-omics metadata
        provenance: Dict         # W3C PROV provenance
        n_omics_types: int       # Number of omics types loaded

    methods:
        update_metadata(): Update dataset metadata
        get_summary(): Get human-readable summary
        save(path): Save dataset to disk
        load(path): Load dataset from disk
```

## Agent System

```python
from bioomics_bridge.agents import AgentOrchestrator

orchestrator = AgentOrchestrator(backend="local")

# List all agents
agents = orchestrator.list_agents()

# Filter by capability
qc_agents = orchestrator.list_agents(capability="qc")

# Parse a query
plan = orchestrator.parse_query(
    "Analyze scRNA-seq data and find drug targets"
)

# Execute a query
result = orchestrator.execute(
    "Find targets in Alzheimer's multi-omics data"
)
```

## Provenance Tracking

```python
from bioomics_bridge.utils import PipelineProgress

progress = PipelineProgress(total_steps=8)
progress.add_step("Data ingestion")
progress.add_step("Quality control")
progress.add_step("Normalization")

progress.start_step("Data ingestion")
# ... do work ...
progress.start_step("Quality control")
# ... do work ...

progress.complete()
print(f"Progress: {progress.progress_pct:.1f}%")
```