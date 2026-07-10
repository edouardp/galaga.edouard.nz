"""Generate the site for galaga.edouard.nz using the iframe approach.

Architecture (matching marimo.app):
1. /e/ — the marimo WASM runtime with empty notebookCode (static export)
2. / and /?nb=<name> — landing page / iframe wrapper that loads /e/#code/<encoded>

The /e/ page is served as a standard marimo WASM export. The parent page
fetches the notebook .py file and passes it to the iframe via the URL hash.
This works on mobile Safari because the iframe loads statically.
"""

import json
import sys
import urllib.parse
from pathlib import Path


def main():
    dist_dir = Path(sys.argv[1])
    notebooks_dir = dist_dir / "notebooks"

    # Get list of notebooks
    notebooks = sorted([f.stem for f in notebooks_dir.glob("*.py")])
    notebooks_json = json.dumps(notebooks)

    # The /e/ directory is already the raw marimo export (with empty code).
    # We just need to patch its index.html to have empty notebookCode.
    e_dir = dist_dir / "e"
    e_index = e_dir / "index.html"
    
    if e_index.exists():
        # Read the exported HTML and blank out the notebook code
        html = e_index.read_text()
        
        # Replace notebookCode value - match from 'notebookCode: "' to the closing '",'
        # accounting for escaped quotes within the string
        import re
        html = re.sub(
            r'notebookCode: "((?:[^"\\]|\\.)*)"',
            'notebookCode: ""',
            html,
        )
        # Also blank out the marimo-code element content
        html = re.sub(
            r'(<marimo-code hidden="">).*?(</marimo-code>)',
            r'\1\2',
            html,
        )
        e_index.write_text(html)
        print("  Patched /e/index.html (blanked notebookCode)")

    # Generate the top-level index.html (landing page + iframe loader)
    top_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>galaga.edouard.nz</title>
  <link rel="icon" href="./e/favicon.ico" />
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{ height: 100%; }}
    .landing {{ font-family: system-ui, -apple-system, sans-serif; max-width: 800px; margin: 0 auto; padding: 2rem; }}
    .landing h1 {{ margin-bottom: 0.5rem; }}
    .landing p {{ color: #666; margin-bottom: 2rem; }}
    .landing ul {{ list-style: none; padding: 0; }}
    .landing li {{ margin-bottom: 0.75rem; }}
    .landing a {{ color: #2563eb; text-decoration: none; font-size: 1.1rem; }}
    .landing a:hover {{ text-decoration: underline; }}
    iframe {{ width: 100%; height: 100%; border: none; }}
  </style>
</head>
<body>
  <div id="root"></div>
  <script>
    (function() {{
      var params = new URLSearchParams(window.location.search);
      var nb = params.get('nb');
      var notebooks = {notebooks_json};

      if (!nb) {{
        document.getElementById('root').innerHTML =
          '<div class="landing">' +
          '<h1>galaga.edouard.nz</h1>' +
          '<p>Interactive marimo notebooks running Python 3.14 via WebAssembly.</p>' +
          '<ul>' + notebooks.map(function(n) {{ return '<li><a href="?nb=' + n + '">' + n.replace(/[_-]/g, ' ') + '</a></li>'; }}).join('') + '</ul>' +
          '</div>';
        return;
      }}

      // Fetch the notebook code, then load it in the iframe via hash
      fetch('./notebooks/' + nb + '.py')
        .then(function(r) {{
          if (!r.ok) throw new Error('Notebook "' + nb + '" not found');
          return r.text();
        }})
        .then(function(code) {{
          var encoded = encodeURIComponent(code);
          var iframe = document.createElement('iframe');
          iframe.src = './e/index.html#code/' + encoded;
          iframe.allow = 'cross-origin-isolated';
          iframe.style.width = '100%';
          iframe.style.height = '100%';
          iframe.style.border = 'none';
          document.getElementById('root').style.height = '100%';
          document.getElementById('root').appendChild(iframe);
        }})
        .catch(function(err) {{
          document.getElementById('root').innerHTML =
            '<div class="landing"><h1>Notebook not found</h1><p>' +
            err.message + '</p><p><a href="./">Back to notebooks</a></p></div>';
        }});
    }})();
  </script>
</body>
</html>"""

    (dist_dir / "index.html").write_text(top_html)
    print(f"  Generated index.html with {len(notebooks)} notebook(s)")


if __name__ == "__main__":
    main()
