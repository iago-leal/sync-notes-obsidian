"""Shared pytest fixtures for the synctotes test suite."""

from __future__ import annotations

from pathlib import Path

import pytest
from fpdf import FPDF


@pytest.fixture
def sample_pdf_path(tmp_path: Path) -> Path:
    """Generate a synthetic 3-page PDF with known text per page."""
    pdf = FPDF()
    pages_text = [
        "Page one - Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Page two - Sed do eiusmod tempor incididunt ut labore et dolore magna.",
        "Page three - Ut enim ad minim veniam, quis nostrud exercitation ullamco.",
    ]
    pdf.set_font("Helvetica", size=12)
    for text in pages_text:
        pdf.add_page()
        pdf.cell(w=0, h=10, text=text)

    output = tmp_path / "sample.pdf"
    pdf.output(str(output))
    return output


SAMPLE_CLIPPINGS_PT_BR = """﻿Dom Casmurro (Machado de Assis)
- Seu destaque na posição 1234-1235 | Adicionado: sexta-feira, 1 de junho de 2018 14:30:25

Capitu olhou-me em silêncio.
==========
Dom Casmurro (Machado de Assis)
- Sua nota na posição 1300 | Adicionado: sexta-feira, 1 de junho de 2018 14:35:00

Esta linha é a chave do livro.
==========
Memórias Póstumas (Machado de Assis)
- Seu destaque na página 42 | Adicionado: sábado, 2 de junho de 2018 10:00:00

Ao verme que primeiro roeu as frias carnes do meu cadáver.
==========
Livro Sem Autor
- Seu marcador na posição 99 | Adicionado: domingo, 3 de junho de 2018 09:15:00


==========
"""

SAMPLE_CLIPPINGS_EN = """﻿Pride and Prejudice (Jane Austen)
- Your Highlight on Location 100-105 | Added on Sunday, June 3, 2018 9:15:00 AM

It is a truth universally acknowledged.
==========
"""


@pytest.fixture
def sample_clippings_pt_br() -> str:
    """Synthetic My Clippings.txt content in PT-BR covering diverse cases."""
    return SAMPLE_CLIPPINGS_PT_BR


@pytest.fixture
def sample_clippings_en() -> str:
    """Synthetic My Clippings.txt content in English."""
    return SAMPLE_CLIPPINGS_EN


_FIXTURES_ROOT = Path(__file__).parent / "fixtures"


@pytest.fixture
def quincas_borba_pd_pdf() -> Path:
    """Public-domain PDF of Quincas Borba (Biblioteca Nacional do Brasil)."""
    return _FIXTURES_ROOT / "machado-quincas-borba" / "pd.pdf"


@pytest.fixture
def quincas_borba_amazon_export_pdf() -> Path:
    """Amazon 'Caderno de anotações' export PDF for Quincas Borba (ASIN B09JWVC7X8)."""
    return _FIXTURES_ROOT / "machado-quincas-borba" / "amazon_export.pdf"
