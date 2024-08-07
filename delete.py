import pandas as pd
import json

with open("fmp_gainers.json", "r") as f:
    gainers_data = json.load(f)
gainers_df = pd.DataFrame(gainers_data)
gainers_filtered = gainers_df[(gainers_df['price'] > 1) & (gainers_df['price'] < 20)]
gainers_filtered = gainers_filtered.reset_index(drop=True)
gainers_filtered = gainers_filtered.rename(columns={'index': 'id'})
gainers_filtered = gainers_filtered.head(10)
gainers_filtered = gainers_filtered
print(gainers_filtered)