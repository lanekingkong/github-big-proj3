"""
Utility functions for BioOmicsBridge.

Includes logging, configuration, visualization, and data utilities.
"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path
import json
import yaml


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Configure logging for BioOmicsBridge.

    Args:
        level: Logging level.
        log_file: Optional log file path.

    Returns:
        Configured root logger.
    """
    logger = logging.getLogger("bioomics_bridge")
    logger.setLevel(getattr(logging, level.upper()))

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from YAML or JSON file.

    Args:
        config_path: Path to config file.

    Returns:
        Configuration dictionary.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(path, "r") as f:
        if path.suffix in [".yaml", ".yml"]:
            return yaml.safe_load(f)
        elif path.suffix == ".json":
            return json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")


def save_config(config: Dict[str, Any], config_path: str) -> None:
    """
    Save configuration to YAML file.

    Args:
        config: Configuration dictionary.
        config_path: Output file path.
    """
    path = Path(config_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)


def format_timestamp() -> str:
    """Get current timestamp string for file naming."""
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def get_package_version() -> str:
    """Get package version."""
    try:
        from bioomics_bridge import __version__
        return __version__
    except ImportError:
        return "unknown"


class PipelineProgress:
    """Track progress through multi-step analysis pipelines."""

    def __init__(self, total_steps: int):
        self.total_steps = total_steps
        self.current_step = 0
        self.step_names: list = []
        self.logger = logging.getLogger(__name__)

    def add_step(self, name: str) -> None:
        """Add a step to the pipeline."""
        self.step_names.append(name)
        self.total_steps = len(self.step_names)

    def start_step(self, name: str) -> None:
        """Mark the start of a pipeline step."""
        self.current_step += 1
        self.logger.info(
            f"[{self.current_step}/{self.total_steps}] Starting: {name}"
        )

    def complete(self) -> None:
        """Mark pipeline as complete."""
        self.logger.info(
            f"Pipeline complete: {self.total_steps} steps finished."
        )

    @property
    def progress_pct(self) -> float:
        """Progress as percentage."""
        if self.total_steps == 0:
            return 100.0
        return (self.current_step / self.total_steps) * 100