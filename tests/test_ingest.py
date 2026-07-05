"""
Tests for BioOmicsBridge Ingest Module
"""
import pytest
import numpy as np
import pandas as pd
from bioomics_bridge.ingest import DataIngestor, MultiOmicsDataset, load_multiomics, SUPPORTED_FORMATS


class TestDataIngestor:
    """Test DataIngestor functionality."""

    @pytest.fixture
    def ingestor(self):
        return DataIngestor(base_dir=None)

    def test_init(self, ingestor):
        assert ingestor.base_dir is not None
        assert isinstance(ingestor.loaded_data, dict)
        assert isinstance(ingestor.metadata, dict)

    def test_detect_omics_type_vcf(self, ingestor):
        result = ingestor.detect_omics_type("test.vcf")
        assert result in SUPPORTED_FORMATS.keys()

    def test_detect_omics_type_h5ad(self, ingestor):
        result = ingestor.detect_omics_type("test.h5ad")
        assert result in SUPPORTED_FORMATS.keys()

    def test_validate_good_data(self, ingestor):
        data = pd.DataFrame({"gene": ["TP53", "BRCA1"], "value": [1.0, 2.0]})
        result = ingestor.validate(data, "genomics")
        assert result["all_passed"]

    def test_validate_empty_data(self, ingestor):
        data = pd.DataFrame(columns=["gene"])
        result = ingestor.validate(data, "genomics")
        assert not result["all_passed"]

    def test_validate_high_missing(self, ingestor):
        data = pd.DataFrame({"gene": ["TP53"], "value": [np.nan]})
        result = ingestor.validate(data, "genomics")
        assert not result["all_passed"]

    def test_add_omics_data(self, ingestor):
        data = pd.DataFrame({"gene": ["TP53"], "value": [1.0]})
        ingestor.add_omics_data("genomics", data)
        assert "genomics" in ingestor.loaded_data
        assert ingestor.n_omics_types == 1

    def test_get_summary(self, ingestor):
        data = pd.DataFrame({"gene": ["TP53"], "value": [1.0]})
        ingestor.add_omics_data("genomics", data)
        summary = ingestor.get_summary()
        assert "genomics" in summary["omics_types"]

    def test_update_metadata(self, ingestor):
        ingestor.update_metadata({"genomics": {"source": "TCGA"}})
        assert ingestor.metadata["genomics"]["source"] == "TCGA"


class TestMultiOmicsDataset:
    """Test MultiOmicsDataset legacy class."""

    def test_init(self):
        ds = MultiOmicsDataset()
        assert ds.n_omics_types == 0
        assert isinstance(ds.provenance, dict)
        assert "steps" in ds.provenance

    def test_add_omics_data(self):
        ds = MultiOmicsDataset()
        ds.add_omics_data("genomics", {"matrix": np.random.randn(10, 5)})
        assert ds.n_omics_types == 1
        assert "genomics" in ds.data

    def test_get_summary(self):
        ds = MultiOmicsDataset()
        ds.add_omics_data("genomics", {"matrix": np.random.randn(10, 5)})
        summary = ds.get_summary()
        assert "MultiOmicsDataset" in summary
        assert "1" in summary


class TestLoadMultiOmics:
    """Test load_multiomics convenience function."""

    def test_load_multiomics(self):
        result = load_multiomics(base_dir=None)
        assert isinstance(result, DataIngestor)
        assert result.n_omics_types == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])