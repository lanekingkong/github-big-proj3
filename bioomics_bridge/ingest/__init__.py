"""
Multi-Omics Data Ingestion Module

Handles loading, parsing, and validation of heterogeneous omics data formats.
Supports genomics, transcriptomics, proteomics, metabolomics, and spatial omics.
"""

from typing import Dict, List, Optional, Union, Any
from pathlib import Path
import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Supported data formats
SUPPORTED_FORMATS = {
    "genomics": [".vcf", ".vcf.gz", ".bed", ".plink", ".bim", ".fam", ".tsv", ".csv"],
    "transcriptomics": [".h5ad", ".h5", ".mtx", ".tsv", ".csv", ".loom"],
    "proteomics": [".txt", ".csv", ".tsv", ".mzML", ".raw"],
    "metabolomics": [".mzML", ".mzXML", ".cdf", ".tsv", ".csv"],
    "spatial": [".h5ad", ".tif", ".tiff", ".jpg", ".png", ".csv"],
}


class DataIngestor:
    """Universal multi-omics data ingestor with automatic format detection."""

    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize the DataIngestor.

        Args:
            base_dir: Base directory for data files.
        """
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.loaded_data: Dict[str, Any] = {}
        self.metadata: Dict[str, Dict] = {}

    def detect_omics_type(self, file_path: str) -> str:
        """
        Automatically detect omics data type from file content and format.

        Args:
            file_path: Path to the data file.

        Returns:
            Detected omics type (genomics/transcriptomics/proteomics/metabolomics/spatial).
        """
        path = Path(file_path)
        ext = path.suffix.lower()

        # Check by extension
        for omics_type, extensions in SUPPORTED_FORMATS.items():
            if ext in extensions:
                return omics_type

        # Fallback: inspect file content
        return self._inspect_content(path)

    def _inspect_content(self, path: Path) -> str:
        """Inspect file content to determine omics type."""
        try:
            with open(path, "r") as f:
                header = f.readline().strip().lower()

            # Common header patterns
            if any(kw in header for kw in ["chr", "pos", "ref", "alt", "snp"]):
                return "genomics"
            elif any(kw in header for kw in ["gene", "fpkm", "tpm", "count"]):
                return "transcriptomics"
            elif any(kw in header for kw in ["protein", "peptide", "intensity", "lfq"]):
                return "proteomics"
            elif any(kw in header for kw in ["metabolite", "mz", "rt", "mass"]):
                return "metabolomics"
            elif any(kw in header for kw in ["x", "y", "spot", "barcode"]):
                return "spatial"
        except Exception:
            pass

        return "unknown"

    def load(self, file_path: str, omics_type: Optional[str] = None, **kwargs) -> Any:
        """
        Load a single omics data file.

        Args:
            file_path: Path to the data file.
            omics_type: Type of omics data. Auto-detected if None.
            **kwargs: Additional arguments passed to the specific loader.

        Returns:
            Loaded data object (DataFrame, AnnData, etc.).
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")

        omics_type = omics_type or self.detect_omics_type(file_path)

        loaders = {
            "genomics": self._load_genomics,
            "transcriptomics": self._load_transcriptomics,
            "proteomics": self._load_proteomics,
            "metabolomics": self._load_metabolomics,
            "spatial": self._load_spatial_omics,
        }

        if omics_type not in loaders:
            raise ValueError(f"Unsupported omics type: {omics_type}. "
                             f"Supported: {list(loaders.keys())}")

        data = loaders[omics_type](path, **kwargs)
        self.loaded_data[omics_type] = data
        self.metadata[omics_type] = {
            "file": str(path),
            "size_bytes": path.stat().st_size,
            "type": omics_type,
        }

        logger.info(f"Loaded {omics_type} data from {path}")
        return data

    def _load_genomics(self, path: Path, **kwargs) -> pd.DataFrame:
        """Load genomics data (VCF, PLINK, BED)."""
        ext = path.suffix.lower()
        if ext in [".vcf", ".vcf.gz"]:
            return self._load_vcf(path, **kwargs)
        elif ext == ".bed":
            return self._load_bed(path, **kwargs)
        else:
            return pd.read_csv(str(path), sep=None, engine="python", **kwargs)

    def _load_vcf(self, path: Path, **kwargs) -> pd.DataFrame:
        """Parse VCF file into DataFrame."""
        records = []
        with open(path) as f:  # type: ignore
            for line in f:
                if line.startswith("##"):
                    continue
                if line.startswith("#"):
                    header = line.strip("#").strip().split("\t")
                    continue
                parts = line.strip().split("\t")
                if len(parts) >= 8:
                    records.append({
                        "chr": parts[0],
                        "pos": int(parts[1]),
                        "id": parts[2],
                        "ref": parts[3],
                        "alt": parts[4],
                        "qual": parts[5],
                        "filter": parts[6],
                        "info": parts[7],
                    })
        return pd.DataFrame(records)

    def _load_bed(self, path: Path, **kwargs) -> pd.DataFrame:
        """Load BED format file."""
        cols = ["chr", "start", "end"]
        df = pd.read_csv(str(path), sep="\t", header=None, **kwargs)
        df.columns = cols + [f"extra_{i}" for i in range(df.shape[1] - 3)]
        return df

    def _load_transcriptomics(self, path: Path, **kwargs) -> Any:
        """Load transcriptomics data (scRNA-seq, bulk RNA-seq)."""
        ext = path.suffix.lower()
        if ext == ".h5ad":
            try:
                import anndata as ad
                return ad.read_h5ad(str(path))
            except ImportError:
                raise ImportError("Install anndata for h5ad support: pip install anndata")
        elif ext == ".loom":
            try:
                import anndata as ad
                return ad.read_loom(str(path))
            except ImportError:
                raise ImportError("Install anndata for loom support: pip install anndata")
        else:
            return pd.read_csv(str(path), sep=None, engine="python", **kwargs)

    def _load_proteomics(self, path: Path, **kwargs) -> pd.DataFrame:
        """Load proteomics data (MaxQuant, DIA-NN)."""
        df = pd.read_csv(str(path), sep=None, engine="python", **kwargs)
        # Detect protein groups column
        protein_cols = [c for c in df.columns if
                        any(kw in c.lower() for kw in
                            ["protein", "uniprot", "gene", "accession"])]
        if protein_cols:
            df.set_index(protein_cols[0], inplace=True)
        return df

    def _load_metabolomics(self, path: Path, **kwargs) -> pd.DataFrame:
        """Load metabolomics data."""
        return pd.read_csv(str(path), sep=None, engine="python", **kwargs)

    def _load_spatial_omics(self, path: Path, **kwargs) -> Any:
        """Load spatial omics data."""
        ext = path.suffix.lower()
        if ext == ".h5ad":
            try:
                import anndata as ad
                return ad.read_h5ad(str(path))
            except ImportError:
                raise ImportError("Install anndata: pip install anndata")
        else:
            return pd.read_csv(str(path), sep=None, engine="python", **kwargs)

    def validate(self, data: Any, omics_type: str) -> Dict[str, bool]:
        """
        Validate loaded data quality and completeness.

        Args:
            data: Loaded data object.
            omics_type: Type of omics data.

        Returns:
            Dictionary of validation checks and their results.
        """
        checks = {}

        # Check for empty data
        if isinstance(data, pd.DataFrame):
            checks["non_empty"] = data.shape[0] > 0
            checks["has_features"] = data.shape[1] > 1
            checks["missing_rate"] = data.isnull().mean().mean() < 0.5
        else:
            checks["non_empty"] = data is not None
            checks["is_anndata"] = hasattr(data, "shape")

        checks["all_passed"] = all(checks.values())
        return checks

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all loaded data."""
        return {
            "omics_types": list(self.loaded_data.keys()),
            "metadata": self.metadata,
        }

    @property
    def n_omics_types(self) -> int:
        """Number of loaded omics types."""
        return len(self.loaded_data)

    def add_omics_data(self, omics_type: str, data: Any, metadata: Optional[Dict] = None):
        """Add omics data to the dataset."""
        self.loaded_data[omics_type] = data
        if metadata:
            self.metadata[omics_type] = metadata

    def update_metadata(self, metadata: Dict[str, Dict]):
        """Update metadata for the dataset."""
        self.metadata.update(metadata)


class MultiOmicsDataset:
    """Legacy dataset class for backward compatibility."""
    
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.metadata: Dict[str, Dict] = {}
        self.provenance: Dict[str, Any] = {
            "created_at": "2024-05-25",
            "steps": [],
        }
    
    def add_omics_data(self, omics_type: str, data: Dict[str, Any]):
        """Add omics data to the dataset."""
        self.data[omics_type] = data
    
    def update_metadata(self, metadata: Dict[str, Dict]):
        """Update metadata for the dataset."""
        self.metadata.update(metadata)
    
    def get_summary(self) -> str:
        """Get human-readable summary."""
        return f"MultiOmicsDataset with {len(self.data)} omics types"
    
    @property
    def n_omics_types(self) -> int:
        """Number of loaded omics types."""
        return len(self.data)


def load_multiomics(
    genomics: Optional[str] = None,
    transcriptomics: Optional[str] = None,
    proteomics: Optional[str] = None,
    metabolomics: Optional[str] = None,
    spatial: Optional[str] = None,
    base_dir: Optional[str] = None,
) -> DataIngestor:
    """
    Convenience function to load multi-omics data from multiple sources.

    Args:
        genomics: Path to genomics data file.
        transcriptomics: Path to transcriptomics data file.
        proteomics: Path to proteomics data file.
        metabolomics: Path to metabolomics data file.
        spatial: Path to spatial omics data file.
        base_dir: Base directory for data files.

    Returns:
        DataIngestor instance with loaded data.

    Example:
        >>> dataset = load_multiomics(
        ...     genomics="data/variants.vcf",
        ...     transcriptomics="data/scrna.h5ad",
        ...     proteomics="data/proteins.txt"
        ... )
    """
    ingestor = DataIngestor(base_dir=base_dir)

    omics_map = {
        "genomics": genomics,
        "transcriptomics": transcriptomics,
        "proteomics": proteomics,
        "metabolomics": metabolomics,
        "spatial": spatial,
    }

    for omics_type, file_path in omics_map.items():
        if file_path:
            ingestor.load(file_path, omics_type)

    return ingestor