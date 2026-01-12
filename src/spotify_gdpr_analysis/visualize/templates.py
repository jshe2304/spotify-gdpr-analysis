from __future__ import annotations

from html import escape

_BASE_STYLE = """
:root {
  color-scheme: light;
  --ink: #1a1a1a;
  --muted: #5b5b5b;
  --accent: #d76b30;
  --card: #ffffff;
  --border: #e6dfd8;
  --background: linear-gradient(140deg, #fff3e4 0%, #f8f4ef 55%, #f1f6f5 100%);
  --shadow: 0 22px 45px rgba(0, 0, 0, 0.08);
}
body {
  margin: 0;
  font-family: "Gill Sans", "Trebuchet MS", sans-serif;
  color: var(--ink);
  background: var(--background);
}
header {
  padding: 48px 24px 24px;
  text-align: center;
}
header h1 {
  margin: 0 0 8px;
  font-size: clamp(2rem, 3vw, 3rem);
  font-family: "Palatino", "Book Antiqua", serif;
  letter-spacing: 0.5px;
}
header p {
  margin: 0;
  color: var(--muted);
  font-size: 1rem;
}
main {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px;
  display: grid;
  gap: 24px;
}
section {
  background: var(--card);
  border-radius: 18px;
  padding: 24px;
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  animation: rise 0.6s ease-out both;
}
details {
  margin: 0;
}
summary {
  list-style: none;
  cursor: pointer;
  display: flex;
  align-items: baseline;
  gap: 12px;
}
summary::-webkit-details-marker {
  display: none;
}
summary::before {
  content: "▸";
  font-size: 1.1rem;
  color: var(--accent);
  transition: transform 0.2s ease;
  transform: translateY(-2px);
}
details[open] summary::before {
  transform: rotate(90deg) translateY(-2px);
}
summary h2 {
  margin: 0;
  line-height: 1.15;
}
section h2 {
  margin: 0 0 16px;
  font-size: 1.4rem;
  color: var(--ink);
  font-family: "Palatino", "Book Antiqua", serif;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}
th, td {
  padding: 10px 8px;
  text-align: left;
  border-bottom: 1px solid var(--border);
}
th {
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.08em;
  color: var(--muted);
}
.chart {
  width: 100%;
  overflow-x: auto;
}
svg {
  width: 100%;
  height: auto;
  display: block;
}
.bar {
  fill: var(--accent);
  opacity: 0.9;
}
.gridline {
  stroke: #efe7de;
  stroke-width: 1;
}
.label {
  font-size: 11px;
  fill: var(--muted);
}
@keyframes rise {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
@media (max-width: 720px) {
  header {
    padding-top: 32px;
  }
  section {
    padding: 18px;
  }
  table {
    font-size: 0.9rem;
  }
}
"""


def render_page(report_title: str, body_html: str) -> str:
    title = escape(report_title)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
{_BASE_STYLE.rstrip()}
  </style>
</head>
<body>
  <header>
    <h1>{title}</h1>
    <p>Generated from Spotify streaming history exports.</p>
  </header>
  <main>
    {body_html}
  </main>
</body>
</html>
"""
