"""
Superfluid Project Intelligence Skill
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from main import scan_project


def run(project_name):
    """
    Analyze a blockchain project using
    the Project Intelligence Engine.
    """

    return scan_project(project_name)