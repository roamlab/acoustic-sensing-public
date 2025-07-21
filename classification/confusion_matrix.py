import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


one_line_9 = np.array([0, 0, 0, 1, 1, 1, 1, 1, 0, 1])
diagonal_2 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
in_hole_8 = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
diagonal_6 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
one_line_1 = np.array([0, 1, 0, 0, 0, 0, 1, 1, 1, 1])
in_hole_3 = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
in_hole_10 = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
one_line_5 = np.array([1, 1, 1, 1, 1, 1, 1, 0, 1, 1])
diagonal_4 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
in_hole_9 = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
diagonal_5 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
in_hole_4 = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
one_line_8 = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 1])
one_line_2 = np.array([1, 0, 1, 1, 0, 1, 1, 0, 1, 1])
in_hole_2 = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
one_line_10 = np.array([2, 2, 1, 2, 1, 1, 2, 1, 2, 2])
diagonal_10 = np.array([1, 0, 0, 0, 0, 1, 0, 0, 0, 1])
diagonal_3 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
diagonal_7 = np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
in_hole_7 = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
diagonal_1 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
one_line_3 = np.array([0, 0, 1, 1, 0, 0, 0, 0, 1, 1])
one_line_6 = np.array([0, 1, 1, 1, 1, 1, 1, 1, 0, 1])
in_hole_1 = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
one_line_7 = np.array([1, 0, 1, 1, 1, 1, 1, 1, 1, 0])
in_hole_5 = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
in_hole_6 = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
one_line_4 = np.array([1, 1, 1, 1, 0, 1, 1, 0, 1, 1])
diagonal_9 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
diagonal_8 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


diagonal_data = [
    diagonal_1, diagonal_2, diagonal_3, diagonal_4, diagonal_5,
    diagonal_6, diagonal_7, diagonal_8, diagonal_9, diagonal_10
]

one_line_data = [
    one_line_1, one_line_2, one_line_3, one_line_4, one_line_5,
    one_line_6, one_line_7, one_line_8, one_line_9, one_line_10
]

in_hole_data = [
    in_hole_1, in_hole_2, in_hole_3, in_hole_4, in_hole_5,
    in_hole_6, in_hole_7, in_hole_8, in_hole_9, in_hole_10
]

# --------------------------------------------------
# 2) Build the final 30×3 matrix
# --------------------------------------------------
# Concatenate all poses in the order: diagonal, one_line, in_hole
all_poses = diagonal_data + one_line_data + in_hole_data  # list of 30 arrays

# Create an empty (30,3) integer matrix
final_matrix = np.zeros((30, 3), dtype=int)

# Loop through each of the 30 poses
for i, predictions in enumerate(all_poses):
    # Count how many times each predicted label appears
    diagonal_count  = np.count_nonzero(predictions == 0)
    one_line_count  = np.count_nonzero(predictions == 1)
    in_hole_count   = np.count_nonzero(predictions == 2)
    
    # Fill row i with [diagonal, in_hole, one_line]
    final_matrix[i] = [diagonal_count, one_line_count, in_hole_count]

# --------------------------------------------------
# 3) Visualize the 30×3 matrix as a heatmap
# --------------------------------------------------

# Row labels for your 30 poses
pose_labels = (
    [f"D{i}" for i in range(1, 11)]  +  # diagonal_1..10
    [f"O{i}" for i in range(1, 11)]  +  # one_line_1..10
    [f"I{i}" for i in range(1, 11)]     # in_hole_1..10
)

# Column labels (in the order we used in final_matrix)
col_labels = ["diagonal", "one_line", "in_hole"]

plt.figure(figsize=(6, 10))  # make it tall to fit 30 rows
sns.heatmap(
    final_matrix,
    annot=True,          # show numeric counts in each cell
    fmt="d",             # integer formatting
    cmap="Blues",        # color palette
    xticklabels=col_labels,
    yticklabels=pose_labels
)

plt.title("30×3 Heatmap of Predictions")
plt.xlabel("Predicted Label")
plt.ylabel("Pose")
plt.tight_layout()  # helps with spacing
plt.show()
