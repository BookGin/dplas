

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
