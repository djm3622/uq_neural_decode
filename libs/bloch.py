import numpy as np
import matplotlib.pyplot as plt
from qutip import Bloch, basis, sigmaz, sigmax


def z_phase_pulse():
    # Time axis
    t = np.linspace(0.0, 10.0, 500)

    # Z gate implemented as a phase jump of pi/2
    phi_Z = np.pi / 2.0
    t_gate_start = 4.0
    t_gate_end = 6.0

    phase = np.zeros_like(t)
    phase[(t >= t_gate_start) & (t <= t_gate_end)] = phi_Z
    phase[t > t_gate_end] = phi_Z

    fig, ax = plt.subplots(figsize=(8, 2.5))
    ax.step(t, phase, where="post", linewidth=2)

    ax.axis("off")

    fig.patch.set_alpha(0.0)
    ax.set_facecolor("none")

    fig.savefig(
        "visuals/z_phase_pulse.png",
        dpi=300,
        transparent=True,
        bbox_inches="tight",
        pad_inches=0.1,
    )

    plt.close(fig)


def x_phase_pulse():
    # Time axis
    t_max = 4.0
    t = np.linspace(-t_max, t_max, 1000)

    # Pulse parameters
    sigma = 1.0
    A = 1.0
    omega = 4.0 * np.pi
    phi = 0.0

    # Envelope and pulse
    envelope = A * np.exp(-0.5 * (t / sigma) ** 2)
    pulse = envelope * np.cos(omega * t + phi)

    # Plot pulse
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(t, pulse, linewidth=2)

    ax.axis("off")

    fig.patch.set_alpha(0.0)
    ax.set_facecolor("none")

    fig.savefig(
        "visuals/x_phase_pulse.png",
        dpi=300,
        transparent=True,
        bbox_inches="tight",
        pad_inches=0.1,
    )

    plt.close(fig)


def bloches():
    # Initial state from your amplitudes
    a = -1.0 + 0.0j
    b = 0.5 - 0.5j
    psi = (a * basis(2, 0) + b * basis(2, 1)).unit()

    # Apply Z and then X
    psi_Z = sigmaz() * psi
    psi_ZX = sigmax() * psi_Z

    def save_bloch(state, filename, dpi=300):
        """Render a Bloch sphere for a state and save as transparent PNG."""
        b = Bloch()
        b.add_states(state)

        # Draw into the figure
        b.render()

        fig = b.fig
        ax = b.axes

        # Transparent backgrounds
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        # Save with some padding to avoid clipping
        fig.savefig(
            filename,
            dpi=dpi,
            transparent=True,
            bbox_inches="tight",
            pad_inches=0.25,
        )
        plt.close(fig)

    # Save Bloch spheres
    save_bloch(psi,    "bloch_initial.png")
    save_bloch(psi_Z,  "bloch_after_Z.png")
    save_bloch(psi_ZX, "bloch_after_ZX.png")


def kets():
    def save_ket(eq, filename, dpi=300):
        """Render a ket expression as LaTeX-like math and save as transparent PNG."""
        fig, ax = plt.subplots(figsize=(8, 1.5))
        ax.axis("off")

        fig.patch.set_alpha(0.0)
        ax.set_facecolor("none")

        ax.text(
            0.5,
            0.5,
            eq,
            ha="center",
            va="center",
            fontsize=24,
        )

        fig.savefig(
            filename,
            dpi=dpi,
            transparent=True,
            bbox_inches="tight",
            pad_inches=0.2,
        )
        plt.close(fig)

    # Initial |psi>
    eq_initial = (
        r"$|\psi\rangle"
        r" = \sqrt{\frac{2}{3}}\,|0\rangle"
        r" + \sqrt{\frac{1}{3}}\,e^{i 3\pi/4}|1\rangle$"
    )

    # After Z: |psi_Z>
    eq_Z = (
        r"$|\psi_Z\rangle"
        r" = \sqrt{\frac{2}{3}}\,|0\rangle"
        r" + \sqrt{\frac{1}{3}}\,e^{-i \pi/4}|1\rangle$"
    )

    # After Z then X: |psi_ZX>
    eq_ZX = (
        r"$|\psi_{ZX}\rangle"
        r" = \sqrt{\frac{1}{3}}\,e^{-i \pi/4}|0\rangle"
        r" + \sqrt{\frac{2}{3}}\,|1\rangle$"
    )

    save_ket(eq_initial, "ket_initial.png")
    save_ket(eq_Z,       "ket_after_Z.png")
    save_ket(eq_ZX,      "ket_after_ZX.png")