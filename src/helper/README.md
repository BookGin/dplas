## Generate Inverted File

First parse `corpus.json` to docs per line, with specific output directory
```
$ ./parseCorpus.py corpus.json ./database/
```

Next, generate inverted files with specific prefix:
(You may need to compile `genInverted.cpp`)
The first command will read `0.txt` and generate `0.vocab`, `0.freq`, `0.misc` files.
```
$ ./lib/genInverted 0
$ ./lib/genInverted 1
```
