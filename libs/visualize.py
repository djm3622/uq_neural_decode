import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def _infer_d_from_code(code):
    n = int(code.Hx.shape[1])
    d = int(round(math.sqrt(n)))
    if d * d != n:
        raise ValueError(f"Cannot infer rotated layout: n={n} not a perfect square.")
    return d

def _pauli_supports(pauli_str):
    x_idx, z_idx = [], []
    for i, p in enumerate(pauli_str):
        if p in ("X", "Y"): x_idx.append(i)
        if p in ("Z", "Y"): z_idx.append(i)
    return np.array(x_idx, int), np.array(z_idx, int)

def plot_rotated_surface_from_code(
    code,
    index_to_rc=None,   # callable i -> (row, col) on a d x d grid
    d=None,
    logical=None,       # None, "X", or "Z"  (overlay logical support)
    title=None,
    colors=("#2b6cb0", "#c53030"),  # (X-plaquette blue, Z-plaquette red)
    logical_color="#33aa55",
):
    Hx, Hz = code.Hx, code.Hz
    n = int(Hx.shape[1])
    if d is None:
        d = _infer_d_from_code(code)
    if index_to_rc is None:
        index_to_rc = lambda i: (i // d, i % d)

    x_col, z_col = colors
    fig, ax = plt.subplots(figsize=(5.0, 5.0))
    ax.set_aspect("equal")

    # Draw checkerboard plaquettes; omit boundary-adjacent ones per rotated patch
    for r in range(d):
        for c in range(d):
            is_x = ((r + c) % 2 == 0)
            color = x_col if is_x else z_col
            if (r == 0 and is_x) or (c == 0 and not is_x) or (r == d-1 and not is_x) or (c == d-1 and is_x):
                continue
            ax.add_patch(Rectangle((c, r), 1, 1, facecolor=color, edgecolor="k", lw=0.8, zorder=0.5))

    # Data qubits on vertices that touch at least one kept plaquette
    def vertex_is_used(rr, cc):
        for pr in (rr-1, rr):
            for pc in (cc-1, cc):
                if 0 <= pr < d and 0 <= pc < d:
                    is_x = ((pr + pc) % 2 == 0)
                    if (pr == 0 and is_x) or (pc == 0 and not is_x) or (pr == d-1 and not is_x) or (pc == d-1 and is_x):
                        continue
                    return True
        return False

    used = set()
    for rr in range(d+1):
        for cc in range(d+1):
            if vertex_is_used(rr, cc):
                used.add((rr, cc))
                ax.plot(cc, rr, "ko", ms=4, zorder=2.0)

    # Overlay logical as ORTHOGONAL segments between neighboring support qubits
    if logical in ("X", "Z"):
        if logical == "X":
            strings = code.x_logicals_as_pauli_strings()
            if not strings: raise RuntimeError("No X logicals exposed by code.")
            supp, _ = _pauli_supports(strings[0])
        else:
            strings = code.z_logicals_as_pauli_strings()
            if not strings: raise RuntimeError("No Z logicals exposed by code.")
            _, supp = _pauli_supports(strings[0])

        # Map indices to (row, col) grid coordinates
        rc = np.array([index_to_rc(i) for i in supp], dtype=int)
        rc_set = {tuple(t) for t in rc}

        # Draw a segment for every Manhattan neighbor pair within the support
        # This avoids diagonals and shows the chain along lattice edges.
        for (r, c) in rc_set:
            for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
                nbr = (r+dr, c+dc)
                if nbr in rc_set and ((r, c) in used) and (nbr in used):
                    ax.plot([c, c+dc], [r, r+dr], color=logical_color, lw=3.0, zorder=2.2)

        # Mark the support vertices
        ax.scatter(rc[:,1], rc[:,0], s=36, facecolors="none", edgecolors=logical_color, lw=2.0, zorder=2.3)

    ax.set_xlim(-0.5, d + 0.5)
    ax.set_ylim(-0.5, d + 0.5)
    ax.axis("off")
    ax.set_title(title or f"Rotated surface code (d={d})")
    plt.tight_layout()
    plt.show()
