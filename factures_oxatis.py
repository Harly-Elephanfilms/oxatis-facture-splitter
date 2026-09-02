"""
Logique commune : découpe un PDF Oxatis contenant plusieurs factures
(une facture = une page) en fichiers PDF individuels, nommés par numéro
de facture.
"""

import re
from pathlib import Path

from pypdf import PdfReader, PdfWriter

# Le numéro de facture Oxatis est un identifiant de 15 chiffres
# (AAAAMM + compteur), affiché seul sur la première ligne de chaque page.
NUMERO_FACTURE_RE = re.compile(r"\b\d{15}\b")


def extraire_numero_facture(texte_page: str, numero_page: int) -> str:
    match = NUMERO_FACTURE_RE.search(texte_page)
    if match:
        return match.group(0)
    print(f"  ! Numero de facture introuvable page {numero_page}, "
          f"utilisation de 'page-{numero_page}' comme nom de secours.")
    return f"page-{numero_page}"


def decouper(pdf_source: Path, dossier_sortie: Path) -> int:
    """Découpe pdf_source en un PDF par page dans dossier_sortie.
    Retourne le nombre de factures écrites."""
    dossier_sortie.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(str(pdf_source))
    total = len(reader.pages)
    print(f"{total} page(s) trouvee(s) dans {pdf_source.name}")

    noms_utilises: dict[str, int] = {}

    for i, page in enumerate(reader.pages, start=1):
        texte = page.extract_text() or ""
        numero = extraire_numero_facture(texte, i)

        # Sécurité anti-doublon si un même numéro apparaît deux fois
        occurrence = noms_utilises.get(numero, 0)
        noms_utilises[numero] = occurrence + 1
        nom_fichier = numero if occurrence == 0 else f"{numero}-{occurrence + 1}"

        writer = PdfWriter()
        writer.add_page(page)

        chemin_sortie = dossier_sortie / f"{nom_fichier}.pdf"
        with open(chemin_sortie, "wb") as f:
            writer.write(f)

        print(f"  page {i}/{total} -> {chemin_sortie.name}")

    return total
