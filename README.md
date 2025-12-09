# arXiv to EPUB Converter

## Notice

This is a fork version.

- remove docker, using conda to run the code. 
- support one file only.

## Usage

```python
python arxiv2epub.py xxxx.xxxxx
```
xxxx.xxxxx comes from https://arxiv.org/abs/xxxx.xxxxx

```python
python arxiv2epub.py xxxx.xxxxx -f xx -o xx
```

- -f or --filename: the file name of saved epub
- -o or --output: the output folder of saved epub

## Installation

pandoc
```bash
brew install pandoc
```

conda

```bash
conda create -n arxiv2epub python=3.10 -y
conda activate arxiv2epub
pip install -r requirements.txt
```

## Features

- Converts arXiv papers to EPUB format
- Optionally downloads PDFs of arXiv papers
- Watches for changes in the input file and processes new URLs automatically
- Downloads and includes images from the arXiv HTML version
- Handles LaTeX math rendering in the generated EPUBs
- Skips already processed papers to avoid duplication

