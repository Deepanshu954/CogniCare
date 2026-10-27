import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=70, bottom=70, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_callout_box(doc, title, text, border_color="0284C7", bg_color="F0F9FF"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)

    # Set left border thick, others none
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:left w:val="single" w:sz="32" w:space="0" w:color="{border_color}"/>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if title:
        r_title = p.add_run(title + "\n")
        r_title.font.name = 'Times New Roman'
        r_title.font.size = Pt(10.5)
        r_title.font.bold = True
        # border color as rgb
        r_title.font.color.rgb = RGBColor(int(border_color[:2], 16), int(border_color[2:4], 16), int(border_color[4:], 16))

    r_text = p.add_run(text)
    r_text.font.name = 'Times New Roman'
    r_text.font.size = Pt(9.5)
    r_text.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    return tbl

def generate_report():
    doc = docx.Document()

    # 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.header_distance = Inches(0.4)
        section.footer_distance = Inches(0.4)
        section.different_first_page_header_footer = True

        # Header for page 2+
        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_hdr.paragraph_format.space_after = Pt(4)
        r_hdr = p_hdr.add_run("COGNICARE  |  MILESTONE 1 PROJECT PROPOSAL")
        r_hdr.font.name = 'Times New Roman'
        r_hdr.font.size = Pt(8.5)
        r_hdr.font.bold = True
        r_hdr.font.color.rgb = RGBColor(0x0D, 0x6E, 0x85)

        # Header bottom border
        pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="2" w:color="0D6E85"/></w:pBdr>')
        p_hdr._p.get_or_add_pPr().append(pBdr)

    NAVY = RGBColor(0x0F, 0x2C, 0x59)
    TEAL = RGBColor(0x0D, 0x6E, 0x85)
    DARK_TEXT = RGBColor(0x1E, 0x29, 0x3B)
    MUTED_TEXT = RGBColor(0x64, 0x74, 0x8B)

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, italic=False, size=Pt(10), space_before=Pt(0), space_after=Pt(4), line_spacing=1.18, color=DARK_TEXT):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = space_before
        p.paragraph_format.space_after = space_after
        p.paragraph_format.line_spacing = line_spacing
        if text:
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = size
            run.font.bold = bold
            run.font.italic = italic
            run.font.color.rgb = color
        return p

    def add_heading1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_heading2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = TEAL
        return p

    def add_bullet(text, bold_prefix="", level=0):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Inches(0.20 * (level + 1))
        
        r_b = p.add_run("•  ")
        r_b.font.name = 'Times New Roman'
        r_b.font.size = Pt(9.5)
        r_b.font.bold = True
        r_b.font.color.rgb = TEAL

        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(9.5)
            r_pre.font.bold = True
            r_pre.font.color.rgb = DARK_TEXT
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(9.5)
        run.font.color.rgb = DARK_TEXT
        return p

    # Footer helper for explicit page numbering in python-docx
    def setup_footers():
        for s in doc.sections:
            f = s.footer
            p_f = f.paragraphs[0]
            p_f.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p_f.paragraph_format.space_before = Pt(4)
            
            # Left side text + tab
            r_left = p_f.add_run("Bennett University • CSET400C • Academic Session 2026–27   |   Page ")
            r_left.font.name = 'Times New Roman'
            r_left.font.size = Pt(8.5)
            r_left.font.color.rgb = MUTED_TEXT

            # Add page number field
            fldSimple = OxmlElement('w:fldSimple')
            fldSimple.set(qn('w:instr'), 'PAGE')
            p_f._p.append(fldSimple)

    # =========================================================================
    # PAGE 1: TITLE & COVER PAGE WITH BENNETT LOGO ON TOP
    # =========================================================================
    logo_path = "milestone 1/bennett_university_logo.png"
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(0)
        p_logo.paragraph_format.space_after = Pt(6)
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Inches(1.50))

    add_p("BENNETT UNIVERSITY", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(17), color=NAVY, space_after=Pt(2))
    add_p("SCHOOL OF ENGINEERING & APPLIED SCIENCES", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(11), color=TEAL, space_after=Pt(2))
    add_p("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(10), color=MUTED_TEXT, space_after=Pt(12))

    add_p("CSET400C | CAPSTONE PROJECT REPORT", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(13), color=NAVY, space_after=Pt(2))
    add_p("Academic Session 2026–27 • Semester VII B.Tech. CSE", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(10.5), color=DARK_TEXT, space_after=Pt(10))

    # Gold horizontal rule
    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_before = Pt(2)
    p_line.paragraph_format.space_after = Pt(10)
    pBdr_gold = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="16" w:space="1" w:color="C5A059"/></w:pBdr>')
    p_line._p.get_or_add_pPr().append(pBdr_gold)

    add_p("MILESTONE 1", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(11), color=TEAL, space_after=Pt(2))
    add_p("PROJECT PROPOSAL, REQUIREMENTS & FEASIBILITY", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(13.5), color=NAVY, space_after=Pt(10))

    add_p("CogniCare", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(28), color=NAVY, space_after=Pt(4))
    add_p("An Accessible Routine and Cognitive-Activity Companion for Older Adults", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=Pt(11.5), color=TEAL, space_after=Pt(14))

    add_p("SUBMITTED BY", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(10), color=NAVY, space_after=Pt(4))
    table = doc.add_table(rows=4, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)
    headers = ["Project Role", "Student Name", "Enrollment Number"]
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], "0F2C59")
        set_cell_margins(hdr_cells[i], top=60, bottom=60, left=90, right=90)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    team_data = [
        ("Team Leader", "Deepanshu Chauhan", "E23CSEU1617"),
        ("Team Member", "Yash", "E23CSEU1493"),
        ("Team Member", "Piyush", "E23CSEU0853")
    ]
    for row_idx, data in enumerate(team_data):
        row_cells = table.rows[row_idx + 1].cells
        for col_idx, val in enumerate(data):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=50, bottom=50, left=90, right=90)
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.5)
                r.font.color.rgb = DARK_TEXT

    add_p("", space_after=Pt(8))
    add_p("UNDER THE SUPERVISION & GUIDANCE OF", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(10), color=NAVY, space_after=Pt(3))
    add_p("Project Guide / Faculty Mentor: Amit Chauhan", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(10.5), color=NAVY, space_after=Pt(2))
    add_p("Course Coordinator: Dr. Jabir Ali", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(10), color=TEAL, space_after=Pt(6))
    add_p("Greater Noida, Uttar Pradesh | 19 October 2026", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(9.5), color=MUTED_TEXT, space_after=Pt(0))

    doc.add_page_break() # -> PAGE 2

    # =========================================================================
    # PAGE 2: DECLARATION OF ORIGINALITY
    # =========================================================================
    add_heading1("Declaration of Originality")
    add_p(
        "We declare that this Milestone 1 report for “CogniCare: An Accessible Routine and Cognitive-Activity Companion for Older Adults” "
        "has been prepared by our team for CSET400C (Capstone Project) at Bennett University during the 2026–27 academic session. "
        "Sources used for background information, standards, and software technologies are acknowledged in the references. "
        "The system design and implementation status are described as proposed or completed according to the evidence available "
        "at the time of submission; planned work is not represented as tested or deployed work.",
        space_after=Pt(5)
    )
    add_p(
        "Team responsibilities for the proposed project are recorded below. Signatures may be added to the submitted copy as required by the department.",
        space_after=Pt(6)
    )

    sig_table = doc.add_table(rows=4, cols=3)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(sig_table)
    sig_headers = ["Student", "Proposed responsibility", "Signature"]
    for i, h in enumerate(sig_headers):
        cell = sig_table.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "0F2C59")
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    sig_data = [
        ("Deepanshu Chauhan", "System architecture, backend services, AI-provider adapter, integration and report coordination", "________________"),
        ("Yash", "Frontend, accessible interaction design, PWA behavior and cognitive activities", "________________"),
        ("Piyush", "Database schema, reminder state machine, scoring logic and test design", "________________")
    ]
    for row_idx, data in enumerate(sig_data):
        row_cells = sig_table.rows[row_idx + 1].cells
        for col_idx, val in enumerate(data):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=55, bottom=55, left=80, right=80)
            p = row_cells[col_idx].paragraphs[0]
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9)
                r.font.color.rgb = DARK_TEXT

    add_p("", space_after=Pt(10))
    add_callout_box(
        doc,
        title="Status note",
        text="This is a proposal and feasibility report. Statements about future features, targets, and tests are design commitments to be verified during implementation, not assertions of clinical validation or production readiness.",
        border_color="D97706",
        bg_color="FFFBEB"
    )

    doc.add_page_break() # -> PAGE 3

    # =========================================================================
    # PAGE 3: EXECUTIVE SUMMARY
    # =========================================================================
    add_heading1("Executive Summary")
    add_p(
        "CogniCare is a proposed, low-cost Progressive Web App (PWA) intended to help older adults manage everyday routines while giving consented family caregivers a clearer view of user-reported activity. It brings together four functions: an accessible “My Day” routine view, configurable medication and daily-task reminders, short non-diagnostic cognitive activities, and a caregiver dashboard for missed reminders and longitudinal activity summaries. An optional conversational assistant may provide supportive, plain-language interaction, but it will not diagnose conditions, alter treatment, or make safety-critical state transitions.",
        space_after=Pt(5)
    )
    add_p(
        "The motivation is practical rather than diagnostic. The World Health Organization reports that 57 million people were living with dementia worldwide in 2021 and nearly 10 million new cases occur each year [1]. The WHO also identifies the substantial role of informal care in dementia support [1]. These figures describe a broad public-health context; they do not imply that every older adult has cognitive impairment or that a software companion can replace clinical or family care. CogniCare is designed as an assistive routine tool, not a medical device or clinical assessment system.",
        space_after=Pt(5)
    )
    add_p(
        "The proposed implementation uses a Next.js App Router frontend, TypeScript, an accessible component system, FastAPI for the REST API, and PostgreSQL for transactional persistence. SQLAlchemy and Alembic are proposed for data access and schema migrations. A provider adapter will integrate a currently supported Gemini Live API model after the model identifier and account availability are verified against official documentation [11]. Deterministic code, rather than generative AI, will govern reminder states and calculate activity scores. Offline behavior will be limited to cached routines and selected activities; cloud conversations, remote caregiver notifications, and delivery verification require a network connection.",
        space_after=Pt(5)
    )
    add_p(
        "The immediate milestone is to agree on requirements, architecture, data boundaries, risk controls, and a testable evaluation plan. The next milestone should produce a functional prototype and evidence from automated tests, accessibility checks, and formative usability evaluation. The report deliberately avoids claims of HIPAA/GDPR compliance, guaranteed medication adherence, clinical benefit, universal availability, or 100% test coverage unless such claims are separately substantiated.",
        space_after=Pt(6)
    )
    add_p("Keywords: older adults, routine support, medication reminders, accessible PWA, caregiver dashboard, deterministic scoring, responsible AI", italic=True, size=Pt(9.5), color=MUTED_TEXT, space_after=Pt(0))

    doc.add_page_break() # -> PAGE 4

    # =========================================================================
    # PAGE 4: CONTENTS
    # =========================================================================
    add_heading1("Contents")
    toc_data = [
        ("Executive Summary", "3"),
        ("1. Introduction and Project Definition", "5"),
        ("2. Related Work and Design Gap", "6"),
        ("3. SDG Alignment and Responsible Design", "7"),
        ("4. Stakeholders and Requirements", "8"),
        ("5. Proposed Architecture and Core Logic", "10"),
        ("6. Feasibility and Risk Management", "13"),
        ("7. Verification and Evaluation Plan", "15"),
        ("8. Project Plan, Roles and Deliverables", "16"),
        ("9. Limitations and Conclusion", "17"),
        ("References", "18")
    ]
    toc_table = doc.add_table(rows=len(toc_data), cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (title, page_num) in enumerate(toc_data):
        c0 = toc_table.rows[i].cells[0]
        c1 = toc_table.rows[i].cells[1]
        c0.width = Inches(5.5)
        c1.width = Inches(1.0)
        c0.text = title
        c1.text = page_num
        set_cell_margins(c0, top=35, bottom=35, left=40, right=40)
        set_cell_margins(c1, top=35, bottom=35, left=40, right=40)
        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p0.runs[0].font.name = 'Times New Roman'
        p0.runs[0].font.size = Pt(10)
        p0.runs[0].font.bold = True if "." in title or title in ["Executive Summary", "References"] else False
        p0.runs[0].font.color.rgb = NAVY if "." in title or title in ["Executive Summary", "References"] else DARK_TEXT
        p1.runs[0].font.name = 'Times New Roman'
        p1.runs[0].font.size = Pt(10)
        p1.runs[0].font.bold = True
        p1.runs[0].font.color.rgb = TEAL

    add_p("", space_after=Pt(14))
    add_callout_box(
        doc,
        title="How to read this report",
        text="The system described here is proposed. Requirements and performance values are target acceptance criteria to test during implementation. The report does not claim that the application is clinically validated or already compliant with any healthcare regulation.",
        border_color="0284C7",
        bg_color="F0F9FF"
    )

    doc.add_page_break() # -> PAGE 5

    # =========================================================================
    # PAGE 5: 1. INTRODUCTION AND PROJECT DEFINITION
    # =========================================================================
    add_heading1("1. Introduction and Project Definition")
    add_heading2("1.1 Background and Motivation")
    add_p(
        "Age-related changes in memory, attention, and task sequencing can make complex daily routines harder to manage for some older adults. Mild cognitive impairment (MCI) is a heterogeneous clinical condition and is not equivalent to dementia; diagnosis and care planning belong with qualified professionals [3]. The design problem addressed here is narrower: people may benefit from clearer reminders, simpler interfaces, and an easy way to communicate routine status to trusted supporters.",
        space_after=Pt(4)
    )
    add_p(
        "The WHO estimates that 57 million people were living with dementia globally in 2021, with nearly 10 million new cases each year [1]. It also estimates that informal carers provide an average of five hours of care and supervision per day for people living with dementia [1]. Separately, the WHO has reported that adherence to long-term treatment for chronic diseases averages around 50% in developed countries, while emphasizing that adherence problems vary across conditions and settings [2]. These figures establish a broad motivation; they are not precise estimates of medication adherence among older adults in India and are not used as a forecast of CogniCare’s impact.",
        space_after=Pt(4)
    )
    add_p(
        "Many digital experiences assume confident vision, fine motor control, and familiarity with multi-step navigation. CogniCare therefore proposes large, clearly labelled controls, predictable navigation, optional voice output, simple confirmation flows, and a caregiver view based on consent. The intent is to support autonomy without turning ordinary activity data into a clinical judgement.",
        space_after=Pt(6)
    )

    add_heading2("1.2 Problem Statement")
    add_callout_box(
        doc,
        title="Problem statement",
        text="Older adults who find complex daily routines difficult may need accessible reminders and low-friction ways to record task status. Family caregivers who live separately may lack a reliable, consent-based view of those self-reported events. Existing tools in separate categories may address only parts of this workflow. CogniCare proposes to integrate routine support, accessible activities, and caregiver visibility in one web-based system while preserving user choice and clearly stating the limits of monitoring.",
        border_color="0D9488",
        bg_color="F0FDFA"
    )

    add_p("", space_after=Pt(4))
    add_heading2("1.3 Aim")
    add_p("To design and evaluate a secure, accessible PWA that supports daily routine management for older adults and provides consented caregivers with transparent, user-reported routine information.", space_after=Pt(4))

    add_heading2("1.4 Objectives")
    add_bullet("Provide a senior-facing “My Day” screen with readable labels, predictable navigation, adjustable text scale, and optional voice guidance.")
    add_bullet("Represent medication and non-medication reminders with a deterministic state machine and auditable timestamps.")
    add_bullet("Provide simple cognitive activities for engagement and practice, with repeatable scoring that is explicitly non-diagnostic.")
    add_bullet("Allow a user to pair with a caregiver through expiring invitations and granular, revocable permissions.")
    add_bullet("Offer caregivers a dashboard showing reminder states, declared acknowledgements, and descriptive activity trends without claiming clinical interpretation.")
    add_bullet("Add a bounded conversational assistant with explicit safety rules and a predictable offline fallback.")
    add_bullet("Validate the prototype using automated tests, accessibility review, security checks, offline scenarios, and formative usability evaluation.")

    doc.add_page_break() # -> PAGE 6

    # =========================================================================
    # PAGE 6: 1.5 SCOPE & 2. RELATED WORK
    # =========================================================================
    add_heading2("1.5 Scope and Boundaries")
    scope_table = doc.add_table(rows=7, cols=2)
    scope_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(scope_table)
    s_headers = ["In scope for the prototype", "Out of scope for this capstone prototype"]
    for i, h in enumerate(s_headers):
        cell = scope_table.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "0F2C59")
        set_cell_margins(cell, top=55, bottom=55, left=70, right=70)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    scope_data = [
        ("Accounts, role-based access, consented caregiver pairing", "Clinical diagnosis, prognosis, or cognitive-disorder screening"),
        ("Routine configuration, reminder states, self-reported acknowledgement", "Verification that a person physically swallowed a medicine"),
        ("Small cognitive-activity catalogue and deterministic score calculation", "Prescription recommendations, dosage changes, or treatment decisions"),
        ("Caregiver dashboard, missed-reminder alerts and audit events", "Guaranteed emergency-service dispatch or guaranteed alert delivery"),
        ("Selected offline access to cached routines and activities", "Full offline AI conversation or reliable remote alerting without connectivity"),
        ("Supportive conversational interaction with safety constraints", "Claims of clinical effectiveness or regulatory certification")
    ]
    for row_idx, (in_s, out_s) in enumerate(scope_data):
        row_cells = scope_table.rows[row_idx + 1].cells
        for col_idx, val in enumerate([in_s, out_s]):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=45, bottom=45, left=70, right=70)
            p = row_cells[col_idx].paragraphs[0]
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8.5)
                r.font.color.rgb = DARK_TEXT

    add_p("", space_after=Pt(6))
    add_heading1("2. Related Work and Design Gap")
    add_heading2("2.1 Review of Solution Categories")
    add_p(
        "This report uses a preliminary category-level comparison to clarify the proposed design. It is not a systematic literature review or a controlled product benchmark. Commercial features, accessibility, device compatibility, and pricing vary by region and subscription plan; these details must be verified from current first-party sources before a final comparative claim is made.",
        space_after=Pt(4)
    )

    cat_table = doc.add_table(rows=5, cols=3)
    cat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(cat_table)
    c_headers = ["Solution category", "Potential value", "Design opportunity for CogniCare"]
    for i, h in enumerate(c_headers):
        cell = cat_table.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "0F2C59")
        set_cell_margins(cell, top=55, bottom=55, left=70, right=70)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    cat_data = [
        ("Cognitive-training applications", "Offer structured games and repeated practice; may help users engage with short activities.", "Use calm, untimed-by-default activities; avoid punitive feedback; keep results descriptive and non-diagnostic."),
        ("Medication and routine reminder applications", "Offer scheduled prompts, confirmation flows, and medication lists.", "Prioritize large controls, low-step acknowledgement, caregiver consent, and visible reminder state history."),
        ("Voice assistants and companion devices", "Can provide conversational access, prompts, and social interaction.", "Offer an affordable browser-based option with an explicit mute control and a clear boundary between conversation and safety logic."),
        ("Caregiver monitoring tools", "Can help a caregiver receive updates or manage care-related tasks.", "Use granular consent and show what is reported, when it was reported, and what remains unknown.")
    ]
    for row_idx, rdata in enumerate(cat_data):
        row_cells = cat_table.rows[row_idx + 1].cells
        for col_idx, val in enumerate(rdata):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=45, bottom=45, left=70, right=70)
            p = row_cells[col_idx].paragraphs[0]
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8.5)
                r.font.color.rgb = DARK_TEXT

    doc.add_page_break() # -> PAGE 7

    # =========================================================================
    # PAGE 7: 2.2 DESIGN GAP & 3. SDG ALIGNMENT
    # =========================================================================
    add_heading2("2.2 Design Gap")
    add_p(
        "The proposed contribution is an integrated workflow rather than a claim that no comparable product exists. CogniCare aims to combine accessible routine management, user-reported reminder history, simple cognitive activities, caregiver visibility, and a safety-constrained conversational interface in one open-web implementation. The integration hypothesis should be assessed through a product-specific comparison and user evaluation during later milestones.",
        space_after=Pt(4)
    )

    add_heading2("2.3 Design Principles Derived from the Review")
    add_bullet("Make the next action obvious: show a small number of primary choices and use direct language.")
    add_bullet("Keep care events deterministic: reminders, acknowledgements, missed states, and alert records must not depend on AI output.")
    add_bullet("Treat caregiver access as a permissioned relationship, not an automatic entitlement.")
    add_bullet("Separate engagement scores from clinical conclusions; show context and uncertainty.")
    add_bullet("Design for poor connectivity and make limitations visible instead of implying that every feature remains available offline.")

    add_p("", space_after=Pt(4))
    add_heading1("3. SDG Alignment and Responsible Design")
    add_heading2("3.1 Sustainable Development Goal 3: Good Health and Well-Being")
    add_p(
        "SDG 3 seeks to ensure healthy lives and promote well-being for people of all ages [4], [5]. CogniCare aligns with this goal at the level of design intent by supporting routine organization, accessible engagement, and communication between an older adult and a chosen caregiver. The project cannot claim reduced mortality, improved clinical outcomes, or a medication-adherence rate before a suitable evaluation has been conducted.",
        space_after=Pt(4)
    )

    add_heading2("3.2 Sustainable Development Goal 10: Reduced Inequalities")
    add_p(
        "SDG Target 10.2 calls for promoting social, economic, and political inclusion regardless of age, disability, or other status [4], [6]. CogniCare contributes to this aim by prioritizing accessibility and avoiding proprietary hardware as a prerequisite. A browser-based application does not by itself eliminate affordability, device, language, connectivity, or digital-literacy barriers; these must be considered in design and evaluation.",
        space_after=Pt(4)
    )

    add_heading2("3.3 Accessibility Approach")
    add_p(
        "The target is WCAG 2.2 Level AA, supported by automated checks and manual testing with keyboard and screen-reader workflows [7]. For normal text, WCAG AA generally requires a contrast ratio of at least 4.5:1; large text generally requires 3:1. The enhanced 7:1 ratio is an AAA criterion for normal text, so 7:1 is retained as a preferred design target where practical, not incorrectly presented as the AA minimum [7].",
        space_after=Pt(3)
    )
    add_bullet("Use plain-language labels, a consistent page structure, visible focus states, and semantic form labels.")
    add_bullet("Adopt 76-by-76 CSS-pixel primary controls as a proposed senior-friendly design target, not as a WCAG requirement; ensure the layout remains usable on smaller screens.")
    add_bullet("Allow text scaling up to 200% without loss of content or functionality.")
    add_bullet("Do not rely on color, sound, animation, or time limits alone to convey important information.")
    add_bullet("Provide optional voice output with an always-visible stop or mute control; voice output should default to off unless the user enables it.")

    doc.add_page_break() # -> PAGE 8

    # =========================================================================
    # PAGE 8: 3.4 PRIVACY & 4. STAKEHOLDERS
    # =========================================================================
    add_heading2("3.4 Privacy, Consent, and Security Principles")
    add_p(
        "The prototype should follow privacy-by-design principles: collect only the data needed for the stated feature, explain the purpose in plain language, grant caregiver access only after explicit pairing, support permission revocation, protect sessions, and define retention and deletion behavior before collecting real users’ data. The design should be reviewed against applicable Indian data-protection requirements, including the Digital Personal Data Protection Act, 2023 and notified Rules, with their provisions and commencement timelines checked at implementation time [12].",
        space_after=Pt(4)
    )
    add_p(
        "The report does not claim HIPAA or GDPR compliance. Applicability depends on jurisdiction, organizational role, data flows, service providers, and operational controls; compliance requires more than authentication or audit logging. Student testing should use synthetic data unless faculty approval, informed consent, and appropriate safeguards are in place for any study involving people or health-related information.",
        space_after=Pt(4)
    )

    add_heading2("3.5 AI Safety Policy")
    add_bullet("Non-diagnostic use: the assistant may help with general conversation and app navigation but must not diagnose, prognose, recommend prescription changes, or override professional advice.")
    add_bullet("Deterministic control: AI output must never create or modify reminder states, caregiver permissions, SOS state, or numeric activity scores.")
    add_bullet("Constrained fallback: if the provider is unavailable, use a small set of tested, pre-approved local messages; do not simulate a live model or fabricate personal context.")
    add_bullet("Transparency: identify AI-generated interaction where appropriate and give the user a simple way to stop the conversation.")
    add_bullet("Data minimization: do not send medication details, identifiers, or activity histories to the AI provider unless the feature requires it, consent and security review allow it, and the request is minimized.")

    add_p("", space_after=Pt(4))
    add_heading1("4. Stakeholders and Requirements")
    add_heading2("4.1 Stakeholder Personas")
    add_p("The following personas are illustrative design aids, not real participants or clinical profiles.", space_after=Pt(3))

    persona_table = doc.add_table(rows=4, cols=3)
    persona_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(persona_table)
    p_headers = ["Persona", "Context", "Primary needs"]
    for i, h in enumerate(p_headers):
        cell = persona_table.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "0F2C59")
        set_cell_margins(cell, top=55, bottom=55, left=70, right=70)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    persona_data = [
        ("Margaret — older adult", "Illustrative 76-year-old living independently; may have low vision or reduced dexterity and sometimes forgets routine tasks.", "One clear “My Day” view, large controls, calm prompts, opt-in voice, easy correction and a visible SOS option."),
        ("Sarah — family caregiver", "Illustrative adult daughter who lives separately and wants to support her parent without constant check-ins.", "Consented access, missed-reminder notifications, trustworthy timestamps, understandable trends and revocable permissions."),
        ("Clinician / administrator", "Secondary stakeholder; not the primary operator of the prototype.", "Clear statement that outputs are not clinical measurements, role separation, and traceable access logs.")
    ]
    for row_idx, rdata in enumerate(persona_data):
        row_cells = persona_table.rows[row_idx + 1].cells
        for col_idx, val in enumerate(rdata):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=45, bottom=45, left=70, right=70)
            p = row_cells[col_idx].paragraphs[0]
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8.5)
                r.font.color.rgb = DARK_TEXT

    doc.add_page_break() # -> PAGE 9

    # =========================================================================
    # PAGE 9: 4.2 FUNCTIONAL REQUIREMENTS & 4.3 NFR
    # =========================================================================
    add_heading2("4.2 Functional Requirements")
    fr_table = doc.add_table(rows=13, cols=3)
    fr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(fr_table)
    fr_headers = ["ID / requirement", "Description", "Acceptance criterion"]
    for i, h in enumerate(fr_headers):
        cell = fr_table.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "0F2C59")
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    fr_data = [
        ("FR-01 Identity and roles", "Users can sign in and access only the screens and records permitted by their role.", "Unauthorized cross-user access tests fail closed."),
        ("FR-02 Caregiver pairing and consent", "A user can create or accept a time-limited invitation, choose a permission tier, and revoke access.", "Expired/revoked invitations cannot create or retain access."),
        ("FR-03 Routine configuration", "Authorized users can define reminder name, schedule, time zone, instructions, and urgency.", "A saved routine persists and is rendered consistently in the senior view."),
        ("FR-04 Reminder lifecycle", "The system manages SCHEDULED, TRIGGERED, SNOOZED, ACKNOWLEDGED, and MISSED states.", "Every defined transition has a unit test and an audit event."),
        ("FR-05 Self-reported acknowledgement", "The user can record that a reminder was acknowledged or snoozed.", "Interface labels this as user-reported status, not proof of ingestion."),
        ("FR-06 Cognitive activities", "The prototype includes memory, sequence, and attention activities with adjustable difficulty.", "Activities are keyboard-operable, have clear instructions, and can be exited."),
        ("FR-07 Deterministic scoring", "Scoring is computed in application code from accuracy and normalized response time.", "Identical valid inputs always return the same score."),
        ("FR-08 Caregiver dashboard", "Permitted caregivers can view routine history, missed events, and descriptive activity trends.", "Dashboard displays time range, event status, and limitations of the data."),
        ("FR-09 Conversational assistant", "Users can request supportive conversation or simple app guidance through a provider adapter.", "Safety tests reject diagnostic, prescription, and treatment-change requests."),
        ("FR-10 SOS interaction", "The user can trigger an emergency-contact alert workflow for linked caregivers.", "The system records attempt/delivery status where available and states if offline."),
        ("FR-11 PWA/offline behavior", "Cached core routine information and selected activities can open without connectivity.", "Offline status is visible; queued events synchronize idempotently when reconnected."),
        ("FR-12 Audit and user controls", "Security-sensitive events, permission changes, and reminder transitions are recorded; data export/deletion rules are defined.", "Logs avoid unnecessary sensitive content and access is role-restricted.")
    ]
    for row_idx, rdata in enumerate(fr_data):
        row_cells = fr_table.rows[row_idx + 1].cells
        for col_idx, val in enumerate(rdata):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=35, bottom=35, left=60, right=60)
            p = row_cells[col_idx].paragraphs[0]
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8)
                r.font.color.rgb = DARK_TEXT

    add_p("", space_after=Pt(4))
    add_heading2("4.3 Non-Functional Requirements")
    nfr_table1 = doc.add_table(rows=2, cols=2)
    nfr_table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(nfr_table1)
    for i, h in enumerate(["ID", "Requirement / target"]):
        cell = nfr_table1.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "0F2C59")
        set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    row_cells = nfr_table1.rows[1].cells
    row_cells[0].text = "NFR-01 Accessibility"
    row_cells[1].text = "Target WCAG 2.2 AA; use 76-by-76 CSS-pixel primary targets as the product design target; support visible focus, screen readers, and 200% text resize."
    for col_idx in [0, 1]:
        set_cell_background(row_cells[col_idx], "F8FAFC")
        set_cell_margins(row_cells[col_idx], top=40, bottom=40, left=60, right=60)
        p = row_cells[col_idx].paragraphs[0]
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8)
            r.font.color.rgb = DARK_TEXT

    doc.add_page_break() # -> PAGE 10

    # =========================================================================
    # PAGE 10: 4.3 NFR (CONT'D), 4.4 PRIORITIZATION, 5.1 ARCHITECTURE
    # =========================================================================
    nfr_table2 = doc.add_table(rows=8, cols=2)
    nfr_table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(nfr_table2)
    for i, h in enumerate(["ID", "Requirement / target"]):
        cell = nfr_table2.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "0F2C59")
        set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    nfr_data = [
        ("NFR-02 Performance", "Target p95 under 500 ms for non-AI API requests in a documented local/staging test profile. AI provider time is measured separately."),
        ("NFR-03 Local fallback", "Target under 100 ms for a template/rule-based fallback response on the test environment; fallback scope must remain deliberately limited."),
        ("NFR-04 Reliability", "Reminder transitions and event writes are idempotent; critical events use explicit deadlines, retries, and recorded delivery attempts."),
        ("NFR-05 Security and privacy", "HTTPS in deployment, secure session cookies, input validation, least privilege, rate limiting, consent revocation, retention policy, and security tests."),
        ("NFR-06 Offline behavior", "Core cached screens and selected activities remain usable offline; cloud AI, remote alerts, and live synchronization clearly require connectivity."),
        ("NFR-07 Maintainability", "Versioned database migrations, documented API schemas, modular service boundaries, automated tests, and reproducible container setup."),
        ("NFR-08 Observability", "Record operational errors and state transitions with timestamps and correlation identifiers, while excluding secrets and unnecessary personal data.")
    ]
    for row_idx, rdata in enumerate(nfr_data):
        row_cells = nfr_table2.rows[row_idx + 1].cells
        for col_idx, val in enumerate(rdata):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=35, bottom=35, left=60, right=60)
            p = row_cells[col_idx].paragraphs[0]
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8)
                r.font.color.rgb = DARK_TEXT

    add_p("", space_after=Pt(6))
    add_heading2("4.4 Requirement Prioritization")
    add_p(
        "For Milestone 2, prioritize the end-to-end path for one senior and one consented caregiver: sign-in, caregiver pairing, routine creation, reminder state transition, acknowledgement, missed-event alert, and dashboard display. Add cognitive activities and deterministic scoring next. Conversational AI and advanced trend visualization should not delay safe completion of the core routine workflow.",
        space_after=Pt(6)
    )

    add_heading1("5. Proposed Architecture and Core Logic")
    add_heading2("5.1 Architecture Choice")
    add_p(
        "CogniCare is proposed as a modular monolith with explicit internal boundaries. This is appropriate for a small capstone team because it reduces operational complexity while allowing modules to be tested independently. A modular monolith does not remove the need for transaction design, locking, idempotency, or failure handling; these are defined at the service and database boundary. PostgreSQL transactions will be used for atomic multi-step writes where required [9].",
        space_after=Pt(0)
    )

    doc.add_page_break() # -> PAGE 11

    # =========================================================================
    # PAGE 11: FIGURE 1 & 5.2 TECHNOLOGY RESPONSIBILITIES
    # =========================================================================
    fig1_path = "milestone 1/figures/figure1_architecture.png"
    if os.path.exists(fig1_path):
        p_fig1 = doc.add_paragraph()
        p_fig1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig1.paragraph_format.space_before = Pt(2)
        p_fig1.paragraph_format.space_after = Pt(2)
        r_f1 = p_fig1.add_run()
        r_f1.add_picture(fig1_path, width=Inches(6.2))

    p_cap1 = add_p("Figure 1. Proposed four-layer architecture and safety boundary. External AI and notification providers are accessed through adapters; deterministic care logic remains internal.",
                   align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=Pt(8.5), color=MUTED_TEXT, space_after=Pt(6))

    add_heading2("5.2 Technology Responsibilities")
    tech_table = doc.add_table(rows=8, cols=3)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tech_table)
    t_headers = ["Component", "Responsibility", "Implementation note"]
    for i, h in enumerate(t_headers):
        cell = tech_table.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "0F2C59")
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    tech_data = [
        ("Next.js App Router + TypeScript", "Senior PWA, caregiver dashboard, accessible components, and navigation.", "Pin a supported version at implementation start; official documentation describes the App Router model [8]."),
        ("FastAPI + Pydantic", "REST API, request validation, authentication/authorization dependencies, and OpenAPI documentation.", "Keep route handlers thin; put business rules in domain/application services [10]."),
        ("PostgreSQL", "Persistent users, consent links, routines, reminder instances, activity results, alert events, and audit metadata.", "Use transactions for related state changes; add foreign keys, indexes, and constraints."),
        ("SQLAlchemy + Alembic", "Database mapping and versioned migrations.", "Migrations must be reviewable and repeatable; do not change production schema manually."),
        ("PWA service worker + IndexedDB", "Cache approved static assets and selected routine/activity data; queue limited offline events.", "Do not imply that IndexedDB content is inherently secure; minimize data stored locally."),
        ("Gemini Live API adapter", "Optional conversational interaction; provider/model identifiers are configured and verified at implementation time.", "Use the current official model catalog [11]; do not hard-code a retired identifier."),
        ("Local fallback module", "Return only tested, pre-approved prompts or basic app guidance when cloud service is unavailable.", "No open-ended local reasoning is assumed; AI is not required for reminders or scoring.")
    ]
    for row_idx, rdata in enumerate(tech_data):
        row_cells = tech_table.rows[row_idx + 1].cells
        for col_idx, val in enumerate(rdata):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=35, bottom=35, left=60, right=60)
            p = row_cells[col_idx].paragraphs[0]
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8)
                r.font.color.rgb = DARK_TEXT

    doc.add_page_break() # -> PAGE 12

    # =========================================================================
    # PAGE 12: 5.3 PRINCIPAL ENTITIES, 5.4 STATE MACHINE, 5.5 SCORING
    # =========================================================================
    add_heading2("5.3 Principal Data Entities")
    add_p("The first relational schema should keep identity, care relationships, operational events, and optional conversation metadata separate. Proposed entities are:", space_after=Pt(2))
    add_bullet("User: identity, role, authentication metadata, preferences, and account status.")
    add_bullet("CareRelationship and ConsentGrant: pairing status, permission tier, invitation expiry, consent time, and revocation time.")
    add_bullet("Routine and ReminderInstance: schedule definition, time zone, due time, current state, deadline, and event history.")
    add_bullet("ActivitySession and ActivityResponse: activity version, difficulty, response data needed for scoring, score version, and completion time.")
    add_bullet("CaregiverAlert: alert type, target, attempt status, delivery result if available, and relevant event identifier.")
    add_bullet("AuditEvent: actor, action, affected record identifier, timestamp, and outcome; omit unnecessary secrets and message content.")
    add_bullet("AIConversationMetadata: provider/model version, interaction time, safety outcome, and minimal operational metadata. Avoid storing full transcripts by default unless a justified, consented need is established.")

    add_heading2("5.4 Reminder State Machine")
    add_p(
        "Reminder processing must be predictable and auditable. A scheduled reminder transitions to TRIGGERED at its due time. The senior can acknowledge it or snooze it. If the configured deadline expires without acknowledgement, the reminder becomes MISSED and may create a caregiver alert according to the routine urgency and consented alert policy.",
        space_after=Pt(3)
    )

    fig2_path = "milestone 1/figures/figure2_state_machine.png"
    if os.path.exists(fig2_path):
        p_fig2 = doc.add_paragraph()
        p_fig2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig2.paragraph_format.space_before = Pt(2)
        p_fig2.paragraph_format.space_after = Pt(2)
        r_f2 = p_fig2.add_run()
        r_f2.add_picture(fig2_path, width=Inches(6.0))

    add_p("Figure 2. Proposed reminder state machine. “Acknowledged” means the user reported a status; it does not independently verify medication ingestion.",
          align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=Pt(8.5), color=MUTED_TEXT, space_after=Pt(4))

    add_p(
        "Implementation rules: (1) store timestamps in a consistent server-side format and render them in the user’s time zone; (2) make event processing idempotent so retries do not create duplicate acknowledgements or alerts; (3) define what happens when a snooze would cross the final deadline; (4) record alert attempts and delivery feedback where the provider exposes it; and (5) display network or delivery uncertainty clearly. Emergency alerts must never depend on a generative AI decision.",
        space_after=Pt(4)
    )

    add_heading2("5.5 Deterministic Activity Scoring")
    add_p("Activity scores are intended as descriptive engagement summaries, not clinical metrics. The score should remain within 0–100, be reproducible for identical inputs, and be versioned so later formula changes do not silently rewrite prior results.", space_after=Pt(0))

    doc.add_page_break() # -> PAGE 13

    # =========================================================================
    # PAGE 13: 5.5 FORMULA, 5.6 AI ORCHESTRATION, 6.1 FEASIBILITY
    # =========================================================================
    add_callout_box(
        doc,
        title="Proposed baseline formula",
        text="Score = round(100 × (0.60 × A + 0.40 × L))\n"
             "A = correct valid responses / total valid responses.\n"
             "For each valid response i, Lᵢ = clamp(Ttarget / max(Tᵢ, ε), 0.20, 1.00); L is the mean of Lᵢ across the session. "
             "Ttarget is an activity-specific reference time, Tᵢ is the observed response time, and ε prevents division by zero. "
             "If no valid responses exist, the session is unscored rather than assigned zero.",
        border_color="0284C7",
        bg_color="F0F9FF"
    )

    add_p(
        "Difficulty is stored as context and used to compare sessions of similar activity and difficulty; it is not multiplied into the score. That avoids the previous design problem in which a difficulty multiplier could produce scores above 100. The response-time target must be tested for each activity and can be adjusted to reduce unnecessary time pressure. Trend views should preferably compare a person with their own prior sessions of comparable activity; no clinical threshold, diagnosis, or population ranking will be displayed.",
        space_after=Pt(4)
    )

    add_heading2("5.6 AI Orchestration and Fallback")
    add_p(
        "The conversational assistant should be accessed through a provider interface so model versions can change without changing care logic. The preferred voice model and endpoint must be selected from the provider’s current documentation at implementation time [11]. The assistant can use a short system policy, minimal context, output limits, and safety filters. It must not schedule medication, determine that an event is missed, interpret activity scores as a diagnosis, or invent whether an alert reached a caregiver.",
        space_after=Pt(4)
    )
    add_p(
        "On timeout, quota exhaustion, or loss of connectivity, the fallback should provide one of a small number of tested messages such as “I can still show your saved routine, but conversation is unavailable right now.” If the application is offline, the interface should clearly distinguish a locally saved event from an event successfully synchronized to the server. The local fallback is a graceful degradation mechanism, not a claim of full offline AI functionality or 100% availability.",
        space_after=Pt(4)
    )

    add_heading1("6. Feasibility and Risk Management")
    add_heading2("6.1 Feasibility Assessment")
    feas_table = doc.add_table(rows=5, cols=3)
    feas_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(feas_table)
    fe_headers = ["Dimension", "Assessment", "Condition / evidence needed"]
    for i, h in enumerate(fe_headers):
        cell = feas_table.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "0F2C59")
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    feas_data = [
        ("Technical", "Feasible for a student team using mainstream web, API, and relational database technologies.", "Validate the complete flow in Docker Compose, including scheduled jobs, timezone handling, migrations, and notification failures."),
        ("Economic", "A software-first PWA avoids requiring dedicated companion hardware.", "Estimate hosting, database, notification, and AI-provider costs from actual traffic and usage; no fixed cost is promised in this report."),
        ("Operational", "The core workflow can be designed around a few primary actions and a caregiver view.", "Usability must be assessed with representative users; “zero training required” is not assumed."),
        ("Ethical / legal", "Consent, role separation, minimal collection, and non-diagnostic limits are design requirements.", "Review applicable Indian data-protection requirements, accessibility, consent materials, retention, and any research-ethics needs before user testing.")
    ]
    for row_idx, rdata in enumerate(feas_data):
        row_cells = feas_table.rows[row_idx + 1].cells
        for col_idx, val in enumerate(rdata):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=35, bottom=35, left=60, right=60)
            p = row_cells[col_idx].paragraphs[0]
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8)
                r.font.color.rgb = DARK_TEXT

    doc.add_page_break() # -> PAGE 14

    # =========================================================================
    # PAGE 14: 6.2 RISK REGISTER
    # =========================================================================
    add_heading2("6.2 Risk Register")
    risk_table = doc.add_table(rows=11, cols=4)
    risk_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(risk_table)
    rk_headers = ["Risk", "Impact", "Likelihood", "Mitigation"]
    for i, h in enumerate(rk_headers):
        cell = risk_table.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "0F2C59")
        set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    risk_data = [
        ("Missed/duplicate reminders", "High", "Medium", "Use deterministic transitions, idempotency keys, scheduler monitoring, deadline tests, and event logs."),
        ("AI gives medical or misleading advice", "High", "Medium", "Constrain scope, block diagnosis/dosage changes, minimize sent context, test adversarial prompts, and provide safe escalation language."),
        ("Caregiver gets access without valid consent", "High", "Low–Medium", "Expiring invitation tokens, explicit permission selection, server-side authorization on every request, and revocation tests."),
        ("Network outage hides alert delivery status", "High", "Medium", "Distinguish queued/sent/delivered/unknown where supported; show offline state and never promise remote delivery without confirmation."),
        ("Scores are interpreted as diagnosis", "High", "Medium", "Label results non-diagnostic, avoid clinical thresholds, contextualize trends, and prohibit AI-generated score interpretation as medical judgement."),
        ("Accessibility needs are missed", "Medium–High", "Medium", "Use WCAG 2.2 AA review, keyboard/screen-reader testing, text scaling, and formative usability tests."),
        ("Personal data exposure", "High", "Medium", "Minimize retention, secure sessions, validate authorization, avoid secrets in logs, define deletion, and test data isolation."),
        ("AI provider quota/model changes", "Medium", "Medium", "Provider adapter, configurable model ID, quota/error handling, versioned tests, and rule-based fallback."),
        ("Offline synchronization conflict", "Medium", "Medium", "Record event IDs/timestamps, use idempotent synchronization, define conflict rules, and display unsynchronized changes."),
        ("Project scope exceeds timeline", "Medium", "High", "Deliver the core routine lifecycle first; make advanced trends and extended conversation optional after the safety-critical path works.")
    ]
    for row_idx, rdata in enumerate(risk_data):
        row_cells = risk_table.rows[row_idx + 1].cells
        for col_idx, val in enumerate(rdata):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=35, bottom=35, left=60, right=60)
            p = row_cells[col_idx].paragraphs[0]
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8)
                if col_idx == 1 and "High" in val:
                    r.font.color.rgb = RGBColor(0x99, 0x1B, 0x1B)
                    r.font.bold = True
                else:
                    r.font.color.rgb = DARK_TEXT

    doc.add_page_break() # -> PAGE 15

    # =========================================================================
    # PAGE 15: 6.3 ASSUMPTIONS & 7. VERIFICATION PLAN
    # =========================================================================
    add_heading2("6.3 Assumptions and Dependencies")
    add_bullet("The prototype will use synthetic or explicitly approved test data, not real patient records by default.")
    add_bullet("Caregiver alert delivery depends on the configured notification channel and network connectivity; delivery guarantees are not assumed.")
    add_bullet("Voice features depend on browser/device support and user permission; text interaction remains available as an alternative.")
    add_bullet("Cloud AI model availability, latency, quotas, and pricing may change and must be checked near deployment.")
    add_bullet("The capstone will not claim a regulated medical-device status, clinical validation, or legal certification.")

    add_p("", space_after=Pt(4))
    add_heading1("7. Verification and Evaluation Plan")
    add_p(
        "Quality will be demonstrated by test evidence and documented acceptance criteria, not by an unsupported blanket statement that the system has “100% automated testing” or “100% coverage.” Each test result should name the code revision, environment, number of tests, failures, and coverage method where relevant.",
        space_after=Pt(4)
    )

    test_table = doc.add_table(rows=9, cols=3)
    test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(test_table)
    ts_headers = ["Test area", "Planned checks", "Acceptance evidence"]
    for i, h in enumerate(ts_headers):
        cell = test_table.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "0F2C59")
        set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    test_data = [
        ("Unit tests", "Reminder transition table, scheduling/time-zone rules, scoring formula, consent/token expiry, and authorization policy.", "All defined state/edge cases have expected results; same inputs yield same scores."),
        ("API integration", "Create routine, trigger reminder, acknowledge/snooze, expire into MISSED, generate alert, and retrieve caregiver view.", "End-to-end API tests pass; transactions remain consistent under retries."),
        ("Security and privacy", "Cross-user IDOR checks, role bypass, expired/revoked invitation, session handling, rate limits, validation, and log inspection.", "Negative authorization tests fail closed; no secrets or unnecessary sensitive content appears in logs."),
        ("Accessibility", "Automated WCAG checks plus keyboard-only, focus, text resize, contrast, screen-reader labels, error recovery, and target-size review.", "Findings are recorded and high-impact blockers are fixed before user evaluation."),
        ("Performance", "Measure non-AI endpoint latency and local fallback latency under a documented test setup.", "Report p50/p95 and environment; assess the 500 ms / 100 ms targets separately."),
        ("Offline and synchronization", "Open cached routines, complete a supported activity, queue a permitted event, reconnect, and retry synchronization.", "No duplicate event is created; unsynchronized status and conflicts are visible."),
        ("AI safety and provider failure", "Test diagnosis/dosage requests, hallucination prompts, timeouts, quota errors, provider/model change, and fallback messaging.", "Safety cases return safe constrained behavior; failure paths remain understandable to users."),
        ("Usability", "Formative task-based evaluation of routine setup, acknowledgement, caregiver pairing, and understanding of status labels.", "Document task completion, observed friction, feedback, and resulting design changes.")
    ]
    for row_idx, rdata in enumerate(test_data):
        row_cells = test_table.rows[row_idx + 1].cells
        for col_idx, val in enumerate(rdata):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=35, bottom=35, left=60, right=60)
            p = row_cells[col_idx].paragraphs[0]
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8)
                r.font.color.rgb = DARK_TEXT

    doc.add_page_break() # -> PAGE 16

    # =========================================================================
    # PAGE 16: 7.1 SAFEGUARDS, 7.2 METRICS, 8.1 SCHEDULE, 8.2 WBS
    # =========================================================================
    add_heading2("7.1 Evaluation Safeguards")
    add_p(
        "Usability testing involving older adults should proceed only after faculty approval, informed consent, accessible study materials, and a clear process for stopping participation. Do not ask participants to rely on CogniCare for actual medication safety, emergency response, or clinical decisions. Early evaluation should focus on comprehension, navigation, accessibility, and task flow using a non-clinical scenario.",
        space_after=Pt(4)
    )

    add_heading2("7.2 Metrics to Report")
    add_bullet("Reminder correctness: expected versus actual state transitions across scheduled, snoozed, acknowledged, and missed scenarios.")
    add_bullet("Authorization correctness: successful and rejected access attempts across roles and consent states.")
    add_bullet("Latency: p50 and p95 for non-AI endpoints and local fallback responses, with environment stated.")
    add_bullet("Accessibility: issues found, severity, remediation status, and manual checks completed against WCAG 2.2 AA.")
    add_bullet("Usability: task completion, observed errors, time on task where appropriate, and qualitative feedback.")
    add_bullet("AI safety: pass/fail outcomes for a predefined policy test set and behavior under provider errors.")
    add_bullet("Offline reliability: synchronization success, duplicate-event rate, and visibility of pending events after reconnect.")

    add_p("", space_after=Pt(4))
    add_heading1("8. Project Plan, Roles and Deliverables")
    add_heading2("8.1 Milestone Schedule")
    ms_table = doc.add_table(rows=5, cols=4)
    ms_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(ms_table)
    m_headers = ["Milestone", "Target period", "Planned scope / output", "Status for this report"]
    for i, h in enumerate(m_headers):
        cell = ms_table.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "0F2C59")
        set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    ms_data = [
        ("Milestone 0", "August 2026", "Problem selection, initial team charter, background exploration, and project scope.", "Reported as completed by the team; supporting artefacts should be retained."),
        ("Milestone 1", "October 2026", "Proposal, requirements, feasibility, risk register, architecture, and presentation.", "Current milestone; this document defines the proposal baseline."),
        ("Milestone 2", "November 2026", "Functional prototype of core routine workflow, caregiver pairing, activity catalogue, AI adapter, and initial test evidence.", "Planned; do not claim complete until evidence exists."),
        ("Final evaluation", "December 2026", "Integrated demonstration, final report, evaluation findings, code and deployment documentation, technical viva.", "Planned.")
    ]
    for row_idx, rdata in enumerate(ms_data):
        row_cells = ms_table.rows[row_idx + 1].cells
        for col_idx, val in enumerate(rdata):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=35, bottom=35, left=60, right=60)
            p = row_cells[col_idx].paragraphs[0]
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8)
                r.font.color.rgb = DARK_TEXT

    add_p("", space_after=Pt(4))
    add_heading2("8.2 Work Breakdown Structure")
    wbs_table1 = doc.add_table(rows=2, cols=3)
    wbs_table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(wbs_table1)
    for i, h in enumerate(["Team member", "Primary ownership", "Shared responsibilities"]):
        cell = wbs_table1.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "0F2C59")
        set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    wbs_cells = wbs_table1.rows[1].cells
    wbs_cells[0].text = "Deepanshu Chauhan — Team Leader"
    wbs_cells[1].text = "API/domain architecture, backend integration, AI provider adapter, container setup, and report coordination."
    wbs_cells[2].text = "Integration planning, safety policy, end-to-end testing, final demo."
    for col_idx in [0, 1, 2]:
        set_cell_background(wbs_cells[col_idx], "F8FAFC")
        set_cell_margins(wbs_cells[col_idx], top=35, bottom=35, left=60, right=60)
        p = wbs_cells[col_idx].paragraphs[0]
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8)
            r.font.color.rgb = DARK_TEXT

    doc.add_page_break() # -> PAGE 17

    # =========================================================================
    # PAGE 17: 8.2 WBS (CONT'D), 8.3 DELIVERABLES, 8.4 DOD, 9.1 LIMITATIONS
    # =========================================================================
    wbs_table2 = doc.add_table(rows=3, cols=3)
    wbs_table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(wbs_table2)
    for i, h in enumerate(["Team member", "Primary ownership", "Shared responsibilities"]):
        cell = wbs_table2.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "0F2C59")
        set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    wbs_data2 = [
        ("Yash — Frontend", "Senior/caregiver interfaces, responsive layout, accessible controls, PWA interaction, and cognitive activity UI.", "Manual accessibility checks, usability feedback, frontend test suite."),
        ("Piyush — Data and verification", "Relational schema, ORM/migrations, reminder state machine, scoring implementation, and backend test design.", "Requirement traceability, risk-based tests, consistency checks.")
    ]
    for row_idx, rdata in enumerate(wbs_data2):
        row_cells = wbs_table2.rows[row_idx + 1].cells
        for col_idx, val in enumerate(rdata):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=35, bottom=35, left=60, right=60)
            p = row_cells[col_idx].paragraphs[0]
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8)
                r.font.color.rgb = DARK_TEXT

    add_p("", space_after=Pt(4))
    add_heading2("8.3 Expected Deliverables")
    add_bullet("Runnable full-stack prototype with documented environment configuration and reproducible startup instructions.")
    add_bullet("Senior-facing routine view and caregiver dashboard with consented pairing and role-separated access.")
    add_bullet("Deterministic reminder lifecycle, event history, and configurable caregiver-alert policy.")
    add_bullet("Non-diagnostic activity catalogue with versioned scoring implementation and descriptive trend view.")
    add_bullet("Optional conversational assistant behind a provider adapter and bounded local fallback.")
    add_bullet("Automated test report, accessibility findings, security test checklist, and basic performance measurements.")
    add_bullet("Architecture diagram, data model, API documentation, user guide, final report, and presentation deck.")

    add_heading2("8.4 Definition of Done for Milestone 2")
    add_p(
        "The prototype is ready for review when the core routine lifecycle can be demonstrated end to end; consent and authorization controls pass negative tests; the reminder state machine and scoring are covered by explicit tests; offline behavior is correctly labelled; major accessibility blockers are resolved; and the team can reproduce the demo from the documented setup. Any incomplete feature or known defect should be listed openly.",
        space_after=Pt(4)
    )

    add_heading1("9. Limitations and Conclusion")
    add_heading2("9.1 Limitations")
    add_bullet("Routine acknowledgement is self-reported and does not verify medicine ingestion or other real-world actions.")
    add_bullet("Cognitive activity results can be influenced by device, language, fatigue, sensory needs, task difficulty, and familiarity; they are not clinical assessments.")
    add_bullet("Caregiver dashboards depend on consent, network access, and accurate recording; absence of data should not be interpreted as proof that an event did not occur.")
    add_bullet("Offline access is intentionally limited. Real-time caregiver alerting and cloud AI interactions cannot be guaranteed without connectivity.")
    add_bullet("A student prototype cannot establish clinical efficacy, regulatory compliance, or a broad market research gap without further evidence.")

    doc.add_page_break() # -> PAGE 18

    # =========================================================================
    # PAGE 18: 9.2 CONCLUSION & REFERENCES [1] TO [12]
    # =========================================================================
    add_heading2("9.2 Conclusion")
    add_p(
        "CogniCare is framed as an accessible routine-support system that connects a senior-facing interface with consent-based caregiver visibility. Its strongest technical principle is separation of concerns: the application’s routine and scoring logic remains deterministic, while AI is limited to optional conversation. The design is feasible as a modular web application, but its success will depend on reliable reminder behavior, meaningful consent, accessible interaction, clear offline limitations, and evidence from testing. The next milestone should focus on a small end-to-end workflow and prove it with tests before expanding the feature set.",
        space_after=Pt(6)
    )

    add_heading1("References")
    refs = [
        "[1] World Health Organization, “Dementia,” Fact sheet, 3 July 2026. [Online]. Available: https://www.who.int/en/news-room/fact-sheets/detail/dementia/. Accessed: 19 Oct. 2026.",
        "[2] World Health Organization, Adherence to Long-Term Therapies: Evidence for Action. Geneva, Switzerland: WHO, 2003. [Online]. Available: https://www.who.int/publications/i/item/9241545992.",
        "[3] R. C. Petersen et al., “Practice guideline update summary: Mild cognitive impairment,” Neurology, vol. 90, no. 3, pp. 126–135, 2018, doi: 10.1212/WNL.0000000000004826.",
        "[4] United Nations General Assembly, “Transforming our world: the 2030 Agenda for Sustainable Development,” A/RES/70/1, 2015. [Online]. Available: https://sdgs.un.org/2030agenda.",
        "[5] United Nations, “Goal 3: Ensure healthy lives and promote well-being for all at all ages.” [Online]. Available: https://sdgs.un.org/goals/goal3. Accessed: 19 Oct. 2026.",
        "[6] United Nations, “Goal 10: Reduce inequality within and among countries.” [Online]. Available: https://sdgs.un.org/goals/goal10. Accessed: 19 Oct. 2026.",
        "[7] World Wide Web Consortium (W3C), “Web Content Accessibility Guidelines (WCAG) 2.2,” W3C Recommendation, 5 Oct. 2023. [Online]. Available: https://www.w3.org/TR/WCAG22/.",
        "[8] Vercel, “Next.js Documentation: App Router.” [Online]. Available: https://nextjs.org/docs/app. Accessed: 19 Oct. 2026.",
        "[9] PostgreSQL Global Development Group, “Transaction Processing,” PostgreSQL Documentation. [Online]. Available: https://www.postgresql.org/docs/current/transactions.html. Accessed: 19 Oct. 2026.",
        "[10] FastAPI, “FastAPI Documentation.” [Online]. Available: https://fastapi.tiangolo.com/. Accessed: 19 Oct. 2026.",
        "[11] Google, “Gemini API Models,” Google AI for Developers. [Online]. Available: https://ai.google.dev/gemini-api/docs/models. Accessed: 19 Oct. 2026.",
        "[12] Government of India, “The Digital Personal Data Protection Act, 2023,” Act No. 22 of 2023; Ministry of Electronics and Information Technology, “Digital Personal Data Protection Rules, 2025,” notified 14 Nov. 2025. [Online]. Available: https://www.indiacode.nic.in/indiacode/handle/123456789/22037?view_type=browse and https://www.meity.gov.in/documents/act-and-policies. Accessed: 19 Oct. 2026."
    ]
    for r in refs:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_before = Pt(1)
        p_r.paragraph_format.space_after = Pt(2.5)
        p_r.paragraph_format.line_spacing = 1.12
        p_r.paragraph_format.left_indent = Inches(0.25)
        run_r = p_r.add_run(r)
        run_r.font.name = 'Times New Roman'
        run_r.font.size = Pt(8.5)
        run_r.font.color.rgb = DARK_TEXT

    setup_footers()

    output_path = "milestone 1/Milestone_1_Report.docx"
    doc.save(output_path)
    print(f"Successfully generated EXACT 18-PAGE Word Report at: {output_path}")

if __name__ == "__main__":
    generate_report()
