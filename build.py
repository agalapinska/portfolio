#!/usr/bin/env python3
"""Składa strony z src/*.html i wspólnego szablonu (nawigacja, stopka).

Użycie:  python3 build.py
Treść stron edytuj w src/, a nie w plikach .html w katalogu głównym.
"""
from pathlib import Path

ROOT = Path(__file__).parent
EMAIL = "agata@quale.agency"
CV_URL = "#"          # TODO: ścieżka do pliku CV, np. assets/cv.pdf
LINKEDIN_URL = "#"    # TODO: adres profilu LinkedIn

NAV = [
    ("case-studies.html", "Case studies"),
    ("referencje.html", "Referencje"),
    ("o-mnie.html", "O mnie"),
    ("eksperymenty.html", "Eksperymenty"),
]

# plik: (tytuł, opis, aktywna pozycja menu, pasek z case study u góry)
PAGES = {
    "index.html": ("Agata Kręczkowska — UX Researcher & Product Builder",
                   "Badania, z których wynika produkt. Badam, syntetyzuję i buduję tak, żeby każda decyzja produktowa miała pokrycie w dowodach i w biznesie.",
                   None, True),
    "case-studies.html": ("Case studies — Agata Kręczkowska",
                          "Od pytania do decyzji: case studies z badań, strategii i projektowania produktów.",
                          "case-studies.html", True),
    "case-formularz.html": ("Czasami to nie formularz jest problemem — case study",
                            "Zespół chciał poprawić formularz. Badania pokazały, że ludzie odpadają wcześniej i z innego powodu.",
                            "case-studies.html", False),
    "referencje.html": ("Referencje — Agata Kręczkowska",
                        "Słowa osób, z którymi pracowałam: przełożonych, developerów i klientów.",
                        "referencje.html", True),
    "o-mnie.html": ("O mnie — Agata Kręczkowska",
                    "Najpierw rozumiem. Potem buduję. UX Researcher & Product Builder.",
                    "o-mnie.html", True),
    "eksperymenty.html": ("Eksperymenty — Agata Kręczkowska",
                          "Buduję, żeby sprawdzić: prototypy, narzędzia i projekty po godzinach.",
                          "eksperymenty.html", True),
}

ANNOUNCE = """
  <a class="announce" href="case-formularz.html">
    <span class="announce__label">Case study</span>
    <span>Czasami to nie formularz jest problemem</span>
    <span aria-hidden="true">→</span>
  </a>
"""

CTA = f"""
    <section class="dark cta">
      <div class="cta__text">
        <h2 class="h2">Masz pytanie, na które zespół <em>nie zna</em> odpowiedzi?</h2>
        <p>Opowiedz mi o nim. Odpiszę, jak bym do niego podeszła i ile to zajmie.</p>
      </div>
      <div class="btn-row">
        <a class="btn btn--light" href="mailto:{EMAIL}">Porozmawiajmy</a>
        <a class="btn btn--ghost" href="mailto:{EMAIL}">{EMAIL} ↗</a>
      </div>
    </section>
"""


def nav_links(active, indent):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        out.append(f'{indent}<a href="{href}"{cur}>{label}</a>')
    return "\n".join(out)


def partials():
    """Wspólne fragmenty: src/_cases.html, _stats.html, _faq.html oraz
    src/_partials.html (kilka fragmentów rozdzielonych <!-- nazwa -->)."""
    src = ROOT / "src"
    parts = {n: (src / f"_{n}.html").read_text(encoding="utf-8") for n in ("cases", "stats", "faq")}
    name = None
    for line in (src / "_partials.html").read_text(encoding="utf-8").splitlines(keepends=True):
        s = line.strip()
        if s.startswith("<!--") and s.endswith("-->"):
            name = s[4:-3].strip()
            parts[name] = ""
        elif name:
            parts[name] += line
    parts.update(cta=CTA, email=EMAIL, cv=CV_URL, linkedin=LINKEDIN_URL)
    return parts


def render(name, title, desc, active, announce):
    body = (ROOT / "src" / name).read_text(encoding="utf-8")
    for key, value in partials().items():
        body = body.replace("{{" + key + "}}", value.rstrip("\n"))
    assert "{{" not in body, f"nieznany fragment w {name}"
    t = title.replace("&", "&amp;")
    return f"""<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{t}</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600&family=Instrument+Serif:ital@1&family=Inter:ital,wght@0,400;1,300;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
{ANNOUNCE if announce else ""}
  <header class="nav">
    <a class="logo" href="index.html" aria-label="Kręczkowska — strona główna">Kręczko<em>w</em>ska</a>
    <nav class="nav__links" aria-label="Główna nawigacja">
{nav_links(active, "      ")}
    </nav>
    <div class="nav__actions">
      <a class="btn btn--outline btn--sm nav__cv" href="{CV_URL}"><span class="u">CV (PDF)</span> ↗</a>
      <a class="btn btn--solid btn--sm" href="mailto:{EMAIL}">Porozmawiajmy</a>
    </div>
  </header>

  <main>
{body.rstrip()}
  </main>

  <footer class="footer">
    <div class="footer__top">
      <a href="index.html" class="footer__logo"><img src="assets/logo.svg" alt="Kręczkowska" width="232" height="34"></a>
      <nav class="footer__links" aria-label="Nawigacja w stopce">
{nav_links(None, "        ")}
      </nav>
    </div>
    <div class="footer__contact">
      <a href="mailto:{EMAIL}">
        <span class="footer__label">E-mail</span>
        <span class="footer__value">{EMAIL}</span>
      </a>
      <a href="https://quale.agency" target="_blank" rel="noopener">
        <span class="footer__label">Agencja</span>
        <span class="footer__value">quale.agency</span>
      </a>
      <a href="{LINKEDIN_URL}">
        <span class="footer__label">LinkedIn</span>
        <span class="footer__value">przejdź do profilu ↗</span>
      </a>
    </div>
    <div class="footer__bottom">
      <span>© 2026 Agata Kręczkowska</span>
      <span>UX Researcher &amp; Product Builder</span>
      <span>Polityka prywatności</span>
    </div>
  </footer>
</body>
</html>
"""


if __name__ == "__main__":
    for name, meta in PAGES.items():
        (ROOT / name).write_text(render(name, *meta), encoding="utf-8")
        print("zbudowano", name)
