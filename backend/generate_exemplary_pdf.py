import os
import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress on cover page

        self.saveState()
        self.setFont("Times-Roman", 8.5)
        self.setFillColor(colors.HexColor("#0D6E85"))

        # Running Header
        header_text = "COGNICARE  |  MILESTONE 1 PROJECT PROPOSAL"
        self.drawRightString(letter[0] - 54, letter[1] - 36, header_text)

        # Header rule
        self.setStrokeColor(colors.HexColor("#0D6E85"))
        self.setLineWidth(0.6)
        self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Running Footer
        self.setFont("Times-Roman", 8.5)
        self.setFillColor(colors.HexColor("#64748B"))
        footer_text = f"Bennett University • CSET400C • Academic Session 2026–27   |   Page {self._pageNumber}"
        self.drawRightString(letter[0] - 54, 34, footer_text)

        self.restoreState()

def create_callout(title, text, border_color="#0284C7", bg_color="#F0F9FF", width=504):
    styles = getSampleStyleSheet()
    t_style = ParagraphStyle(
        'CalloutTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor(border_color),
        spaceAfter=3
    )
    b_style = ParagraphStyle(
        'CalloutBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.8,
        leading=12,
        textColor=colors.HexColor("#1E293B")
    )

    flowables = []
    if title:
        flowables.append(Paragraph(title, t_style))
    flowables.append(Paragraph(text, b_style))

    t = Table([[flowables]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
        ('LINELEFT', (0,0), (0,0), 3.0, colors.HexColor(border_color)),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

def generate_pdf(output_path="milestone 1/Milestone_1_Report.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    
    NAVY = colors.HexColor("#0F2C59")
    TEAL = colors.HexColor("#0D6E85")
    DARK = colors.HexColor("#1E293B")
    MUTED = colors.HexColor("#64748B")

    body_style = ParagraphStyle('AcademicBody', parent=styles['Normal'], fontName='Times-Roman', fontSize=9.5, leading=13.5, textColor=DARK, spaceAfter=5)
    bullet_style = ParagraphStyle('AcademicBullet', parent=styles['Normal'], fontName='Times-Roman', fontSize=9, leading=12.5, textColor=DARK, leftIndent=14, firstLineIndent=-10, spaceAfter=2.5)
    h1_style = ParagraphStyle('AcademicH1', parent=styles['Normal'], fontName='Times-Bold', fontSize=13, leading=16, textColor=NAVY, spaceBefore=7, spaceAfter=4)
    h2_style = ParagraphStyle('AcademicH2', parent=styles['Normal'], fontName='Times-Bold', fontSize=10.5, leading=14, textColor=TEAL, spaceBefore=5, spaceAfter=3)

    story = []

    # =========================================================================
    # PAGE 1: COVER
    # =========================================================================
    logo_path = "milestone 1/bennett_university_logo.png"
    if os.path.exists(logo_path):
        story.append(Spacer(1, 5))
        img = RLImage(logo_path, width=1.45*72, height=1.65*72)
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(Spacer(1, 8))

    story.append(Paragraph("BENNETT UNIVERSITY", ParagraphStyle('BU', fontName='Times-Bold', fontSize=17, leading=20, alignment=TA_CENTER, textColor=NAVY)))
    story.append(Spacer(1, 2))
    story.append(Paragraph("SCHOOL OF ENGINEERING & APPLIED SCIENCES", ParagraphStyle('SEAS', fontName='Times-Bold', fontSize=10.5, leading=13, alignment=TA_CENTER, textColor=TEAL)))
    story.append(Spacer(1, 2))
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", ParagraphStyle('DCSE', fontName='Times-Roman', fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=MUTED)))
    story.append(Spacer(1, 10))

    story.append(Paragraph("CSET400C | CAPSTONE PROJECT REPORT", ParagraphStyle('CSET', fontName='Times-Bold', fontSize=12.5, leading=15, alignment=TA_CENTER, textColor=NAVY)))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Academic Session 2026–27 • Semester VII B.Tech. CSE", ParagraphStyle('Sess', fontName='Times-Roman', fontSize=10, leading=13, alignment=TA_CENTER, textColor=DARK)))
    story.append(Spacer(1, 8))

    story.append(HRFlowable(width="60%", thickness=1.8, color=colors.HexColor("#C5A059"), spaceAfter=10, spaceBefore=2))

    story.append(Paragraph("MILESTONE 1", ParagraphStyle('M1', fontName='Times-Bold', fontSize=11, leading=13, alignment=TA_CENTER, textColor=TEAL)))
    story.append(Spacer(1, 2))
    story.append(Paragraph("PROJECT PROPOSAL, REQUIREMENTS & FEASIBILITY", ParagraphStyle('PR', fontName='Times-Bold', fontSize=13, leading=16, alignment=TA_CENTER, textColor=NAVY)))
    story.append(Spacer(1, 10))

    story.append(Paragraph("CogniCare", ParagraphStyle('Title', fontName='Times-Bold', fontSize=26, leading=30, alignment=TA_CENTER, textColor=NAVY)))
    story.append(Spacer(1, 3))
    story.append(Paragraph("An Accessible Routine and Cognitive-Activity Companion for Older Adults", ParagraphStyle('Sub', fontName='Times-Italic', fontSize=11.5, leading=14, alignment=TA_CENTER, textColor=TEAL)))
    story.append(Spacer(1, 14))

    story.append(Paragraph("SUBMITTED BY", ParagraphStyle('SubBy', fontName='Times-Bold', fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=NAVY)))
    story.append(Spacer(1, 4))

    cover_table_data = [
        [Paragraph("<b>Project Role</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=8.5, textColor=colors.white)),
         Paragraph("<b>Student Name</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=8.5, textColor=colors.white)),
         Paragraph("<b>Enrollment Number</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=8.5, textColor=colors.white))],
        [Paragraph("Team Leader", ParagraphStyle('B', fontName='Times-Roman', fontSize=8.5, textColor=DARK)),
         Paragraph("Deepanshu Chauhan", ParagraphStyle('B', fontName='Times-Roman', fontSize=8.5, textColor=DARK)),
         Paragraph("E23CSEU1617", ParagraphStyle('B', fontName='Times-Roman', fontSize=8.5, textColor=DARK))],
        [Paragraph("Team Member", ParagraphStyle('B', fontName='Times-Roman', fontSize=8.5, textColor=DARK)),
         Paragraph("Yash", ParagraphStyle('B', fontName='Times-Roman', fontSize=8.5, textColor=DARK)),
         Paragraph("E23CSEU1493", ParagraphStyle('B', fontName='Times-Roman', fontSize=8.5, textColor=DARK))],
        [Paragraph("Team Member", ParagraphStyle('B', fontName='Times-Roman', fontSize=8.5, textColor=DARK)),
         Paragraph("Piyush", ParagraphStyle('B', fontName='Times-Roman', fontSize=8.5, textColor=DARK)),
         Paragraph("E23CSEU0853", ParagraphStyle('B', fontName='Times-Roman', fontSize=8.5, textColor=DARK))]
    ]
    t_cover = Table(cover_table_data, colWidths=[150, 190, 140])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0,2), (-1,2), colors.white),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#F8FAFC")),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_cover)
    story.append(Spacer(1, 10))

    story.append(Paragraph("UNDER THE SUPERVISION & GUIDANCE OF", ParagraphStyle('SG', fontName='Times-Bold', fontSize=9, leading=12, alignment=TA_CENTER, textColor=NAVY)))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Project Guide / Faculty Mentor: Amit Chauhan", ParagraphStyle('G1', fontName='Times-Bold', fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=NAVY)))
    story.append(Spacer(1, 1))
    story.append(Paragraph("Course Coordinator: Dr. Jabir Ali", ParagraphStyle('G2', fontName='Times-Bold', fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=TEAL)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Greater Noida, Uttar Pradesh | 19 October 2026", ParagraphStyle('G3', fontName='Times-Roman', fontSize=9, leading=11, alignment=TA_CENTER, textColor=MUTED)))

    story.append(PageBreak()) # -> PAGE 2

    # =========================================================================
    # PAGE 2: DECLARATION OF ORIGINALITY
    # =========================================================================
    story.append(Paragraph("Declaration of Originality", h1_style))
    story.append(Paragraph(
        "We declare that this Milestone 1 report for “CogniCare: An Accessible Routine and Cognitive-Activity Companion for Older Adults” has been prepared by our team for CSET400C (Capstone Project) at Bennett University during the 2026–27 academic session. Sources used for background information, standards, and software technologies are acknowledged in the references. The system design and implementation status are described as proposed or completed according to the evidence available at the time of submission; planned work is not represented as tested or deployed work.",
        body_style
    ))
    story.append(Paragraph(
        "Team responsibilities for the proposed project are recorded below. Signatures may be added to the submitted copy as required by the department.",
        body_style
    ))
    story.append(Spacer(1, 4))

    sig_data = [
        [Paragraph("<b>Student</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=8.5, textColor=colors.white)),
         Paragraph("<b>Proposed responsibility</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=8.5, textColor=colors.white)),
         Paragraph("<b>Signature</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=8.5, textColor=colors.white))],
        [Paragraph("Deepanshu Chauhan", ParagraphStyle('B', fontName='Times-Roman', fontSize=8.5, textColor=DARK)),
         Paragraph("System architecture, backend services, AI-provider adapter, integration and report coordination", ParagraphStyle('B', fontName='Times-Roman', fontSize=8, textColor=DARK)),
         Paragraph("________________", ParagraphStyle('B', fontName='Times-Roman', fontSize=8, textColor=DARK))],
        [Paragraph("Yash", ParagraphStyle('B', fontName='Times-Roman', fontSize=8.5, textColor=DARK)),
         Paragraph("Frontend, accessible interaction design, PWA behavior and cognitive activities", ParagraphStyle('B', fontName='Times-Roman', fontSize=8, textColor=DARK)),
         Paragraph("________________", ParagraphStyle('B', fontName='Times-Roman', fontSize=8, textColor=DARK))],
        [Paragraph("Piyush", ParagraphStyle('B', fontName='Times-Roman', fontSize=8.5, textColor=DARK)),
         Paragraph("Database schema, reminder state machine, scoring logic and test design", ParagraphStyle('B', fontName='Times-Roman', fontSize=8, textColor=DARK)),
         Paragraph("________________", ParagraphStyle('B', fontName='Times-Roman', fontSize=8, textColor=DARK))]
    ]
    t_sig = Table(sig_data, colWidths=[120, 240, 140])
    t_sig.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0,2), (-1,2), colors.white),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#F8FAFC")),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sig)
    story.append(Spacer(1, 14))

    story.append(create_callout(
        title="Status note",
        text="This is a proposal and feasibility report. Statements about future features, targets, and tests are design commitments to be verified during implementation, not assertions of clinical validation or production readiness.",
        border_color="#D97706",
        bg_color="#FFFBEB",
        width=500
    ))

    story.append(PageBreak()) # -> PAGE 3

    # =========================================================================
    # PAGE 3: EXECUTIVE SUMMARY
    # =========================================================================
    story.append(Paragraph("Executive Summary", h1_style))
    story.append(Paragraph(
        "CogniCare is a proposed, low-cost Progressive Web App (PWA) intended to help older adults manage everyday routines while giving consented family caregivers a clearer view of user-reported activity. It brings together four functions: an accessible “My Day” routine view, configurable medication and daily-task reminders, short non-diagnostic cognitive activities, and a caregiver dashboard for missed reminders and longitudinal activity summaries. An optional conversational assistant may provide supportive, plain-language interaction, but it will not diagnose conditions, alter treatment, or make safety-critical state transitions.",
        body_style
    ))
    story.append(Paragraph(
        "The motivation is practical rather than diagnostic. The World Health Organization reports that 57 million people were living with dementia worldwide in 2021 and nearly 10 million new cases occur each year [1]. The WHO also identifies the substantial role of informal care in dementia support [1]. These figures describe a broad public-health context; they do not imply that every older adult has cognitive impairment or that a software companion can replace clinical or family care. CogniCare is designed as an assistive routine tool, not a medical device or clinical assessment system.",
        body_style
    ))
    story.append(Paragraph(
        "The proposed implementation uses a Next.js App Router frontend, TypeScript, an accessible component system, FastAPI for the REST API, and PostgreSQL for transactional persistence. SQLAlchemy and Alembic are proposed for data access and schema migrations. A provider adapter will integrate a currently supported Gemini Live API model after the model identifier and account availability are verified against official documentation [11]. Deterministic code, rather than generative AI, will govern reminder states and calculate activity scores. Offline behavior will be limited to cached routines and selected activities; cloud conversations, remote caregiver notifications, and delivery verification require a network connection.",
        body_style
    ))
    story.append(Paragraph(
        "The immediate milestone is to agree on requirements, architecture, data boundaries, risk controls, and a testable evaluation plan. The next milestone should produce a functional prototype and evidence from automated tests, accessibility checks, and formative usability evaluation. The report deliberately avoids claims of HIPAA/GDPR compliance, guaranteed medication adherence, clinical benefit, universal availability, or 100% test coverage unless such claims are separately substantiated.",
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Keywords:</b> older adults, routine support, medication reminders, accessible PWA, caregiver dashboard, deterministic scoring, responsible AI", ParagraphStyle('KW', fontName='Times-Italic', fontSize=9, leading=12, textColor=MUTED)))

    story.append(PageBreak()) # -> PAGE 4

    # =========================================================================
    # PAGE 4: CONTENTS
    # =========================================================================
    story.append(Paragraph("Contents", h1_style))
    toc_data = [
        [Paragraph("<b>Executive Summary</b>", ParagraphStyle('T', fontName='Times-Bold', fontSize=9.5, textColor=NAVY)), Paragraph("<b>3</b>", ParagraphStyle('P', fontName='Times-Bold', fontSize=9.5, alignment=TA_RIGHT, textColor=TEAL))],
        [Paragraph("<b>1. Introduction and Project Definition</b>", ParagraphStyle('T', fontName='Times-Bold', fontSize=9.5, textColor=NAVY)), Paragraph("<b>5</b>", ParagraphStyle('P', fontName='Times-Bold', fontSize=9.5, alignment=TA_RIGHT, textColor=TEAL))],
        [Paragraph("<b>2. Related Work and Design Gap</b>", ParagraphStyle('T', fontName='Times-Bold', fontSize=9.5, textColor=NAVY)), Paragraph("<b>6</b>", ParagraphStyle('P', fontName='Times-Bold', fontSize=9.5, alignment=TA_RIGHT, textColor=TEAL))],
        [Paragraph("<b>3. SDG Alignment and Responsible Design</b>", ParagraphStyle('T', fontName='Times-Bold', fontSize=9.5, textColor=NAVY)), Paragraph("<b>7</b>", ParagraphStyle('P', fontName='Times-Bold', fontSize=9.5, alignment=TA_RIGHT, textColor=TEAL))],
        [Paragraph("<b>4. Stakeholders and Requirements</b>", ParagraphStyle('T', fontName='Times-Bold', fontSize=9.5, textColor=NAVY)), Paragraph("<b>8</b>", ParagraphStyle('P', fontName='Times-Bold', fontSize=9.5, alignment=TA_RIGHT, textColor=TEAL))],
        [Paragraph("<b>5. Proposed Architecture and Core Logic</b>", ParagraphStyle('T', fontName='Times-Bold', fontSize=9.5, textColor=NAVY)), Paragraph("<b>10</b>", ParagraphStyle('P', fontName='Times-Bold', fontSize=9.5, alignment=TA_RIGHT, textColor=TEAL))],
        [Paragraph("<b>6. Feasibility and Risk Management</b>", ParagraphStyle('T', fontName='Times-Bold', fontSize=9.5, textColor=NAVY)), Paragraph("<b>13</b>", ParagraphStyle('P', fontName='Times-Bold', fontSize=9.5, alignment=TA_RIGHT, textColor=TEAL))],
        [Paragraph("<b>7. Verification and Evaluation Plan</b>", ParagraphStyle('T', fontName='Times-Bold', fontSize=9.5, textColor=NAVY)), Paragraph("<b>15</b>", ParagraphStyle('P', fontName='Times-Bold', fontSize=9.5, alignment=TA_RIGHT, textColor=TEAL))],
        [Paragraph("<b>8. Project Plan, Roles and Deliverables</b>", ParagraphStyle('T', fontName='Times-Bold', fontSize=9.5, textColor=NAVY)), Paragraph("<b>16</b>", ParagraphStyle('P', fontName='Times-Bold', fontSize=9.5, alignment=TA_RIGHT, textColor=TEAL))],
        [Paragraph("<b>9. Limitations and Conclusion</b>", ParagraphStyle('T', fontName='Times-Bold', fontSize=9.5, textColor=NAVY)), Paragraph("<b>17</b>", ParagraphStyle('P', fontName='Times-Bold', fontSize=9.5, alignment=TA_RIGHT, textColor=TEAL))],
        [Paragraph("<b>References</b>", ParagraphStyle('T', fontName='Times-Bold', fontSize=9.5, textColor=NAVY)), Paragraph("<b>18</b>", ParagraphStyle('P', fontName='Times-Bold', fontSize=9.5, alignment=TA_RIGHT, textColor=TEAL))]
    ]
    t_toc = Table(toc_data, colWidths=[420, 80])
    t_toc.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 16))

    story.append(create_callout(
        title="How to read this report",
        text="The system described here is proposed. Requirements and performance values are target acceptance criteria to test during implementation. The report does not claim that the application is clinically validated or already compliant with any healthcare regulation.",
        border_color="#0284C7",
        bg_color="#F0F9FF",
        width=500
    ))

    story.append(PageBreak()) # -> PAGE 5

    # =========================================================================
    # PAGE 5: 1. INTRODUCTION AND PROJECT DEFINITION
    # =========================================================================
    story.append(Paragraph("1. Introduction and Project Definition", h1_style))
    story.append(Paragraph("1.1 Background and Motivation", h2_style))
    story.append(Paragraph(
        "Age-related changes in memory, attention, and task sequencing can make complex daily routines harder to manage for some older adults. Mild cognitive impairment (MCI) is a heterogeneous clinical condition and is not equivalent to dementia; diagnosis and care planning belong with qualified professionals [3]. The design problem addressed here is narrower: people may benefit from clearer reminders, simpler interfaces, and an easy way to communicate routine status to trusted supporters.",
        body_style
    ))
    story.append(Paragraph(
        "The WHO estimates that 57 million people were living with dementia globally in 2021, with nearly 10 million new cases each year [1]. It also estimates that informal carers provide an average of five hours of care and supervision per day for people living with dementia [1]. Separately, the WHO has reported that adherence to long-term treatment for chronic diseases averages around 50% in developed countries, while emphasizing that adherence problems vary across conditions and settings [2]. These figures establish a broad motivation; they are not precise estimates of medication adherence among older adults in India and are not used as a forecast of CogniCare’s impact.",
        body_style
    ))
    story.append(Paragraph(
        "Many digital experiences assume confident vision, fine motor control, and familiarity with multi-step navigation. CogniCare therefore proposes large, clearly labelled controls, predictable navigation, optional voice output, simple confirmation flows, and a caregiver view based on consent. The intent is to support autonomy without turning ordinary activity data into a clinical judgement.",
        body_style
    ))

    story.append(Paragraph("1.2 Problem Statement", h2_style))
    story.append(create_callout(
        title="Problem statement",
        text="Older adults who find complex daily routines difficult may need accessible reminders and low-friction ways to record task status. Family caregivers who live separately may lack a reliable, consent-based view of those self-reported events. Existing tools in separate categories may address only parts of this workflow. CogniCare proposes to integrate routine support, accessible activities, and caregiver visibility in one web-based system while preserving user choice and clearly stating the limits of monitoring.",
        border_color="#0D9488",
        bg_color="#F0FDFA",
        width=500
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1.3 Aim", h2_style))
    story.append(Paragraph("To design and evaluate a secure, accessible PWA that supports daily routine management for older adults and provides consented caregivers with transparent, user-reported routine information.", body_style))

    story.append(Paragraph("1.4 Objectives", h2_style))
    story.append(Paragraph("• Provide a senior-facing “My Day” screen with readable labels, predictable navigation, adjustable text scale, and optional voice guidance.", bullet_style))
    story.append(Paragraph("• Represent medication and non-medication reminders with a deterministic state machine and auditable timestamps.", bullet_style))
    story.append(Paragraph("• Provide simple cognitive activities for engagement and practice, with repeatable scoring that is explicitly non-diagnostic.", bullet_style))
    story.append(Paragraph("• Allow a user to pair with a caregiver through expiring invitations and granular, revocable permissions.", bullet_style))
    story.append(Paragraph("• Offer caregivers a dashboard showing reminder states, declared acknowledgements, and descriptive activity trends without claiming clinical interpretation.", bullet_style))
    story.append(Paragraph("• Add a bounded conversational assistant with explicit safety rules and a predictable offline fallback.", bullet_style))
    story.append(Paragraph("• Validate the prototype using automated tests, accessibility review, security checks, offline scenarios, and formative usability evaluation.", bullet_style))

    story.append(PageBreak()) # -> PAGE 6

    # =========================================================================
    # PAGE 6: 1.5 SCOPE & 2. RELATED WORK
    # =========================================================================
    story.append(Paragraph("1.5 Scope and Boundaries", h2_style))
    scope_rows = [
        [Paragraph("<b>In scope for the prototype</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=8, textColor=colors.white)),
         Paragraph("<b>Out of scope for this capstone prototype</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=8, textColor=colors.white))],
        [Paragraph("Accounts, role-based access, consented caregiver pairing", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK)),
         Paragraph("Clinical diagnosis, prognosis, or cognitive-disorder screening", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK))],
        [Paragraph("Routine configuration, reminder states, self-reported acknowledgement", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK)),
         Paragraph("Verification that a person physically swallowed a medicine", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK))],
        [Paragraph("Small cognitive-activity catalogue and deterministic score calculation", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK)),
         Paragraph("Prescription recommendations, dosage changes, or treatment decisions", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK))],
        [Paragraph("Caregiver dashboard, missed-reminder alerts and audit events", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK)),
         Paragraph("Guaranteed emergency-service dispatch or guaranteed alert delivery", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK))],
        [Paragraph("Selected offline access to cached routines and activities", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK)),
         Paragraph("Full offline AI conversation or reliable remote alerting without connectivity", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK))],
        [Paragraph("Supportive conversational interaction with safety constraints", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK)),
         Paragraph("Claims of clinical effectiveness or regulatory certification", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK))]
    ]
    t_scope = Table(scope_rows, colWidths=[250, 250])
    t_scope.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0,2), (-1,2), colors.white),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0,4), (-1,4), colors.white),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0,6), (-1,6), colors.white),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_scope)
    story.append(Spacer(1, 6))

    story.append(Paragraph("2. Related Work and Design Gap", h1_style))
    story.append(Paragraph("2.1 Review of Solution Categories", h2_style))
    story.append(Paragraph(
        "This report uses a preliminary category-level comparison to clarify the proposed design. It is not a systematic literature review or a controlled product benchmark. Commercial features, accessibility, device compatibility, and pricing vary by region and subscription plan; these details must be verified from current first-party sources before a final comparative claim is made.",
        body_style
    ))

    cat_rows = [
        [Paragraph("<b>Solution category</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=8, textColor=colors.white)),
         Paragraph("<b>Potential value</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=8, textColor=colors.white)),
         Paragraph("<b>Design opportunity for CogniCare</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=8, textColor=colors.white))],
        [Paragraph("Cognitive-training applications", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK)),
         Paragraph("Offer structured games and repeated practice; may help users engage with short activities.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK)),
         Paragraph("Use calm, untimed-by-default activities; avoid punitive feedback; keep results descriptive and non-diagnostic.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK))],
        [Paragraph("Medication and routine reminder applications", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK)),
         Paragraph("Offer scheduled prompts, confirmation flows, and medication lists.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK)),
         Paragraph("Prioritize large controls, low-step acknowledgement, caregiver consent, and visible reminder state history.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK))],
        [Paragraph("Voice assistants and companion devices", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK)),
         Paragraph("Can provide conversational access, prompts, and social interaction.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK)),
         Paragraph("Offer an affordable browser-based option with an explicit mute control and a clear boundary between conversation and safety logic.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK))],
        [Paragraph("Caregiver monitoring tools", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK)),
         Paragraph("Can help a caregiver receive updates or manage care-related tasks.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK)),
         Paragraph("Use granular consent and show what is reported, when it was reported, and what remains unknown.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK))]
    ]
    t_cat = Table(cat_rows, colWidths=[130, 170, 200])
    t_cat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0,2), (-1,2), colors.white),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0,4), (-1,4), colors.white),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_cat)

    story.append(PageBreak()) # -> PAGE 7

    # =========================================================================
    # PAGE 7: 2.2 DESIGN GAP & 3. SDG ALIGNMENT
    # =========================================================================
    story.append(Paragraph("2.2 Design Gap", h2_style))
    story.append(Paragraph(
        "The proposed contribution is an integrated workflow rather than a claim that no comparable product exists. CogniCare aims to combine accessible routine management, user-reported reminder history, simple cognitive activities, caregiver visibility, and a safety-constrained conversational interface in one open-web implementation. The integration hypothesis should be assessed through a product-specific comparison and user evaluation during later milestones.",
        body_style
    ))

    story.append(Paragraph("2.3 Design Principles Derived from the Review", h2_style))
    story.append(Paragraph("• Make the next action obvious: show a small number of primary choices and use direct language.", bullet_style))
    story.append(Paragraph("• Keep care events deterministic: reminders, acknowledgements, missed states, and alert records must not depend on AI output.", bullet_style))
    story.append(Paragraph("• Treat caregiver access as a permissioned relationship, not an automatic entitlement.", bullet_style))
    story.append(Paragraph("• Separate engagement scores from clinical conclusions; show context and uncertainty.", bullet_style))
    story.append(Paragraph("• Design for poor connectivity and make limitations visible instead of implying that every feature remains available offline.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("3. SDG Alignment and Responsible Design", h1_style))
    story.append(Paragraph("3.1 Sustainable Development Goal 3: Good Health and Well-Being", h2_style))
    story.append(Paragraph(
        "SDG 3 seeks to ensure healthy lives and promote well-being for people of all ages [4], [5]. CogniCare aligns with this goal at the level of design intent by supporting routine organization, accessible engagement, and communication between an older adult and a chosen caregiver. The project cannot claim reduced mortality, improved clinical outcomes, or a medication-adherence rate before a suitable evaluation has been conducted.",
        body_style
    ))

    story.append(Paragraph("3.2 Sustainable Development Goal 10: Reduced Inequalities", h2_style))
    story.append(Paragraph(
        "SDG Target 10.2 calls for promoting social, economic, and political inclusion regardless of age, disability, or other status [4], [6]. CogniCare contributes to this aim by prioritizing accessibility and avoiding proprietary hardware as a prerequisite. A browser-based application does not by itself eliminate affordability, device, language, connectivity, or digital-literacy barriers; these must be considered in design and evaluation.",
        body_style
    ))

    story.append(Paragraph("3.3 Accessibility Approach", h2_style))
    story.append(Paragraph(
        "The target is WCAG 2.2 Level AA, supported by automated checks and manual testing with keyboard and screen-reader workflows [7]. For normal text, WCAG AA generally requires a contrast ratio of at least 4.5:1; large text generally requires 3:1. The enhanced 7:1 ratio is an AAA criterion for normal text, so 7:1 is retained as a preferred design target where practical, not incorrectly presented as the AA minimum [7].",
        body_style
    ))
    story.append(Paragraph("• Use plain-language labels, a consistent page structure, visible focus states, and semantic form labels.", bullet_style))
    story.append(Paragraph("• Adopt 76-by-76 CSS-pixel primary controls as a proposed senior-friendly design target, not as a WCAG requirement; ensure the layout remains usable on smaller screens.", bullet_style))
    story.append(Paragraph("• Allow text scaling up to 200% without loss of content or functionality.", bullet_style))
    story.append(Paragraph("• Do not rely on color, sound, animation, or time limits alone to convey important information.", bullet_style))
    story.append(Paragraph("• Provide optional voice output with an always-visible stop or mute control; voice output should default to off unless the user enables it.", bullet_style))

    story.append(PageBreak()) # -> PAGE 8

    # =========================================================================
    # PAGE 8: 3.4 PRIVACY & 4. STAKEHOLDERS
    # =========================================================================
    story.append(Paragraph("3.4 Privacy, Consent, and Security Principles", h2_style))
    story.append(Paragraph(
        "The prototype should follow privacy-by-design principles: collect only the data needed for the stated feature, explain the purpose in plain language, grant caregiver access only after explicit pairing, support permission revocation, protect sessions, and define retention and deletion behavior before collecting real users’ data. The design should be reviewed against applicable Indian data-protection requirements, including the Digital Personal Data Protection Act, 2023 and notified Rules, with their provisions and commencement timelines checked at implementation time [12].",
        body_style
    ))
    story.append(Paragraph(
        "The report does not claim HIPAA or GDPR compliance. Applicability depends on jurisdiction, organizational role, data flows, service providers, and operational controls; compliance requires more than authentication or audit logging. Student testing should use synthetic data unless faculty approval, informed consent, and appropriate safeguards are in place for any study involving people or health-related information.",
        body_style
    ))

    story.append(Paragraph("3.5 AI Safety Policy", h2_style))
    story.append(Paragraph("• <b>Non-diagnostic use:</b> the assistant may help with general conversation and app navigation but must not diagnose, prognose, recommend prescription changes, or override professional advice.", bullet_style))
    story.append(Paragraph("• <b>Deterministic control:</b> AI output must never create or modify reminder states, caregiver permissions, SOS state, or numeric activity scores.", bullet_style))
    story.append(Paragraph("• <b>Constrained fallback:</b> if the provider is unavailable, use a small set of tested, pre-approved local messages; do not simulate a live model or fabricate personal context.", bullet_style))
    story.append(Paragraph("• <b>Transparency:</b> identify AI-generated interaction where appropriate and give the user a simple way to stop the conversation.", bullet_style))
    story.append(Paragraph("• <b>Data minimization:</b> do not send medication details, identifiers, or activity histories to the AI provider unless the feature requires it, consent and security review allow it, and the request is minimized.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("4. Stakeholders and Requirements", h1_style))
    story.append(Paragraph("4.1 Stakeholder Personas", h2_style))
    story.append(Paragraph("The following personas are illustrative design aids, not real participants or clinical profiles.", body_style))

    p_rows = [
        [Paragraph("<b>Persona</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=8, textColor=colors.white)),
         Paragraph("<b>Context</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=8, textColor=colors.white)),
         Paragraph("<b>Primary needs</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=8, textColor=colors.white))],
        [Paragraph("Margaret — older adult", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK)),
         Paragraph("Illustrative 76-year-old living independently; may have low vision or reduced dexterity and sometimes forgets routine tasks.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK)),
         Paragraph("One clear “My Day” view, large controls, calm prompts, opt-in voice, easy correction and a visible SOS option.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK))],
        [Paragraph("Sarah — family caregiver", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK)),
         Paragraph("Illustrative adult daughter who lives separately and wants to support her parent without constant check-ins.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK)),
         Paragraph("Consented access, missed-reminder notifications, trustworthy timestamps, understandable trends and revocable permissions.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK))],
        [Paragraph("Clinician / administrator", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.8, textColor=DARK)),
         Paragraph("Secondary stakeholder; not the primary operator of the prototype.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK)),
         Paragraph("Clear statement that outputs are not clinical measurements, role separation, and traceable access logs.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK))]
    ]
    t_persona = Table(p_rows, colWidths=[120, 180, 200])
    t_persona.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0,2), (-1,2), colors.white),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#F8FAFC")),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_persona)

    story.append(PageBreak()) # -> PAGE 9

    # =========================================================================
    # PAGE 9: 4.2 FUNCTIONAL REQUIREMENTS & 4.3 NFR
    # =========================================================================
    story.append(Paragraph("4.2 Functional Requirements", h2_style))
    fr_rows = [
        [Paragraph("<b>ID / requirement</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Description</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Acceptance criterion</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white))],
        [Paragraph("FR-01 Identity and roles", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Users can sign in and access only the screens and records permitted by their role.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Unauthorized cross-user access tests fail closed.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("FR-02 Caregiver pairing and consent", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("A user can create or accept a time-limited invitation, choose a permission tier, and revoke access.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Expired/revoked invitations cannot create or retain access.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("FR-03 Routine configuration", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Authorized users can define reminder name, schedule, time zone, instructions, and urgency.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("A saved routine persists and is rendered consistently in the senior view.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("FR-04 Reminder lifecycle", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("The system manages SCHEDULED, TRIGGERED, SNOOZED, ACKNOWLEDGED, and MISSED states.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Every defined transition has a unit test and an audit event.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("FR-05 Self-reported acknowledgement", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("The user can record that a reminder was acknowledged or snoozed.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Interface labels this as user-reported status, not proof of ingestion.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("FR-06 Cognitive activities", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("The prototype includes memory, sequence, and attention activities with adjustable difficulty.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Activities are keyboard-operable, have clear instructions, and can be exited.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("FR-07 Deterministic scoring", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Scoring is computed in application code from accuracy and normalized response time.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Identical valid inputs always return the same score.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("FR-08 Caregiver dashboard", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Permitted caregivers can view routine history, missed events, and descriptive activity trends.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Dashboard displays time range, event status, and limitations of the data.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("FR-09 Conversational assistant", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Users can request supportive conversation or simple app guidance through a provider adapter.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Safety tests reject diagnostic, prescription, and treatment-change requests.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("FR-10 SOS interaction", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("The user can trigger an emergency-contact alert workflow for linked caregivers.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("The system records attempt/delivery status where available and states if offline.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("FR-11 PWA/offline behavior", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Cached core routine information and selected activities can open without connectivity.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Offline status is visible; queued events synchronize idempotently when reconnected.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("FR-12 Audit and user controls", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Security-sensitive events, permission changes, and reminder transitions are recorded; data export/deletion rules are defined.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Logs avoid unnecessary sensitive content and access is role-restricted.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))]
    ]
    t_fr = Table(fr_rows, colWidths=[140, 200, 160])
    t_fr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_fr)
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.3 Non-Functional Requirements", h2_style))
    nfr_rows1 = [
        [Paragraph("<b>ID</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Requirement / target</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white))],
        [Paragraph("NFR-01 Accessibility", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Target WCAG 2.2 AA; use 76-by-76 CSS-pixel primary targets as the product design target; support visible focus, screen readers, and 200% text resize.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK))]
    ]
    t_nfr1 = Table(nfr_rows1, colWidths=[140, 360])
    t_nfr1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_nfr1)

    story.append(PageBreak()) # -> PAGE 10

    # =========================================================================
    # PAGE 10: 4.3 NFR (CONT'D), 4.4 PRIORITIZATION, 5.1 ARCHITECTURE
    # =========================================================================
    nfr_rows2 = [
        [Paragraph("<b>ID</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Requirement / target</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white))],
        [Paragraph("NFR-02 Performance", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Target p95 under 500 ms for non-AI API requests in a documented local/staging test profile. AI provider time is measured separately.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK))],
        [Paragraph("NFR-03 Local fallback", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Target under 100 ms for a template/rule-based fallback response on the test environment; fallback scope must remain deliberately limited.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK))],
        [Paragraph("NFR-04 Reliability", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Reminder transitions and event writes are idempotent; critical events use explicit deadlines, retries, and recorded delivery attempts.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK))],
        [Paragraph("NFR-05 Security and privacy", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("HTTPS in deployment, secure session cookies, input validation, least privilege, rate limiting, consent revocation, retention policy, and security tests.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK))],
        [Paragraph("NFR-06 Offline behavior", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Core cached screens and selected activities remain usable offline; cloud AI, remote alerts, and live synchronization clearly require connectivity.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK))],
        [Paragraph("NFR-07 Maintainability", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Versioned database migrations, documented API schemas, modular service boundaries, automated tests, and reproducible container setup.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK))],
        [Paragraph("NFR-08 Observability", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Record operational errors and state transitions with timestamps and correlation identifiers, while excluding secrets and unnecessary personal data.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK))]
    ]
    t_nfr2 = Table(nfr_rows2, colWidths=[140, 360])
    t_nfr2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_nfr2)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.4 Requirement Prioritization", h2_style))
    story.append(Paragraph(
        "For Milestone 2, prioritize the end-to-end path for one senior and one consented caregiver: sign-in, caregiver pairing, routine creation, reminder state transition, acknowledgement, missed-event alert, and dashboard display. Add cognitive activities and deterministic scoring next. Conversational AI and advanced trend visualization should not delay safe completion of the core routine workflow.",
        body_style
    ))

    story.append(Paragraph("5. Proposed Architecture and Core Logic", h1_style))
    story.append(Paragraph("5.1 Architecture Choice", h2_style))
    story.append(Paragraph(
        "CogniCare is proposed as a modular monolith with explicit internal boundaries. This is appropriate for a small capstone team because it reduces operational complexity while allowing modules to be tested independently. A modular monolith does not remove the need for transaction design, locking, idempotency, or failure handling; these are defined at the service and database boundary. PostgreSQL transactions will be used for atomic multi-step writes where required [9].",
        body_style
    ))

    story.append(PageBreak()) # -> PAGE 11

    # =========================================================================
    # PAGE 11: FIGURE 1 & 5.2 TECH RESPONSIBILITIES
    # =========================================================================
    fig1_path = "milestone 1/figures/figure1_architecture.png"
    if os.path.exists(fig1_path):
        img_f1 = RLImage(fig1_path, width=6.5*72, height=3.67*72)
        img_f1.hAlign = 'CENTER'
        story.append(img_f1)
        story.append(Spacer(1, 3))

    story.append(Paragraph(
        "<i>Figure 1. Proposed four-layer architecture and safety boundary. External AI and notification providers are accessed through adapters; deterministic care logic remains internal.</i>",
        ParagraphStyle('Cap', fontName='Times-Italic', fontSize=8, leading=11, alignment=TA_CENTER, textColor=MUTED)
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("5.2 Technology Responsibilities", h2_style))
    tech_rows = [
        [Paragraph("<b>Component</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Responsibility</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Implementation note</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white))],
        [Paragraph("Next.js App Router + TypeScript", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Senior PWA, caregiver dashboard, accessible components, and navigation.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Pin a supported version at implementation start; official documentation describes the App Router model [8].", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("FastAPI + Pydantic", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("REST API, request validation, authentication/authorization dependencies, and OpenAPI documentation.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Keep route handlers thin; put business rules in domain/application services [10].", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("PostgreSQL", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Persistent users, consent links, routines, reminder instances, activity results, alert events, and audit metadata.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Use transactions for related state changes; add foreign keys, indexes, and constraints.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("SQLAlchemy + Alembic", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Database mapping and versioned migrations.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Migrations must be reviewable and repeatable; do not change production schema manually.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("PWA service worker + IndexedDB", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Cache approved static assets and selected routine/activity data; queue limited offline events.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Do not imply that IndexedDB content is inherently secure; minimize data stored locally.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("Gemini Live API adapter", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Optional conversational interaction; provider/model identifiers are configured and verified at implementation time.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Use the current official model catalog [11]; do not hard-code a retired identifier.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("Local fallback module", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Return only tested, pre-approved prompts or basic app guidance when cloud service is unavailable.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("No open-ended local reasoning is assumed; AI is not required for reminders or scoring.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))]
    ]
    t_tech = Table(tech_rows, colWidths=[130, 180, 190])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_tech)

    story.append(PageBreak()) # -> PAGE 12

    # =========================================================================
    # PAGE 12: 5.3 PRINCIPAL ENTITIES, 5.4 STATE MACHINE, 5.5 SCORING
    # =========================================================================
    story.append(Paragraph("5.3 Principal Data Entities", h2_style))
    story.append(Paragraph("The first relational schema should keep identity, care relationships, operational events, and optional conversation metadata separate. Proposed entities are:", body_style))
    story.append(Paragraph("• <b>User:</b> identity, role, authentication metadata, preferences, and account status.", bullet_style))
    story.append(Paragraph("• <b>CareRelationship and ConsentGrant:</b> pairing status, permission tier, invitation expiry, consent time, and revocation time.", bullet_style))
    story.append(Paragraph("• <b>Routine and ReminderInstance:</b> schedule definition, time zone, due time, current state, deadline, and event history.", bullet_style))
    story.append(Paragraph("• <b>ActivitySession and ActivityResponse:</b> activity version, difficulty, response data needed for scoring, score version, and completion time.", bullet_style))
    story.append(Paragraph("• <b>CaregiverAlert:</b> alert type, target, attempt status, delivery result if available, and relevant event identifier.", bullet_style))
    story.append(Paragraph("• <b>AuditEvent:</b> actor, action, affected record identifier, timestamp, and outcome; omit unnecessary secrets and message content.", bullet_style))
    story.append(Paragraph("• <b>AIConversationMetadata:</b> provider/model version, interaction time, safety outcome, and minimal operational metadata. Avoid storing full transcripts by default unless a justified, consented need is established.", bullet_style))

    story.append(Paragraph("5.4 Reminder State Machine", h2_style))
    story.append(Paragraph(
        "Reminder processing must be predictable and auditable. A scheduled reminder transitions to TRIGGERED at its due time. The senior can acknowledge it or snooze it. If the configured deadline expires without acknowledgement, the reminder becomes MISSED and may create a caregiver alert according to the routine urgency and consented alert policy.",
        body_style
    ))

    fig2_path = "milestone 1/figures/figure2_state_machine.png"
    if os.path.exists(fig2_path):
        img_f2 = RLImage(fig2_path, width=6.2*72, height=2.77*72)
        img_f2.hAlign = 'CENTER'
        story.append(img_f2)
        story.append(Spacer(1, 2))

    story.append(Paragraph(
        "<i>Figure 2. Proposed reminder state machine. “Acknowledged” means the user reported a status; it does not independently verify medication ingestion.</i>",
        ParagraphStyle('Cap', fontName='Times-Italic', fontSize=8, leading=11, alignment=TA_CENTER, textColor=MUTED)
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Implementation rules:</b> (1) store timestamps in a consistent server-side format and render them in the user’s time zone; (2) make event processing idempotent so retries do not create duplicate acknowledgements or alerts; (3) define what happens when a snooze would cross the final deadline; (4) record alert attempts and delivery feedback where the provider exposes it; and (5) display network or delivery uncertainty clearly. Emergency alerts must never depend on a generative AI decision.",
        body_style
    ))

    story.append(Paragraph("5.5 Deterministic Activity Scoring", h2_style))
    story.append(Paragraph("Activity scores are intended as descriptive engagement summaries, not clinical metrics. The score should remain within 0–100, be reproducible for identical inputs, and be versioned so later formula changes do not silently rewrite prior results.", body_style))

    story.append(PageBreak()) # -> PAGE 13

    # =========================================================================
    # PAGE 13: 5.5 FORMULA, 5.6 AI ORCHESTRATION, 6.1 FEASIBILITY
    # =========================================================================
    story.append(create_callout(
        title="Proposed baseline formula",
        text="<b>Score = round(100 × (0.60 × A + 0.40 × L))</b><br/>"
             "<b>A</b> = correct valid responses / total valid responses.<br/>"
             "For each valid response i, <b>Lᵢ = clamp(Ttarget / max(Tᵢ, ε), 0.20, 1.00)</b>; <b>L</b> is the mean of Lᵢ across the session. "
             "Ttarget is an activity-specific reference time, Tᵢ is the observed response time, and ε prevents division by zero. "
             "If no valid responses exist, the session is unscored rather than assigned zero.",
        border_color="#0284C7",
        bg_color="#F0F9FF",
        width=500
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "Difficulty is stored as context and used to compare sessions of similar activity and difficulty; it is not multiplied into the score. That avoids the previous design problem in which a difficulty multiplier could produce scores above 100. The response-time target must be tested for each activity and can be adjusted to reduce unnecessary time pressure. Trend views should preferably compare a person with their own prior sessions of comparable activity; no clinical threshold, diagnosis, or population ranking will be displayed.",
        body_style
    ))

    story.append(Paragraph("5.6 AI Orchestration and Fallback", h2_style))
    story.append(Paragraph(
        "The conversational assistant should be accessed through a provider interface so model versions can change without changing care logic. The preferred voice model and endpoint must be selected from the provider’s current documentation at implementation time [11]. The assistant can use a short system policy, minimal context, output limits, and safety filters. It must not schedule medication, determine that an event is missed, interpret activity scores as a diagnosis, or invent whether an alert reached a caregiver.",
        body_style
    ))
    story.append(Paragraph(
        "On timeout, quota exhaustion, or loss of connectivity, the fallback should provide one of a small number of tested messages such as “I can still show your saved routine, but conversation is unavailable right now.” If the application is offline, the interface should clearly distinguish a locally saved event from an event successfully synchronized to the server. The local fallback is a graceful degradation mechanism, not a claim of full offline AI functionality or 100% availability.",
        body_style
    ))

    story.append(Paragraph("6. Feasibility and Risk Management", h1_style))
    story.append(Paragraph("6.1 Feasibility Assessment", h2_style))
    feas_rows = [
        [Paragraph("<b>Dimension</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Assessment</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Condition / evidence needed</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white))],
        [Paragraph("Technical", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK)),
         Paragraph("Feasible for a student team using mainstream web, API, and relational database technologies.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Validate the complete flow in Docker Compose, including scheduled jobs, timezone handling, migrations, and notification failures.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK))],
        [Paragraph("Economic", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK)),
         Paragraph("A software-first PWA avoids requiring dedicated companion hardware.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Estimate hosting, database, notification, and AI-provider costs from actual traffic and usage; no fixed cost is promised in this report.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK))],
        [Paragraph("Operational", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK)),
         Paragraph("The core workflow can be designed around a few primary actions and a caregiver view.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Usability must be assessed with representative users; “zero training required” is not assumed.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK))],
        [Paragraph("Ethical / legal", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.5, textColor=DARK)),
         Paragraph("Consent, role separation, minimal collection, and non-diagnostic limits are design requirements.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Review applicable Indian data-protection requirements, accessibility, consent materials, retention, and any research-ethics needs before user testing.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK))]
    ]
    t_feas = Table(feas_rows, colWidths=[100, 190, 210])
    t_feas.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_feas)

    story.append(PageBreak()) # -> PAGE 14

    # =========================================================================
    # PAGE 14: 6.2 RISK REGISTER
    # =========================================================================
    story.append(Paragraph("6.2 Risk Register", h2_style))
    risk_rows = [
        [Paragraph("<b>Risk</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Impact</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Likelihood</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Mitigation</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white))],
        [Paragraph("Missed/duplicate reminders", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("High", ParagraphStyle('B', fontName='Times-Bold', fontSize=7, textColor=colors.HexColor("#991B1B"))),
         Paragraph("Medium", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Use deterministic transitions, idempotency keys, scheduler monitoring, deadline tests, and event logs.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("AI gives medical or misleading advice", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("High", ParagraphStyle('B', fontName='Times-Bold', fontSize=7, textColor=colors.HexColor("#991B1B"))),
         Paragraph("Medium", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Constrain scope, block diagnosis/dosage changes, minimize sent context, test adversarial prompts, and provide safe escalation language.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("Caregiver gets access without valid consent", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("High", ParagraphStyle('B', fontName='Times-Bold', fontSize=7, textColor=colors.HexColor("#991B1B"))),
         Paragraph("Low–Medium", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Expiring invitation tokens, explicit permission selection, server-side authorization on every request, and revocation tests.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("Network outage hides alert delivery status", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("High", ParagraphStyle('B', fontName='Times-Bold', fontSize=7, textColor=colors.HexColor("#991B1B"))),
         Paragraph("Medium", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Distinguish queued/sent/delivered/unknown where supported; show offline state and never promise remote delivery without confirmation.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("Scores are interpreted as diagnosis", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("High", ParagraphStyle('B', fontName='Times-Bold', fontSize=7, textColor=colors.HexColor("#991B1B"))),
         Paragraph("Medium", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Label results non-diagnostic, avoid clinical thresholds, contextualize trends, and prohibit AI-generated score interpretation as medical judgement.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("Accessibility needs are missed", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Medium–High", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Medium", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Use WCAG 2.2 AA review, keyboard/screen-reader testing, text scaling, and formative usability tests.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("Personal data exposure", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("High", ParagraphStyle('B', fontName='Times-Bold', fontSize=7, textColor=colors.HexColor("#991B1B"))),
         Paragraph("Medium", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Minimize retention, secure sessions, validate authorization, avoid secrets in logs, define deletion, and test data isolation.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("AI provider quota/model changes", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Medium", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Medium", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Provider adapter, configurable model ID, quota/error handling, versioned tests, and rule-based fallback.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("Offline synchronization conflict", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Medium", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Medium", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Record event IDs/timestamps, use idempotent synchronization, define conflict rules, and display unsynchronized changes.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("Project scope exceeds timeline", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Medium", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("High", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Deliver the core routine lifecycle first; make advanced trends and extended conversation optional after the safety-critical path works.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))]
    ]
    t_risk = Table(risk_rows, colWidths=[130, 65, 65, 240])
    t_risk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_risk)

    story.append(PageBreak()) # -> PAGE 15

    # =========================================================================
    # PAGE 15: 6.3 ASSUMPTIONS & 7. VERIFICATION PLAN
    # =========================================================================
    story.append(Paragraph("6.3 Assumptions and Dependencies", h2_style))
    story.append(Paragraph("• The prototype will use synthetic or explicitly approved test data, not real patient records by default.", bullet_style))
    story.append(Paragraph("• Caregiver alert delivery depends on the configured notification channel and network connectivity; delivery guarantees are not assumed.", bullet_style))
    story.append(Paragraph("• Voice features depend on browser/device support and user permission; text interaction remains available as an alternative.", bullet_style))
    story.append(Paragraph("• Cloud AI model availability, latency, quotas, and pricing may change and must be checked near deployment.", bullet_style))
    story.append(Paragraph("• The capstone will not claim a regulated medical-device status, clinical validation, or legal certification.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("7. Verification and Evaluation Plan", h1_style))
    story.append(Paragraph(
        "Quality will be demonstrated by test evidence and documented acceptance criteria, not by an unsupported blanket statement that the system has “100% automated testing” or “100% coverage.” Each test result should name the code revision, environment, number of tests, failures, and coverage method where relevant.",
        body_style
    ))

    test_rows = [
        [Paragraph("<b>Test area</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Planned checks</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Acceptance evidence</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white))],
        [Paragraph("Unit tests", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Reminder transition table, scheduling/time-zone rules, scoring formula, consent/token expiry, and authorization policy.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("All defined state/edge cases have expected results; same inputs yield same scores.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("API integration", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Create routine, trigger reminder, acknowledge/snooze, expire into MISSED, generate alert, and retrieve caregiver view.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("End-to-end API tests pass; transactions remain consistent under retries.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("Security and privacy", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Cross-user IDOR checks, role bypass, expired/revoked invitation, session handling, rate limits, validation, and log inspection.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Negative authorization tests fail closed; no secrets or unnecessary sensitive content appears in logs.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("Accessibility", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Automated WCAG checks plus keyboard-only, focus, text resize, contrast, screen-reader labels, error recovery, and target-size review.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Findings are recorded and high-impact blockers are fixed before user evaluation.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("Performance", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Measure non-AI endpoint latency and local fallback latency under a documented test setup.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Report p50/p95 and environment; assess the 500 ms / 100 ms targets separately.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("Offline and synchronization", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Open cached routines, complete a supported activity, queue a permitted event, reconnect, and retry synchronization.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("No duplicate event is created; unsynchronized status and conflicts are visible.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("AI safety and provider failure", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Test diagnosis/dosage requests, hallucination prompts, timeouts, quota errors, provider/model change, and fallback messaging.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Safety cases return safe constrained behavior; failure paths remain understandable to users.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))],
        [Paragraph("Usability", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Formative task-based evaluation of routine setup, acknowledgement, caregiver pairing, and understanding of status labels.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK)),
         Paragraph("Document task completion, observed friction, feedback, and resulting design changes.", ParagraphStyle('B', fontName='Times-Roman', fontSize=6.8, textColor=DARK))]
    ]
    t_test = Table(test_rows, colWidths=[120, 200, 180])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_test)

    story.append(PageBreak()) # -> PAGE 16

    # =========================================================================
    # PAGE 16: 7.1 SAFEGUARDS, 7.2 METRICS, 8.1 SCHEDULE, 8.2 WBS
    # =========================================================================
    story.append(Paragraph("7.1 Evaluation Safeguards", h2_style))
    story.append(Paragraph(
        "Usability testing involving older adults should proceed only after faculty approval, informed consent, accessible study materials, and a clear process for stopping participation. Do not ask participants to rely on CogniCare for actual medication safety, emergency response, or clinical decisions. Early evaluation should focus on comprehension, navigation, accessibility, and task flow using a non-clinical scenario.",
        body_style
    ))

    story.append(Paragraph("7.2 Metrics to Report", h2_style))
    story.append(Paragraph("• Reminder correctness: expected versus actual state transitions across scheduled, snoozed, acknowledged, and missed scenarios.", bullet_style))
    story.append(Paragraph("• Authorization correctness: successful and rejected access attempts across roles and consent states.", bullet_style))
    story.append(Paragraph("• Latency: p50 and p95 for non-AI endpoints and local fallback responses, with environment stated.", bullet_style))
    story.append(Paragraph("• Accessibility: issues found, severity, remediation status, and manual checks completed against WCAG 2.2 AA.", bullet_style))
    story.append(Paragraph("• Usability: task completion, observed errors, time on task where appropriate, and qualitative feedback.", bullet_style))
    story.append(Paragraph("• AI safety: pass/fail outcomes for a predefined policy test set and behavior under provider errors.", bullet_style))
    story.append(Paragraph("• Offline reliability: synchronization success, duplicate-event rate, and visibility of pending events after reconnect.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("8. Project Plan, Roles and Deliverables", h1_style))
    story.append(Paragraph("8.1 Milestone Schedule", h2_style))
    ms_rows = [
        [Paragraph("<b>Milestone</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Target period</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Planned scope / output</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Status for this report</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white))],
        [Paragraph("Milestone 0", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("August 2026", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Problem selection, initial team charter, background exploration, and project scope.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Reported as completed by the team; supporting artefacts should be retained.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK))],
        [Paragraph("Milestone 1", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("October 2026", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Proposal, requirements, feasibility, risk register, architecture, and presentation.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Current milestone; this document defines the proposal baseline.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK))],
        [Paragraph("Milestone 2", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("November 2026", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Functional prototype of core routine workflow, caregiver pairing, activity catalogue, AI adapter, and initial test evidence.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Planned; do not claim complete until evidence exists.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK))],
        [Paragraph("Final evaluation", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("December 2026", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Integrated demonstration, final report, evaluation findings, code and deployment documentation, technical viva.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Planned.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK))]
    ]
    t_ms = Table(ms_rows, colWidths=[90, 80, 180, 150])
    t_ms.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F8FAFC"), colors.white]),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_ms)
    story.append(Spacer(1, 4))

    story.append(Paragraph("8.2 Work Breakdown Structure", h2_style))
    wbs_rows1 = [
        [Paragraph("<b>Team member</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Primary ownership</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Shared responsibilities</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white))],
        [Paragraph("Deepanshu Chauhan — Team Leader", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("API/domain architecture, backend integration, AI provider adapter, container setup, and report coordination.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Integration planning, safety policy, end-to-end testing, final demo.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK))]
    ]
    t_wbs1 = Table(wbs_rows1, colWidths=[140, 180, 180])
    t_wbs1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_wbs1)

    story.append(PageBreak()) # -> PAGE 17

    # =========================================================================
    # PAGE 17: 8.2 WBS (CONT'D), 8.3 DELIVERABLES, 8.4 DOD, 9.1 LIMITATIONS
    # =========================================================================
    wbs_rows2 = [
        [Paragraph("<b>Team member</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Primary ownership</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white)),
         Paragraph("<b>Shared responsibilities</b>", ParagraphStyle('H', fontName='Times-Bold', fontSize=7.5, textColor=colors.white))],
        [Paragraph("Yash — Frontend", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Senior/caregiver interfaces, responsive layout, accessible controls, PWA interaction, and cognitive activity UI.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Manual accessibility checks, usability feedback, frontend test suite.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK))],
        [Paragraph("Piyush — Data and verification", ParagraphStyle('B', fontName='Times-Roman', fontSize=7.2, textColor=DARK)),
         Paragraph("Relational schema, ORM/migrations, reminder state machine, scoring implementation, and backend test design.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK)),
         Paragraph("Requirement traceability, risk-based tests, consistency checks.", ParagraphStyle('B', fontName='Times-Roman', fontSize=7, textColor=DARK))]
    ]
    t_wbs2 = Table(wbs_rows2, colWidths=[140, 180, 180])
    t_wbs2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0,2), (-1,2), colors.white),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_wbs2)
    story.append(Spacer(1, 4))

    story.append(Paragraph("8.3 Expected Deliverables", h2_style))
    story.append(Paragraph("• Runnable full-stack prototype with documented environment configuration and reproducible startup instructions.", bullet_style))
    story.append(Paragraph("• Senior-facing routine view and caregiver dashboard with consented pairing and role-separated access.", bullet_style))
    story.append(Paragraph("• Deterministic reminder lifecycle, event history, and configurable caregiver-alert policy.", bullet_style))
    story.append(Paragraph("• Non-diagnostic activity catalogue with versioned scoring implementation and descriptive trend view.", bullet_style))
    story.append(Paragraph("• Optional conversational assistant behind a provider adapter and bounded local fallback.", bullet_style))
    story.append(Paragraph("• Automated test report, accessibility findings, security test checklist, and basic performance measurements.", bullet_style))
    story.append(Paragraph("• Architecture diagram, data model, API documentation, user guide, final report, and presentation deck.", bullet_style))

    story.append(Paragraph("8.4 Definition of Done for Milestone 2", h2_style))
    story.append(Paragraph(
        "The prototype is ready for review when the core routine lifecycle can be demonstrated end to end; consent and authorization controls pass negative tests; the reminder state machine and scoring are covered by explicit tests; offline behavior is correctly labelled; major accessibility blockers are resolved; and the team can reproduce the demo from the documented setup. Any incomplete feature or known defect should be listed openly.",
        body_style
    ))

    story.append(Paragraph("9. Limitations and Conclusion", h1_style))
    story.append(Paragraph("9.1 Limitations", h2_style))
    story.append(Paragraph("• Routine acknowledgement is self-reported and does not verify medicine ingestion or other real-world actions.", bullet_style))
    story.append(Paragraph("• Cognitive activity results can be influenced by device, language, fatigue, sensory needs, task difficulty, and familiarity; they are not clinical assessments.", bullet_style))
    story.append(Paragraph("• Caregiver dashboards depend on consent, network access, and accurate recording; absence of data should not be interpreted as proof that an event did not occur.", bullet_style))
    story.append(Paragraph("• Offline access is intentionally limited. Real-time caregiver alerting and cloud AI interactions cannot be guaranteed without connectivity.", bullet_style))
    story.append(Paragraph("• A student prototype cannot establish clinical efficacy, regulatory compliance, or a broad market research gap without further evidence.", bullet_style))

    story.append(PageBreak()) # -> PAGE 18

    # =========================================================================
    # PAGE 18: 9.2 CONCLUSION & REFERENCES [1] TO [12]
    # =========================================================================
    story.append(Paragraph("9.2 Conclusion", h2_style))
    story.append(Paragraph(
        "CogniCare is framed as an accessible routine-support system that connects a senior-facing interface with consent-based caregiver visibility. Its strongest technical principle is separation of concerns: the application’s routine and scoring logic remains deterministic, while AI is limited to optional conversation. The design is feasible as a modular web application, but its success will depend on reliable reminder behavior, meaningful consent, accessible interaction, clear offline limitations, and evidence from testing. The next milestone should focus on a small end-to-end workflow and prove it with tests before expanding the feature set.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("References", h1_style))
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
    ref_style = ParagraphStyle('Ref', fontName='Times-Roman', fontSize=7.2, leading=9.5, textColor=DARK, leftIndent=15, firstLineIndent=-15, spaceAfter=2.5)
    for r in refs:
        story.append(Paragraph(r, ref_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated EXACT 18-PAGE Vector PDF at: {output_path}")

if __name__ == "__main__":
    generate_pdf()
