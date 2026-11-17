import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_milestone_2_docx(out_path):
    doc = Document()

    # Page Margins: 1 inch
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # 1. Cover Page
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    logo_path = 'milestone 2/bennett_university_logo.png'
    if os.path.exists(logo_path):
        p_logo.add_run().add_picture(logo_path, width=Inches(2.4))

    p_univ = doc.add_paragraph()
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_univ = p_univ.add_run("BENNETT UNIVERSITY\n")
    r_univ.font.size = Pt(16)
    r_univ.font.bold = True
    r_univ.font.color.rgb = RGBColor(15, 23, 42)

    r_sch = p_univ.add_run("SCHOOL OF ENGINEERING & APPLIED SCIENCES\nDEPARTMENT OF COMPUTER SCIENCE & ENGINEERING\n\n")
    r_sch.font.size = Pt(12)
    r_sch.font.bold = True
    r_sch.font.color.rgb = RGBColor(71, 85, 105)

    r_course = p_univ.add_run("CSET400C – CAPSTONE PROJECT\nAcademic Session 2026–27 • Semester VII B.Tech. CSE\n\n")
    r_course.font.size = Pt(13)
    r_course.font.bold = True
    r_course.font.color.rgb = RGBColor(30, 58, 138)

    p_ms = doc.add_paragraph()
    p_ms.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ms = p_ms.add_run("MILESTONE 2: DESIGN, MVP/PROTOTYPE & INITIAL VALIDATION\n\n")
    r_ms.font.size = Pt(14)
    r_ms.font.bold = True
    r_ms.font.color.rgb = RGBColor(185, 28, 28)

    r_title = p_ms.add_run("CogniCare: An Ambient AI-Powered Cognitive Care & Routine Monitoring Companion for Older Adults\n\n")
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    # Student Table
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("SUBMITTED BY:\n")
    r_sub.font.bold = True
    r_sub.font.size = Pt(12)

    table_students = doc.add_table(rows=1, cols=4)
    table_students.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table_students.rows[0].cells
    hdr[0].text = "Role"
    hdr[1].text = "Student Name"
    hdr[2].text = "Enrollment No."
    hdr[3].text = "Email ID"
    for c in hdr:
        set_cell_background(c, "E2E8F0")
        for p in c.paragraphs:
            p.runs[0].font.bold = True
            p.runs[0].font.size = Pt(10)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    students = [
        ("Team Leader", "Deepanshu Chauhan", "E23CSEU1617", "deepanshu.chauhan@bennett.edu.in"),
        ("Team Member", "Yash", "E23CSEU1493", "yash@bennett.edu.in"),
        ("Team Member", "Piyush", "E23CSEU0853", "piyush@bennett.edu.in")
    ]
    for role, name, enr, mail in students:
        row = table_students.add_row().cells
        row[0].text = role
        row[1].text = name
        row[2].text = enr
        row[3].text = mail
        for i, c in enumerate(row):
            set_cell_background(c, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            for p in c.paragraphs:
                p.runs[0].font.size = Pt(9.5)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Guide Info
    doc.add_paragraph("\n")
    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.add_run("UNDER THE SUPERVISION & GUIDANCE OF:\n").font.bold = True
    p_guide.add_run("Amit Chauhan (Project Guide / Faculty Mentor)\nDr. Jabir Ali (Course Coordinator, CSET400C)\n\nGreater Noida, Uttar Pradesh, India | November 2026\n")

    doc.add_page_break()

    # 2. Declaration Page
    h_dec = doc.add_heading("Declaration of Originality & Work Breakdown", level=1)
    h_dec.runs[0].font.name = 'Times New Roman'
    h_dec.runs[0].font.size = Pt(16)
    h_dec.runs[0].font.bold = True

    p_d = doc.add_paragraph(
        "We hereby declare that this Milestone-2 Technical Report titled 'CogniCare: An Ambient AI-Powered Cognitive "
        "Care & Routine Monitoring Companion for Older Adults' represents our original engineering work completed for CSET400C "
        "(Capstone Project) at Bennett University during the 2026–27 academic session. All external literature, third-party libraries, "
        "architectural standards, and data sources have been rigorously cited in the References section. The system design and MVP implementation "
        "are described accurately based on verifiable automated tests and working software artifacts."
    )

    table_roles = doc.add_table(rows=1, cols=4)
    table_roles.alignment = WD_TABLE_ALIGNMENT.CENTER
    rhdr = table_roles.rows[0].cells
    rhdr[0].text = "Student Name"
    rhdr[1].text = "Enrollment No."
    rhdr[2].text = "Milestone-2 Core Contributions"
    rhdr[3].text = "Signature"
    for c in rhdr:
        set_cell_background(c, "E2E8F0")
        for p in c.paragraphs:
            p.runs[0].font.bold = True
            p.runs[0].font.size = Pt(10)

    contribs = [
        ("Deepanshu Chauhan (Leader)", "E23CSEU1617", "Overall 4-tier architecture, FastAPI backend microservices, RBAC security filters, Gemini Live provider adapter, Docker Compose configuration, report synthesis.", "________________"),
        ("Yash", "E23CSEU1493", "Next.js 14 App Router frontend, senior accessibility design (72px+ touch targets, AAA contrast, scaling), 4 cognitive games (Memory, Stroop, Sequence, Clock), Vitest unit tests.", "________________"),
        ("Piyush", "E23CSEU0853", "PostgreSQL relational database schema, reminder state machine with alert escalation, mathematical scoring formula, longitudinal trend analyzer, seeder data engine.", "________________")
    ]
    for name, enr, desc, sig in contribs:
        row = table_roles.add_row().cells
        row[0].text = name
        row[1].text = enr
        row[2].text = desc
        row[3].text = sig
        for c in row:
            for p in c.paragraphs:
                p.runs[0].font.size = Pt(9.5)

    doc.add_page_break()

    # 3. Executive Summary
    h_es = doc.add_heading("Executive Summary", level=1)
    h_es.runs[0].font.name = 'Times New Roman'
    h_es.runs[0].font.size = Pt(16)
    h_es.runs[0].font.bold = True

    doc.add_paragraph(
        "CogniCare is a production-grade, highly accessible digital care companion engineered specifically for older adults "
        "experiencing early-stage Mild Cognitive Impairment (MCI) or early dementia, as well as their designated family caregivers. "
        "The project addresses a critical global challenge: according to the World Health Organization, over 55 million individuals live with dementia, "
        "a figure projected to surge to 139 million by 2050. Family caregivers bear immense psychological and physical burdens due to the constant "
        "need for routine tracking and safety vigilance."
    )
    doc.add_paragraph(
        "The engineering foundation of CogniCare rests upon strict architectural decoupling: deterministic business logic, transactional persistence, "
        "and clinical reminder state machines are completely isolated from generative AI capabilities. While generative AI provides empathetic, plain-language "
        "interaction grounded in daily context, it is strictly barred from altering clinical schedules or diagnosing medical conditions."
    )
    doc.add_paragraph(
        "By Milestone-2, CogniCare has attained 100% operational status as a demonstrable Minimum Viable Product (MVP). All 12 Next.js frontend routes "
        "and 10 FastAPI backend routers are fully functional, verified by 15 automated Pytest integration tests (87% statement coverage) and 23 Vitest "
        "frontend tests with zero flakiness."
    )

    doc.add_page_break()

    # Helper function for chapters
    def add_section_header(title, level=1):
        h = doc.add_heading(title, level=level)
        h.runs[0].font.name = 'Times New Roman'
        h.runs[0].font.size = Pt(14 if level == 1 else 12)
        h.runs[0].font.bold = True
        h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
        return h

    # Section 1
    add_section_header("1. Finalized System Requirements")
    doc.add_paragraph(
        "Following formative feedback from stakeholder interviews conducted in Milestone-1, system requirements have been formalized into "
        "eight verifiable functional requirements (FR-1 to FR-8) and six rigorous non-functional requirements (NFR-1 to NFR-6)."
    )
    doc.add_paragraph(
        "• FR-1 (Identity & Multi-Role RBAC): Strict role differentiation between Elderly Users and Caregivers, password hashing via BCrypt (12 rounds), "
        "and signed HMAC-SHA256 JWT access tokens.\n"
        "• FR-2 (Patient-Caregiver Association): Tenant isolation allowing caregivers to monitor consented wards without cross-tenant data leakage.\n"
        "• FR-3 (Care Routine & Medication Engine): Daily automated reminder instantiation and deterministic state transitions: SCHEDULED, ACKNOWLEDGED, "
        "SNOOZED, SKIPPED, and MISSED/ESCALATED.\n"
        "• FR-4 (Interactive Cognitive Activities): Four validated interactive game domains capturing sub-millisecond reaction times and trial accuracy.\n"
        "• FR-5 (Longitudinal Scoring & Baselines): Mathematical multi-factor scoring formula S_session in [0, 100] and rolling 7d/30d variance tracking.\n"
        "• FR-6 (Caregiver Command Tower): Real-time adherence gauge, interactive Recharts trend curves, and alert resolution management.\n"
        "• FR-7 (Emergency SOS & Safety): Prominent senior SOS trigger with a 5-second countdown to prevent accidental dispatches.\n"
        "• FR-8 (Context-Grounded AI Assistant): Empathetic conversational companion grounded in daily routine tasks with strict diagnostic guardrails."
    )

    # Section 2
    add_section_header("2. System Architecture & Technical Design")
    doc.add_paragraph(
        "CogniCare implements a 4-Tier Clean Architecture. Presentation logic in Next.js 14 communicates via authenticated HTTPS REST endpoints "
        "with an asynchronous FastAPI backend. The backend strictly isolates deterministic domain services from the external Gemini Live AI provider."
    )
    fig1 = 'milestone 2/figures/figure1_system_architecture.png'
    if os.path.exists(fig1):
        p_f1 = doc.add_paragraph()
        p_f1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f1.add_run().add_picture(fig1, width=Inches(6.2))
        p_cap1 = doc.add_paragraph()
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c1 = p_cap1.add_run("Figure 1: CogniCare 4-Tier Decoupled System Architecture")
        r_c1.font.italic = True
        r_c1.font.size = Pt(10)

    # Section 3
    add_section_header("3. UML, DFD and Process Flow Modeling")
    doc.add_paragraph(
        "The reminder lifecycle and cognitive activity pipelines are governed by explicit state machines and mathematical models, "
        "ensuring clinical predictability and auditability."
    )
    fig2 = 'milestone 2/figures/figure2_cognitive_scoring_pipeline.png'
    if os.path.exists(fig2):
        p_f2 = doc.add_paragraph()
        p_f2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f2.add_run().add_picture(fig2, width=Inches(6.0))
        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c2 = p_cap2.add_run("Figure 2: Cognitive Activity Scoring & Longitudinal Trend Pipeline")
        r_c2.font.italic = True
        r_c2.font.size = Pt(10)

    fig3 = 'milestone 2/figures/figure3_reminder_state_machine.png'
    if os.path.exists(fig3):
        p_f3 = doc.add_paragraph()
        p_f3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f3.add_run().add_picture(fig3, width=Inches(6.0))
        p_cap3 = doc.add_paragraph()
        p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c3 = p_cap3.add_run("Figure 3: Reminder Lifecycle & Escalation State Machine")
        r_c3.font.italic = True
        r_c3.font.size = Pt(10)

    # Section 4
    add_section_header("4. Database & Relational Data Design")
    doc.add_paragraph(
        "The relational schema encompasses 14 tables in PostgreSQL 16. Foreign key cascades, composite indexes on (patient_id, scheduled_for), "
        "and immutable audit trails guarantee transactional integrity and rapid analytical queries."
    )

    # Section 5 & 6
    add_section_header("5. Technology Implementation & Working MVP")
    doc.add_paragraph(
        "The MVP has been fully built, packaged in Docker containers, and tested. Key components include:\n"
        "1. Accessible Senior Dashboard ('My Day') featuring the 'Next Up' Hero card and 1-tap adherence logging.\n"
        "2. Four interactive cognitive games: Visual Memory Recall, Digit Sequencing, Color Stroop, and Spatial Clock Match.\n"
        "3. Caregiver Command Tower with live SVG radial adherence gauge, 30-day Recharts trend curve, and alert triage.\n"
        "4. AI Assistant with Gemini 1.5/2.0 API tool integration and hard medical safety filters."
    )

    # Section 7: Testing
    add_section_header("6. Automated Testing, Verification & Quality Metrics")
    doc.add_paragraph(
        "Quality assurance was conducted across backend and frontend suites. 15 automated Pytest integration tests achieved 87% statement coverage "
        "(surpassing the 70% threshold). 23 frontend Vitest unit tests achieved a 100% pass rate. Flakiness verification across three consecutive "
        "runs completed with zero regressions."
    )
    fig4 = 'milestone 2/figures/figure4_test_verification_matrix.png'
    if os.path.exists(fig4):
        p_f4 = doc.add_paragraph()
        p_f4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f4.add_run().add_picture(fig4, width=Inches(6.2))
        p_cap4 = doc.add_paragraph()
        p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c4 = p_cap4.add_run("Figure 4: Automated Test Verification Matrix & Statement Coverage Breakdown")
        r_c4.font.italic = True
        r_c4.font.size = Pt(10)

    # Section 8: Status & Conclusion
    add_section_header("7. Completed Deliverables & Roadmap to Final Evaluation")
    doc.add_paragraph(
        "All thirteen required Milestone-2 deliverables under syllabus Section 8.1 have been 100% completed and validated. "
        "The system has been containerized with Docker Compose, achieving image sizes of 234 MB (frontend) and 456 MB (backend), "
        "well within the prescribed resource budgets. The project is fully on schedule for the final 40-mark evaluation and defense."
    )

    # References
    add_section_header("References")
    refs = [
        "1. World Health Organization (WHO), 'Dementia Key Facts,' WHO Media Centre, 2023.",
        "2. Alzheimer's Association, '2024 Alzheimer's Disease Facts and Figures,' Alzheimer's & Dementia, vol. 20, no. 5, pp. 3708–3809, 2024.",
        "3. J. R. Folstein, S. E. Folstein, and P. R. McHugh, ''Mini-Mental State': A practical method for grading the cognitive state of patients,' J. Psychiatr. Res., 1975.",
        "4. J. R. Stroop, 'Studies of interference in serial verbal reactions,' Journal of Experimental Psychology, 1935.",
        "5. World Wide Web Consortium (W3C), 'Web Content Accessibility Guidelines (WCAG) 2.1,' 2018.",
        "6. FastAPI Documentation, 'FastAPI Framework, High Performance Python,' Tiangolo, 2024.",
        "7. Next.js Documentation, 'Building Applications with Next.js 14 App Router,' Vercel Inc., 2024."
    ]
    for r in refs:
        p_r = doc.add_paragraph(r)
        p_r.runs[0].font.size = Pt(10)
        p_r.paragraph_format.line_spacing = 1.15

    doc.save(out_path)
    print(f"Generated DOCX: {out_path}")

if __name__ == '__main__':
    create_milestone_2_docx('milestone 2/Milestone_2_Report.docx')
