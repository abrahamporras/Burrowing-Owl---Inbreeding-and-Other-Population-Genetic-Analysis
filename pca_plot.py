import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

# ----------------------------
# LOAD PCA
# ----------------------------
pca = pd.read_csv("pca.eigenvec", sep=r"\s+", header=None)
pca = pca.iloc[:, [0, 2, 3]]
pca.columns = ["sample", "PC1", "PC2"]

# ----------------------------
# LOAD METADATA
# ----------------------------
meta = pd.read_csv(
    "pca_meta_final.txt",
    sep=r"\s+",
    header=None,
    names=["sample", "pop", "time"]
)

df = pd.merge(pca, meta, on="sample")

pops = sorted(df["pop"].unique())

colors = plt.cm.tab20(np.linspace(0, 1, len(pops)))
color_map = dict(zip(pops, colors))

# ----------------------------
# AXES (YOUR FIXED SCALE)
# ----------------------------
X_LIM = (0.009, 0.0115)
Y_LIM = (-0.018, -0.008)

# ----------------------------
# CONVEX HULL FUNCTION
# ----------------------------
def draw_hull(points, ax, color, alpha=0.25):
    if len(points) < 3:
        return

    hull = ConvexHull(points)
    verts = points[hull.vertices]

    ax.fill(
        verts[:, 0],
        verts[:, 1],
        color=color,
        alpha=alpha,
        edgecolor=color,
        linewidth=1.5
    )

# ----------------------------
# LEGEND (COMBINED ONLY)
# ----------------------------
def build_combined_legend(ax):
    pop_handles = [
        plt.Line2D([0], [0], marker='s', color='w',
                   markerfacecolor=color_map[p], markersize=8, label=p)
        for p in pops
    ]

    time_handles = [
        plt.Line2D([0], [0], marker='o', color='black',
                   linestyle='None', markersize=6, label='OLD'),
        plt.Line2D([0], [0], marker='^', color='black',
                   linestyle='None', markersize=6, label='NEW')
    ]

    leg1 = ax.legend(handles=pop_handles, title="Population",
                     bbox_to_anchor=(1.05, 1), loc="upper left")

    ax.add_artist(leg1)

    ax.legend(handles=time_handles, title="Time",
              bbox_to_anchor=(1.05, 0.55), loc="upper left")

# ============================================================
# 1) OLD ONLY
# ============================================================
fig, ax = plt.subplots()

old_df = df[df["time"] == "OLD"]

for pop in pops:
    sub = old_df[old_df["pop"] == pop][["PC1", "PC2"]].values
    draw_hull(sub, ax, color_map[pop])

ax.set_title("PCA - OLD only")
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_xlim(X_LIM)
ax.set_ylim(Y_LIM)

plt.tight_layout()
plt.savefig("PCA_OLD.pdf")
plt.close()

# ============================================================
# 2) NEW ONLY
# ============================================================
fig, ax = plt.subplots()

new_df = df[df["time"] == "NEW"]

for pop in pops:
    sub = new_df[new_df["pop"] == pop][["PC1", "PC2"]].values
    draw_hull(sub, ax, color_map[pop])

ax.set_title("PCA - NEW only")
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_xlim(X_LIM)
ax.set_ylim(Y_LIM)

plt.tight_layout()
plt.savefig("PCA_NEW.pdf")
plt.close()

# ============================================================
# 3) COMBINED OLD vs NEW
# ============================================================
fig, ax = plt.subplots()

for pop in pops:
    sub = df[df["pop"] == pop]

    old = sub[sub["time"] == "OLD"][["PC1", "PC2"]].values
    new = sub[sub["time"] == "NEW"][["PC1", "PC2"]].values

    draw_hull(old, ax, color_map[pop], alpha=0.18)
    draw_hull(new, ax, color_map[pop], alpha=0.18)

ax.set_title("PCA - Combined OLD vs NEW")
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_xlim(X_LIM)
ax.set_ylim(Y_LIM)

build_combined_legend(ax)

plt.tight_layout()
plt.savefig("PCA_COMBINED.pdf")
plt.close()

print("DONE: 3 PCA PDF plots generated")
