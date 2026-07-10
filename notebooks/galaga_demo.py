# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "galaga",
#     "galaga-marimo",
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.23.13"
app = marimo.App(width="medium")


@app.cell
def _():
    from galaga import Algebra
    import galaga_marimo as gm
    import marimo as mo

    return Algebra, gm, mo


@app.cell(hide_code=True)
def _(gm):
    gm.md(t"""
    # Geometric Algebra with galaga

    This notebook demonstrates the **galaga** library running in the browser via WebAssembly (Python 3.14).
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors(lazy=True)
    return alg, e1, e2, e3


@app.cell
def _(e1, e2, e3, gm):
    v = (3 * e1 + 2 * e2 - e3).name("v")
    B = (e1 ^ e2).name("B")

    gm.md(t"""
    ## Vectors and Bivectors

    A vector: {v.display()}

    A bivector (oriented plane): {B.display()}
    """)
    return v, B


@app.cell
def _(alg, B, v, gm):
    from galaga import sandwich

    R = alg.rotor(B, degrees=45).name("R")
    v_rotated = sandwich(v, R).name("v'")

    gm.md(t"""
    ## Rotations via Rotors

    Rotor (45° in the {B.display()} plane): {R.display()}

    Rotated vector: {v_rotated.display()}
    """)
    return


if __name__ == "__main__":
    app.run()
