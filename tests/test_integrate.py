"""
Tests for BioOmicsBridge Integrate Module
"""
import pytest
import numpy as np
import pandas as pd
from bioomics_bridge.integrate import MultiOmicsIntegrator, integrate, build_knowledge_graph, learn_embeddings


class TestMultiOmicsIntegrator:
    """Test MultiOmicsIntegrator functionality."""

    @pytest.fixture
    def integrator(self):
        return MultiOmicsIntegrator()

    @pytest.fixture
    def mock_data(self):
        return {
            "genomics": pd.DataFrame(np.random.randn(100, 10)),
            "transcriptomics": pd.DataFrame(np.random.randn(100, 10)),
        }

    def test_init(self, integrator):
        assert integrator is not None
        assert integrator.integration_method == "graph"
        assert integrator.n_components == 50

    def test_build_knowledge_graph(self, integrator, mock_data):
        result = integrator.build_knowledge_graph(mock_data)
        assert result is not None
        assert "nodes" in result
        assert "edges" in result
        assert "omics_types" in result

    def test_learn_embeddings(self, integrator, mock_data):
        result = integrator.learn_embeddings(mock_data)
        assert isinstance(result, np.ndarray)
        assert result.shape[1] <= integrator.n_components

    def test_compute_feature_importance(self, integrator, mock_data):
        integrator.learn_embeddings(mock_data)
        result = integrator.compute_feature_importance()
        assert isinstance(result, pd.DataFrame)
        assert "feature" in result.columns
        assert "importance" in result.columns

    def test_integrate(self, integrator, mock_data):
        result = integrator.integrate(mock_data)
        assert isinstance(result, dict)
        assert "graph" in result
        assert "embeddings" in result
        assert "feature_importance" in result


class TestConvenienceFunctions:
    """Test convenience functions."""

    @pytest.fixture
    def mock_data(self):
        return {
            "genomics": pd.DataFrame(np.random.randn(50, 5)),
            "transcriptomics": pd.DataFrame(np.random.randn(50, 5)),
        }

    def test_build_knowledge_graph(self, mock_data):
        result = build_knowledge_graph(mock_data)
        assert result is not None
        assert "nodes" in result

    def test_learn_embeddings(self, mock_data):
        result = learn_embeddings(mock_data)
        assert isinstance(result, dict)
        assert "embeddings" in result

    def test_integrate(self, mock_data):
        result = integrate(mock_data)
        assert isinstance(result, dict)
        assert "graph" in result
        assert "embeddings" in result
        assert "feature_importance" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])