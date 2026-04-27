# Academic CV Template

A YAML-driven academic CV generator. Edit one file (`cv.yaml`), run one script (`build.py`), compile the output with pdflatex.

Based on [Geoff Boeing's CV template](https://github.com/gboeing/cv).

## Requirements

- Python 3 with [PyYAML](https://pypi.org/project/PyYAML/) (`pip install pyyaml`)
- A LaTeX distribution with pdflatex (e.g. [TeX Live](https://tug.org/texlive/) or [MiKTeX](https://miktex.org/))

## Usage

1. Fork or clone this repo.
2. Edit `cv.yaml` with your details — this is the only file you need to touch.
3. Run `python build.py` to generate `cv.tex`.
4. Compile: `pdflatex cv.tex`

## YAML schema

| Key                       | Description                                            |
| ------------------------- | ------------------------------------------------------ |
| `meta`                    | Name, affiliation, and contact details                 |
| `education`               | Degrees, fields, institutions, and years               |
| `research_areas`          | Free-text bullet points                                |
| `publications`            | Subsections keyed by type (e.g. `journal_articles`)    |
| `invited_talks`           | `seminars_and_workshops` and `conference_activity`     |
| `grants_and_awards`       | `awards_and_honors` and `competitive_scholarships`     |
| `teaching`                | Per-institution course lists                           |
| `professional_employment` | Employment history                                     |
| `service`                 | `service_to_field` and `service_to_university`         |
| `skills`                  | `programming` (list) and `languages` (list with level) |

### Year fields

```yaml
year: 2024              # single year
year_start: 2024        # open-ended range
year_end: present       # "present" is a string literal
year_start: 2020        # closed range
year_end: 2023
```

### DOIs

Store without the `https://doi.org/` prefix:

```yaml
doi: 10.1080/02699931.2025.2597887
```

### Presenting author (conference entries)

```yaml
presenting_author: null          # first author presented
presenting_author: J. Doe		 # someone else presented
```

Non-first presenters are italicised in the output, with a footnote explaining the convention.
