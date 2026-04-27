# CV Data

`cv.yaml` is the single source of truth for the cv. The LaTeX file (`cv.tex`) and PDF (`cv.pdf`) are generated from it.

---

## Schema overview

| Key                       | Description                                                     |
| ------------------------- | --------------------------------------------------------------- |
| `meta`                    | Name, affiliation, and contact details                          |
| `education`               | Degrees, fields, institutions, and years                        |
| `research_areas`          | Free-text bullet points                                         |
| `publications`            | Subsections keyed by type (e.g. `journal_articles`)             |
| `invited_talks`           | `seminars_and_workshops` and `conference_activity`              |
| `grants_and_awards`       | `awards_and_honors` and `competitive_scholarships`              |
| `teaching`                | Per-institution lists of courses, one entry per year per course |
| `professional_employment` | Employment history                                              |
| `service`                 | `service_to_field` and `service_to_university`                  |
| `skills`                  | `programming` (list) and `languages` (list with level)          |

### Year fields

Entries use one of three patterns depending on whether they span a range:

```yaml
year: 2024 # single year
year_start: 2024 # open-ended or closed range
year_end: present # "present" is a string literal
```

### `presenting_author` in conference activity

`presenting_author` is `null` when the first-listed author presented, or the author's name string when someone else did. This mirrors the LaTeX footnote convention of italicising non-first presenters.

```yaml
presenting_author: null          # first author presented
presenting_author: K. Ioannidis  # this person presented instead
```

### DOI links

DOIs are stored without the `https://doi.org/` prefix. Prepend it when generating links:

```python
url = f"https://doi.org/{entry['doi']}"
```

---

## Editing the CV

1. Edit `cv.yaml` — this is the only file you need to touch for content changes.
2. Re-run `build.py` to regenerate `cv.tex` / `cv.pdf`.
