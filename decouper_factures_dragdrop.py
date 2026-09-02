#!/usr/bin/env python3
"""
Version "glisser-deposer" pour Windows.

Il suffit de glisser le PDF de factures Oxatis sur l'icone de l'exe
(ou du script). Un dossier "Facture Oxatis" est cree a cote du fichier
depose, avec un PDF par facture a l'interieur.

Compile en .exe via PyInstaller (voir .github/workflows/build-exe.yml).
"""

import sys
import traceback
from pathlib import Path

from factures_oxatis import decouper

NOM_DOSSIER_SORTIE = "Facture Oxatis"


def pause() -> None:
    try:
        input("\nAppuyez sur Entree pour fermer cette fenetre...")
    except EOFError:
        pass


def traiter_fichier(chemin: Path) -> None:
    if not chemin.exists():
        print(f"Fichier introuvable : {chemin}")
        return
    if chemin.suffix.lower() != ".pdf":
        print(f"Ignore (pas un PDF) : {chemin.name}")
        return

    dossier_sortie = chemin.parent / NOM_DOSSIER_SORTIE
    print(f"Traitement de {chemin.name}...")
    total = decouper(chemin, dossier_sortie)
    print(f"\n{total} facture(s) creee(s) dans le dossier :\n{dossier_sortie}")


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

    fichiers = sys.argv[1:]

    if not fichiers:
        print("Glissez-deposez un PDF de factures Oxatis sur cet executable")
        print("pour le decouper en une facture par fichier PDF.")
        pause()
        return

    try:
        for arg in fichiers:
            traiter_fichier(Path(arg))
    except Exception:
        print("\nUne erreur est survenue :\n")
        traceback.print_exc()

    pause()


if __name__ == "__main__":
    main()
