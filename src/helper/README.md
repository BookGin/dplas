## Generate Inverted File

First parse `corpus.json` to docs per line, with specific output directory
```
$ ./parseCorpus.py corpus.json ./database/
```

Next, generate inverted files with specific prefix:
(You may need to compile `genInverted.cpp`)
The first command will read `0.txt` and generate `0.vocab`, `0.freq`, `0.misc` files.

```
$ ./lib/genInverted database/0
```

## How to Use issuemodel.py
```python
from helper import issuemodel

# The directory should contain 0.vocab, 0.freq, ... N.vocab..
issuemodel.load("./model/database/")

# @param ("doc raw text", label num)
# @return (list). Note that the order is according to the basis of LABEL_NUM model.
vec = issuemodel.measure("每天都要吃小黃瓜", 7)
```
## How to Use knn.py
```python
from helper import knn

# @param vectors (numpy sparse matrix)
knn.nearestNeighbors(vectors)

# @param (vector, how many k nearest vector you want)
# @return (indices list). You can use these indices (sorted by distance) to access vectors[i]
>>> knn.kneighbors(yourvector, k):
[1, 3, 5, 7, 2] 
``
