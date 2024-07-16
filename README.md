# KattisPDF

KattisPDF is a Python library and tool that allows to convert problem statements from [Kattis](https://open.kattis.com) to pdf.

## Installation

To install KattisPDF just use `pip`:

```
pip install kattispdf
```

It is necessary to install a $\LaTeX$ processor such as [TeX Live](https://tug.org/texlive/) or [MiKTeX](https://miktex.org/). As `pdflatex` or `latexmk` are used to create the pdf.

### Linux

### Windows

## How to use
KattisPDF includes a CLI tool to download the problems automaticly, but it can also be used in a python script.
### CLI Tool
```
kpdf problem-id -o directory/path
```
### Python script
```python
import kattispdf

problem_id = "hello"
kattispdf.generate_pdf(problem_id)
```
