# KattisPDF

KattisPDF is a Python library and tool that allows to convert problem statements from [Kattis](https://open.kattis.com) to pdf.

## Installation

To install KattisPDF just use `pip`:

```
pip install kattispdf
```

It is necessary to install a LaTeX processor such as [TeX Live](https://tug.org/texlive/) or [MiKTeX](https://miktex.org/). As [PyLaTeX](https://github.com/JelteF/PyLaTeX/tree/master) is used and it needs `pdflatex` or `latexmk` to create the pdf.

### Linux

### Windows
- __Winget__
```
winget install MiKTeX.MiKTeX
```
## How to use
KattisPDF includes a CLI tool `kpdf` to download the problems automaticly, but it can also be used in a python script.
### CLI Tool
```
kpdf problem-id -o path/to/output
```
### Python Script
```python
import kattispdf

problem_id = "alchemy101"
kattispdf.generate_pdf(problem_id)
```

To see an example of the outputed pdf look at [example.pdf](https://github.com/NotTete/kattispdf/blob/main/example.pdf).
