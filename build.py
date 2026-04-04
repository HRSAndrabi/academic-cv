#!/usr/bin/env python3
"""
build.py -- Generate cv.tex from cv.yaml.

Usage:
    python build.py                        # cv.yaml -> cv.tex
    python build.py input.yaml             # custom input -> cv.tex
    python build.py input.yaml output.tex  # custom input -> custom output
"""

import sys
import yaml


# ---------------------------------------------------------------------------
# LaTeX helpers
# ---------------------------------------------------------------------------

def tex_escape(s: str) -> str:
    """Escape LaTeX-special characters that appear in plain-text YAML values."""
    s = str(s)
    s = s.replace("&", r"\&")
    s = s.replace("$", r"\$")
    return s


def latex_quotes(s: str) -> str:
    """
    Convert ASCII single-quote pairs to LaTeX style: 'word' -> `word'

    Heuristic: a ' preceded by a space, tab, newline, or opening parenthesis
    is treated as an opening quote and replaced with a backtick.
    """
    result = []
    for i, ch in enumerate(s):
        if ch == "'" and (i == 0 or s[i - 1] in " \t\n("):
            result.append("`")
        else:
            result.append(ch)
    return "".join(result)


def enquote(s: str) -> str:
    return rf"\enquote{{{s}}}"


def textit(s: str) -> str:
    return rf"\textit{{{s}}}"


def href(url: str, display: str) -> str:
    return rf"\href{{{url}}}{{{display}}}"


def url_cmd(u: str) -> str:
    return rf"\url{{{u}}}"


def doi_link(doi: str) -> str:
    return href(f"https://doi.org/{doi}", f"doi.org/{doi}")


def display_year(entry: dict, context: str = "default") -> str:
    """
    Return a LaTeX year label string from a YAML entry.

    Single year:   year: 2024             -> "2024"
    Open range:    year_start: 2024,      -> "2024--present"  (education)
                   year_end: present         "2024--"          (everything else)
    Closed range:  year_start: 2020,      -> "2020--23"  (last 2 digits of end)
                   year_end: 2023
    """
    if "year" in entry:
        return str(entry["year"])
    start = entry["year_start"]
    end = entry.get("year_end", "present")
    if end == "present":
        return f"{start}--present" if context == "education" else f"{start}--"
    return f"{start}--{str(end)[-2:]}"


def tab_item(label: str, body: str, indent: int = 8) -> str:
    return " " * indent + rf"\item[{label}] \tab{{}}{body}"


# ---------------------------------------------------------------------------
# Static preamble  (reproduced verbatim from the original cv.tex)
# ---------------------------------------------------------------------------

PREAMBLE = r"""% !TeX program = pdflatex

\RequirePackage[l2tabu,orthodox]{nag}
\documentclass[11pt,letterpaper]{report}

\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{ebgaramond}
\usepackage{tgheros}

\usepackage[USenglish]{babel}
\usepackage[strict,autostyle]{csquotes}
\usepackage[babel=true]{microtype}

\usepackage{datetime}
\usepackage{enumitem}
\usepackage{geometry}
\usepackage{setspace}
\usepackage{tabto}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{xcolor}

\newcommand{\myname}{Hassan R. S. Andrabi}
\newcommand{\listtabwidth}{1.9cm}
\newcommand{\namefont}[1]{{\normalfont\bfseries\Huge{#1}}}
\definecolor{cvred}{HTML}{850900}

\SetTracking{encoding=*, family=\sfdefault}{30}
\titleformat{\section}{\color{cvred}\lsstyle\sffamily\small\bfseries\uppercase}{}{}{}{}
\titlespacing{\section}{0pt}{30pt plus 4pt minus 4pt}{8pt plus 2pt minus 2pt}

\titleformat{\subsection}{\lsstyle\sffamily\footnotesize\bfseries}{}{}{}{}
\titlespacing{\subsection}{0pt}{16pt plus 4pt minus 4pt}{4pt plus 2pt minus 2pt}

\geometry{body={6.5in, 9.0in},
    left=1.0in,
    top=1.0in}

\setlength\parindent{0em}
\setstretch{0.9}
\newcommand{\listitemspace}{0.25em}

\renewenvironment{itemize}
{\begin{list}{}{\setlength{\leftmargin}{0em}
                \setlength{\parskip}{0em}
                \setlength{\itemsep}{\listitemspace}
                \setlength{\parsep}{\listitemspace}}}
{\end{list}}

\TabPositions{\listtabwidth}
\newlist{tablist}{description}{3}
\setlist[tablist]{leftmargin=\listtabwidth,
    labelindent=0em,
    topsep=0em,
    partopsep=0em,
    itemsep=\listitemspace,
    parsep=\listitemspace,
    font=\normalfont}

\newdateformat{monthyeardate}{\monthname[\THEMONTH] \THEYEAR}

\hypersetup{
    colorlinks  = true,
    urlcolor    = black,
    citecolor   = black,
    linkcolor   = black,
    pdfauthor   = {\myname},
    pdftitle    = {\myname: Curriculum Vitae},
    pdfsubject  = {Curriculum Vitae},
    pdfpagemode = UseNone
}"""


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def build_document_header(cv: dict) -> str:
    meta = cv["meta"]
    aff = meta["affiliation"]
    c = meta["contact"]
    website_display = c["website"].replace("https://", "")
    return "\n".join([
        r"\begin{document}",
        r"    \raggedright{}",
        "",
        r"    \namefont{\myname}",
        "",
        r"    \vspace{1em}",
        r"    \begin{minipage}[t]{0.700\textwidth}",
        f"        {tex_escape(aff['unit'])} \\\\",
        f"        {tex_escape(aff['department'])} \\\\",
        f"        {tex_escape(aff['institution'])}",
        r"    \end{minipage}",
        r"    \begin{minipage}[t]{0.295\textwidth}",
        r"        \raggedleft{}",
        f"        \\href{{mailto:{c['email']}}}{{{c['email']}}} \\\\",
        f"        {c['phone']} \\\\",
        f"        \\href{{{c['website']}}}{{{website_display}}}",
        r"    \end{minipage}",
    ])


def build_education(cv: dict) -> str:
    lines = [r"    \section*{Education}", "", r"    \begin{tablist}"]
    for e in cv["education"]:
        yr = display_year(e, context="education")
        body = f"{tex_escape(e['field'])}, {tex_escape(e['institution'])}, {yr}"
        lines.append(tab_item(e["degree"], body))
    lines += [r"    \end{tablist}", ""]
    return "\n".join(lines)


def build_research_areas(cv: dict) -> str:
    lines = [r"    \section*{Research Areas}", "", r"    \begin{itemize}"]
    for area in cv["research_areas"]:
        # Guard: YAML parses "Key: value" without quotes as a dict
        if isinstance(area, dict):
            k, v = next(iter(area.items()))
            text = f"{k}: {v}"
        else:
            text = str(area)
        lines.append(f"        \\item {tex_escape(text)}")
    lines += [r"    \end{itemize}", ""]
    return "\n".join(lines)


def _format_journal_entry(article: dict) -> str:
    """Format a single journal article as a LaTeX tablist body string."""
    # Author string, with optional prefix ("With") for unusual authorship
    prefix = article.get("author_prefix", "")
    author_str = (f"{prefix} " if prefix else "") + ", ".join(article["authors"]) + "."

    # Journal + volume/issue/pages
    journal = textit(tex_escape(article["journal"]))
    if "volume" in article:
        vol = article["volume"]
        if "issue" in article:
            loc = f"{vol} ({article['issue']})"
        elif "article_number" in article:
            loc = f"{vol} ({article['article_number']})"
        else:
            loc = str(vol)
        if "pages" in article:
            citation = f"{journal} {loc}, {article['pages']}."
        else:
            citation = f"{journal} {loc}."
    else:
        citation = f"{journal}."

    title = enquote(latex_quotes(article["title"]))
    doi = doi_link(article["doi"])
    # Use inter-word space (\  ) after the author period, but plain space before DOI
    # when the citation ends with pagination (matching original cv.tex spacing).
    if "pages" in article:
        return rf"{author_str}\ {title} {citation} {doi}"
    return rf"{author_str}\ {title} {citation}\ {doi}"


def build_publications(cv: dict) -> str:
    lines = [
        r"    \section*{Publications}",
        "",
        r"    \subsection*{Journal Articles}",
        "",
        r"    \begin{tablist}",
    ]
    for a in cv["publications"]["journal_articles"]:
        lines.append(tab_item(str(a["year"]), _format_journal_entry(a)))
    lines += [r"    \end{tablist}", ""]
    return "\n".join(lines)


def _format_seminar(talk: dict) -> str:
    """Format a seminar/workshop entry: enquoted title then event details."""
    title = enquote(latex_quotes(talk["title"]))
    parts = [
        title,
        tex_escape(talk["event"]) + ".",
        tex_escape(talk["institution"]) + ".",
        tex_escape(talk["location"]) + ".",
        str(talk["date"]) + ".",
    ]
    return " ".join(parts)


def _format_conference(conf: dict) -> str:
    """
    Format a conference entry.
    If presenting_author is set and differs from the first author, that
    author's name is italicised (matching the footnote convention in cv.tex).
    """
    presenter = conf.get("presenting_author")
    author_parts = [
        textit(a) if (presenter and a == presenter) else a
        for a in conf["authors"]
    ]
    author_str = ", ".join(author_parts)

    title = enquote(latex_quotes(conf["title"]))
    parts = [
        title,
        tex_escape(conf["conference"]) + ".",
        tex_escape(conf["location"]) + ".",
        str(conf["date"]) + ".",
    ]
    return rf"{author_str}.\ {' '.join(parts)}"


def build_invited_talks(cv: dict) -> str:
    talks = cv["invited_talks"]
    footnote = (
        r"\footnote{Presenting author \textit{italicised} if other than first author.}"
    )
    lines = [r"    \section*{Invited Talks}", ""]

    lines += [r"    \subsection*{Seminars and Workshops}", r"    \begin{tablist}"]
    for t in talks["seminars_and_workshops"]:
        lines.append(tab_item(str(t["year"]), _format_seminar(t)))
    lines += [r"    \end{tablist}", ""]

    lines += [
        f"    \\subsection*{{Conference Activity{footnote}}}",
        r"    \begin{tablist}",
    ]
    for c in talks["conference_activity"]:
        lines.append(tab_item(str(c["year"]), _format_conference(c)))
    lines += [r"    \end{tablist}", ""]

    return "\n".join(lines)


def build_grants_awards(cv: dict) -> str:
    ga = cv["grants_and_awards"]
    lines = [r"    \section*{Grants and Awards}", ""]

    lines += [r"    \subsection*{Awards and Honors}", "", r"    \begin{tablist}"]
    for a in ga["awards_and_honors"]:
        body = (
            f"{tex_escape(a['title'])}, {tex_escape(a['organization'])}."
            f" {tex_escape(a['amount'])}"
        )
        if not body.endswith("."):
            body += "."
        lines.append(tab_item(str(a["year"]), body))
    lines += [r"    \end{tablist}", ""]

    lines += [r"    \subsection*{Competitive Scholarships}", r"    \begin{tablist}"]
    for s in ga["competitive_scholarships"]:
        body = (
            f"{tex_escape(s['title'])}, {tex_escape(s['organization'])}."
            f" {tex_escape(s['amount'])}"
        )
        if not body.endswith("."):
            body += "."
        lines.append(tab_item(str(s["year"]), body))
    lines += [r"    \end{tablist}", ""]

    return "\n".join(lines)


def build_teaching(cv: dict) -> str:
    lines = [r"    \section*{Teaching}", ""]
    for inst_block in cv["teaching"]:
        # lines.append(f"    \\subsection*{{{tex_escape(inst_block['institution'])}}}")
        lines.append("")
        lines.append(r"    \begin{tablist}")
        # Aggregate courses by year, preserving order of first appearance
        by_year: dict[int, list[str]] = {}
        for c in inst_block["courses"]:
            yr = c["year"]
            entry = f"{c['name']} ({c['level']}), {c['role']}"
            by_year.setdefault(yr, []).append(entry)
        for yr, entries in by_year.items():
            lines.append(tab_item(str(yr), "; ".join(entries)))
        lines += [r"    \end{tablist}", ""]
    return "\n".join(lines)


def build_employment(cv: dict) -> str:
    lines = [r"    \section*{Professional Employment}", "", r"    \begin{tablist}"]
    for e in cv["professional_employment"]:
        yr = display_year(e)
        body = f"{tex_escape(e['title'])}, {tex_escape(e['organization'])}"
        lines.append(tab_item(yr, body))
    lines += [r"    \end{tablist}", ""]
    return "\n".join(lines)


def build_service(cv: dict) -> str:
    svc = cv["service"]
    lines = [r"    \section*{Service}", ""]

    lines += [r"    \subsection*{Service to the Field}", r"    \begin{tablist}"]
    for item in svc["service_to_field"]:
        yr = display_year(item)
        body = tex_escape(item["description"])
        if "url" in item:
            # Use inter-word space (\  ) before \url to suppress end-of-sentence stretch
            body += rf"\ {url_cmd(item['url'])}."
        lines.append(tab_item(yr, body))
    lines += [r"    \end{tablist}", ""]

    lines += [r"    \subsection*{Service to the University}", r"    \begin{tablist}"]
    for item in svc["service_to_university"]:
        yr = display_year(item)
        body = f"{tex_escape(item['role'])}, {tex_escape(item['organization'])}"
        lines.append(tab_item(yr, body))
    lines += [r"    \end{tablist}", ""]

    return "\n".join(lines)


def build_skills(cv: dict) -> str:
    skills = cv["skills"]
    prog = ", ".join(skills["programming"])
    langs = ", ".join(
        f"{lang['name']} ({lang['level']})" for lang in skills["languages"]
    )
    lines = [
        r"    \section*{Skills}",
        "",
        r"    \begin{itemize}",
        f"        \\item Programming: {prog}",
        f"        \\item Languages: {langs}",
        r"    \end{itemize}",
        "",
    ]
    return "\n".join(lines)


def build_footer() -> str:
    return "\n".join([
        r"    % display today's date as Month Year after a vertical space below the end of the text",
        r"    \begin{center}",
        r"        \vfill",
        r"        Updated \monthyeardate\today",
        r"    \end{center}",
        r"\end{document}",
    ])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def generate(yaml_path: str = "cv.yaml", tex_path: str = "cv.tex") -> None:
    with open(yaml_path) as f:
        cv = yaml.safe_load(f)

    blocks = [
        PREAMBLE,
        "",
        build_document_header(cv),
        "",
        build_education(cv),
        build_research_areas(cv),
        build_publications(cv),
        build_invited_talks(cv),
        build_grants_awards(cv),
        build_teaching(cv),
        build_employment(cv),
        build_service(cv),
        build_skills(cv),
        build_footer(),
    ]

    output = "\n".join(blocks) + "\n"

    with open(tex_path, "w") as f:
        f.write(output)

    print(f"Written: {tex_path}")


if __name__ == "__main__":
    args = sys.argv[1:]
    _yaml = args[0] if len(args) > 0 else "cv.yaml"
    _tex  = args[1] if len(args) > 1 else "cv.tex"
    generate(_yaml, _tex)
