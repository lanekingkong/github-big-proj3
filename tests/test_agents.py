"""
Tests for BioOmicsBridge Agent Orchestration Module
"""

import pytest
from bioomics_bridge.agents import AgentOrchestrator, AGENT_REGISTRY, agent_query


class TestAgentRegistry:
    """Test agent registry."""

    def test_agent_count(self):
        assert len(AGENT_REGISTRY) == 22

    def test_agent_structure(self):
        for agent_id, info in AGENT_REGISTRY.items():
            assert "name" in info
            assert "description" in info
            assert "capabilities" in info
            assert isinstance(info["capabilities"], list)


class TestAgentOrchestrator:
    """Test AgentOrchestrator."""

    @pytest.fixture
    def orchestrator(self):
        return AgentOrchestrator(backend="local")

    def test_init(self, orchestrator):
        assert orchestrator.backend == "local"
        assert len(orchestrator.agents) == 22

    def test_get_agent_info(self, orchestrator):
        info = orchestrator.get_agent_info("genomics_qc")
        assert info is not None
        assert info["name"] == "Genomics QC Agent"

    def test_get_agent_info_invalid(self, orchestrator):
        info = orchestrator.get_agent_info("nonexistent")
        assert info is None

    def test_list_agents(self, orchestrator):
        agents = orchestrator.list_agents()
        assert len(agents) == 22

    def test_list_agents_filtered(self, orchestrator):
        agents = orchestrator.list_agents(capability="qc")
        assert len(agents) > 0
        for agent in agents:
            assert "qc" in agent["capabilities"]

    def test_parse_query_scrna(self, orchestrator):
        plan = orchestrator.parse_query(
            "Analyze scRNA-seq data and annotate cell types"
        )
        assert len(plan["required_agents"]) > 0
        assert "scrna_preprocess" in plan["required_agents"]

    def test_parse_query_target(self, orchestrator):
        plan = orchestrator.parse_query(
            "Find drug targets for cancer using integrated multi-omics"
        )
        assert len(plan["required_agents"]) > 0
        assert "target_scoring" in plan["required_agents"]

    def test_parse_query_default(self, orchestrator):
        plan = orchestrator.parse_query("Hello")
        assert "pipeline_orchestrator" in plan["required_agents"]

    def test_execute(self, orchestrator):
        result = orchestrator.execute("Analyze scRNA-seq data")
        assert result["status"] == "completed"
        assert "agents_used" in result

    def test_agent_query_convenience(self):
        result = agent_query("Find drug targets")
        assert result["status"] == "completed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])