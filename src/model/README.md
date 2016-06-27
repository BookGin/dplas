## How to Use issuemodel.py
```python
from model import issuemodel

# The directory should contain 0.vocab, 0.freq, ... N.vocab..
issuemodel.load("./model/database/")

# @param ("doc raw text", label num)
# @return (list). Note that the order is according to the basis of LABEL_NUM model.
vec = issuemodel.measure("宋楚瑜的老媽蔡英文說每天都要吃小黃瓜", 7)
```
## How to Use knn.py
```python
from model import knn

# many vector (sparse matrix)
knn.nearestNeighbors(vectors)

# @param (vector, how many k nearest vector you want)
# @return (indices list). You can use these indices (sorted by distance) to access vectors[i]
knn.kneighbors(yourvector, k):
```
