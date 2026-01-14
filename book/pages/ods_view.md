---
title: ODS 檔案預覽與下載
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

# ODS 檔案預覽與下載

本頁會讀取並預覽下列兩個檔案（每個工作表顯示前 10 列），同時提供直接下載連結：

- **地理學名詞-測繪學名詞.ods**  
  {download}`下載 地理學名詞-測繪學名詞.ods <../assets/sites/地理學名詞-測繪學名詞.ods>`  

- **地理學名詞-GIS名詞.ods**  
  {download}`下載 地理學名詞-GIS名詞.ods <../assets/sites/地理學名詞-GIS名詞.ods>`  

> 補充
> -  ` 地理學名詞-測繪學名詞.ods ` 與 `地理學名詞-GIS名詞.ods` 皆出自 [樂詞網下載專區](https://terms.naer.edu.tw/download/)
> - 若想將不同領域的英文翻譯成中文，只需上傳該領域的中英對照表至 glossary 即可

---

## 預覽工具

```{code-cell} ipython3
import pandas as pd
from pathlib import Path
from IPython.display import display, Markdown

pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 0)

def preview_ods(path: str, max_rows: int = 10):
    try:
        xl = pd.ExcelFile(path, engine="odf")
    except ModuleNotFoundError:
        display(Markdown(f"**載入失敗**：`{path}`\n\n需要安裝套件：`pip install pandas odfpy`"))
        return
    except Exception as e:
        display(Markdown(f"**載入失敗**：`{path}`\n\n錯誤：`{e}`"))
        return

    sheets = xl.sheet_names
    display(Markdown(f"**檔案**：`{Path(path).name}`"))

    for s in sheets:
        try:
            df = pd.read_excel(path, sheet_name=s, engine="odf")
            display(df.head(max_rows))
        except Exception as e:
            display(Markdown(f"- 無法讀取工作表 `{s}`：`{e}`"))

for p in ("../assets/sites/地理學名詞-測繪學名詞.ods", "../assets/sites/地理學名詞-GIS名詞.ods"):
    p = Path(p)
    if not p.exists():
        display(Markdown(f"**找不到檔案**：`{p}`（目前工作目錄：`{Path.cwd()}`）"))
        continue
    preview_ods(str(p), max_rows=10)
