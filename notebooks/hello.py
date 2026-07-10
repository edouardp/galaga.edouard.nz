import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Hello from galaga.edouard.nz

        This notebook is running **Python 3.14** entirely in your browser via WebAssembly (Pyodide).

        No backend server required!
        """
    )
    return


@app.cell
def _(mo):
    slider = mo.ui.slider(1, 100, value=42, label="Pick a number")
    slider
    return (slider,)


@app.cell
def _(mo, slider):
    mo.md(f"You picked: **{slider.value}**")
    return


@app.cell
def _(slider):
    slider.value * "🎮"
    return


if __name__ == "__main__":
    app.run()
