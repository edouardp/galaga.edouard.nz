# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "galaga>=1.7.5",
#     "galaga-marimo>=1.7.5",
#     "galaga-matrix>=1.7.5",
#     "marimo",
#     "numpy",
# ]
# ///

import marimo

__generated_with = "0.23.13"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import galaga_marimo as gm
    import marimo as mo
    import numpy as np
    from galaga import Algebra, b_sta, b_pga
    from galaga.algebra import Multivector
    from galaga_matrix import MatrixRepr, from_matrix, to_matrix

    return (
        Algebra,
        Multivector,
        b_pga,
        b_sta,
        from_matrix,
        gm,
        mo,
        np,
        to_matrix,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Multivectors to matrices—and back again

    `galaga_matrix` converts a multivector to a matrix representation and can
    recover the multivector afterwards:

    $$
    \rho^{-1}(\rho(M))=M.
    $$

    Matrix representations also preserve the geometric product:

    $$
    \rho^{-1}\!\left(\rho(M)\rho(N)\right)=MN.
    $$

    Every example starts with a multivector. Its matrix therefore lies in the
    image of the representation, where conversion back is meaningful.

    NumPy uses `A @ B` for matrix multiplication; `A * B` is elementwise
    multiplication.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A first compact roundtrip: $Cl(2,0)$

    The four-dimensional algebra $Cl(2,0)$ has a faithful $2\times2$ real
    matrix representation. It is the smallest example that contains scalars,
    vectors, and a bivector.
    """)
    return


@app.cell
def _(Algebra, from_matrix, gm, to_matrix):
    _alg = Algebra(2, 0, display_repr=True)
    _e1, _e2 = _alg.basis_vectors()
    _e12 = _e1 * _e2

    _m = (2 + 3 * _e1 - _e2 + 0.5 * _e12).name(latex="m")

    gm.md(rt"""
    Construct a multivector:

    {_m}

    Convert it with `to_matrix()`:

    {to_matrix(_m)}

    Convert the matrix with `from_matrix()`:

    {from_matrix(to_matrix(_m))}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pauli matrices: compact $Cl(3,0)$

    In three-dimensional Euclidean geometric algebra, compact mode uses the
    $2\times2$ complex Pauli representation:

    $$
    \rho(e_1)=\sigma_1,\qquad
    \rho(e_2)=\sigma_2,\qquad
    \rho(e_3)=\sigma_3.
    $$

    Complex entries make the representation smaller; the multivector still has
    real coefficients.
    """)
    return


@app.cell
def _(Algebra, from_matrix, gm, to_matrix):
    _alg = Algebra(3, 0, display_repr=True)
    _e1, _e2, _e3 = _alg.basis_vectors()

    _m = (
        0.5
        + _e1
        - 2 * _e2
        + 0.75 * _e3
        + 0.25 * (_e1^_e2)
        - 0.5 * (_e2^_e3)
        + 1.25 * (_e1^_e2^_e3)
    ).name(latex="m")

    gm.md(rt"""
    Start with basis-vector multivectors and convert them:

    {_e1} $\longmapsto$ {to_matrix(_e1).name(latex=r"\sigma_1")}

    {_e2} $\longmapsto$ {to_matrix(_e2).name(latex=r"\sigma_2")}

    {_e3} $\longmapsto$ {to_matrix(_e3).name(latex=r"\sigma_3")}

    The same conversion works for a mixed-grade multivector:

    {_m}

    {to_matrix(_m)}

    And converting back from Matrix to Multivector preserves the roundtrip

    {from_matrix(to_matrix(_m))}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dirac matrices: compact spacetime algebra

    Spacetime algebra $Cl(1,3)$ has signature $(+,-,-,-)$. Compact mode uses
    $4\times4$ complex Dirac matrices. The basis vectors become gamma matrices
    whose squares preserve the metric:

    $$
    (\gamma^0)^2=+\mathbb I_4,
    \qquad
    (\gamma^1)^2=(\gamma^2)^2=(\gamma^3)^2=-\mathbb I_4.
    $$
    """)
    return


@app.cell
def _(Algebra, b_sta, from_matrix, gm, np, to_matrix):
    _alg = Algebra(1, 3, blades=b_sta(), display_repr=True)
    _g0, _g1, _g2, _g3 = _alg.basis_vectors()
    _i = _alg.pseudoscalar()
    _matrix_identity = np.eye(4)

    _m = (
        1
        + 2 * _g0
        -     _g1
        + 0.5 * _g2
        + 1.25 * (_g0^_g1)
        - 0.75 * (_g2^_g3)
        + 0.2 * _i
    ).name(latex="m")



    gm.md(rt"""
    Start with spacetime basis-vector multivectors:

    {_g0} $\longmapsto$ {to_matrix(_g0).name(latex=r"\gamma^0")}

    {_g1} $\longmapsto$ {to_matrix(_g1).name(latex=r"\gamma^1")}

    {_g2} $\longmapsto$ {to_matrix(_g2).name(latex=r"\gamma^2")}

    {_g3} $\longmapsto$ {to_matrix(_g3).name(latex=r"\gamma^3")}

    Their computed squares match the metric:

    - $(\gamma^0)^2=+\mathbb I_4$: `{np.allclose(to_matrix(_g0) @ to_matrix(_g0),   _matrix_identity)}`
    - $(\gamma^1)^2=-\mathbb I_4$: `{np.allclose(to_matrix(_g1) @ to_matrix(_g1), - _matrix_identity)}`
    - $(\gamma^2)^2=-\mathbb I_4$: `{np.allclose(to_matrix(_g2) @ to_matrix(_g2), - _matrix_identity)}`
    - $(\gamma^3)^2=-\mathbb I_4$: `{np.allclose(to_matrix(_g3) @ to_matrix(_g3), - _matrix_identity)}`

    A mixed-grade spacetime multivector roundtrips through the same basis:

    {_m}

    {to_matrix(_m)}

    {from_matrix(to_matrix(_m))}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Spacetime algebra as quaternion matrices

    $Cl(1,3)$ is also a matrix algebra over the quaternions. With
    `mode="quaternion"`, a multivector is rendered as a $2\times2$ matrix with
    quaternion entries.

    `MatrixRepr` makes `@` look like quaternion matrix multiplication, but
    NumPy multiplies a $4\times4$ complex backing array. Each displayed
    quaternion is embedded as a $2\times2$ complex block. This block basis is
    different from the Dirac basis above, although both preserve the same
    geometric product.
    """)
    return


@app.cell
def _(Algebra, b_sta, from_matrix, gm, to_matrix):
    _alg = Algebra(1, 3, blades=b_sta(), display_repr=True)
    _g0, _g1, _g2, _g3 = _alg.basis_vectors()
    _i = _g0^_g1^_g2^_g3

    _a = (1 + _g0 + 0.75 * (_g2 * _g3) + 0.2 * _i).name("a")
    _b = (-0.5 + _g3 + 0.4 * (_g0 * _g2) - 0.3 * _i).name("b")

    _a_qmat = to_matrix(_a, mode="quaternion")
    _b_qmat = to_matrix(_b, mode="quaternion")

    gm.md(rt"""
    Start with two multivectors:

    {_a} <br/>
    {_b}

    Convert both to quaternion-block matrices:

    {_a_qmat}

    {_b_qmat}

    `MatrixRepr` lets us multiply them directly with `_a_qmat @ _b_qmat`:

    {_a_qmat @ _b_qmat}

    Convert the matrix product back:

    {from_matrix(_a_qmat @ _b_qmat)}

    Compare with the direct geometric product of $a$ and $b$:

    {_a * _b}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Degenerate algebras use left-regular matrices

    Compact mode requires a non-degenerate Clifford algebra. If the metric has
    a null direction, `to_matrix` defaults to the **left-regular**
    representation.

    Left multiplication by $M$ is the linear map

    $$
    L_M:X\longmapsto MX.
    $$

    Its matrix is larger—$2^n\times2^n$ for an $n$-dimensional vector
    space—but it is faithful for every Clifford algebra.
    """)
    return


@app.cell
def _(Algebra, b_pga, from_matrix, gm, to_matrix):
    _alg = Algebra(2, 0, 1, blades=b_pga(), display_repr=True)
    _e0, _e1, _e2 = _alg.basis_vectors()

    _a = (1 + 2 * _e0 - _e1 + 0.5 * _e2 + 1.25 * (_e0 ^ _e1)).name(latex="a")

    _matrix = to_matrix(_a, mode="left-regular")

    gm.md(rt"""
    Construct a multivector in an algebra with computed signature `{_alg.signature}`:

    {_a}

    Convert it to the left-regular representation. The matrix has shape `{_matrix.shape[0]} × {_matrix.shape[1]}`:

    {_matrix}

    Convert it back:

    {from_matrix(_matrix)}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Accumulated roundtrip check

    The examples above show individual values. This final cell concentrates all
    of the verification in one place. For each faithful representation it:

    1. constructs two random multivectors $M$ and $N$;
    2. checks $\rho^{-1}(\rho(M))=M$;
    3. checks $\rho^{-1}(\rho(M)\rho(N))=MN$;
    4. repeats the process and records the largest coefficient error.
    """)
    return


@app.cell
def _(Algebra, Multivector, from_matrix, gm, np, to_matrix):
    _rng = np.random.default_rng(42)
    _specifications = [
        ("$Cl(2,0)$ compact real", Algebra(2, 0), "compact"),
        ("$Cl(3,0)$ Pauli", Algebra(3, 0), "compact"),
        ("$Cl(1,3)$ Dirac", Algebra(1, 3), "compact"),
        ("$Cl(1,3)$ quaternion", Algebra(1, 3), "quaternion"),
        ("$Cl(2,0,1)$ left-regular", Algebra(2, 0, 1), "left-regular"),
    ]

    _results = []
    for _label, _alg, _mode in _specifications:
        _roundtrip_errors = []
        _product_errors = []

        for _ in range(50):
            _M = Multivector(_alg, _rng.standard_normal(_alg.dim))
            _N = Multivector(_alg, _rng.standard_normal(_alg.dim))

            _M_matrix = to_matrix(_M, mode=_mode)
            _M_back = from_matrix(_M_matrix)

            _matrix_product = to_matrix(_M, mode=_mode) @ to_matrix(
                _N, mode=_mode
            )
            _product_back = from_matrix(_matrix_product)
            _direct_product = _M * _N

            _roundtrip_errors.append(
                float(np.max(np.abs(_M_back.data - _M.data)))
            )
            _product_errors.append(
                float(
                    np.max(
                        np.abs(_product_back.data - _direct_product.data)
                    )
                )
            )

        _max_roundtrip_error = max(_roundtrip_errors)
        _max_product_error = max(_product_errors)
        assert _max_roundtrip_error < 1e-10
        assert _max_product_error < 1e-10
        _results.append(
            (_label, _max_roundtrip_error, _max_product_error)
        )

    _rows = "\n".join(
        f"| {_label} | {_roundtrip:.3e} | {_product:.3e} |"
        for _label, _roundtrip, _product in _results
    )

    gm.md(rt"""
    Each row accumulates **50 multivector pairs**:

    | Representation | Maximum $M$ roundtrip error | Maximum product roundtrip error |
    |---|---:|---:|
    {_rows}

    Every accumulated error is below `1e-10`. Numerically, all 250 pairs satisfy

    $$
    \rho^{-1}(\rho(M))=M,
    \qquad
    \rho^{-1}(\rho(M)\rho(N))=MN.
    $$

    This reflects the algebra-homomorphism property
    $\rho(MN)=\rho(M)\rho(N)$; the trials exercise the implementation across
    several concrete representations.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Compact representations are the natural first choice because they are
    small. Quaternion mode exposes quaternion structure while using complex
    blocks underneath. Left-regular mode stays faithful when a degenerate
    metric prevents a compact representation.

    Some non-degenerate Clifford algebras split into two simple summands. A
    single irreducible compact representation is then not injective, so
    `from_matrix` cannot uniquely recover every multivector. All roundtrips in
    this notebook deliberately use faithful representations.
    """)
    return


if __name__ == "__main__":
    app.run()
