from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def add_page_border(doc):
    section = doc.sections[0]
    sectPr = section._sectPr

    pgBorders = OxmlElement("w:pgBorders")
    pgBorders.set(qn("w:offsetFrom"), "page")

    for side in ["top", "left", "bottom", "right"]:
        border = OxmlElement(f"w:{side}")
        border.set(qn("w:val"), "double")
        # border.set(qn("w:sz"), "18")
        border.set(qn("w:sz"), "16")
        # border.set(qn("w:space"), "20")
        border.set(qn("w:space"), "24")
        border.set(qn("w:color"), "000000")
        pgBorders.append(border)

    sectPr.append(pgBorders)

def set_table_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr

    borders = OxmlElement("w:tblBorders")

    for border_name in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        border = OxmlElement(f"w:{border_name}")
        border.set(qn("w:val"), "single")
        # border.set(qn("w:sz"), "12")
        border.set(qn("w:sz"), "20")
        border.set(qn("w:space"), "0")
        border.set(qn("w:color"), "000000")
        borders.append(border)

    tblCellSpacing = OxmlElement("w:tblCellSpacing")
    tblCellSpacing.set(qn("w:w"), "0")
    tblCellSpacing.set(qn("w:type"), "dxa")
    tblPr.append(tblCellSpacing)
    # tblPr.append(borders)
    