import pandas as pd
import matplotlib.pyplot as plt

# Load CFD line data (Points:1 in meters -> convert to mm, sort by x)
df_line = pd.read_csv("line_1st.csv")
df_line["x_mm"] = df_line["Points:1"] * 1000.0
df_line = df_line.sort_values("x_mm")

df2_line = pd.read_csv("line_2nd.csv")
df2_line["x_mm"] = df2_line["Points:1"] * 1000.0
df2_line = df2_line.sort_values("x_mm")


def make_figure(ref_csv, ref_col, cfd_col, ylabel, title, out_png, cfd_scale=1.0, flip_ref_x=True):
    df_ref = pd.read_csv(ref_csv, header=None, names=["x_mm", ref_col])
    if flip_ref_x:
        df_ref["x_mm"] = 13.0 - df_ref["x_mm"]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df_line["x_mm"], df_line[cfd_col] * cfd_scale,
            color="tab:blue", linewidth=1.5, label="CFD 1st order")
    ax.plot(df2_line["x_mm"], df2_line[cfd_col] * cfd_scale,
            color="tab:green", linewidth=1.5, label="CFD 2nd order")
    ax.plot(df_ref["x_mm"], df_ref[ref_col],
            "ko", markersize=5, label="Exp. Sung et al. (1995)")
    ax.set_xlabel("Distance x [mm]")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xlim(0.0, 13.0)
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.show()


# Temperature
make_figure(
    "counterflow_Strain_56_T.csv", "T",
    "Temperature",
    "Temperature [K]", "Temperature vs. Distance, S = 56 [1/s]",
    "temperature_comparison.png",
)

# Species mass fractions
species = [
    ("O2",  "counterflow_Strain_56_O2.csv",  "lookup_X-O2",  "X_O2"),
    ("H2O", "counterflow_Strain_56_H2O.csv", "lookup_X-H2O", "X_H2O"),
    ("CO2", "counterflow_Strain_56_CO2.csv", "lookup_X-CO2", "X_CO2"),
    ("CO",  "counterflow_Strain_56_CO.csv",  "lookup_X-CO",  "X_CO"),
    ("CH4", "counterflow_Strain_56_CH4.csv", "lookup_X-CH4", "X_CH4"),
]

for name, ref_csv, cfd_col, ref_col in species:
    make_figure(
        ref_csv, ref_col,
        cfd_col,
        f"Mole fraction {name} [-]",
        f"{name} mole fraction vs. Distance, S = 56 [1/s]",
        f"{name.lower()}_comparison.png",
    )

# Axial velocity
make_figure(
    "counterflow_Strain_56_U.csv", "U",
    "Velocity:1",
    "Axial velocity [cm/s]", "Axial velocity vs. Distance, S = 56 [1/s]",
    "velocity_comparison.png",
    cfd_scale=100.0,
    flip_ref_x=False,
)

# Temperature vs. mixture fraction
df_meas = pd.read_csv("counterflow_Strain_56_Z_T.csv", header=None, names=["Z", "T"])
df_cantera = pd.read_csv("counterflow_T303K.csv", usecols=["MixtureFraction", "Temperature"])
df_cantera = df_cantera.sort_values("MixtureFraction")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(df_line["MixtureFraction"], df_line["Temperature"],
        color="tab:blue", linewidth=1.5, label="CFD 1st order")
ax.plot(df2_line["MixtureFraction"], df2_line["Temperature"],
        color="tab:green", linewidth=1.5, label="CFD 2nd order")
ax.plot(df_cantera["MixtureFraction"], df_cantera["Temperature"],
        color="tab:red", linewidth=1.5, linestyle="--", label="Cantera")
ax.plot(df_meas["Z"], df_meas["T"],
        "ko", markersize=5, label="Exp. Sung et al. (1995)")
ax.set_xlabel("Mixture fraction [-]")
ax.set_ylabel("Temperature [K]")
ax.set_title("Temperature vs. Mixture Fraction")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("temperature_Z_comparison.png", dpi=150)
plt.show()
