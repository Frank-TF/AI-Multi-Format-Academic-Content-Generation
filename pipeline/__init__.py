"""AI-Assisted Multi-Format Academic Content Generation System."""

from .config import ProjectMeta
from .orchestrator import RunResult, run_pipeline

__all__ = ["ProjectMeta", "RunResult", "run_pipeline"]
__version__ = "1.0.0"
