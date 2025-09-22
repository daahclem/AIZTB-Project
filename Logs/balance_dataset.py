import pandas as pd

# Load the full (imbalanced) dataset
full_df = pd.read_csv('full_dataset.csv')

# Identify the target class column (assuming 'behavior_context' is the label)
label_col = 'behavior_context'

# Find the minimum class count for balancing
min_count = full_df[label_col].value_counts().min()

# Sample min_count from each class to balance
df_balanced = (
    full_df.groupby(label_col, group_keys=False)
    .apply(lambda x: x.sample(min_count, random_state=42))
    .reset_index(drop=True)
)

# Shuffle the result
balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to dataset.csv
balanced.to_csv('dataset.csv', index=False)

print(f"Balanced dataset saved to dataset.csv with {len(balanced)} rows.")
