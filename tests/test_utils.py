"""
Tests for BioOmicsBridge Utils Module
"""

import pytest
from bioomics_bridge.utils import (
    setup_logging,
    load_config,
    save_config,
    format_timestamp,
    PipelineProgress,
)


class TestUtils:
    """Test utility functions."""

    def test_setup_logging(self):
        logger = setup_logging(level="INFO")
        assert logger is not None
        assert logger.name == "bioomics_bridge"

    def test_setup_logging_with_file(self, tmp_path):
        log_file = str(tmp_path / "test.log")
        logger = setup_logging(level="DEBUG", log_file=log_file)
        assert logger is not None

    def test_format_timestamp(self):
        ts = format_timestamp()
        assert len(ts) == 15  # YYYYMMDD_HHMMSS
        assert "_" in ts

    def test_load_config_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            load_config("nonexistent.yml")

    def test_save_and_load_config(self, tmp_path):
        config_path = str(tmp_path / "config.yml")
        config = {"test": True, "value": 42}
        save_config(config, config_path)

        loaded = load_config(config_path)
        assert loaded["test"] is True
        assert loaded["value"] == 42


class TestPipelineProgress:
    """Test PipelineProgress."""

    def test_init(self):
        pp = PipelineProgress(total_steps=5)
        assert pp.total_steps == 5
        assert pp.current_step == 0

    def test_add_step(self):
        pp = PipelineProgress(total_steps=0)
        pp.add_step("Step 1")
        pp.add_step("Step 2")
        assert pp.total_steps == 2

    def test_start_step(self):
        pp = PipelineProgress(total_steps=3)
        pp.start_step("Step 1")
        assert pp.current_step == 1

    def test_progress_pct(self):
        pp = PipelineProgress(total_steps=4)
        assert pp.progress_pct == 0.0
        pp.start_step("Step 1")
        assert pp.progress_pct == 25.0

    def test_complete(self):
        pp = PipelineProgress(total_steps=3)
        pp.start_step("1")
        pp.start_step("2")
        pp.start_step("3")
        pp.complete()
        assert pp.current_step == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])