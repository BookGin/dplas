## How to Use issuemodel.py
```python
from model import issuemodel

# This is like a function object 
# the database should contain 0.vocab, 0.freq, ... N.vocab..
measure = issuemodel.load("./model/database/")

# @param ("doc raw text", label num)
# @return (list). Note that the order is according to the basis of LABEL_NUM model.
vec = measure("宋楚瑜的老媽蔡英文說每天都要吃小黃瓜", 7)
```

## Generate Inverted File

First parse `corpus.json` to docs per line, with specific topic number
```
$ ./lib/parseJson.py corpus.json 0 > 0.txt
$ ./lib/parseJson.py corpus.json 1 > 1.txt
$ ./lib/parseJson.py corpus.json 2 > 2.txt
......
```

Segment words with `jieba`:
```
$ ./lib/segment.py 0.txt > 0seg.txt
$ ./lib/segment.py 1.txt > 1seg.txt
......
```

Next, generate inverted files with specific prefix:
(You may need to compile `genInverted.cpp`)
The first command will generate `0.vocab`, `0.freq`, `0.misc` files.
```
$ ./lib/genInverted 0seg.txt 0
$ ./lib/genInverted 1seg.txt 1
```
