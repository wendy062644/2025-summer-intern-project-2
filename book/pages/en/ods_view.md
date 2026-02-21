---
title: ODS File Preview & Download
thebe: true
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  name: python3
  display_name: Python 3
---

<style>
.dataframe{ width:100%; margin:0px 0 24px !important; }
</style>

# ODS File Preview & Download

This page reads and previews the following two files (showing the first 10 rows of each worksheet) and provides direct download links:

- **Geography Terms – Surveying & Mapping.ods**  
  {download}`Download Geography Terms – Surveying & Mapping.ods <../assets/sites/地理學名詞-測繪學名詞.ods>`  

- **Geography Terms – GIS.ods**  
  {download}`Download Geography Terms – GIS.ods <../assets/sites/地理學名詞-GIS名詞.ods>`  

> Notes  
> - `Geography Terms – Surveying & Mapping.ods` and `Geography Terms – GIS.ods` are sourced from the [NAER Terminology Download Center](https://terms.naer.edu.tw/download/).  
> - To translate English terms from other domains into Chinese, simply upload the corresponding bilingual glossary to the glossary section.

---

## Preview Tool

```{code-cell} ipython3
:tags: [remove-input]
import pandas as pd
from pathlib import Path
from IPython.display import display, Markdown

pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 0)

def preview_ods(path: str, max_rows: int = 10):
    try:
        xl = pd.ExcelFile(path, engine="odf")
    except ModuleNotFoundError:
        display(Markdown(f"**Load failed**: `{path}`\n\nPlease install: `pip install pandas odfpy`"))
        return
    except Exception as e:
        display(Markdown(f"**Load failed**: `{path}`\n\nError: `{e}`"))
        return

    sheets = xl.sheet_names
    display(Markdown(f"**File**: `{Path(path).name}`"))

    for s in sheets:
        try:
            df = pd.read_excel(path, sheet_name=s, engine="odf")
            display(df.head(max_rows))
        except Exception as e:
            display(Markdown(f"- Cannot read sheet `{s}`: `{e}`"))

for p in ("../assets/sites/地理學名詞-測繪學名詞.ods", "../assets/sites/地理學名詞-GIS名詞.ods"):
    p = Path(p)
    if not p.exists():
        display(Markdown(f"**File not found**: `{p}` (current working directory: `{Path.cwd()}`)"))
        continue
    preview_ods(str(p), max_rows=10)