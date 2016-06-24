# NTU IR Final Project

Please check the Issues to follow the latest progress.

# usage of Jieba
`pip3 install jieba`
`jieba.set_dictionary('dict.txt.big')`

# spec

[spec](https://hackmd.io/CwIwzMDGCMBsIFoBMBWAhkhxZtgksAnJAoWmiMIQCYCm10AHCEA=)

# datas

[data](https://drive.google.com/folderview?id=0B97NsvGFvI6Nc3hNQ29FbkZWOEk&usp=sharing)


# Liberty Times News
- Spec:
**talk是社論類別，但裡面也有聊健康的....**

```c++
category = "politics" // "politics" ,  "talk" ,  "society"
time = "20160501" // "YYYYMMDD", 20150601 - 20160531
title = ["TITLE1", "TITLE2"]
content = ["content1", "content2"]
link = "URL"
```

- Data:
```sh
wget 'https://www.csie.ntu.edu.tw/~b03902078/ir/talk.json'
wget 'https://www.csie.ntu.edu.tw/~b03902078/ir/society.json'
wget 'https://www.csie.ntu.edu.tw/~b03902078/ir/politics.json'
```
