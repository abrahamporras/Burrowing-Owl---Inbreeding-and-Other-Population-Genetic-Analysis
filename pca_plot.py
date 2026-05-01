import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import numpy as np

# -----------------------
# LOAD DATA
# -----------------------

pca = pd.read_csv("pca.eigenvec", sep=" ", header=None)

meta = pd.read_csv(
    "pca_meta_final.txt",
    sep=" ",
    names=["ID", "POP", "GROUP"]
)

df = pd.merge(meta, pca, left_on="ID", right_on=0)

df = df[[ "ID", "POP", "GROUP", 2, 3 ]]
df.columns = ["ID", "POP", "GROUP", "PC1", "PC2"]

# -----------------------
# COLOR MAP (EDIT IF NEEDED)
# -----------------------

pops = sorted(df["POP"].unique())

colors = {
    pop: plt.cm.tab20(i % 20)
    for i, pop in enumerate(pops)
}

# -----------------------
# PLOTTING FUNCTION
# -----------------------

def plot_group(group, filename):

    fig, ax = plt.subplots(figsize=(8,6))

    sub = df[df["GROUP"] == group]

    for pop in pops:
        d = sub[sub["POP"] == pop]

        if len(d) < 3:
            continue

        pts = d[["PC1", "PC2"]].values

        # scatter points
        marker = "o" if group == "OLD" else "^"
        ax.scatter(
            pts[:,0], pts[:,1],
            color=colors[pop],
            label=pop,
            alpha=0.7,
            marker=marker
        )

        # convex hull (population boundary)
        hull = ConvexHull(pts)
        hull_pts = pts[hull.vertices]

        ax.fill(
            hull_pts[:,0],
            hull_pts[:,1],
            color=colors[pop],
            alpha=0.15
        )

    ax.set_title(f"PCA - {group}")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")

    ax.set_xlim(df["PC1"].min(), df["PC1"].max())
    ax.set_ylim(df["PC2"].min(), df["PC2"].max())

    # single clean legend
    ax.legend(title="Population", bbox_to_anchor=(1.05,1), loc="upper left")

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# -----------------------
# RUN ALL 3 PLOTS
# -----------------------

plot_group("OLD", "PCA_OLD.pdf")
plot_group("NEW", "PCA_NEW.pdf")

# OVERLAY
fig, ax = plt.subplots(figsize=(8,6))

for group, marker in [("OLD","o"), ("NEW","^")]:

    sub = df[df["GROUP"] == group]

    for pop in pops:
        d = sub[sub["POP"] == pop]

        if len(d) < 3:
            continue

        pts = d[["PC1", "PC2"]].values

        ax.scatter(
            pts[:,0], pts[:,1],
            color=colors[pop],
            marker=marker,
            alpha=0.6,
            label=f"{pop}-{group}"
        )

        hull = ConvexHull(pts)
        hull_pts = pts[hull.vertices]

        ax.plot(hull_pts[:,0], hull_pts[:,1], color=colors[pop], alpha=0.2)

ax.set_title("PCA - OVERLAY OLD vs NEW")
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")

ax.legend(bbox_to_anchor=(1.05,1), loc="upper left")
plt.tight_layout()
plt.savefig("PCA_OVERLAY.pdf")
plt.close()
