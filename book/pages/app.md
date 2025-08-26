---
title: App
---

# App

```{replite}
:kernel: python
:height: 720px
import asyncio
try:
    from pyodide.http import pyfetch
    async def _go():
        r = await pyfetch("_static/app.py")
        code = await r.string()
        exec(code, globals())
    asyncio.get_event_loop().run_until_complete(_go())
except Exception as e:
    print("載入 _static/app.py 失敗：", e)
```
