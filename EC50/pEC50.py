#pIC50 [log M] = -log10(IC50 [M]) = -log10(IC50 [μM]) + 6 (micromolar)
#pIC50 [log M] = -log10(IC50 [M]) = -log10(IC50 [μM]) + 9  (nanomolar)
#sample file given active_compounds.txt

import pandas as pd
import numpy as np

active_compounds = pd.read_csv('active_compounds.txt')

concentration = active_compounds.EC50
data = []

for line in concentration:
    logIC50_n = np.log10(line)
    b = 6 - logIC50_n
    b = '{0:.4f}'.format(b)
    data.append(b)


newDF = pd.DataFrame({'pIC50': data})
active_compounds = newDF

active_compounds.to_csv('pIC50.txt',index=False)

print(active_compounds)
