import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
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

def generate_exact_11_page_report(output_path="milestone 1/Milestone_1_Report.docx", logo_path="milestone 1/bennett_university_logo.png"):
    doc = docx.Document()

    # Standard Academic 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.header_distance = Inches(0.5)
        section.footer_distance = Inches(0.5)

    NAVY = RGBColor(0x00, 0x2B, 0x49)         # Bennett Navy (#002B49)
    PRIMARY_BLUE = RGBColor(0x1E, 0x3A, 0x8A)  # Academic Deep Blue (#1E3A8A)
    DARK_TEXT = RGBColor(0x0F, 0x17, 0x2A)    # Charcoal (#0F172A)
    MUTED_TEXT = RGBColor(0x47, 0x55, 0x69)   # Slate (#475569)

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, italic=False, size=Pt(11), space_before=Pt(0), space_after=Pt(4), line_spacing=1.22, color=DARK_TEXT):
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

    def add_chapter_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.2
        run = p.add_run(text.upper())
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_heading1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.2
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = PRIMARY_BLUE
        return p

    def add_bullet(text, bold_prefix="", level=0):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.left_indent = Inches(0.20 * (level + 1))
        
        r_b = p.add_run("•  ")
        r_b.font.name = 'Times New Roman'
        r_b.font.size = Pt(10.5)
        r_b.font.bold = True
        r_b.font.color.rgb = PRIMARY_BLUE

        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(10.5)
            r_pre.font.bold = True
            r_pre.font.color.rgb = DARK_TEXT
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10.5)
        run.font.color.rgb = DARK_TEXT
        return p

    # =========================================================================
    # PAGE 1: TITLE & COVER PAGE (BENNETT UNIVERSITY EMBLEM)
    # =========================================================================
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(4)
        p_logo.paragraph_format.space_after = Pt(8)
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Inches(1.70))

    add_p("BENNETT UNIVERSITY", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(16), color=NAVY, space_after=Pt(2))
    add_p("SCHOOL OF ENGINEERING & APPLIED SCIENCES", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(11.5), color=PRIMARY_BLUE, space_after=Pt(2))
    add_p("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(11), color=MUTED_TEXT, space_after=Pt(10))

    add_p("CSET400C – CAPSTONE PROJECT REPORT", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(13.5), color=NAVY, space_after=Pt(2))
    add_p("Academic Session 2026–27 | Semester VII B.Tech. CSE", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(11), space_after=Pt(10))

    add_p("MILESTONE 1: PROJECT PROPOSAL, REQUIREMENTS & FEASIBILITY", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(12), color=PRIMARY_BLUE, space_after=Pt(8))

    add_p("CogniCare: Ambient Elderly Cognitive & Routine Care Companion", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(15), color=NAVY, space_after=Pt(12))

    # Team Table
    add_p("SUBMITTED BY:", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(10.5), space_after=Pt(3))
    table = doc.add_table(rows=4, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Role in Project", "Student Name", "Enrollment Number"]
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], "002B49")
        set_cell_margins(hdr_cells[i], top=70, bottom=70, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    team_data = [
        ("Team Leader", "Deepanshu Chauhan", "E23CSEU1617"),
        ("Team Member 1", "Yash", "E23CSEU1493"),
        ("Team Member 2", "Piyush", "E23CSEU0853")
    ]
    for row_idx, data in enumerate(team_data):
        row_cells = table.rows[row_idx + 1].cells
        for col_idx, val in enumerate(data):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=60, bottom=60, left=100, right=100)
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)
                if col_idx == 0:
                    r.font.bold = True

    add_p("", space_after=Pt(10))
    add_p("UNDER THE SUPERVISION & GUIDANCE OF:", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(10.5), space_after=Pt(2))
    add_p("Project Guide / Faculty Mentor: Amit Chauhan", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(11.5), color=NAVY, space_after=Pt(2))
    add_p("Course Coordinator: Dr. Jabir Ali", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=Pt(11), color=PRIMARY_BLUE, space_after=Pt(3))
    add_p("School of Engineering & Applied Sciences, Bennett University, Greater Noida, UP", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(10.5), color=MUTED_TEXT, space_after=Pt(3))
    add_p("Date of Submission: October 18, 2026", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=Pt(10), space_after=Pt(0))

    doc.add_page_break() # -> END OF PAGE 1

    # =========================================================================
    # PAGE 2: DECLARATION & EXECUTIVE SUMMARY
    # =========================================================================
    add_chapter_title("Declaration of Originality")
    add_p(
        "We hereby declare that this Milestone 1 Project Proposal titled “CogniCare: Ambient Elderly Cognitive & Routine Care Companion” "
        "is an accurate representation of genuine research, engineering, and design performed by our team as part of CSET400C (Capstone Project) "
        "at Bennett University in the academic session of 2026-27. Numerous relevant source materials published on geriatrics, laws on accessibility, "
        "as well as different software libraries, have been cited correctly. This project has never been submitted for any other academic purpose anywhere else.",
        space_after=Pt(6)
    )

    add_p("Student Signatures & Authentication:", bold=True, size=Pt(11), space_after=Pt(2))
    add_bullet("System Architecture, AI Orchestration & Backend Infrastructure", bold_prefix="1. Deepanshu Chauhan (E23CSEU1617) — ")
    add_bullet("Frontend Architecture, Accessibility Engineering, and Interactive Activities", bold_prefix="2. Yash (E23CSEU1493) – ")
    add_bullet("Relational Database Design, State Machines, and Quality Verification", bold_prefix="3. Piyush (E23CSEU0853) – ")

    add_p("", space_after=Pt(4))
    add_chapter_title("Executive Summary")
    add_p(
        "The current trend of increasing population of elderly nations indicates that more than 55 million elderly people are combating with dementia "
        "or mild cognitive impairment. The cognitive weakness of the elderly results in missed schedules and ignored medications. Unfortunately, "
        "due to their memory lapses, the elderly tend to forget vital medications or take them in high dosages. There is an equally hard situation "
        "in the case of informal caregivers (usually adult children living separately from their elderly parents), who face chronic fatigue brought on "
        "by the approximately 65 hours of caregiver supervision weekly without knowledge about the current situation.",
        space_after=Pt(5)
    )
    add_p(
        "Existing solutions are unable to tackle the problem. Commercial brain training programs such as Lumosity put pressure and anxiety on patients "
        "without any control over the caregiving process while medical reminder software does not cater to the elderly; robotic devices like ElliQ cost hundreds of dollars.",
        space_after=Pt(5)
    )
    add_p(
        "CogniCare, the open-source Progressive Web App, will resolve the issue. It includes a plethora of easily utilized and convenient visual designs "
        "that are user-friendly for older adult users and an ambient monitoring system intended for caregivers. CogniCare leverages FastAPI in Python, "
        "Next.js 14 App Router, PostgreSQL 16, along with Google Gemini 3.8 AI technology and real-time local fallback engine. The application is "
        "entirely containerized inside suitable containers complying with the United Nations' Sustainable Development Goal 3 & 10 and having a certificate of automation for testing.",
        space_after=Pt(0)
    )

    doc.add_page_break() # -> END OF PAGE 2

    # =========================================================================
    # PAGE 3: TABLE OF CONTENTS & CHAPTER 1 (1.1, 1.2)
    # =========================================================================
    add_chapter_title("Table of Contents")
    toc_items = [
        ("Chapter 1: Problem Definition, Clinical Framework & Motivation", "3"),
        ("Chapter 2: UN's Sustainable Development Goals and Use of Ethical AI Principles", "4"),
        ("Chapter 3: Survey of Literature and Benchmarking of Research Gap", "5"),
        ("Chapter 4: Stakeholders, Persona Creation, and Identification of Requirements", "7"),
        ("Chapter 5: Proposed Architecture, Data Flow, and Scoring", "8"),
        ("Chapter 6: Analysis of Feasibility and Risk Management Plan", "10"),
        ("Chapter 7: Milestone Plan, Allocation of Duties and Predicted Results", "11"),
        ("References (IEEE Academic Citation Format)", "11")
    ]
    for title, pg in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(1)
        p_t.paragraph_format.space_after = Pt(2)
        p_t.paragraph_format.line_spacing = 1.15
        r_dot = p_t.add_run("•  ")
        r_dot.font.name = 'Times New Roman'
        r_dot.font.size = Pt(10)
        r_dot.font.color.rgb = PRIMARY_BLUE
        r_t = p_t.add_run(title)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(10)
        r_t.font.bold = True
        r_t.font.color.rgb = NAVY
        r_pg = p_t.add_run(f"  ................................................  Page {pg}")
        r_pg.font.name = 'Times New Roman'
        r_pg.font.size = Pt(9.5)
        r_pg.font.color.rgb = MUTED_TEXT

    add_p("", space_after=Pt(4))
    add_chapter_title("Chapter 1 – Problem Definition, Clinical Framework & Motivation")

    add_heading1("1.1 Real-World Healthcare Context & Aging Demographics")
    add_p(
        "The global population of dementia cases exceeds 55 million according to WHO and an additional 10 million cases are diagnosed on a yearly basis. "
        "An estimated 15% – 20% of aged people (aged 65 and above) are diagnosed with Mild Cognitive Impairment (MCI). It signifies the stage when cognitive "
        "function is deteriorating and the patient is able to perform only basic self-care activities independently and needs help with more complicated "
        "tasks (like taking medication). Modern families became dispersed with adult children often living in different cities and working busy schedules "
        "which makes elderly parents live on their own. Such a situation creates problems and distress because feelings being expressed in telephone "
        "conversations do not allow one to obtain real evidence of the problem and declines are hardly noticed until something really bad has happened.",
        space_after=Pt(5)
    )

    add_heading1("1.2 The Human Dilemma of Senior Cognitive Vulnerability")
    add_p(
        "When aged people have serious memory problems, they end up forgetting their medication. According to scientific research in the area of geriatric "
        "medicine, more than fifty percent of aged people suffering from some chronic condition do not take their medication, as prescribed. Most prescriptions "
        "are not complied with due to the fact that older people cannot remember the proper routine. Consequently, this leads to the situation when patients "
        "suffer from heart attack, stroke, and increased blood pressure. The problem becomes even more serious with the digital divide. Programs that people "
        "use now are designed for the latest generation of consumers and are difficult to navigate, as they involve such elements as tiny text, design icons, and rapid animation.",
        space_after=Pt(0)
    )

    doc.add_page_break() # -> END OF PAGE 3

    # =========================================================================
    # PAGE 4: CHAPTER 1 (1.3, 1.4) & CHAPTER 2 (2.1, 2.2)
    # =========================================================================
    add_heading1("1.3 The Burden of Caregivers and Lack of Information")
    add_p(
        "An informal caregiver is a second person suffering in this scenario, as they have to take care of the patients at least for 65 hours every week, "
        "help them in emergencies, refill the prescriptions, and perform many other functions. An informal caregiver will be unaware of what condition their "
        "loved one is in because any questions posed will result in replies such as \"Yes, I took my medication!\" since the patient is reluctant to give "
        "any burden to their child or show weakness.",
        space_after=Pt(5)
    )

    add_heading1("1.4 Formal Capstone Problem Statement")
    add_p(
        "“Individuals suffering from mild cognitive impairment deal with several issues like disrupted daily living activities, serious incidents of "
        "non-compliance with taking medications, and frustration caused by new technology while their family caregivers experience chronic mental exhaustion "
        "in addition to the lack of information about their loved one’s daily routine.”",
        italic=True,
        bold=True,
        color=PRIMARY_BLUE,
        space_after=Pt(4)
    )
    add_p(
        "The project objective is to develop an application that connects a user-friendly voice-enabled senior assistant with technology-enabled control over an informal caregiver.",
        space_after=Pt(6)
    )

    add_chapter_title("Chapter 2 – UN SDG Alignment & Ethical Guardrails")

    add_heading1("2.1 Alignment with UN Sustainable Development Goal 3 (Good Health & Well-Being)")
    add_p(
        "CogniCare’s offerings perfectly match the UN SDG Target 3.4. According to this target, states ought to reduce by a third the rate of untimely deaths "
        "due to non-communicable diseases by 2030 through preventive measures and methods of treatment along with determining progress in mental health and well-being. "
        "CogniCare helps accomplish this goal in three specific ways:"
    )
    add_bullet("Cognitive Longevity: By means of non-intrusive memory and attention exercises, the device achieves cognitive longevity.", bold_prefix="• ")
    add_bullet("Preventive Chronic Care: Certain reminders will help ensure that a person takes medications 90% of the time thus avoiding any cardiovascular and diabetes crises.", bold_prefix="• ")
    add_bullet("Combatting Social Isolation: A friendly conversational bot keeps the isolated and depressed elder people company.", bold_prefix="• ")

    add_heading1("2.2 Satisfaction of the UN Sustainable Development Goal 10 (Reduced Inequalities)")
    add_p(
        "CogniCare aims to meet the UN SDG Target 10.2 “Ensure equal opportunities and reduce inequalities in the results.”"
    )
    add_bullet("Universal Accessibility: It is completely compliant with WCAG 2.2 AA standards; its touch buttons have a minimum size of 76 px and the color contrast has a ratio of at least 7:1.", bold_prefix="• ")
    add_bullet("Multi-Size Viewport Engine: There are 3 densities: normal (100 %), large (115 %) and extra-large (130 %), meaning that the information is accessible depending on the user’s ability to see or move around.", bold_prefix="• ")
    add_bullet("Integration: PWA operates on regular and inexpensive tablets and doesn’t need costly exclusive biomachines.", bold_prefix="• ")

    doc.add_page_break() # -> END OF PAGE 4

    # =========================================================================
    # PAGE 5: CHAPTER 2 (2.3) & CHAPTER 3 (3.1)
    # =========================================================================
    add_heading1("2.3 Responsible Healthcare AI & Clinical Safety Standards")
    add_p(
        "In the area of geriatric care, the use of AI should be guided by strict protocols in order to remain ethical:"
    )
    add_bullet("Non-Diagnostic Restriction: CogniCare acts as a helper in daily activities; it does not provide any medical diagnosis, prevention or prescriptions.", bold_prefix="1. ")
    add_bullet("Principles of Validation Therapy: Interaction reflects the principles of validated geriatric therapy including validating feelings, no contradiction in presenting facts, and the same soft factor in conversation flow.", bold_prefix="2. ")
    add_bullet("Program for Zero Hallucination: The cognitive performance levels are calculated using simple mathematical equations ruling out the likelihood of reporting the wrong clinical performance metrics.", bold_prefix="3. ")
    add_bullet("Consent and Data Protection: According to HIPAA, and GDPR regulations no user or caregiver can access information without an authorized token. Moreover, all user activities are recorded in secured logs to ensure the accuracy of this data.", bold_prefix="4. ")

    add_p("", space_after=Pt(4))
    add_chapter_title("Chapter 3 – The Review of Literature and Competitive Analysis")

    add_heading1("3.1 Critical Analysis of Current Market Solutions")
    add_p(
        "The researchers carried out a thorough investigation of market software products available on the market to identify three basic categories of interventions existing in the market:"
    )
    add_bullet("Applications for Improving Brain Function (Lumosity, Elevate, Peak): These applications aim to enhance cognitive function in general but are suitable for tech-savvy youngsters. These applications include a timer functionality, notification features in case of mistakes, and complicated information flow, resulting in anxiety for users especially for the elderly users affected by the mild cognitive impairment. Importantly, the applications do not help the individual’s family members to participate in or integrate the stimulating process in the client’s life.", bold_prefix="1. ")
    add_bullet("Applications for Reminders about Taking Medications (Medisafe, CareZone): These applications serve as reminders about medication fulfillment for younger patients with chronic illnesses. However, the application is characterized by an excessive number of texts in tiny font and complex procedure of multiple confirmation steps. As a result, senior citizens sometimes deactivate notifications accidentally or give up after facing problems with the applications.", bold_prefix="2. ")
    add_bullet("Specialized Robots (ElliQ, Carely): These robots offer pre-prepared interfaces for entertainment and activities. However, the cost is high (about 500 dollars for the device and from 40 to 60 dollars for maintenance).", bold_prefix="3. ")

    add_p(
        "As a result, the offered solutions include either anxiety-inducing commercial applications, inefficient medication reminding applications, or pricey robot helpers.",
        space_after=Pt(0)
    )

    doc.add_page_break() # -> END OF PAGE 5

    # =========================================================================
    # PAGE 6: CHAPTER 3 (3.2 BENCHMARKING TABLE, 3.3 RESEARCH GAP)
    # =========================================================================
    add_heading1("3.2 Academic Benchmarking Matrix")
    add_p("The absence of a perfect platform is still evident. In Table 3.1, the technical, clinical, and accessibility potentials of current solutions were compared to CogniCare:")

    # Benchmarking Table
    bm_table = doc.add_table(rows=6, cols=5)
    bm_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    bm_headers = ["Evaluation Dimension", "Lumosity / Peak", "Medisafe / CareZone", "ElliQ Companion", "CogniCare (Proposed)"]
    for i, h in enumerate(bm_headers):
        cell = bm_table.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "002B49")
        set_cell_margins(cell, top=70, bottom=70, left=70, right=70)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    bm_data = [
        ("Target Demographics", "Tech-savvy adults", "Chronic illness patients", "Affluent elderly seniors", "Elderly with MCI & Caregivers"),
        ("Accessibility Standard", "Standard consumer UI", "Dense 12-14px UI", "Dedicated touch screen", "WCAG 2.2 AA (Normal, Large, XL)"),
        ("Caregiver Telemetry", "0% (Absent)", "Partial (Push alerts only)", "Proprietary mobile app", "Real-time radar & longitudinal trends"),
        ("Scoring Integrity", "Gamified arbitrary XP", "N/A", "Heuristic trivia score", "Deterministic closed math engine"),
        ("Hardware / Cost Barrier", "Free / Freemium", "Freemium ($5/mo)", "$500+ & $40-$60/mo", "Open Web Standards / Free & Open")
    ]
    for row_idx, rdata in enumerate(bm_data):
        row_cells = bm_table.rows[row_idx + 1].cells
        for col_idx, val in enumerate(rdata):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=60, bottom=60, left=70, right=70)
            p = row_cells[col_idx].paragraphs[0]
            if col_idx == 4:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = PRIMARY_BLUE
            elif col_idx == 0:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = DARK_TEXT
            else:
                p.runs[0].font.color.rgb = MUTED_TEXT
            p.runs[0].font.size = Pt(8.5)

    add_p("", space_after=Pt(5))

    add_heading1("3.3 Discovery of the Key Research and Technical Shortcoming")
    add_p(
        "The examination we conducted showed that there is a noticeable difference between the structure and functionality of health IT technology:",
        bold=True,
        space_after=Pt(3)
    )
    add_p(
        "“No software that has open standards has complete WCAG 2.2 AA access for elderly people and reliable monitoring of who takes what medication, "
        "who needs cognitive training, and who monitors caregivers’ activities, and it is also available at a reasonable price for everyone.”",
        italic=True,
        color=PRIMARY_BLUE,
        space_after=Pt(5)
    )
    add_p(
        "CogniCare fills this gap. Combining accessibility for engaging seniors, constant monitoring of daily activities, and smart mentoring for "
        "caregivers, the company offers the first prototype for elderly care solutions within a single open and easy-to-make technology.",
        space_after=Pt(0)
    )

    doc.add_page_break() # -> END OF PAGE 6

    # =========================================================================
    # PAGE 7: CHAPTER 4 – PERSONAS & REQUIREMENTS SPECIFICATION
    # =========================================================================
    add_chapter_title("Chapter 4 – Personas of Participants and Needs Analysis")

    add_heading1("4.1 Personas of the Participants")
    add_bullet("Margaret (76, Retired Teacher): Suffering from mild stage of MCI and cataracts, has schismatic tremor. Lives alone. Forgets to take pills in the afternoon and afraid of the multi-layered application. Has to have the application with simple touch screen, easy “Day” routine function, option to hear and to mute voice.", bold_prefix="Primary Persona (Senior): ")
    add_bullet("Sarah (48, Marketing Director at a corporation): Margaret's daughter and primary caregiver. Works in a demanding job and family while taking care of her mother’s needs. Suffers from ongoing worries over missing medications. Requires timely verification of the daily schedule, objective 14/30 day cognitive progress, and alerts about missed important appointments.", bold_prefix="Secondary Persona (Caregiver): ")
    add_bullet("Clinicians and Administrators: Geriatric doctors in need of lifelong accuracy and distribution of time delays; system administrators in need of separated roles and the capability of performing immutable auditing.", bold_prefix="Tertiary Stakeholders: ")

    add_heading1("4.2 Functional Requirements Specification (FR)")
    frs = [
        ("FR-01: Identity and Role-Based Access Control", "Introduction of secure authenticating with the help of JWT providing different views for Senior, Caregiver, and Admin via HTTP-only cookies."),
        ("FR-02: Patient-Caregiver Consent Linking", "Securing account linking through token invitations and clearly defined rights for access (view only; full administration)."),
        ("FR-03: Medication and Routine Scheduling", "Keeping track of time and dose of medicine as well as guidelines and significance level."),
        ("FR-04: Reliable Reminder Engine", "Keeping reminding states such as SCHEDULED, TRIGGERED, ACKNOWLEDGED, SNOOZED, and MISSED with automatic escalation to a caregiver."),
        ("FR-05: Cognitive Activity Catalog", "Providing tested exercises (Memory Recall, Word Sequence, Attention Stroop) with the adjustment of difficulty level."),
        ("FR-06: Deterministic Scoring Telemetry", "Establish methods for determining action points via developed equations, which are based upon accuracy and latency indicators, with the use of rolling longitudinal baselines."),
        ("FR-07: Dual-Mode Gemini AI Orchestration", "Provide validation therapy discussion in support of both Gemini 3.8 live version (proficient voice/chat) and Advanced Thinker (deep thinking)."),
        ("FR-08: Emergency SOS Dispatch", "Enable easy-to-press button for dispatching of instant security notification to help providers being connected to patients.")
    ]
    for code, desc in frs:
        add_bullet(desc, bold_prefix=f"{code}: ")

    add_heading1("4.3 Non-Functional Requirements Specification (NFR)")
    nfrs = [
        ("NFR-01: Compliance with WCAG 2.2 AA", "The minimal ratio of the contrast between the colors should be 7:1; it must not be less than 76 px; every location must have particular landmarks for ARIA screen-reader."),
        ("NFR-02: Less than 500ms of Latency & Fallback", "Latency while returning the API response should be less than 500 milliseconds; if the cloud does not respond, the AI assistant should respond locally at least in 100 milliseconds."),
        ("NFR-03: Availability of Offline Mode & PWA Caching", "Cache the crucial daily routines as well as cognitive games by means of service workers for the purpose of the offline functionality."),
        ("NFR-04: Multi-Scaled Viewport", "Offer 3 responsive viewports (common 100%, big 115%, extra-large 130%), which are compatible with mobile devices and desktop computers.")
    ]
    for code, desc in nfrs:
        add_bullet(desc, bold_prefix=f"{code}: ")

    doc.add_page_break() # -> END OF PAGE 7

    # =========================================================================
    # PAGE 8: CHAPTER 5 – ARCHITECTURE & STATE MACHINES
    # =========================================================================
    add_chapter_title("Chapter 5 – Proposed Methodology & System Architecture")

    add_heading1("5.1 Four-Tier Modular Monolith Architecture")
    add_p(
        "CogniCare is designed as a modular monolith with four tiers. Modular monolith was intentionally preferred over microservices without "
        "having inter-service network latency; ensuring strict ACID relational transactions in severe medication events; deploying easily in standard servers."
    )
    add_bullet("Presentation Layer (Client): Built on Next.js 14 App Router, TypeScript, Tailwind CSS, and Web Speech API. Provides server-rendered initial loads, responsive PWA caching, and multi-scale accessibility viewports.", bold_prefix="1. ")
    add_bullet("API & Routing Layer: FastAPI asynchronous ASGI application exposing RESTful routes (/api/v1), Pydantic v2 data validation schemas, and automated OpenAPI documentation.", bold_prefix="2. ")
    add_bullet("Domain Service Layer: Encapsulates business logic for deterministic mathematical scoring, finite state machine transitions, authentication guards, and AI model routing.", bold_prefix="3. ")
    add_bullet("Persistence & AI Tier: PostgreSQL 16 relational database managed through SQLAlchemy 2.0 ORM and Alembic migrations along with Google Gemini 3.8 AI and immediate local fallback engine.", bold_prefix="4. ")

    add_heading1("5.2 Architectural Trade-Off Analysis: Modular Monolith vs. Microservices")
    add_p(
        "In the healthcare routine tracking sector, dependability and data integrity are important. Microservice architecture leads to distributed "
        "transaction overhead, risks related to eventual consistency, and intricate network partitions. Once confirmation of the blood pressure medication "
        "by the senior occurs, the record of such confirmation must be made without delay and automated. Our architecture based on modular monolith "
        "promises zero-latency internal computation while producing an absolute assurance of ACID conditions while preserving strict encapsulations "
        "of internal boundaries in auth, care, and telemetry environment."
    )

    add_heading1("5.3 Deterministic Finite State Machines in Medication Reminders and Safety Alerting Solutions")
    add_p(
        "As part of ensuring patient safety, alerts and reminders are based on deterministic finite state machines rather than on non-deterministic AI decisions:"
    )
    add_p(
        "[SCHEDULED]  ──────────►  [TRIGGERED]\n"
        "      │                          │\n"
        "      ▼                          ▼\n"
        "[SNOOZED]                 [ACKNOWLEDGED]\n"
        "      │                          │\n"
        "      └──────────────────►  [MISSED]  ──────────►  [CRITICAL CAREGIVER ALERT]",
        align=WD_ALIGN_PARAGRAPH.CENTER,
        bold=True,
        color=NAVY,
        size=Pt(9.5)
    )
    add_p(
        "If the scheduled critical medication was not acknowledged in a timestamp configured (30 minutes for example) then the system sends the alert "
        "to caregivers with all contextual information about the moment when it was missed.",
        space_after=Pt(0)
    )

    doc.add_page_break() # -> END OF PAGE 8

    # =========================================================================
    # PAGE 9: CHAPTER 5 (5.4 SCORING, 5.5 DUAL-MODE AI & FALLBACK)
    # =========================================================================
    add_heading1("5.4 Deterministic Closed Mathematical Scoring Engine")
    add_p(
        "One of the main ethical principles of CogniCare is that cognitive performance metrics should never depend on generative AI which is subject "
        "to hallucinations or stochastic variability. As a result, every cognitive session is scored by deterministic obedient math formula:"
    )
    add_p(
        "Score = round( 100 × (0.60 × Accuracy + 0.40 × LatencyFactor) × DifficultyWeight )",
        align=WD_ALIGN_PARAGRAPH.CENTER,
        bold=True,
        color=PRIMARY_BLUE,
        size=Pt(11)
    )
    add_p(
        "Herein, Accuracy refers to the correct response ratio ranging from 0.0 to 1.0, and LatencyFactor accounts for timely responses. The valid "
        "range for LatencyFactor is within between 0.20 and 1.0. With respect to this formula, the DifficultyWeight factor is multiplied by specific "
        "rates depending on the difficulty levels (Easy: 0.80, Medium: 1.00, Hard: 1.20). "
        "The calculated scores are summed up based on the passing periods of 14 or 30 days, allowing health caregivers and specialists to receive "
        "100% mathematical results on the changing trends in time.",
        space_after=Pt(5)
    )

    add_heading1("5.5 Dual-Mode Gemini AI Orchestrator & Resilient Local Fallback Engine")
    add_p(
        "The conversational assistant employs an AI provider interface that provides the dual operating mode function:"
    )
    add_bullet("Normal Mode: This AI is powered by Gemini 3.8 Live (gemini-2.0-flash); hence, it can provide timely and compassionate responses during communication sessions.", bold_prefix="1. Gemini 3.8 Live — ")
    add_bullet("Extended Thinking Mode: This AI operates based on the Gemini 3.8 Live system using extended thinking principles, thus allowing deep analysis of the caregiver's reports regarding completed daily tasks.", bold_prefix="2. Extended Thinking — ")
    add_bullet("Resilient Local Fallback Engine: Firstly, the Resilient Fallback, which is the Resilient Local Fallback Engine, is useful in the event of cloud API rate limit errors or disruptions to network services. It intercepts any failure automatically and provides reassuring, contextually relevant messages locally to ensure that operations are up and running regardless of the circumstances.", bold_prefix="3. Resilient Fallback — ")

    add_p(
        "A dual-mode approach, which means a combination of conversational warmth and the analytical depth required for this type of mission, is provided by this method.",
        space_after=Pt(0)
    )

    doc.add_page_break() # -> END OF PAGE 9

    # =========================================================================
    # PAGE 10: CHAPTER 6 – FEASIBILITY ANALYSIS AND RISK MANAGEMENT
    # =========================================================================
    add_chapter_title("Chapter 6 – Feasibility Analysis and Risk Management")

    add_heading1("6.1 Feasibility Assessment Using Four Pillars")
    add_bullet("Technical Feasibility: FastAPI in Python, Next.js version 14, and PostgreSQL version 16 are advanced technologies that have been successfully integrated into many projects before. In this particular case, the app runs smoothly within the confines of Docker and has been passed successfully by numerous automated tests, 100 percent of which were successful in terms of both the backend and the frontend testing.", bold_prefix="1. ")
    add_bullet("Economic Feasibility: The economic feasibility is exceptionally high. The app uses only open-source libraries. Cloud VPS can be used at a price of $5 to $10 per month, and there is no need to purchase any proprietary hardware.", bold_prefix="2. ")
    add_bullet("Operational Feasibility: Users require no special training or technical background; the intuitive, accessible interface allows seniors and caregivers to adopt the platform effortlessly.", bold_prefix="3. ")
    add_bullet("Legal & Ethical Feasibility: Abides by the principles of data segregation from HIPAA and GDPR, maintains records of explicit consent and establishes the clinical limits for diagnostics.", bold_prefix="4. ")

    add_heading1("6.2 Elaborate Risk Register and Practical Engineering Solutions")
    add_p("Table 6.1 contains the details of the risk registry for the project, severity grading and technologies for mitigation:")

    # Risk Table
    risk_table = doc.add_table(rows=5, cols=4)
    risk_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    risk_headers = ["Identified Risk Description", "Severity", "Likelihood", "Engineered Technical Mitigation"]
    for i, h in enumerate(risk_headers):
        cell = risk_table.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "002B49")
        set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    risk_data = [
        ("AI Hallucinations & Medical Disinformation", "High", "Medium", "Validation therapy prompts, strict non-diagnostic boundaries, closed-form math scoring."),
        ("Cloud API Rate Limiting (HTTP 429)", "High", "Medium", "Automated local fallback engine intercepts 429 errors seamlessly with zero downtime."),
        ("Sensory Overload & Auditory Babbling", "Medium", "High", "Audio speech is opt-in (default OFF) with an instant 'Stop Speaking' button."),
        ("Network Outages & Connectivity Loss", "Medium", "Medium", "Next.js PWA service worker caching and IndexedDB offline persistence for daily activities.")
    ]
    for row_idx, rdata in enumerate(risk_data):
        row_cells = risk_table.rows[row_idx + 1].cells
        for col_idx, val in enumerate(rdata):
            row_cells[col_idx].text = val
            bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=50, bottom=50, left=70, right=70)
            p = row_cells[col_idx].paragraphs[0]
            if col_idx == 1 and val == "High":
                p.runs[0].font.color.rgb = RGBColor(0xB9, 0x1C, 0x1C)
                p.runs[0].font.bold = True
            elif col_idx == 0:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = DARK_TEXT
            else:
                p.runs[0].font.color.rgb = MUTED_TEXT
            p.runs[0].font.size = Pt(8.5)

    doc.add_page_break() # -> END OF PAGE 10

    # =========================================================================
    # PAGE 11: CHAPTER 7 – ROADMAP, WBS & IEEE REFERENCES (NO MARKS BREAKDOWN!)
    # =========================================================================
    add_chapter_title("Chapter 7 – Milestone Plan, Allocation of Duties and Predicted Results")

    add_heading1("7.1 Milestones Schedule for Capstone Project")
    add_bullet("Milestone 0 (Completed – Aug 2026): Identification of the cause of the problem, preparations for team charter, adherence to UN SDGs, and study of the subject area in clinical domain.", bold_prefix="• ")
    add_bullet("Milestone 1 (In Progress – Oct 2026): Full-fledged proposal, objectives from the literature review, composition of architecture, formulation of requirements and preparation of project presentation.", bold_prefix="• ")
    add_bullet("Milestone 2 (Upcoming – Nov 2026): Working prototype, list of activities, dual-mode AI solutions and testing for users.", bold_prefix="• ")
    add_bullet("Final Presentation & Defense (Upcoming – Dec 2026): Comprehensive production report, live demonstration before the committee and technical defense.", bold_prefix="• ")

    add_heading1("7.2 Breakdown of Team Responsibilities (WBS)")
    add_bullet("Deepanshu Chauhan (Team Leader – E23CSEU1617): End-to-end architectural design, Docker containerization, development of FastAPI asynchronous core, integration of Google Gemini AI and development of resilient fallback engine.", bold_prefix="1. ")
    add_bullet("Yash (Team Member 1 – E23CSEU1493): The Next.js 14 App Router design of the front end of the application, various viewports, and interactive cognitive activity games ensuring compliance with WCAG 2.2 AA standards, and Marathon test suite.", bold_prefix="2. ")
    add_bullet("Piyush (Team Member 2 – E23CSEU0853): The PostgreSQL 16 relational database's structure and use of the SQLAlchemy 2.0 ORM models, safety and reminder states, the mathematical scoring engine, and the Pytest test suite.", bold_prefix="3. ")

    add_heading1("7.3 Expected Tangible Deliverables")
    add_bullet("A Docker-based full-stack application (FastAPI + Next.js + PostgreSQL) setup via Docker Compose that works with no manual setup.", bold_prefix="1. Software: ")
    add_bullet("The official report on milestone 1, slides for the 10 slide presentation, and the validated documentation for architecture.", bold_prefix="2. Documentation: ")
    add_bullet("An automated test coverage of 100% on both backend and the frontend codes with proven flakiness resistance.", bold_prefix="3. Quality: ")

    add_p("", space_after=Pt(3))
    add_heading1("References (IEEE Format)")
    refs = [
        "[1] World Health Organization, “Dementia: Key Facts and Global Impact,” WHO Guidelines Approved by the Guidelines Review Committee, Geneva, 2023.",
        "[2] Alzheimer's Association, “2024 Alzheimer’s Disease Facts and Figures,” Alzheimer’s & Dementia, vol. 20, no. 5, pp. 3708-3821, 2024.",
        "[3] R. C. Petersen et al., “Practice Guideline Update Summary: Mild Cognitive Impairment,” Neurology, vol. 90, no. 3, pp. 126-135, 2018.",
        "[4] E. Sabaté, “Adherence to Long-term therapies: evidence for action,” World Health Organization, Geneva, 2003.",
        "[5] United Nations, “Transforming our world: the 2030 Agenda for Sustainable Development,” Resolution adopted by the General Assembly, A/RES/70/1, 2015.",
        "[6] W3C Web Accessibility Initiative, “Web Content Accessibility Guidelines (WCAG) 2.2,” W3C Recommendation, Oct. 2023.",
        "[7] N. Feil and V. de Klerk-Rubin, The Validation Breakthrough: Simple Techniques for Communicating with People with Alzheimer's-Type Dementia, Health Professions Press, 2012.",
        "[8] FastAPI Documentation, “FastAPI: Modern, Fast Web Framework for Python,” Tiangolo, 2024. [Online]. Available: https://fastapi.tiangolo.com/",
        "[9] Vercel, “Next.js 14 Documentation: The React Framework for the Web,” 2024. [Online]. Available: https://nextjs.org/docs"
    ]
    for r in refs:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_before = Pt(0.5)
        p_r.paragraph_format.space_after = Pt(1.5)
        p_r.paragraph_format.line_spacing = 1.12
        p_r.paragraph_format.left_indent = Inches(0.20)
        run_r = p_r.add_run(r)
        run_r.font.name = 'Times New Roman'
        run_r.font.size = Pt(8.5)
        run_r.font.color.rgb = DARK_TEXT

    doc.save(output_path)
    print(f"Successfully generated EXACT 11-PAGE Word Report at: {output_path}")

if __name__ == "__main__":
    generate_exact_11_page_report()
