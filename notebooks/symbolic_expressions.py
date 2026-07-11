# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "galaga>=1.7.5",
#     "galaga-marimo",
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.23.13"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import galaga_marimo as gm
    import marimo as mo

    return gm, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Symbolic Expressions

    The introduction notebook used Galaga as a direct numeric library. That is
    enough for many programs.

    For teaching, documentation, and exploratory work, we often want the
    intermediate expression too. We want to see not just that `e1 ^ e2`
    evaluates to the bivector `e12`, but that the calculation was written as an
    outer product of two vectors.

    This notebook introduces Galaga's symbolic mode: values still evaluate in
    the algebra, but they also remember the expression that produced them.
    """)
    return


@app.cell
def _():
    from galaga import Algebra, b_default
    from galaga import BladeConvention

    return Algebra, BladeConvention, b_default


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Numeric values and symbolic values

    A basis vector is one of the unit directions of the algebra. In 3D Euclidean
    GA these are usually called `e1`, `e2`, and `e3`.

    A basis blade is a product of basis vectors. For example, `e12` is the
    oriented plane element formed by `e1` and `e2`.

    With ordinary basis vectors, Galaga evaluates products immediately. With
    symbolic basis vectors, Galaga keeps the written expression as well.
    """)
    return


@app.cell
def _(Algebra):
    numeric_alg = Algebra((1, 1, 1))
    numeric_e1, numeric_e2, numeric_e3 = numeric_alg.basis_vectors()
    numeric_plane = numeric_e1 ^ numeric_e2

    symbolic_alg = Algebra((1, 1, 1))
    symbolic_e1, symbolic_e2, symbolic_e3 = symbolic_alg.basis_vectors(
        symbolic=True
    )
    symbolic_plane = symbolic_e1 ^ symbolic_e2

    {
        "numeric e1 ^ e2": numeric_plane,
        "symbolic e1 ^ e2": symbolic_plane,
        "symbolic value evaluated": symbolic_plane.eval(),
    }
    return symbolic_e1, symbolic_e2, symbolic_e3


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The symbolic value still knows its numeric value. `.eval()` asks for the
    evaluated multivector and drops the expression tree.

    This is the core idea: symbolic mode is not a separate algebra. It is the
    same calculation with a remembered expression attached.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Printing symbolic values

    By default, `str(...)` and `repr(...)` stay compact. The expression can still
    produce LaTeX, and it can still evaluate to an ordinary multivector.
    """)
    return


@app.cell
def _(symbolic_e1, symbolic_e2, symbolic_e3):
    symbolic_vector = 2 * symbolic_e1 + symbolic_e2
    symbolic_other = symbolic_e1 - symbolic_e3
    symbolic_product = symbolic_vector * symbolic_other

    {
        "str(symbolic_product)": str(symbolic_product),
        "repr(symbolic_product)": repr(symbolic_product),
        "symbolic_product.latex()": symbolic_product.latex(),
        "symbolic_product.eval()": symbolic_product.eval(),
    }
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Named expressions for teaching

    In a derivation, we usually name the objects we want the reader to track.
    The vector `u`, the vector `w`, and their product are more meaningful than a
    long anonymous expression.

    `.name(...)` gives a value a display name. `.display()` shows the useful
    teaching form: name, expression, and evaluated value.
    """)
    return


@app.cell
def _(symbolic_e1, symbolic_e2, symbolic_e3):
    u = (2 * symbolic_e1 + symbolic_e2).name(latex="u")
    w = (symbolic_e1 - symbolic_e3).name(latex="w")

    uw = (u * w).name(latex="uw")
    u_outer_w = (u ^ w).name(latex=r"u \wedge w")
    u_inner_w = (u | w).name(latex=r"u \cdot w")
    return u, u_inner_w, u_outer_w, uw, w


@app.cell
def _(gm, u, u_inner_w, u_outer_w, uw, w):
    gm.md(t"""
    {u.display()} <br/>
    {w.display()}

    Now the products read like a short derivation:

    {uw.display()} <br/>
    {u_outer_w.display()} <br/>
    {u_inner_w.display()}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The outer product `u ^ w` keeps the oriented plane part. The inner product
    `u | w` keeps the scalar overlap. The geometric product `u * w` contains
    both pieces in one multivector.

    That is enough GA vocabulary for this page: symbolic mode is simply helping
    us show those steps clearly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `display_repr=True`

    In a notebook, you may want the richer display form to appear whenever a
    value is shown as the output of a code cell. `display_repr=True` changes the
    default representation for values created by that algebra.

    This is useful for pedagogical notebooks, but it is usually too verbose for
    ordinary library code.
    """)
    return


@app.cell
def _(Algebra):
    _alg = Algebra((1, 1, 1), display_repr=True)
    _e1, _e2, _e3 = _alg.basis_vectors(symbolic=True)

    _B = (_e1 ^ _e2).name(latex="B")
    _m = (1 + _e1 + 2 * _B).name(latex="m")

    _m
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Getting many basis blades with `alg.locals`

    Early examples often only need basis vectors. Longer notebooks often need
    basis vectors and basis bivectors.

    `alg.locals(...)` returns a dictionary of named basis blades. The keys are
    ordinary Python-friendly names like `e1`, `e2`, and `e12`.
    """)
    return


@app.cell
def _(Algebra):
    _alg = Algebra((1, 1, 1))
    _basis = _alg.locals()

    _basis
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In a plain script or a top-level interactive session, you may choose to
    inject these names:

    ```python
    basis = alg.locals(grades=[1, 2], symbolic=True)
    locals().update(basis)
    ```

    In marimo cells, returning the variables you need explicitly is usually
    clearer, because marimo tracks cell dependencies for you.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Choosing basis blade names

    Basis names are part of the teaching surface. A notebook about ordinary
    Euclidean GA can use `e1`, `e2`, and `e3`. A notebook about another tradition
    may want different names or a different blade style.

    Choose the convention when you construct the algebra. That way all basis
    vectors and basis blades agree from the start.
    """)
    return


@app.cell
def _(Algebra, b_default):
    _alg = Algebra(3,
        blades=b_default(prefix="v", style="wedge", overrides={"pss": "I"}),
    )
    _basis = _alg.locals()

    _basis
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here `prefix="x"` changes the vector names from `e1`, `e2`, `e3` to `x1`,
    `x2`, `x3`. `style="wedge"` prints bivectors as wedge products, such as
    `x1 ^ x2`, instead of compact names like `x12`.

    The override names the pseudoscalar `I`. In 3D GA, the pseudoscalar is the
    oriented unit volume element.
    """)
    return


@app.cell
def _(Algebra, BladeConvention):
    _alg = Algebra(3, blades=BladeConvention(
          vector_names=[
              ("ex", "eₓ", r"e_x"),
              ("ey", "eᵧ", r"e_y"),
              ("ez", "e_z", r"e_z"),
          ],
          overrides={"pss": "i"},
      ))
    _basis = _alg.locals()

    _basis
    return


app._unparsable_cell(
    r"""
    "I had a problem_alg = Algebra(3, blades=BladeConvention(
          vector_names=["x", "y", "z"],
          style="wedge",
          overrides={"pss": "I"},
      ))
    _basis = _alg.locals()

    _basis
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Quick reference

    | Task | Code |
    | --- | --- |
    | Get symbolic basis vectors | `e1, e2, e3 = alg.basis_vectors(symbolic=True)` |
    | Get symbolic basis blades | `basis = alg.locals(grades=[1, 2], symbolic=True)` |
    | Name a value | `B = (e1 ^ e2).name(latex="B")` |
    | Show name, expression, and value | `B.display()` |
    | Evaluate a symbolic value | `B.eval()` |
    | Make rich display the default repr | `Algebra((1, 1, 1), display_repr=True)` |
    | Choose a blade convention | `Algebra((1, 1, 1), blades=b_default(...))` |

    Use symbolic mode when the expression itself is part of what you are
    teaching. Use the ordinary numeric mode when you only need the computed
    value.
    """)
    return


if __name__ == "__main__":
    app.run()
