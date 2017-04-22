#extract the information from the sitehttps://www.nirfindia.org/uni

import pandas as pd
import matplotlib.pyplot as plt

india_rank = pd.read_html("https://www.nirfindia.org/univ")[0]
india_rank = india_rank.dropna()

columns_to_drop = [2,3,4,5,6,7,8,9,10,11]
india_rank = india_rank.drop(india_rank.columns[columns_to_drop], axis=1)
india_rank = india_rank.rename(columns={'Unnamed: 12': 'City', 'Unnamed: 13': 'State', 'Unnamed: 14': 'Score', 'Unnamed: 15': 'Rank'})

india_rank_state = india_rank.groupby(["State"])["City"].count().reset_index(name="State_count")

india_rank_state.plot(x='State', y='State_count', kind='bar', legend=False)
india_rank_state.to_csv("india_rank_list.csv", sep='\t')
plt.show()
