import marimo

__generated_with = "0.23.13"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Welcome to Galaga

    Galaga is a Geometric Algebra library that emphasises teaching in notebooks (like this Marimo one).

    ## Getting Started writing Galaga code
    """)
    return


if __name__ == "__main__":
    app.run()
