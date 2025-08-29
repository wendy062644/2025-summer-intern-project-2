1) 系統需求
Python 3.9+（3.10/3.11 皆可）
pip 或 conda（擇一）

2) 建議的虛擬環境
使用 venv（內建）或 conda 皆可：

venv：
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

conda：
conda create -n jb python=3.11 -y
conda activate jb

3) 安裝套件
pip install -U jupyter-book

4) 建置（Build）網站
與 `_config.yml` 同一層
jb build .

5) 啟動伺服器
# 方法一：切到輸出資料夾再開
cd _build/html
python -m http.server 8000

# 方法二：在專案根目錄直接指定目錄
python -m http.server 8000 -d _build/html

6) 在本機上預覽
http://127.0.0.1:8000