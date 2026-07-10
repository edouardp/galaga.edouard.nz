# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "anywidget",
#     "traitlets",
#     "galaga-marimo",
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import galaga_marimo as gm
    import marimo as mo
    import anywidget
    import traitlets

    return anywidget, gm, mo, traitlets


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Circles as Plane Slices of the Paraboloid

    In the Euclidean plane, a circle is curved. After the conformal lift, that
    same circle becomes a planar slice of the paraboloid.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For a circle

    $$
    (x-c_x)^2 + (y-c_y)^2 = r^2,
    $$

    write

    $$
    z = \frac12(x^2+y^2).
    $$

    Substituting gives

    $$
    z = c_x x + c_y y + \frac12(r^2 - c_x^2 - c_y^2),
    $$

    which is a plane equation in the lifted coordinates.
    """)
    return


@app.cell
def _(mo):
    cx = mo.ui.slider(
        -1.2, 1.2, step=0.05, value=0.4, label="centre x", show_value=True
    )
    cy = mo.ui.slider(
        -1.2, 1.2, step=0.05, value=-0.2, label="centre y", show_value=True
    )
    radius = mo.ui.slider(
        0.2, 1.4, step=0.05, value=0.8, label="radius", show_value=True
    )
    show_cylinder = mo.ui.checkbox(value=False, label="Show projection cylinder")
    return cx, cy, radius, show_cylinder


@app.cell
def _(cx, cy, gm, mo, radius, show_cylinder, viz):
    _v = viz.value
    _cx = _v["cx"]
    _cy = _v["cy"]
    _r = _v["radius"]
    _const = 0.5 * (_r**2 - _cx**2 - _cy**2)
    _md = rf"""
    Circle in the plane:

    $$
    (x-{_cx:.2f})^2 + (y-{_cy:.2f})^2 = {_r:.2f}^2
    $$

    Corresponding plane upstairs:

    $$
    z = {_cx:.2f}\,x + {_cy:.2f}\,y + {_const:.3f}
    $$

    Drag the circle or edge in the 2D view, or use the sliders.
    Drag the 3D view to rotate.
    """
    mo.vstack([cx, cy, radius, show_cylinder, gm.md(_md), viz])
    return


@app.cell(hide_code=True)
def _(cx, cy, paraboloid_widget, radius, show_cylinder):
    viz = paraboloid_widget(
        cx=cx.value,
        cy=cy.value,
        radius=radius.value,
        show_cylinder=show_cylinder.value,
    )
    return (viz,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Key Point

    Every circle in the Euclidean plane lifts to a planar cross-section of the
    paraboloid. Changing the centre translates the slicing plane; changing the
    radius tilts it. This is why CGA can represent circles with linear
    (blade) algebra — they are flat objects upstairs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Widget Code
    """)
    return


@app.cell(hide_code=True)
def _(anywidget, mo, traitlets):
    _ESM = """
    function render({ model, el }) {
      const W3 = 500, W2 = 380, H = 420;

      const container = document.createElement("div");
      container.style.display = "flex";
      container.style.gap = "10px";
      container.style.userSelect = "none";
      el.appendChild(container);

      const canvas2d = document.createElement("canvas");
      canvas2d.width = W2; canvas2d.height = H;
      canvas2d.style.borderRadius = "6px";
      canvas2d.style.background = "#f8fafc";
      container.appendChild(canvas2d);
      const c2 = canvas2d.getContext("2d");

      const canvas3d = document.createElement("canvas");
      canvas3d.width = W3; canvas3d.height = H;
      canvas3d.style.borderRadius = "6px";
      canvas3d.style.background = "#f8fafc";
      canvas3d.style.cursor = "grab";
      container.appendChild(canvas3d);
      const c3 = canvas3d.getContext("2d");

      const ox = W2/2, oy = H/2, s = 95;
      function toScreen(x, y) { return [ox + x*s, oy - y*s]; }
      function toWorld(sx, sy) { return [(sx - ox)/s, -(sy - oy)/s]; }

      // --- 2D drag ---
      let dragMode = null;

      function hitTest(sx, sy) {
        const cx = model.get("cx"), cy = model.get("cy"), r = model.get("radius");
        const [scx, scy] = toScreen(cx, cy);
        const dc = Math.hypot(sx - scx, sy - scy);
        if (dc < 14) return "centre";
        if (Math.abs(dc - r*s) < 14) return "radius";
        return null;
      }

      canvas2d.addEventListener("pointerdown", e => {
        const rect = canvas2d.getBoundingClientRect();
        dragMode = hitTest(e.clientX - rect.left, e.clientY - rect.top);
        if (dragMode) {
          canvas2d.setPointerCapture(e.pointerId);
          canvas2d.style.cursor = "grabbing";
        }
      });

      canvas2d.addEventListener("pointermove", e => {
        const rect = canvas2d.getBoundingClientRect();
        const sx = e.clientX - rect.left, sy = e.clientY - rect.top;
        if (!dragMode) {
          canvas2d.style.cursor = hitTest(sx, sy) ? "grab" : "default";
          return;
        }
        const [wx, wy] = toWorld(sx, sy);
        const snap = (v, lo, hi) => Math.round(Math.max(lo, Math.min(hi, v)) * 20) / 20;
        if (dragMode === "centre") {
          model.set("cx", snap(wx, -1.2, 1.2));
          model.set("cy", snap(wy, -1.2, 1.2));
        } else {
          const r = Math.hypot(wx - model.get("cx"), wy - model.get("cy"));
          model.set("radius", snap(r, 0.2, 1.4));
        }
        model.save_changes();
        drawAll();
      });

      canvas2d.addEventListener("pointerup", () => {
        dragMode = null;
        canvas2d.style.cursor = "default";
      });

      // --- 3D camera (read initial from Python-side dict via traitlets) ---
      let azimuth = -0.9;
      let elevation = 0.45;
      let camDrag = false, camX0 = 0, camY0 = 0, az0 = 0, el0 = 0;

      canvas3d.addEventListener("pointerdown", e => {
        camDrag = true; camX0 = e.clientX; camY0 = e.clientY;
        az0 = azimuth; el0 = elevation;
        canvas3d.setPointerCapture(e.pointerId);
        canvas3d.style.cursor = "grabbing";
      });
      window.addEventListener("pointermove", e => {
        if (!camDrag) return;
        azimuth = az0 + (e.clientX - camX0) * 0.008;
        elevation = Math.max(0.05, Math.min(1.4, el0 - (e.clientY - camY0) * 0.008));
        draw3d();
      });
      window.addEventListener("pointerup", () => {
        if (camDrag) { camDrag = false; canvas3d.style.cursor = "grab"; }
      });

      function project(x, y, z) {
        const ca = Math.cos(azimuth), sa = Math.sin(azimuth);
        const ce = Math.cos(elevation), se = Math.sin(elevation);
        return [W3/2 + (ca*x + sa*y)*105, H/2 - (-sa*ce*x + ca*ce*y + se*z)*105];
      }

      const wireframe = [];
      const n = 28, lo = -1.8, hi = 1.8;
      for (let i = 0; i <= n; i++) {
        const u = lo+(hi-lo)*i/n, pts = [];
        for (let j = 0; j <= n; j++) { const v = lo+(hi-lo)*j/n; pts.push([u,v,0.5*(u*u+v*v)]); }
        wireframe.push(pts);
      }
      for (let j = 0; j <= n; j++) {
        const v = lo+(hi-lo)*j/n, pts = [];
        for (let i = 0; i <= n; i++) { const u = lo+(hi-lo)*i/n; pts.push([u,v,0.5*(u*u+v*v)]); }
        wireframe.push(pts);
      }

      function drawPath(ctx, pts) {
        ctx.beginPath();
        for (let i = 0; i < pts.length; i++) {
          const [sx,sy] = project(pts[i][0], pts[i][1], pts[i][2]);
          if (i===0) ctx.moveTo(sx,sy); else ctx.lineTo(sx,sy);
        }
        ctx.stroke();
      }

      function draw2d() {
        const cx = model.get("cx"), cy = model.get("cy"), r = model.get("radius");
        c2.clearRect(0, 0, W2, H);

        c2.strokeStyle = "#e2e8f0"; c2.lineWidth = 0.5;
        for (let i = -8; i <= 8; i++) {
          c2.beginPath(); c2.moveTo(ox+i*s/4,0); c2.lineTo(ox+i*s/4,H); c2.stroke();
          c2.beginPath(); c2.moveTo(0,oy+i*s/4); c2.lineTo(W2,oy+i*s/4); c2.stroke();
        }
        c2.strokeStyle = "#cbd5e1"; c2.lineWidth = 0.8;
        for (let i = -2; i <= 2; i++) {
          c2.beginPath(); c2.moveTo(ox+i*s,0); c2.lineTo(ox+i*s,H); c2.stroke();
          c2.beginPath(); c2.moveTo(0,oy+i*s); c2.lineTo(W2,oy+i*s); c2.stroke();
        }
        c2.strokeStyle = "#94a3b8"; c2.lineWidth = 1.2;
        c2.beginPath(); c2.moveTo(ox,0); c2.lineTo(ox,H); c2.stroke();
        c2.beginPath(); c2.moveTo(0,oy); c2.lineTo(W2,oy); c2.stroke();

        c2.strokeStyle = "#2563eb"; c2.lineWidth = 2.5;
        c2.beginPath(); c2.arc(ox+cx*s, oy-cy*s, r*s, 0, 2*Math.PI); c2.stroke();

        c2.fillStyle = "#dc2626";
        c2.beginPath(); c2.arc(ox+cx*s, oy-cy*s, 5, 0, 2*Math.PI); c2.fill();

        const hx = ox+(cx+r)*s, hy = oy-cy*s;
        c2.fillStyle = "#2563eb";
        c2.beginPath(); c2.arc(hx, hy, 4, 0, 2*Math.PI); c2.fill();

        c2.fillStyle = "#334155"; c2.font = "13px sans-serif"; c2.textAlign = "center";
        c2.fillText("Circle in the Euclidean plane", W2/2, 20);
        c2.fillStyle = "#94a3b8"; c2.font = "11px sans-serif";
        c2.fillText("drag centre or edge", W2/2, H-10);
      }

      function draw3d() {
        const cx = model.get("cx"), cy = model.get("cy"), r = model.get("radius");
        c3.clearRect(0, 0, W3, H);

        c3.strokeStyle = "rgba(196,181,253,0.3)"; c3.lineWidth = 0.6;
        for (const line of wireframe) drawPath(c3, line);

        const k = 0.5*(r*r-cx*cx-cy*cy);
        const corners = [[lo,lo,cx*lo+cy*lo+k],[hi,lo,cx*hi+cy*lo+k],[hi,hi,cx*hi+cy*hi+k],[lo,hi,cx*lo+cy*hi+k]];
        c3.fillStyle = "rgba(191,219,254,0.25)";
        c3.strokeStyle = "rgba(59,130,246,0.4)"; c3.lineWidth = 1;
        c3.beginPath();
        for (let i = 0; i < 4; i++) {
          const [sx,sy] = project(corners[i][0], corners[i][1], corners[i][2]);
          if (i===0) c3.moveTo(sx,sy); else c3.lineTo(sx,sy);
        }
        c3.closePath(); c3.fill(); c3.stroke();

        c3.strokeStyle = "#7c3aed"; c3.lineWidth = 2.8;
        c3.beginPath();
        for (let i = 0; i <= 200; i++) {
          const t = 2*Math.PI*i/200;
          const px = cx+r*Math.cos(t), py = cy+r*Math.sin(t);
          const [sx,sy] = project(px, py, 0.5*(px*px+py*py));
          if (i===0) c3.moveTo(sx,sy); else c3.lineTo(sx,sy);
        }
        c3.stroke();

        c3.strokeStyle = "#64748b"; c3.lineWidth = 1.2;
        c3.font = "12px sans-serif"; c3.fillStyle = "#475569";
        for (const [f,t,l] of [[[0,0,0],[2,0,0],"e\u2081"],[[0,0,0],[0,2,0],"e\u2082"],[[0,0,0],[0,0,3.2],"z"]]) {
          const [x0,y0] = project(...f), [x1,y1] = project(...t);
          c3.beginPath(); c3.moveTo(x0,y0); c3.lineTo(x1,y1); c3.stroke();
          c3.fillText(l, x1+4, y1-4);
        }

        // Projection cylinder (vertical lines from paraboloid to ground)
        if (model.get("show_cylinder")) {
          c3.strokeStyle = "rgba(124,58,237,0.18)";
          c3.lineWidth = 0.7;
          for (let i = 0; i <= 200; i++) {
            const t = 2*Math.PI*i/200;
            const px = cx+r*Math.cos(t), py = cy+r*Math.sin(t);
            const pz = 0.5*(px*px+py*py);
            const [sx0,sy0] = project(px, py, pz);
            const [sx1,sy1] = project(px, py, -1);
            c3.beginPath(); c3.moveTo(sx0,sy0); c3.lineTo(sx1,sy1); c3.stroke();
          }
        }

        // Ground plane grid (matches 2D grid density)
        c3.strokeStyle = "rgba(226,232,240,0.6)"; c3.lineWidth = 0.5;
        for (let i = -7; i <= 7; i++) {
          const u = i * 0.25;
          const [x0,y0] = project(u,lo,-1), [x1,y1] = project(u,hi,-1);
          c3.beginPath(); c3.moveTo(x0,y0); c3.lineTo(x1,y1); c3.stroke();
          const [x2,y2] = project(lo,u,-1), [x3,y3] = project(hi,u,-1);
          c3.beginPath(); c3.moveTo(x2,y2); c3.lineTo(x3,y3); c3.stroke();
        }
        c3.strokeStyle = "rgba(203,213,225,0.8)"; c3.lineWidth = 0.8;
        for (let i = -2; i <= 2; i++) {
          const [x0,y0] = project(i,lo,-1), [x1,y1] = project(i,hi,-1);
          c3.beginPath(); c3.moveTo(x0,y0); c3.lineTo(x1,y1); c3.stroke();
          const [x2,y2] = project(lo,i,-1), [x3,y3] = project(hi,i,-1);
          c3.beginPath(); c3.moveTo(x2,y2); c3.lineTo(x3,y3); c3.stroke();
        }
        // Axis lines on ground plane (matches 2D #94a3b8)
        c3.strokeStyle = "rgba(148,163,184,0.9)"; c3.lineWidth = 1.2;
        let [ax0,ay0] = project(lo,0,-1), [ax1,ay1] = project(hi,0,-1);
        c3.beginPath(); c3.moveTo(ax0,ay0); c3.lineTo(ax1,ay1); c3.stroke();
        [ax0,ay0] = project(0,lo,-1); [ax1,ay1] = project(0,hi,-1);
        c3.beginPath(); c3.moveTo(ax0,ay0); c3.lineTo(ax1,ay1); c3.stroke();

        // Projected circle on ground plane (z=0)
        c3.strokeStyle = "rgba(37,99,235,0.5)"; c3.lineWidth = 2;
        c3.beginPath();
        for (let i = 0; i <= 200; i++) {
          const t = 2*Math.PI*i/200;
          const px = cx+r*Math.cos(t), py = cy+r*Math.sin(t);
          const [sx,sy] = project(px, py, -1);
          if (i===0) c3.moveTo(sx,sy); else c3.lineTo(sx,sy);
        }
        c3.stroke();

        // Centre dot on ground
        const [ccx,ccy] = project(cx, cy, -1);
        c3.fillStyle = "rgba(220,38,38,0.5)";
        c3.beginPath(); c3.arc(ccx, ccy, 3, 0, 2*Math.PI); c3.fill();

        // Radius handle on projected circle
        const [rhx,rhy] = project(cx+r, cy, -1);
        c3.fillStyle = "rgba(37,99,235,0.5)";
        c3.beginPath(); c3.arc(rhx, rhy, 3, 0, 2*Math.PI); c3.fill();

        c3.fillStyle = "#334155"; c3.font = "13px sans-serif"; c3.textAlign = "center";
        c3.fillText("Planar slice of the paraboloid", W3/2, 20);
      }

      function drawAll() { draw2d(); draw3d(); }

      model.on("change:cx", drawAll);
      model.on("change:cy", drawAll);
      model.on("change:radius", drawAll);
      model.on("change:show_cylinder", drawAll);
      drawAll();
    }

    export default { render };
    """


    class _ParaboloidWidget(anywidget.AnyWidget):
        _esm = _ESM
        cx = traitlets.Float(0.0).tag(sync=True)
        cy = traitlets.Float(0.0).tag(sync=True)
        radius = traitlets.Float(0.8).tag(sync=True)
        show_cylinder = traitlets.Bool(False).tag(sync=True)


    def paraboloid_widget(
        *, cx, cy, radius, show_cylinder=False
    ):
        return mo.ui.anywidget(
            _ParaboloidWidget(
                cx=cx,
                cy=cy,
                radius=radius,
                show_cylinder=show_cylinder,
            )
        )

    return (paraboloid_widget,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
