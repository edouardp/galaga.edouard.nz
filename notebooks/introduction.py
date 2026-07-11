# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "galaga>=1.7.5",
#     "marimo",
# ]
# ///

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
    # Introduction

    Galaga is a small Python library for working with Geometric Algebra.

    This notebook is the first page of the manual. It is not trying to teach all
    of GA, and it is not trying to show every feature in the library. It is here
    to answer the first practical questions:

    - how do I import the package?
    - how do I create an algebra?
    - how do I get basis vectors?
    - how do I build simple multivectors?
    - how do I use the first few operators and helper functions?

    If you are reading this in the browser, the examples run here with no local
    install. If you want to use Galaga in your own Python project, install it
    with:

    ```bash
    pip install galaga
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Who this is for

    If you have heard of GA but have not used it yet, this page gives you enough
    syntax to start experimenting.

    If you already know some GA and are comparing libraries, this page shows the
    API style: ordinary Python objects, a small dependency footprint, and
    operator shorthand that reads naturally in notebooks.

    If you already use GA regularly, skim the code cells and the quick reference
    near the end.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Import Galaga

    We'll import `Algebra` and a few common helper functions explicitly. You can
    also use `from galaga import *` while exploring, but explicit imports make a
    manual easier to read.
    """)
    return


@app.cell
def _():
    from galaga import Algebra, grade, norm, unit

    return Algebra, grade, norm, unit


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Create an algebra

    An `Algebra` defines the space you are working in. The tuple `(1, 1, 1)`
    means 3D Euclidean space: three basis vectors, each squaring to `+1`.
    """)
    return


@app.cell
def _(Algebra):
    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors()

    e1, e2, e3
    return alg, e1, e2, e3


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The basis vectors are normal Galaga values. You can multiply them and inspect
    the result directly.
    """)
    return


@app.cell
def _(e1, e2, e3):
    {
        "e1 * e1": e1 * e1,
        "e2 * e2": e2 * e2,
        "e3 * e3": e3 * e3,
    }
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Scalars belong to the algebra

    A scalar is a native GA value: it is the grade-0 part of the algebra.

    This is similar to how `2` can be treated as the complex number `2 + 0i`.
    Most of the time you can just write normal Python numbers in expressions,
    such as `1 + e1`.

    If you want to be explicit, `alg.scalar(1)` means "the scalar 1 inside this
    algebra".
    """)
    return


@app.cell
def _(alg, e1):
    one = alg.scalar(1)

    {
        "1 + e1": 1 + e1,
        "alg.scalar(1)": one,
        "alg.scalar(1) + e1": one + e1,
    }
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Build multivectors

    In Galaga, scalars, vectors, bivectors, and mixed-grade values are all
    represented as multivectors. You build them with normal Python arithmetic.
    """)
    return


@app.cell
def _(e1, e2):
    v = 3 * e1 + 4 * e2
    B = e1 ^ e2
    m = 1 + 2 * e1 + 3 * B

    {
        "v": v,
        "B": B,
        "m": m,
    }
    return m, v


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The object represented by `B = e1 ^ e2` is a bivector: an oriented plane
    element made from `e1` and `e2`. You do not need a separate class for it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Use operators

    The first operators to know are:

    | Code | Meaning |
    | --- | --- |
    | `a + b` | add multivectors |
    | `a - b` | subtract multivectors |
    | `a * b` | geometric product |
    | `a ^ b` | outer product |
    | `a | b` | inner product shorthand |

    For basis vectors in this Euclidean algebra:
    """)
    return


@app.cell
def _(e1, e2):
    {
        "e1 + e2": e1 + e2,
        "e1 - e2": e1 - e2,
        "e1 * e2": e1 * e2,
        "e1 ^ e2": e1 ^ e2,
        "e1 | e2": e1 | e2,
        "e1 | e1": e1 | e1,
    }
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In words: `e1` and `e2` are orthogonal, so their inner product is zero. Their
    geometric and outer products both give the same basis bivector in this simple
    case.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pull grades back out

    A multivector can contain several grades at once. Use `grade(value, k)` to
    extract one grade. The shorthand `value[k]` does the same thing.
    """)
    return


@app.cell
def _(grade, m):
    {
        "grade(m, 0)": grade(m, 0),
        "grade(m, 1)": grade(m, 1),
        "grade(m, 2)": grade(m, 2),
        "m[1]": m[1],
    }
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A small numeric example

    Galaga values are still numeric objects. You can measure and normalize a
    vector.
    """)
    return


@app.cell
def _(norm, unit, v):
    {
        "norm(v)": norm(v),
        "unit(v)": unit(v),
    }
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Quick reference

    The core workflow is:

    ```python
    from galaga import Algebra

    alg = Algebra((1, 1, 1))
    e1, e2, e3 = alg.basis_vectors()

    v = 3*e1 + 4*e2
    B = e1 ^ e2
    m = 1 + 2*e1 + 3*B
    ```

    The most common first operations are:

    | Task | Code |
    | --- | --- |
    | Create an algebra | `Algebra((1, 1, 1))` |
    | Get basis vectors | `alg.basis_vectors()` |
    | Explicitly create a scalar | `alg.scalar(2)` |
    | Build a vector | `3*e1 + 4*e2` |
    | Build a bivector | `e1 ^ e2` |
    | Add multivectors | `a + b` |
    | Subtract multivectors | `a - b` |
    | Geometric product | `a * b` |
    | Outer product | `a ^ b` |
    | Inner product shorthand | `a | b` |
    | Extract a grade | `grade(m, 1)` or `m[1]` |
    | Get a vector length | `norm(v)` |
    | Normalize a vector | `unit(v)` |

    The next notebook can cover Galaga's notebook-friendly display tools and
    symbolic rendering. This one stops at the package basics.
    """)
    return


if __name__ == "__main__":
    app.run()
