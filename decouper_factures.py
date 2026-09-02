#!/usr/bin/env python3
"""
Découpe un PDF Oxatis contenant plusieurs factures (une facture = une page)
en fichiers PDF individuels, nommés par numéro de facture.

Usage:
    python3 decouper_factures.py Facture.pdf
    python3 decouper_factures.py Facture.pdf --sortie ./factures
"""

import argparse
import sys
from pathlib import Path

from factures_oxatis import decouper


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf_source", type=Path, help="PDF Oxatis fusionné (une facture par page)")
    parser.add_argument(
        "--sortie", type=Path, default=None,
        help="Dossier de sortie (par défaut: <nom_du_pdf>_factures à côté du fichier source)",
    )
    args = parser.parse_args()

    if not args.pdf_source.exists():
        print(f"Fichier introuvable : {args.pdf_source}", file=sys.stderr)
        sys.exit(1)

    dossier_sortie = args.sortie or args.pdf_source.with_name(args.pdf_source.stem + "_factures")
    total = decouper(args.pdf_source, dossier_sortie)
    print(f"\nTermine : {total} facture(s) ecrite(s) dans {dossier_sortie}")


if __name__ == "__main__":
    main()
