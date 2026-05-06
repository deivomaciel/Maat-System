import sys
import os

# Garante que o root do projeto está no Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app  # noqa: F401 — Vercel usa o objeto `app`
