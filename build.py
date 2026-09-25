"""
Build dashboard.html (and index.html, for GitHub Pages) from template.html + data.json.

Run after pipeline.py refreshes data.json, or after editing template.html.
"""
import json
import os

DIR = os.path.dirname(os.path.abspath(__file__))


def build(data=None):
    if data is None:
        with open(os.path.join(DIR, "data.json")) as f:
            data = json.load(f)
    with open(os.path.join(DIR, "template.html")) as f:
        template = f.read()
    html = template.replace("__DATA_JSON__", json.dumps(data))
    out_paths = [os.path.join(DIR, "dashboard.html"), os.path.join(DIR, "index.html")]
    for p in out_paths:
        with open(p, "w") as f:
            f.write(html)
    return out_paths


if __name__ == "__main__":
    out_paths = build()
    for p in out_paths:
        print(f"Wrote {p}")
