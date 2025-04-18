# pypi search

See <https://github.com/searxng/searxng/issues/4093>

```sh
pypisearch download
```

```text
Status: 200
Content-type: text/html
```

```sh
pypisearch search fasttext
```

```text
Error fetching https://pypi.org/pypi/fasttextpy/json: 404, message='Not Found', url='https://pypi.org/pypi/fasttextpy/json'
fasttext
   summary: fasttext Python bindings
   version: 0.9.3
fasttext-github
   summary: fastText Python bindings
   version: 0.8.22
fasttext-langdetect
   summary: 80x faster and 95% accurate language identification with Fasttext
   version: 1.0.5
fasttext-langdetect-wheel
   summary: 80x faster and 95% accurate language identification with Fasttext
   version: 1.0.5
fasttext-language-detection
   summary: Language detection wrapper with fasttext
   version: 0.4
fasttext-numpy2
   summary: fasttext Python bindings, fixed numpy 2 compatibiliy
   version: 0.10.4
fasttext-numpy2-wheel
   summary: fasttext Python bindings
   version: 0.9.2
fasttext-parallel
   summary: FastText Multithreading Inference
   version: 0.1.4
fasttext-predict
   summary: fasttext with wheels and no external dependency, but only the predict method (<1MB)
   version: 0.9.2.4
fasttext-reducer
   summary: Lightweight package that allows for downloading fasttext models to any location and reducing their dimensions through a one-liner.
   version: 0.1.3
fasttext-server
   summary: Deploy fasttext models
   version: 0.1.10
fasttext-serving
   summary: fasttext-serving gRPC client
   version: 0.2.0
fasttext-serving-protos
   summary: FastText Serving Protocol Bufers Python implementation
   version: 0.0.13
fasttext-serving-server
   summary: fastText model serving API server
   version: 0.6.2
fasttext-wheel
   summary: fasttext Python bindings
   version: 0.9.2
fasttext-win
   summary: A Python interface for Facebook fastText library
   version: 0.8.3
FastText_Shop
   summary: FastText_Shop是一个基于FastText和结巴分词的短文本分类工具，特点是高效易用，同时支持中文和英文语料。基本使用方法、灵感来自TextGrocery,并且和TextGrocery基本相同。
   version: 0.0.8
fasttextannotator
   summary: A python package that allows the user to annotate corpuses for FastText
   version: 1.0.0
fasttextaug
   summary: None
   version: 0.1.1
fasttextmirror
   summary: fastText Python bindings
   version: 0.8.22
FastTextProcessor
   summary: A tool for processing text data in various formats
   version: 2.0.0
fasttextpy
FastTextRank
   summary: Extract abstracts and keywords from Chinese text
   version: 1.4
fasttextsearch
   summary: Some fast-ish algorithms for batch text search in moderate-sized collections, intended for data cleanup.
   version: 0.12
--------------------
cputime= {'load': 0.00237930599999997, 'query': 0.064144274, 'total': 0.06652357999999997}
runtime= {'load': 0.0023805570090189576, 'query': 0.14010328706353903, 'total': 0.14248384407255799}
memory usage for dataset = 794624 bytes
```
