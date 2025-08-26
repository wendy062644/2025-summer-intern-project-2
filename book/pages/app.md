---
title: App
---

# App

```{replite}
:kernel: python
:height: 420px
import asyncio, json
from pyodide.http import pyfetch
import ipywidgets as w
from IPython.display import display

api = w.Password(description='API Key:')
runb = w.Button(description='Run')
out = w.Output()

async def call_api(_):
    out.clear_output()
    headers = {"Authorization": f"Bearer {api.value}",
               "Content-Type": "application/json"}
    # Demo：打到可公開測的 httpbin（換成你的 API）
    resp = await pyfetch("https://httpbin.org/post", method="POST",
                         headers=headers, body=json.dumps({"hello": "world"}))
    with out:
        print("Status:", resp.status)
        print(await resp.json())

runb.on_click(lambda _: asyncio.ensure_future(call_api(_)))
display(w.VBox([api, runb, out]))
```
