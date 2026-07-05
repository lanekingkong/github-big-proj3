"""
Tests for BioOmicsBridge Harmonize Module
"""

import pytest
import numpy as np
import pandas as pd
from bioomics_bridge.harmonize import DataHarmonizer
from bioomics_bridge.ingest import DataIngestor


class TestDataHarmonizer:
    """Test DataHarmonizer functionality."""

    @pytest.fixture
    def mock_dataset(self):
        dataset = DataIngestor()
        dataset.add_omics_data("genomics", pd.DataFrame(
            np.random.randn(100, 10),
            columns=[f"gene_{i}" for i in range(10)],
        ))
        dataset.add_omics_data("transcriptomics", pd.DataFrame(
            np.random.randn(200, 10),
            columns=[f"gene_{i}" for i in range(10)],
        ))
        return dataset

    @pytest.fixture
    def harmonizer(self):
        return DataHarmonizer()

    def test_init(self, harmonizer):
        assert harmonizer.method is not None
        assert harmonizer.method in ["auto", "zscore", "minmax", "quantile"]

    def test_normalize_zscore(self, harmonizer, mock_dataset):
        result = harmonizer.normalize_omics(mock_dataset, method="zscore")
        assert result is not None

    @pytest.mark.skip(reason="pandas version compatibility — uses internals API")
    def test_normalize_minmax(self, harmonizer, mock_dataset):
        result = harmonizer.normalize_omics(mock_dataset, method="minmax")
        assert result is not None

    def test_normalize_quantile(self, harmonizer, mock_dataset):
        result = harmonizer.normalize_omics(mock_dataset, method="quantile")
        assert result is not None

    def test_normalize_invalid_method(self, harmonizer, mock_dataset):
        result = harmonizer.normalize_omics(mock_dataset, method="invalid")
        assert result is not None

    def test_get_methods(self, harmonizer):
        methods = harmonizer.get_available_methods()
        assert isinstance(methods, list)
        assert "auto" in methods

    def test_detect_batch_effects(self, harmonizer, mock_dataset):
        result = harmonizer.detect_batch_effects(mock_dataset)
        assert result is not None

    def test_impute_missing(self, harmonizer):
        data = pd.DataFrame({
            "a": [1, 2, np.nan, 4, 5],
            "b": [np.nan, 2, 3, 4, np.nan],
        })
        result = harmonizer._impute_knn(data)
        assert result is not None
        assert not result.isnull().any().any()

    def test_generate_qc_report(self, harmonizer, mock_dataset):
        report = harmonizer.generate_qc_report(mock_dataset)
        assert report is not None
        assert isinstance(report, dict)
        assert "genomics" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v"])