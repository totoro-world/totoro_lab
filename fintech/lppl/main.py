import lppl
from matplotlib import pyplot as plt
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
sns.set_style('white')

limits = ([0, 7], [0, 5], [0, 1000], [-2,2], [-3,3], [0,4], [0, 7])
#limits = ([0, 3], [.1, 1], [520, 850], [1, 2], [-1,1], [.1,2], [-1, 1])
#limits = ([8.4, 8.8], [-1, -0.1], [350, 400], [.1,.9], [-1,1], [12,18], [0, 2*np.pi])

x = lppl.Population(limits, 20, 0.3, 1.5, .05, 4)
for i in range (5):
    x.Fitness()
    x.Eliminate()
    x.Mate()
    x.Mutate()

x.Fitness()
values = x.BestSolutions(3)
for x in values:
    print(x.PrintIndividual())

data = pd.DataFrame({'Date':values[0].getDataSeries()[0],'Index':values[0].getDataSeries()[1],'Fit1':values[0].getExpData(),'Fit2':values[1].getExpData(),'Fit3':values[2].getExpData()})
data = data.set_index('Date')
data.plot(figsize=(14,8))
plt.show()

