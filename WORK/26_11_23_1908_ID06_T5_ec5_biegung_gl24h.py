"""T5 Sollwert-Pruefung EC5-1-1 §6.1.6 Biegung, BSH GL24h, Einfeldtraeger."""
def run() -> dict[str, float]:
    b, h, L, q_d = 120.0, 360.0, 5.0, 6.0        # mm, mm, m, kN/m
    f_mk, k_mod, gamma_M = 24.0, 0.8, 1.25        # N/mm2 (EN 14080), Tab. 3.1 NKL1/mittel, Tab. 2.3 BSH
    k_h = min((600.0 / h) ** 0.1, 1.1)            # §3.3(3) BSH, h<600 mm
    M_d = q_d * L**2 / 8.0                        # kNm
    W = b * h**2 / 6.0                            # mm3
    sigma = M_d * 1e6 / W                         # N/mm2
    f_md = k_mod * k_h * f_mk / gamma_M           # N/mm2
    return {"M_d_kNm": M_d, "W_mm3": W, "sigma_md": sigma, "k_h": k_h, "f_md": f_md, "eta": sigma / f_md}
if __name__ == "__main__":
    for k, v in run().items(): print(f"{k} = {v:.4f}")
