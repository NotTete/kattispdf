from pylatex import *
from pylatex.utils import *
import pylatex.base_classes
from bs4 import BeautifulSoup
import requests
import random
import string
import time
from pathlib import Path
import os

_files_to_remove = []
sample_number = 0

class ThePage(pylatex.base_classes.CommandBase):
    _latex_name="thepage"

    def __init__(self):
        super().__init__()

class NewParagraph(pylatex.base_classes.CommandBase):
    _latex_name="par"

    def __init__(self):
        super().__init__()

class Url(pylatex.base_classes.CommandBase):
    _repr_attributes_mapping = {
        "url": "arguments",
    }

    packages = [Package("hyperref")]

    def __init__(self, url):
        self.url = url
        super().__init__(arguments=[url])

class Verb(pylatex.base_classes.Environment):
    _latex_name="verbatim"
    content_separator=""

class Minipage(pylatex.base_classes.Environment):
    _repr_attributes_mapping = {
        "width": "arguments",
    }

    _latex_name="minipage"

    def __init__(self, width):
        self.width = width
        super().__init__(arguments=[width])

class Hspace(pylatex.base_classes.CommandBase):
    _repr_attributes_mapping = {
        "width": "arguments",
    }

    _latex_name="hspace"

    def __init__(self, width):
        self.width = width
        super().__init__(arguments=[width])

class Href(pylatex.base_classes.CommandBase):
    _repr_attributes_mapping = {
        "marker": "arguments",
        "text": "arguments",
    }
    packages = [Package("hyperref")]

    def __init__(self, marker, text):
        marker = NoEscape(marker.replace("%", r"\%"))
        self.text = text
        self.marker = marker
        super().__init__(arguments=[marker, text])
    

class Hypersetup(pylatex.base_classes.CommandBase):
    _repr_attributes_mapping = {
        "marker": "arguments",
        "text": "arguments",
    }
    
    packages = [Package("hyperref")]

    def __init__(self, hyperindex=True, linktocpage=False, breaklinks=False, 
    colorlinks=False, linkcolor="red", anchorcolor="black", citecolor="green",
    filecolor="green", urlcolor="magenta", frenchlinks=False, bookmarks = True,
    bookmarksopen= False, citebordercolor=[0, 1, 0], filebordercolor=[0, 1, 0],
    linkbordercolor=[1, 0, 0], menubordercolor=[1, 0, 0], urlbordercolor=[0, 1, 1],
    pdfpagemode="", pdfauthor = None, pdftitle = None, pdfstartpage = 1):
        arguments = ""

        #Linking style options
        arguments += f"hyperindex={str(hyperindex).lower()},"
        arguments += f"linktocpage={str(linktocpage).lower()},"
        arguments += f"breaklinks={str(breaklinks).lower()},"
        arguments += f"colorlinks={str(colorlinks).lower()},"
        arguments += f"linkcolor={linkcolor},"
        arguments += f"anchorcolor={anchorcolor},"
        arguments += f"citecolor={citecolor},"
        arguments += f"filecolor={filecolor},"
        arguments += f"urlcolor={urlcolor},"
        arguments += f"frenchlinks={str(frenchlinks).lower()},"

        #PDF options
        arguments += f"bookmarks={str(bookmarks).lower()},"
        arguments += f"bookmarksopen={str(bookmarksopen).lower()},"
        arguments += f"citebordercolor={" ".join(map(str, citebordercolor))},"
        arguments += f"filebordercolor={" ".join(map(str, filebordercolor))},"
        arguments += f"linkbordercolor={" ".join(map(str, linkbordercolor))},"
        arguments += f"menubordercolor={" ".join(map(str, menubordercolor))},"
        arguments += f"urlbordercolor ={" ".join(map(str, urlbordercolor))},"
        arguments += f"pdfpagemode={pdfpagemode},"
        if(pdftitle != None):
            arguments += f"pdftitle={pdftitle},"
        if(pdfauthor != None):
            arguments += f"pdfauthor={pdfauthor},"
        arguments += f"pdfstartpage={pdfstartpage},"

        super().__init__(arguments=[arguments])

class WrappingFigure(pylatex.base_classes.Float):
    _repr_attributes_mapping = {
        "position": "arguments",
        "width": "arguments",
    }

    packages = [Package("wrapfig")]
    _latex_name="wrapfigure"

    def add_image(
        self,
        filename,
        *,
        width=NoEscape(r"0.8\textwidth"),
        placement=NoEscape(r"\centering")
    ):
        if width is not None:
            if self.escape:
                width = escape_latex(width)

            width = "width=" + str(width)

        if placement is not None:
            self.append(placement)

        self.append(
            StandAloneGraphic(image_options=width, filename=fix_filename(filename))
        )

    def __init__(self, position, width):
        width = NoEscape(width)
        super().__init__(arguments=[position, width])

class Fbox(pylatex.base_classes.CommandBase):
    _repr_attributes_mapping = {
        "text": "arguments",
    }

    def __init__(self, text):
        self.text = text
        super().__init__(arguments=[text])

class Parbox(pylatex.base_classes.CommandBase):
    _repr_attributes_mapping = {
        "width": "arguments",
        "text": "arguments",
    }

    def __init__(self, width, text):
        super().__init__(arguments=[width, text])  

class Tcolorbox(pylatex.base_classes.Environment):
    _repr_attributes_mapping = {
        "text": "arguments",
        "options": "options"
    }
    packages = [Package("xcolor", options=["usenames", "dvipsnames"]), Package("tcolorbox")]

    def __init__(self, text, options=None):
        if(options != None):
            options = NoEscape(options)
        super().__init__(arguments=[text], options=options)   

def strikethrough(text):
    """Needs soul package"""
    return NoEscape(r"\st{" + text + "}")


class Empty(pylatex.base_classes.Environment):
    _latex_name="@empty"

class _KattisMetadata:
    def __init__(self, memory_limit, time_limit, url, author, license):
        self.memory_limit = memory_limit
        self.time_limit = time_limit
        self.url = url
        self.author = author
        self.license = license

def _random_image_path() -> str:
    random_file = ""
    
    for i in range(20):
        random_file += random.choice(string.ascii_letters)
    random_file += ".png"
    return random_file

def _load_image(url, path) -> str:
    if(len(url) <= 8 or url[:8] != "https://"):
        url = _kattis_url() + url

    path = Path(path, _random_image_path())
    request = requests.get(url, stream=True)
    request.raise_for_status()
    with open(path, 'wb') as file:
        for chunk in request.iter_content(1024):
            file.write(chunk)

    _files_to_remove.append(path)
    return path

def _kattis_url(problem: str = None) -> str:
    if(problem == None):
        return "https://open.kattis.com"
    return f"https://open.kattis.com/problems/{problem}"


def _get_html(problem: str) -> BeautifulSoup:
    url = _kattis_url(problem)
    request = requests.get(url, params={"tab": "metadata"})
    request.raise_for_status()
    parser = BeautifulSoup(request.text, "html.parser")
    return parser

def _get_metadata(problem: str, parser: BeautifulSoup) -> _KattisMetadata:
    cards = parser.find_all("div", {"class": "card"})
    
    time_limit = cards[0].find("span", { "class": "text-lg" }).get_text()
    time_limit = time_limit.replace("second", "sec")
    memory_limit = cards[1].find("span", { "class": "text-lg" }).get_text()

    source_tags = cards[5].find_all("span", { "class": "gap-3" })

    source = []
    for tag in source_tags:
        href = tag.find("a")
        text = tag.get_text()

        if(href == None):
            source.append(text)
            continue

        url = href.get("href")
        img = href.find("img")

        if(img == None):
            url = _kattis_url() + url
        else:
            text = img.get("alt")

        source.append(Href(url, text))
    
    license = source[-1]
    author = source[:-1]
    
    url = Url(_kattis_url(problem))

    metadata = _KattisMetadata(memory_limit, time_limit, url, author, license)
    return metadata

def _generate_header(problem: str, document: Document, parser: BeautifulSoup):
    metadata = _get_metadata(problem, parser)
    style = "fancy"
    header = PageStyle(style, header_thickness=1)

    with header.create(Head("L")):


        header.append(bold("Site: "))
        header.append(metadata.url)
        header.append(LineBreak())
        if(len(metadata.author) >= 1):
            header.append(bold("License: "))
            header.append(metadata.license)
            header.append(LineBreak())
            header.append(bold("Author: "))
            length = 0
            for author in metadata.author[:-1]:
                header.append(author)
                header.append(", ")
            header.append(metadata.author[-1])

        else: 
            header.append(bold("Source: "))
            header.append(metadata.license)
    
    with header.create(Foot("R")):
        header.append(ThePage())

    document.preamble.append(header)
    document.change_document_style(style)
    return metadata

def _generate_minipage(document, element, path):
    width = element.get("style")
    start_index = width.find("width:") + 6
    end_index = width[start_index:].find(" ")
    if(end_index == -1):
        width = NoEscape(width[start_index:])

    else:
        end_index += start_index
        width = NoEscape(width[start_index:end_index])

    minipage = Minipage(width)
    _process_content(minipage, element, path)
    document.append(minipage)
    document.append(NoEscape(r"\vskip0pt"))


def _generate_pre(document, element):
    text = NoEscape(element.get_text())
    enviroment = Verb()
    enviroment.append(text)
    document.append(enviroment)

def _process_text(tag):
    tag_text = tag.get_text()

    if(tag == None):
        return ""
    if(tag.name == "span" and "tex2jax_process" in tag.get("class")):
        return NoEscape(tag_text)
    elif(tag.name == "em"):
        return italic(tag_text)
    elif(tag.name == "b"):
        return bold(NoEscape(tag_text))
    elif(tag.name == "tt"):
        delimiter = "|"
        if tag_text.find("|") != -1:
            delimiter="^"
        if delimiter == "^" and tag_text.find("^") != -1:
            delimiter="<"
        return verbatim(tag_text.replace("\n", " "), delimiter=delimiter)
    elif(tag.name == "a"):
        return _get_href(tag)
    elif(tag.name == "del"):
        return strikethrough(tag_text)
    else:
        return tag_text.replace("\n", " ")

def _generate_paragraph(document, element, path):
    if(element.name == "p"):
        document.append(NewParagraph())
    text = ""
    for tag in element:
        if(tag != None and tag.name == "img"):
            document.append(NoEscape(text))
            _generate_image(document, tag, path)
            text = ""
        else:
            text += _process_text(tag)
    document.append(NoEscape(text))

def _generate_math(document, element):
    document.append(NoEscape(element.get_text()))

def _generate_subsection(document, element):
    text = element.get_text().replace("\n","")
    document.append(Subsection(text, numbering=False))

def _get_href(element):
    url = element.get("href")
    if(len(url) <= 8 or url[:8] != "https://"):
        url = _kattis_url() + url

    text = ""
    for tag in element:
        text += _process_text(tag)

    return Href(url, text).dumps_as_content()

def _generate_figure(document, element, path):
    image_tag = element.find("img")
    if(image_tag != None):
        image_url = image_tag.get("src")
    else:
        _process_content(document,element,path)
        return
    caption_tag = element.find("div", { "class": "caption" })

    width = image_tag.get("alt")
    start_index = width.find("width=") + 6
    end_index = width[start_index:].find(" ")
    if(end_index == -1):
        end_index = width[start_index:].find("]")
    else:
        end_index += start_index

    width = NoEscape(width[start_index:end_index])
    image_path = NoEscape(_load_image(image_url, path).name)

    if caption_tag != None:
        text = ""
        for tag in caption_tag:
            text += _process_text(tag)
        text = NoEscape(text)

    with document.create(Figure(position='h')) as fig:
        fig.add_image(image_path, width=width)
        fig.add_caption(text)

def _generate_itemize(document, element, path, itemize=True):
    enviroment = Itemize()
    if(not itemize):
        enviroment = Enumerate()

    with document.create(enviroment) as itemize:
        for tag in filter(lambda x: x.name == "li", element):
            container = []
            for element in filter(lambda x: x != None, tag):
                _process_content(container, element, path)
            itemize.add_item(dumps_list(container, escape=False, token=" "))



def _generate_ilustration(document, element, path):
    image_tag = element.find("img")
    image_url = image_tag.get("src")
    image_path = NoEscape(_load_image(image_url, path).name)

    description_tag = element.find("div", {"class": "description"})
    text = r"\footnotesize "
    for tag in description_tag:
        text += _process_text(tag)
    text = NoEscape(text)

    width = element.get("style")
    start_index = width.find("width:") + 6
    end_index = width[start_index:].find("%") + start_index
    width = float(width[start_index:end_index]) / 100
    width = NoEscape(f"{width}\\textwidth")

    with document.create(WrappingFigure(position='r', width=width)) as fig:
        fig.add_image(image_path, width=width)
        fig.add_caption(text)

def _generate_image(document, tag, path):
    url = tag.get("src")
    path = NoEscape(_load_image(url, path).name)

    width = tag.get("alt")
    start_index = width.find("width=") + 6
    end_index = width[start_index:].find(" ")
    if(end_index == -1):
        end_index = width[start_index:].find("]")
    else:
        end_index += start_index

    width = NoEscape("width=" + width[start_index:end_index])
    graphic = StandAloneGraphic(path, width)
    document.append(graphic)
    graphic

def _generate_quote(document, element):
        center = Center()
        text = italic(element.get_text())
        center.append(Fbox(text))
        document.append(center) 

def _generate_tabular(document, element):
    rows = []
    for row in filter(lambda x: x.name != None, element):
        current_row =[]
        for column in filter(lambda x: x.name != None, row):
            text = ""

            column_p = column.find("p")
            if(column_p == None):
                column_p = column

            for tag in column_p:
                text += _process_text(tag)

            if(column.name == "th"):
                current_row.append(bold(text))
            else:
                current_row.append(text)
        rows.append(current_row)
    td = element.find("td")
    if(td == None):
        td = element.find("th")
    style = td.get("style")

    has_border_top = style.find("border-top") != -1
    has_border_sides = style.find("border-right") != -1

    separator = " "
    if(has_border_sides):
        separator = "|"

    start_index = style.find("text-align:") + len("text-align:")
    end_index = style[start_index:].find(";")

    if(end_index == -1):
        style = style[start_index:].strip()
    else:
        style = style[start_index:end_index + start_index].strip()

    letter = "l"
    if(style == "center"):
        letter = "c"
    elif(style == "right"):
        letter = "r"

    if(len(rows) > 0):
        length = len(rows[0])
        spec = (separator + letter) * length + separator
        tabular = Tabular(spec)
        if(has_border_top):
            tabular.add_hline()
        for row in rows:
            tabular.add_row(row, escape=False)
            if(has_border_top):
                tabular.add_hline()

        document.append(NewParagraph())
        document.append(tabular)
def _process_content(document: Document, content: BeautifulSoup, path):
    text = ""
    for tag in content:
        if type(tag) == str:
            text += escape_latex(tag.replace("\n", " "))
        elif tag.name == "p":
            document.append(NoEscape(text))
            text = ""
            _generate_paragraph(document, tag, path)            
        elif tag.name == "span" and "tex2jax_process" in tag.get("class"):
            document.append(NoEscape(text))
            text = ""
            _generate_math(document, tag)
        elif tag.name == "h2":
            document.append(NoEscape(text))
            text = ""
            _generate_subsection(document, tag)
        elif tag.name == "pre":
            document.append(NoEscape(text))
            text = ""
            _generate_pre(document, tag)
        elif tag.name == "div" and "figure" in tag.get("class"):
            document.append(NoEscape(text))
            text = ""
            _generate_figure(document, tag, path)
        elif tag.name == "div" and "illustration" in tag.get("class"):
            document.append(NoEscape(text))
            text = ""
            _generate_ilustration(document, tag, path)
        elif tag.name == "img":
            document.append(NoEscape(text))
            text = ""
            _generate_image(document, tag, path)
        elif tag.name == "center":
            document.append(NoEscape(text))
            text = ""
            center = Center()
            _process_content(center, tag, path)
            document.append(center)
        elif tag.name == "blockquote":
            document.append(NoEscape(text))
            text = ""
            _generate_quote(document, tag)
        elif tag.name == "table" and "tabular" in tag.get("class"):
            document.append(NoEscape(text))
            text = ""
            _generate_tabular(document, tag)
        elif tag.name == "ul" or tag.name == "ol":
            document.append(NoEscape(text))
            text = ""
            _generate_itemize(document, tag, path, tag.name == "ul")
        elif tag.name == "table" and "sample" in tag.get("class"):
            document.append(NoEscape(text))
            text = ""
            _generate_sample(document, tag, path)        
        elif tag.name == "div" and "minipage" in tag.get("class"):
            document.append(NoEscape(text))
            text = ""
            _generate_minipage(document, tag, path)  
        elif tag.name == "div" and "sampleinteractionwrite" in tag.get("class"):
            document.append(NoEscape(text))
            text = ""
            _generate_interactive_write(document, tag, path)  
        elif tag.name == "div" and "sampleinteractionread" in tag.get("class"):
            document.append(NoEscape(text))
            text = ""
            _generate_interactive_read(document, tag, path)  
        else:
            text += _process_text(tag)
    document.append(NoEscape(text))

def _generate_sample(document, element, path):
    global sample_number
    if(sample_number == 0):
        document.append(Subsection(f"Sample", numbering=False))

    sample_number += 1
    document.append(Subsubsection(f"Sample {sample_number}", numbering=False))

    elements = []
    for td in element.find_all("td"):
        content = []
        _process_content(content, td, path)
        elements.append(content)

    for element in elements:
        document.append(Tcolorbox(dumps_list(element, escape=False, token=" ") + NoEscape("\n")))

def _generate_interactive_write(document, element, path):
    content = []
    _process_content(content, element, path)
    document.append(Tcolorbox(dumps_list(content, escape=False, token=" ") + NoEscape("\n"), """colback=lime!10, grow to left by=-10mm"""))

def _generate_interactive_read(document, element, path):
    content = []
    _process_content(content, element, path)
    document.append(Tcolorbox(dumps_list(content, escape=False, token=" ") + NoEscape("\n"), """colback=yellow!10, grow to right by=-10mm"""))

def _generate_content(problem: str, document: Document, parser: BeautifulSoup, metadata, path):
    content = parser.find("div", { "book-page-fixed_width"})
    title = escape_latex(content.find("h1").get_text())
    title += r" \mdseries\large" + f"{metadata.memory_limit}, {metadata.time_limit}"
    document.append(Section(NoEscape(title), numbering=False))

    body = content.find("div", { "class": "problembody" })
    _process_content(document, body, path)

    foot = content.find("div", { "class": "footnotes" })

    if(foot != None):
        _process_content(document, foot, path)


def _get_document() -> Document:
    # Geometry setup
    geometry_settings = {
        "paperwidth": "21cm", 
        "paperheight": "29.7cm",
        "textwidth": "17cm",
        "headsep" : "1.5cm",
        "footskip": "3cm" 
    }

    document = Document(geometry_options=geometry_settings)

    # Extra packages setup
    packages = [
        ("wrapfig", None),
        ("amssymb", None),
        ("amsmath", None),
        ("soul", None),
        ("parskip", { "skip": "10pt", "indent": "0pt" }),
        ("caption", { "labelformat": "empty" }),
    ]


    for package, options in packages:
        document.preamble.append(Package(package, options=options))

    # Hypereference setup
    hyperref_config = Hypersetup(colorlinks=True, urlcolor="black")
    document.preamble.append(hyperref_config)



    # Wrapfigure sep
    document.preamble.append(NoEscape(r"\setlength{\intextsep}{0pt}"))

    return document

def generate_pdf(problem: str, path = None):
    global sample_number
    try:
        if(path == None):
            path = Path(problem)
        else:
            path = path.with_suffix("")

        sample_number = 0    
        parser = _get_html(problem)
        document = _get_document()
        metadata = _generate_header(problem, document, parser)
        _generate_content(problem, document, parser, metadata, path.parent)
        
        document.generate_pdf(clean_tex=True, filepath=path)
    
    except KeyboardInterrupt:
        extensions = [".aux", ".log", ".out", ".fls", ".fdb_latexmk", ".tex", ".pdf"]
        for ext in extensions:
            try:
                os.remove(path.with_suffix(ext))
            except (FileNotFoundError):
                pass
    finally:
        for file in _files_to_remove:
            file.unlink()
        _files_to_remove.clear()