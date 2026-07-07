import sys
import os
import pytest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def plik_config(tmp_path: Path) -> Path:
    """Tymczasowy plik konfiguracyjny do testów zadania 12."""
    p = tmp_path / "config.txt"
    p.write_text("host=localhost\nport=8080\nbad_line\nuser=admin", encoding="utf-8")
    return p
