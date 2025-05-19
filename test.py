import pandas as pd

import matplotlib.pyplot as plt

data = pd.read_csv('Pokemon.csv')
data['HP_Attack'] = data['HP'] + data['Attack']
top_10 = data.nlargest(10, 'HP_Attack')
top_10feu = data[(data['Type 1'] == 'Fire') | (data['Type 2'] == 'Fire')].nlargest(10, 'HP_Attack')
top_10eau = data[(data['Type 1'] == 'Water') | (data['Type 2'] == 'Water')].nlargest(10, 'HP_Attack')
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

axes[0].bar(top_10['Name'], top_10['HP_Attack'], color='blue')
axes[0].set_xlabel('Name')
axes[0].set_ylabel('HP + Attack')
axes[0].tick_params(axis='x', rotation=45)

axes[1].bar(top_10feu['Name'], top_10feu['HP_Attack'], color='red')
axes[1].bar(top_10eau['Name'], top_10eau['HP_Attack'], color='blue', alpha=0.5)
axes[1].set_xlabel('Name')
axes[1].set_ylabel('HP + Attack')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()