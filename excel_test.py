import pandas as pd

df = pd.read_excel('du_lieu/data.xlsx')
customer_code = df.iloc[0:, 0].values.tolist()