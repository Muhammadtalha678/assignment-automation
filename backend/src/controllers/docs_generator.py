import json
import os
import shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from src.controllers.generate_image import generate_image

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Utility to set internal cell padding."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def generate_assignment_docx(json_data_str: str, output_path: str = "Assignment.docx", logo_path: str = None):
    # 1. Parse JSON Input
    if isinstance(json_data_str, str):
        data = json.loads(json_data_str)
    else:
        data = json_data_str

    # assignment_info = data.get("assignment", {})
    questions = data.get("questions", [])

    # 2. Setup Images Directory at Project Root
    image_dir = os.path.join(os.getcwd(), "quest_images")
    os.makedirs(image_dir, exist_ok=True)

    # -------------------------------------------------------------------------
    # PHASE 1: PRE-GENERATE ALL IMAGES
    # -------------------------------------------------------------------------
    print("--> Phase 1: Generating images for all questions...")
    image_map = {}  # { q_index: file_path }

    for idx, q in enumerate(questions, start=1):
        diagram_desc = q.get("diagram_description")
        if diagram_desc:
            temp_file_path = os.path.join(image_dir, f"temp_{idx}.png")
            print(f"Generating image {idx}/{len(questions)}: temp_{idx}.png")
            
            success = generate_image(diagram_desc, temp_file_path)
            if success:
                image_map[idx] = temp_file_path
            else:
                image_map[idx] = None
    print(image_map)
    # 2. Initialize Document
    doc = Document()

    # Set Document Page Margins (Normal 1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # -------------------------------------------------------------
    # HEADER / LOGO SECTION
    # -------------------------------------------------------------
    if logo_path and os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(1.8))
        p_logo.paragraph_format.space_after = Pt(12)

    # Main Header: Assignment # 01 (Calibri)
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run(f"Assignment # 0{data.get('assignment_no', 1)}")
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x00, 0x33, 0x66) # Deep Navy
    p_title.paragraph_format.space_after = Pt(18)

    # -------------------------------------------------------------
    # STUDENT DETAILS TABLE
    # -------------------------------------------------------------
    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    details = [
        ("Student Name:", str(data.get("student_name", ""))),
        ("Registration ID:", str(data.get("registration_id", ""))),
        ("Course Code:", str(data.get("course_code", ""))),
        ("Semester:", str(data.get("semester", "")))
    ]

    for i, (label, val) in enumerate(details):
        row = table.rows[i]
        
        # Label Cell
        cell_lbl = row.cells[0]
        cell_lbl.width = Inches(2.2)
        p_lbl = cell_lbl.paragraphs[0]
        p_lbl.paragraph_format.space_after = Pt(4)
        run_lbl = p_lbl.add_run(label)
        run_lbl.font.name = 'Calibri'
        run_lbl.font.size = Pt(11)
        run_lbl.font.bold = True

        # Value Cell
        cell_val = row.cells[1]
        cell_val.width = Inches(4.3)
        p_val = cell_val.paragraphs[0]
        p_val.paragraph_format.space_after = Pt(4)
        run_val = p_val.add_run(val)
        run_val.font.name = 'Calibri'
        run_val.font.size = Pt(11)

        set_cell_margins(cell_lbl, top=80, bottom=80, left=100, right=100)
        set_cell_margins(cell_val, top=80, bottom=80, left=100, right=100)

    # Add light border/shading to table cells
    for row in table.rows:
        for cell in row.cells:
            shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F4F6F9"/>')
            cell._tc.get_or_add_tcPr().append(shading)

    doc.add_paragraph().paragraph_format.space_after = Pt(18)

    # -------------------------------------------------------------
    # QUESTIONS & ANSWERS LOOP
    # -------------------------------------------------------------
    for q_idx, q in enumerate(questions, start=1):

        # --- Question Heading (Times New Roman, Size 16, Bold) ---
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(18)
        p_q.paragraph_format.space_after = Pt(8)
        p_q.paragraph_format.keep_with_next = True
        
        run_q = p_q.add_run(f"Q.{q.get('question_number', q_idx)}: {q.get('question_text', '')}")
        run_q.font.name = 'Times New Roman'
        run_q.font.size = Pt(16)
        run_q.font.bold = True
        run_q.font.color.rgb = RGBColor(0x11, 0x11, 0x11)

        # --- Answer Introduction ---
        if q.get("introduction"):
            p_intro = doc.add_paragraph()
            p_intro.paragraph_format.space_after = Pt(10)
            p_intro.paragraph_format.line_spacing = 1.15
            run_intro = p_intro.add_run(q.get("introduction"))
            run_intro.font.name = 'Times New Roman'
            run_intro.font.size = Pt(12)

        # --- Sections / Sub-headings (Times New Roman, Size 14, Bold) ---
        for sec in q.get("sections", []):
            p_h = doc.add_paragraph()
            p_h.paragraph_format.space_before = Pt(12)
            p_h.paragraph_format.space_after = Pt(4)
            p_h.paragraph_format.keep_with_next = True

            run_h = p_h.add_run(sec.get("heading", ""))
            run_h.font.name = 'Times New Roman'
            run_h.font.size = Pt(14)
            run_h.font.bold = True
            run_h.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

            p_body = doc.add_paragraph()
            p_body.paragraph_format.space_after = Pt(10)
            p_body.paragraph_format.line_spacing = 1.15
            run_body = p_body.add_run(sec.get("explanation", ""))
            run_body.font.name = 'Times New Roman'
            run_body.font.size = Pt(12)

        # --- Diagram Description Box ---
        # Add Pre-generated Image from Phase 1
        img_path = image_map.get(idx)
        # if q.get("diagram_description"):
        #     diag_table = doc.add_table(rows=1, cols=1)
        #     diag_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        #     diag_cell = diag_table.rows[0].cells[0]
        #     diag_cell.width = Inches(6.5)

        #     # Box styling (Light cyan background with border)
        #     shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F0F7FF"/>')
        #     diag_cell._tc.get_or_add_tcPr().append(shd)
        #     set_cell_margins(diag_cell, top=140, bottom=140, left=180, right=180)

        #     p_diag = diag_cell.paragraphs[0]
        #     p_diag.paragraph_format.space_after = Pt(0)
            
        #     run_diag_lbl = p_diag.add_run("Diagram / Flowchart Illustration:\n")
        #     run_diag_lbl.font.name = 'Times New Roman'
        #     run_diag_lbl.font.size = Pt(11)
        #     run_diag_lbl.font.bold = True
        #     run_diag_lbl.font.italic = True
        #     run_diag_lbl.font.color.rgb = RGBColor(0x00, 0x55, 0x99)

        #     run_diag_txt = p_diag.add_run(q.get("diagram_description"))
        #     run_diag_txt.font.name = 'Times New Roman'
        #     run_diag_txt.font.size = Pt(11)
        #     run_diag_txt.font.italic = True

        #     doc.add_paragraph().paragraph_format.space_after = Pt(10)
        if img_path and os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(10)
            
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=Inches(4.8))

            # # Caption
            # p_cap = doc.add_paragraph()
            # p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            # run_cap = p_cap.add_run(f"Figure {idx}: {q.get('diagram_description')}")
            # run_cap.font.name = 'Times New Roman'
            # run_cap.font.size = Pt(10)
            # run_cap.font.italic = True
            # run_cap.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        # --- Conclusion Section (Times New Roman, Size 14, Bold) ---
        if q.get("conclusion"):
            p_conc_h = doc.add_paragraph()
            p_conc_h.paragraph_format.space_before = Pt(12)
            p_conc_h.paragraph_format.space_after = Pt(4)
            p_conc_h.paragraph_format.keep_with_next = True

            run_conc_h = p_conc_h.add_run("Conclusion")
            run_conc_h.font.name = 'Times New Roman'
            run_conc_h.font.size = Pt(14)
            run_conc_h.font.bold = True

            p_conc_body = doc.add_paragraph()
            p_conc_body.paragraph_format.space_after = Pt(16)
            p_conc_body.paragraph_format.line_spacing = 1.15
            run_conc_body = p_conc_body.add_run(q.get("conclusion"))
            run_conc_body.font.name = 'Times New Roman'
            run_conc_body.font.size = Pt(12)

    # Save Word Document
    doc.save(output_path)
    print("--> Phase 3: Cleaning up temporary images...")
    try:
        shutil.rmtree(image_dir)  # Puray folder ko uski files samet delete kar dega
        print("Cleanup complete. 'quest_images' folder removed.")
    except Exception as e:
        print(f"Warning: Could not clear image directory: {e}")
    return output_path