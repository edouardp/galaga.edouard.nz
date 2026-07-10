"""Generate index.html that dynamically loads notebooks via ?nb= parameter.

Takes the marimo WASM export structure and creates a single index.html that:
1. Reads ?nb=<name> from the URL
2. Fetches notebooks/<name>.py
3. Sets window.__MARIMO_EXPORT_CONTEXT__ with the code
4. THEN loads the marimo runtime module (ordering matters)

If no ?nb= param is provided, shows a listing of available notebooks.
"""

import json
import sys
from pathlib import Path


def main():
    dist_dir = Path(sys.argv[1])
    notebooks_dir = dist_dir / "notebooks"

    # Find the main JS entry point from the assets
    assets_dir = dist_dir / "assets"
    main_js = None
    main_css = None
    for f in assets_dir.iterdir():
        if f.name.startswith("index-") and f.name.endswith(".js"):
            main_js = f"assets/{f.name}"
        if f.name.startswith("index-") and f.name.endswith(".css"):
            main_css = f"assets/{f.name}"

    if not main_js:
        print("ERROR: Could not find index-*.js in assets/", file=sys.stderr)
        sys.exit(1)

    # Get list of notebooks for the landing page
    notebooks = sorted([f.stem for f in notebooks_dir.glob("*.py")])
    notebooks_json = json.dumps(notebooks)

    # Find preload fonts
    preload_fonts = []
    for f in assets_dir.iterdir():
        if f.suffix == ".woff2" and (
            "FiraMono" in f.name or "PTSans" in f.name or "Lora" in f.name
        ):
            preload_fonts.append(f"assets/{f.name}")

    preload_html = "\n    ".join(
        f'<link rel="preload" href="./{font}" as="font" type="font/woff2" crossorigin="anonymous" />'
        for font in sorted(preload_fonts)[:6]
    )

    css_link = f'<link rel="stylesheet" crossorigin href="./{main_css}" />' if main_css else ""

    # The mount config JSON - same as what marimo export generates
    mount_config = json.dumps({
        "filename": "notebook.py",
        "cwd": "",
        "lspWorkspace": None,
        "mode": "edit",
        "version": "0.23.13",
        "serverToken": "unused",
        "config": {"ai": {"custom_providers": {}, "enabled": True, "models": {"custom_models": [], "displayed_models": []}}, "completion": {"activate_on_typing": True, "auto_close_pairs": True, "copilot": False, "signature_hint_on_typing": False}, "diagnostics": {"sql_linter": True}, "display": {"cell_output": "below", "code_editor_font_size": 14, "dataframes": "rich", "default_table_max_columns": 50, "default_table_page_size": 10, "default_width": "medium", "reference_highlighting": True, "theme": "light"}, "formatting": {"line_length": 79}, "keymap": {"overrides": {}, "preset": "default"}, "language_servers": {"pylsp": {"enable_flake8": False, "enable_mypy": True, "enable_pydocstyle": False, "enable_pyflakes": False, "enable_pylint": False, "enable_ruff": True, "enabled": False}}, "mcp": {"mcpServers": {}, "presets": []}, "package_management": {"manager": "uv"}, "runtime": {"auto_instantiate": True, "auto_reload": "off", "default_csv_encoding": "utf-8", "default_sql_output": "auto", "on_cell_change": "autorun", "output_max_bytes": 8000000, "reactive_tests": True, "show_tracebacks": False, "std_stream_max_bytes": 1000000, "watcher_on_save": "lazy"}, "save": {"autosave": "off", "autosave_delay": 1000, "format_on_save": False}, "server": {"browser": "default", "follow_symlink": False}, "snippets": {"custom_paths": [], "include_default_snippets": True}},
        "configOverrides": {},
        "appConfig": {"sql_output": "auto", "width": "medium"},
        "view": {"showAppCode": False},
        "notebook": None,
        "session": None,
        "runtimeConfig": None,
    })

    html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="./favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="galaga.edouard.nz - Interactive Python notebooks" />
    <link rel="apple-touch-icon" href="./apple-touch-icon.png" />
    {preload_html}
    {css_link}
    <title>galaga.edouard.nz</title>

    <script data-marimo="true">
      function __resizeIframe(obj) {{
        const scrollbarHeight = 20;
        function setHeight() {{
          if (!obj.contentWindow?.document?.documentElement) return;
          const element = obj.contentWindow.document.documentElement;
          if (element.scrollHeight === element.clientHeight) return;
          const hasHorizontalScrollbar = element.scrollWidth > element.clientWidth;
          const newHeight = element.scrollHeight + (hasHorizontalScrollbar ? scrollbarHeight : 0);
          if (obj.style.height !== `${{newHeight}}px`) obj.style.height = `${{newHeight}}px`;
        }}
        setHeight();
        const resizeObserver = new ResizeObserver(() => setHeight());
        if (obj.contentWindow?.document?.body) resizeObserver.observe(obj.contentWindow.document.body);
      }}
    </script>

    <marimo-filename hidden>notebook.py</marimo-filename>
    <marimo-version data-version="{{{{ version }}}}" hidden></marimo-version>
    <marimo-user-config data-config="{{{{ user_config }}}}" hidden></marimo-user-config>
    <marimo-server-token data-token="{{{{ server_token }}}}" hidden></marimo-server-token>

    <style>
      .landing {{ font-family: system-ui, -apple-system, sans-serif; max-width: 800px; margin: 0 auto; padding: 2rem; }}
      .landing h1 {{ margin-bottom: 0.5rem; }}
      .landing p {{ color: #666; margin-bottom: 2rem; }}
      .landing ul {{ list-style: none; padding: 0; }}
      .landing li {{ margin-bottom: 0.75rem; }}
      .landing a {{ color: #2563eb; text-decoration: none; font-size: 1.1rem; }}
      .landing a:hover {{ text-decoration: underline; }}
    </style>

    <script data-marimo="true">
      // Synchronous notebook loader - must run before module script
      (function() {{
        var params = new URLSearchParams(window.location.search);
        var nb = params.get('nb');

        if (!nb) {{
          window.__GALAGA_LANDING__ = true;
          return;
        }}

        // Synchronous XHR to fetch notebook code BEFORE module loads
        var xhr = new XMLHttpRequest();
        xhr.open('GET', './notebooks/' + nb + '.py', false);
        xhr.send();

        if (xhr.status !== 200) {{
          window.__GALAGA_LANDING__ = true;
          window.__GALAGA_ERROR__ = 'Notebook "' + nb + '" not found';
          return;
        }}

        var code = xhr.responseText;

        // Set the export context synchronously
        Object.defineProperty(window, "__MARIMO_EXPORT_CONTEXT__", {{
          value: Object.freeze({{ trusted: true, notebookCode: code }}),
          writable: false, configurable: false,
        }});

        // Set marimo-code element
        document.querySelector('marimo-code').textContent = encodeURIComponent(code);

        // Set the mount config
        Object.defineProperty(window, "__MARIMO_MOUNT_CONFIG__", {{
          value: Object.freeze({mount_config}),
          writable: false, configurable: false,
        }});
      }})();
    </script>

    <marimo-code hidden=""></marimo-code>

    <marimo-wasm hidden=""></marimo-wasm>
    <script>
      if (window.location.protocol === 'file:') {{
        alert('Warning: This file must be served by an HTTP server to function correctly.');
      }}
    </script>
    <style>
      #save-button {{ display: none !important; }}
      #filename-input {{ display: none !important; }}
    </style>

    <script>
      // Only load the marimo runtime if we have a notebook
      if (!window.__GALAGA_LANDING__) {{
        document.write('<script type="module" crossorigin src="./{main_js}"><\\/script>');
      }}
    </script>
  </head>
  <body>
    <div id="root"></div>
    <div id="portal" data-testid="glide-portal" style="position: fixed; left: 0; top: 0; z-index: 9999"></div>

    <script data-marimo="true">
      // Landing page or error rendering
      if (window.__GALAGA_LANDING__) {{
        var notebooks = {notebooks_json};
        if (window.__GALAGA_ERROR__) {{
          document.getElementById('root').innerHTML =
            '<div class="landing"><h1>Notebook not found</h1><p>' +
            window.__GALAGA_ERROR__ + '</p><p><a href="./">Back to notebooks</a></p></div>';
        }} else {{
          document.getElementById('root').innerHTML =
            '<div class="landing">' +
            '<h1>galaga.edouard.nz</h1>' +
            '<p>Interactive marimo notebooks running Python 3.14 via WebAssembly.</p>' +
            '<ul>' + notebooks.map(function(n) {{ return '<li><a href="?nb=' + n + '">' + n.replace(/[_-]/g, ' ') + '</a></li>'; }}).join('') + '</ul>' +
            '</div>';
        }}
      }}
    </script>
  </body>
</html>"""

    (dist_dir / "index.html").write_text(html)
    print(f"  Generated index.html with {len(notebooks)} notebook(s)")


if __name__ == "__main__":
    main()
