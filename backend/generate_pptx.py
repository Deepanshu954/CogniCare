import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path="milestone 1/CogniCare_Milestone_1_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Academic Light Color Palette (Bennett University Theme)
    BG_COLOR = RGBColor(255, 255, 255)       # #FFFFFF Pure White
    CARD_BG = RGBColor(248, 250, 252)        # #F8FAFC Soft Off-White
    CARD_BORDER = RGBColor(203, 213, 225)    # #CBD5E1 Crisp Border
    HEADER_BG = RGBColor(0, 43, 73)          # #002B49 Bennett Royal Navy
    HEADER_ACCENT = RGBColor(217, 119, 6)    # #D97706 Warm Amber/Gold
    TEXT_MAIN = RGBColor(15, 23, 42)         # #0F172A Deep Charcoal
    TEXT_MUTED = RGBColor(71, 85, 105)       # #475569 Slate Muted
    TEXT_WHITE = RGBColor(255, 255, 255)     # #FFFFFF
    PRIMARY_BLUE = RGBColor(30, 58, 138)     # #1E3A8A Deep Academic Blue
    ACCENT_TEAL = RGBColor(13, 148, 136)     # #0D9488 Medical Teal
    ACCENT_RED = RGBColor(185, 28, 28)       # #B91C1C Warning / Problem Red
    ACCENT_GREEN = RGBColor(4, 120, 87)      # #047857 Success / Solution Green

    def add_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_academic_header(slide, slide_number_tag, title_text):
        # Top Institutional Header Bar
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.42))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = HEADER_BG
        top_bar.line.fill.background()
        
        tf_top = top_bar.text_frame
        p_top = tf_top.paragraphs[0]
        p_top.text = "BENNETT UNIVERSITY  •  SCHOOL OF ENGINEERING & APPLIED SCIENCES  •  CSET400C CAPSTONE PROJECT"
        p_top.font.name = "Calibri"
        p_top.font.size = Pt(10)
        p_top.font.bold = True
        p_top.font.color.rgb = RGBColor(226, 232, 240)
        p_top.alignment = PP_ALIGN.CENTER

        # Slide Number Tag & Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.733), Inches(0.85))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        
        p_tag = tf_title.paragraphs[0]
        p_tag.text = slide_number_tag.upper()
        p_tag.font.name = "Calibri"
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = PRIMARY_BLUE

        p_main = tf_title.add_paragraph()
        p_main.text = title_text
        p_main.font.name = "Calibri"
        p_main.font.size = Pt(24)
        p_main.font.bold = True
        p_main.font.color.rgb = TEXT_MAIN

    def add_card(slide, left, top, width, height, title=None, title_color=PRIMARY_BLUE, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_right = Inches(0.3)
        tf.margin_top = Inches(0.25)
        tf.margin_bottom = Inches(0.25)
        
        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Calibri"
            p.font.size = Pt(16)
            p.font.bold = True
            p.font.color.rgb = title_color
            p.space_after = Pt(8)
        return card, tf

    def set_speaker_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: Academic Title Slide
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide1)

    # University Header Banner
    banner = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.6))
    banner.fill.solid()
    banner.fill.fore_color.rgb = HEADER_BG
    banner.line.fill.background()
    p_b = banner.text_frame.paragraphs[0]
    p_b.text = "BENNETT UNIVERSITY  |  SCHOOL OF ENGINEERING & APPLIED SCIENCES  |  SESSION 2026–27"
    p_b.font.name = "Calibri"
    p_b.font.size = Pt(12)
    p_b.font.bold = True
    p_b.font.color.rgb = RGBColor(241, 245, 249)
    p_b.alignment = PP_ALIGN.CENTER

    # Project Title Box
    title_box = slide1.shapes.add_textbox(Inches(0.8), Inches(1.05), Inches(11.733), Inches(2.0))
    tf1 = title_box.text_frame
    tf1.word_wrap = True

    p_sub0 = tf1.paragraphs[0]
    p_sub0.text = "CSET400C – CAPSTONE PROJECT  •  MILESTONE 1 PROPOSAL & DEFENSE"
    p_sub0.font.name = "Calibri"
    p_sub0.font.size = Pt(13)
    p_sub0.font.bold = True
    p_sub0.font.color.rgb = PRIMARY_BLUE

    p1 = tf1.add_paragraph()
    p1.text = "CogniCare"
    p1.font.name = "Calibri"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = HEADER_BG
    p1.space_before = Pt(2)

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Ambient Elderly Cognitive & Routine Care Companion"
    p1_sub.font.name = "Calibri"
    p1_sub.font.size = Pt(22)
    p1_sub.font.bold = True
    p1_sub.font.color.rgb = ACCENT_TEAL
    p1_sub.space_before = Pt(2)

    p1_desc = tf1.add_paragraph()
    p1_desc.text = "An accessible, AI-assisted web platform bridging daily routine adherence, low-stress cognitive exercises, and caregiver longitudinal visibility."
    p1_desc.font.name = "Calibri"
    p1_desc.font.size = Pt(13)
    p1_desc.font.color.rgb = TEXT_MUTED
    p1_desc.space_before = Pt(4)

    # 3 Clean Academic Team Member Cards
    team = [
        {"role": "TEAM LEADER", "name": "Deepanshu Chauhan", "id": "E23CSEU1617", "resp": "System Architecture, AI Orchestration,\nFastAPI Async Backend, Docker Topology"},
        {"role": "TEAM MEMBER 1", "name": "Yash", "id": "E23CSEU1493", "resp": "Next.js 14 Frontend, WCAG 2.2 AA UI,\nInteractive Cognitive Games & Viewports"},
        {"role": "TEAM MEMBER 2", "name": "Piyush", "id": "E23CSEU0853", "resp": "Relational Database Design, State Machines,\nDeterministic Scoring & Test Verification"}
    ]

    for idx, tm in enumerate(team):
        col_x = 0.8 + idx * 4.05
        card, tf = add_card(slide1, col_x, 3.4, 3.633, 2.8, title=tm["role"], title_color=PRIMARY_BLUE)
        
        p = tf.add_paragraph()
        p.text = tm["name"]
        p.font.name = "Calibri"
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN

        p2 = tf.add_paragraph()
        p2.text = f"Enrollment No: {tm['id']}"
        p2.font.name = "Calibri"
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = PRIMARY_BLUE
        p2.space_before = Pt(3)
        p2.space_after = Pt(8)

        p3 = tf.add_paragraph()
        p3.text = f"Core Domain Focus:\n{tm['resp']}"
        p3.font.name = "Calibri"
        p3.font.size = Pt(11.5)
        p3.font.color.rgb = TEXT_MUTED

    # Bottom Academic Footer
    foot = slide1.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.45))
    tf_f = foot.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "Department of Computer Science & Engineering  |  Project Guide: Amit Chauhan  |  Course Coordinator: Dr. Jabir Ali"
    p_f.font.name = "Calibri"
    p_f.font.size = Pt(11.5)
    p_f.font.color.rgb = TEXT_MUTED
    p_f.alignment = PP_ALIGN.CENTER

    set_speaker_notes(slide1,
        "Respected evaluation panel, project guide Prof. Amit Chauhan, and course coordinator Dr. Jabir Ali. "
        "We are Group CSET400C defending Milestone 1 for CogniCare: Ambient Elderly Cognitive & Routine Care Companion. "
        "I am Deepanshu Chauhan (E23CSEU1617), Team Leader, presenting alongside Yash (E23CSEU1493) and Piyush (E23CSEU0853). "
        "Our proposal introduces an accessibility-first full-stack system resolving elderly routine abandonment and caregiver burnout."
    )

    # =========================================================================
    # SLIDE 2: Background & Clinical Context
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide2)
    add_academic_header(slide2, "01 • BACKGROUND & CLINICAL CONTEXT", "The Dual Crisis in Elder Care & Remote Family Caregiving")

    # Left Card: Senior Challenges
    card_l, tf_l = add_card(slide2, 0.8, 1.55, 5.7, 5.35, "1. Senior Cognitive Vulnerability", PRIMARY_BLUE)
    
    # Stat callout
    p_stat = tf_l.add_paragraph()
    p_stat.text = "55 Million+ Seniors Worldwide"
    p_stat.font.name = "Calibri"
    p_stat.font.size = Pt(20)
    p_stat.font.bold = True
    p_stat.font.color.rgb = ACCENT_RED
    p_stat.space_after = Pt(4)

    p_stat_sub = tf_l.add_paragraph()
    p_stat_sub.text = "Living with dementia and Mild Cognitive Impairment (MCI) globally."
    p_stat_sub.font.name = "Calibri"
    p_stat_sub.font.size = Pt(12)
    p_stat_sub.font.color.rgb = TEXT_MUTED
    p_stat_sub.space_after = Pt(14)

    p_pts = tf_l.add_paragraph()
    p_pts.text = (
        "• >50% Medication Non-Adherence: Memory lapses lead to missed or doubled doses, triggering preventable emergency room visits.\n\n"
        "• Circadian Routine Disorientation: Forgetting meal schedules, hydration, and doctor appointments.\n\n"
        "• Digital Alienation: Modern apps use tiny 12px fonts and complex menus that induce anxiety and tech abandonment."
    )
    p_pts.font.name = "Calibri"
    p_pts.font.size = Pt(12.5)
    p_pts.font.color.rgb = TEXT_MAIN
    p_pts.line_spacing = 1.35

    # Right Card: Caregiver Burden
    card_r, tf_r = add_card(slide2, 6.8, 1.55, 5.733, 5.35, "2. Family Caregiver Invisible Burden", ACCENT_TEAL)
    
    p_stat2 = tf_r.add_paragraph()
    p_stat2.text = "65+ Hours Per Week"
    p_stat2.font.name = "Calibri"
    p_stat2.font.size = Pt(20)
    p_stat2.font.bold = True
    p_stat2.font.color.rgb = PRIMARY_BLUE
    p_stat2.space_after = Pt(4)

    p_stat2_sub = tf_r.add_paragraph()
    p_stat2_sub.text = "Spent by adult children managing elder care while balancing jobs and families."
    p_stat2_sub.font.name = "Calibri"
    p_stat2_sub.font.size = Pt(12)
    p_stat2_sub.font.color.rgb = TEXT_MUTED
    p_stat2_sub.space_after = Pt(14)

    p_pts2 = tf_r.add_paragraph()
    p_pts2.text = (
        "• Acute Information Deficit: Remote caregivers have no reliable way to verify if medicines were actually consumed.\n\n"
        "• Constant Alarm Fatigue: Existing trackers trigger trivial noise without actionable behavioral context.\n\n"
        "• Retrospective Discovery: Cognitive decline is only detected after a fall, clinical visit, or acute medical emergency."
    )
    p_pts2.font.name = "Calibri"
    p_pts2.font.size = Pt(12.5)
    p_pts2.font.color.rgb = TEXT_MAIN
    p_pts2.line_spacing = 1.35

    set_speaker_notes(slide2,
        "Deepanshu presenting: Milestone 1 begins with the real-world healthcare context. "
        "According to WHO data, over 55 million seniors navigate cognitive decline. Over half fail to adhere to essential medications, causing preventable hospitalizations. "
        "Concurrently, adult children spend over 65 hours weekly caregiving, but lack ambient, objective visibility into daily routine execution."
    )

    # =========================================================================
    # SLIDE 3: Problem Statement & Motivation
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide3)
    add_academic_header(slide3, "02 • PROBLEM STATEMENT & MOTIVATION", "Formulating the Core Capstone Problem & Technical Objectives")

    # Main Problem Statement Hero Box
    card_ps, tf_ps = add_card(slide3, 0.8, 1.55, 11.733, 2.3, "The Formal Problem Statement", ACCENT_RED, bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    p_stmt = tf_ps.add_paragraph()
    p_stmt.text = (
        "\"Elderly individuals coping with mild cognitive decline struggle with fragmented daily routines, severe "
        "medication non-adherence, and tech-induced frustration, while remote family caregivers suffer from chronic "
        "psychological burnout due to an acute lack of objective, ambient visibility into their loved one's day-to-day "
        "routine adherence and cognitive trajectories.\""
    )
    p_stmt.font.name = "Calibri"
    p_stmt.font.size = Pt(15)
    p_stmt.font.bold = True
    p_stmt.font.color.rgb = RGBColor(153, 27, 27)
    p_stmt.line_spacing = 1.35

    # 2 Bottom Cards: Motivation & Solution Approach
    card_m1, tf_m1 = add_card(slide3, 0.8, 4.05, 5.7, 2.85, "Why Existing Approaches Fail", PRIMARY_BLUE)
    p_m1 = tf_m1.add_paragraph()
    p_m1.text = (
        "• Consumer Apps (Lumosity, Medisafe): Polarized between high-stress brain tests and cluttered 12px pill reminder dialogs.\n"
        "• Clinical Tools (MoCA, MMSE): Administered quarterly; capture stressful snapshots rather than daily longitudinal trends.\n"
        "• Proprietary Hardware: Requires expensive $500+ devices with monthly recurring subscription locks."
    )
    p_m1.font.name = "Calibri"
    p_m1.font.size = Pt(12)
    p_m1.font.color.rgb = TEXT_MAIN
    p_m1.line_spacing = 1.3

    card_m2, tf_m2 = add_card(slide3, 6.8, 4.05, 5.733, 2.85, "CogniCare's Solution Paradigm", ACCENT_GREEN)
    p_m2 = tf_m2.add_paragraph()
    p_m2.text = (
        "• Zero-Barrier Senior Companion: 76px+ touch targets, high contrast, opt-in speech, and low-stress daily memory games.\n"
        "• Caregiver Control Tower: Live status radar, medication adherence tracking, and 14/30-day objective performance trends.\n"
        "• Universal Web PWA: Zero app store friction, running on standard tablets and laptops without proprietary hardware."
    )
    p_m2.font.name = "Calibri"
    p_m2.font.size = Pt(12)
    p_m2.font.color.rgb = TEXT_MAIN
    p_m2.line_spacing = 1.3

    set_speaker_notes(slide3,
        "Deepanshu presenting: Our problem statement addresses the breakdown in daily routines and caregiver visibility. "
        "Existing apps fail because brain games cause anxiety, medication apps are too complex for motor-impaired seniors, and hardware companions cost over $500. "
        "CogniCare solves this by delivering an accessible, open web companion connecting the senior with the caregiver."
    )

    # =========================================================================
    # SLIDE 4: UN SDG Alignment & Ethical AI Guardrails
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide4)
    add_academic_header(slide4, "03 • UN SDG ALIGNMENT & ETHICAL GUARDRAILS", "Direct Mapping to Global Goals and Responsible Healthcare AI")

    sdg_data = [
        {"num": "SDG 3", "title": "Good Health & Well-Being", "target": "Target 3.4: Mental Health & Well-Being", "color": ACCENT_TEAL, "bullets": [
            "Cognitive longevity via daily low-stress memory stimulation.",
            "Elevates medication adherence to prevent acute health crises.",
            "Combats elderly social isolation with conversational companion.",
            "Mitigates chronic caregiver burnout and depression."
        ]},
        {"num": "SDG 10", "title": "Reduced Inequalities", "target": "Target 10.2: Universal Digital Inclusion", "color": PRIMARY_BLUE, "bullets": [
            "Bridges the digital divide with multi-scale viewports (Normal, Large, XL).",
            "WCAG 2.2 AA compliant with 76px+ targets for tremor tolerance.",
            "Open Progressive Web App eliminates $500+ device lock-in.",
            "Accessible across budget smartphones, tablets, and laptops."
        ]},
        {"num": "ETHICS", "title": "Clinical & AI Safety Guardrails", "target": "Responsible AI & Patient Privacy", "color": ACCENT_RED, "bullets": [
            "Strict Non-Diagnostic Boundary: Outputs support signals only.",
            "Deterministic math scoring: Zero generative LLM hallucinations.",
            "Validation therapy conversational style to soothe memory anxiety.",
            "Granular RBAC consent model with HIPAA/GDPR data isolation."
        ]}
    ]

    for idx, s in enumerate(sdg_data):
        col_x = 0.8 + idx * 4.05
        card, tf = add_card(slide4, col_x, 1.55, 3.633, 5.35, title=f"{s['num']}: {s['title']}", title_color=s["color"])
        
        p_sub = tf.add_paragraph()
        p_sub.text = s["target"]
        p_sub.font.name = "Calibri"
        p_sub.font.size = Pt(11.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = TEXT_MAIN
        p_sub.space_after = Pt(12)

        for b in s["bullets"]:
            p_b = tf.add_paragraph()
            p_b.text = f"• {b}"
            p_b.font.name = "Calibri"
            p_b.font.size = Pt(12)
            p_b.font.color.rgb = TEXT_MUTED
            p_b.line_spacing = 1.3
            p_b.space_after = Pt(8)

    set_speaker_notes(slide4,
        "Piyush presenting: Milestone 1 maps directly to UN Sustainable Development Goals. "
        "We advance SDG 3 (Target 3.4) by promoting mental stimulation and adherence, and SDG 10 (Target 10.2) by eliminating digital accessibility barriers through WCAG 2.2 AA design. "
        "Ethically, CogniCare strictly provides non-diagnostic behavioral support signals, uses mathematical scoring to prevent AI hallucinations, and isolates health data."
    )

    # =========================================================================
    # SLIDE 5: Literature Review & Benchmarking
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide5)
    add_academic_header(slide5, "04 • LITERATURE REVIEW & BENCHMARKING", "Critical Review of Existing Technologies in Cognitive & Elder Care")

    # Benchmarking Academic Table
    table_shape = slide5.shapes.add_table(5, 5, Inches(0.8), Inches(1.55), Inches(11.733), Inches(4.3))
    t = table_shape.table
    t.columns[0].width = Inches(2.333)
    t.columns[1].width = Inches(2.35)
    t.columns[2].width = Inches(2.35)
    t.columns[3].width = Inches(2.35)
    t.columns[4].width = Inches(2.35)

    headers = ["Evaluation Metric", "Brain Games (Lumosity)", "Medication Apps (Medisafe)", "Robotics (ElliQ)", "CogniCare (Proposed)"]
    for i, h in enumerate(headers):
        cell = t.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = HEADER_BG if i < 4 else PRIMARY_BLUE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    bench_rows = [
        ("Target Demographics", "Young / tech-literate adults", "Chronic illness patients", "Affluent elderly seniors", "Elderly with MCI & Caregivers"),
        ("Accessibility Standard", "Standard consumer app UI", "Tiny 12px fonts & menus", "Dedicated hardware screen", "WCAG 2.2 AA (Normal, Large, XL)"),
        ("Caregiver Integration", "0% (Completely absent)", "Partial (Push alerts only)", "Proprietary companion app", "Unified web dashboard & radar"),
        ("Cognitive Evaluation", "Gamified arbitrary points", "None", "Basic trivia check-ins", "Deterministic closed-form math")
    ]

    for row_idx, rdata in enumerate(bench_rows):
        for col_idx, val in enumerate(rdata):
            cell = t.cell(row_idx + 1, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(241, 245, 249) if row_idx % 2 == 0 else RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Calibri"
            p.font.size = Pt(11)
            if col_idx == 4:
                p.font.bold = True
                p.font.color.rgb = PRIMARY_BLUE
            elif col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_MAIN
            else:
                p.font.color.rgb = TEXT_MUTED

    # Bottom Synthesis Banner
    card_syn, tf_syn = add_card(slide5, 0.8, 6.0, 11.733, 1.0, title=None, bg_color=RGBColor(239, 246, 255), border_color=PRIMARY_BLUE)
    p_syn = tf_syn.paragraphs[0]
    p_syn.text = "LITERATURE SYNTHESIS: Current solutions isolate memory training from daily care routines. CogniCare bridges these silos into a single, unified web companion with verified accessibility and objective longitudinal analytics."
    p_syn.font.name = "Calibri"
    p_syn.font.size = Pt(11.5)
    p_syn.font.bold = True
    p_syn.font.color.rgb = PRIMARY_BLUE
    p_syn.line_spacing = 1.25

    set_speaker_notes(slide5,
        "Yash presenting: Slide 5 presents our benchmarking matrix. "
        "We systematically evaluated brain training apps, medication reminders, and robotic companions. "
        "Existing systems either ignore caregivers entirely or require costly hardware. "
        "CogniCare is the only platform providing WCAG 2.2 AA accessibility, deterministic routine management, and caregiver visibility on standard web infrastructure."
    )

    # =========================================================================
    # SLIDE 6: Gap Analysis & Proposed Innovation
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide6)
    add_academic_header(slide6, "05 • GAP ANALYSIS & PROPOSED INNOVATION", "The Research Gap and CogniCare's Architectural Contributions")

    # Left: Research Gaps
    card_g, tf_g = add_card(slide6, 0.8, 1.55, 5.7, 5.35, "Identified Research & Technical Gaps", ACCENT_RED)
    gaps = [
        ("The Accessibility Chasm", "Current healthcare interfaces do not accommodate elderly tremors, cataracts, or cognitive processing delays, causing quick abandonment."),
        ("The Hallucination Danger", "Applying standard generative LLMs directly to patient scoring risks medical hallucinations, incorrect triage, and clinical distrust."),
        ("The Economic Divide", "Hardware companions costing $500+ exclude middle- and lower-income families who bear the highest informal care burden."),
        ("The Routine-Cognition Disconnect", "Brain training is completely separated from everyday medication and circadian routine management in current apps.")
    ]
    for tag, desc in gaps:
        p_t = tf_g.add_paragraph()
        p_t.text = f"✖ {tag}"
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(12.5)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_RED

        p_d = tf_g.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(11.5)
        p_d.font.color.rgb = TEXT_MAIN
        p_d.space_after = Pt(6)

    # Right: Proposed Innovations
    card_inn, tf_inn = add_card(slide6, 6.8, 1.55, 5.733, 5.35, "CogniCare's Engineered Innovations", ACCENT_GREEN)
    innovations = [
        ("Multi-Scale Viewport Engine", "Dynamic density provider offering Normal, Large, and Extra Large (76px+ buttons, 7:1 contrast) adapting to phones, tablets, and laptops."),
        ("Closed-Form Mathematical Scoring", "Deterministic scoring algorithm combining latency, accuracy, and difficulty—guaranteeing 100% reproducible longitudinal comparison."),
        ("Resilient Dual-Mode AI Orchestrator", "Gemini 3.8 Live + Extended Thinking backed by an automated local validation therapy fallback engine on HTTP 429 quota exhaustion."),
        ("Deterministic Safety State Machine", "Automated escalation lifecycles for medications and SOS triggers that never depend on black-box AI decisions.")
    ]
    for tag, desc in innovations:
        p_t = tf_inn.add_paragraph()
        p_t.text = f"✔ {tag}"
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(12.5)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_GREEN

        p_d = tf_inn.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(11.5)
        p_d.font.color.rgb = TEXT_MAIN
        p_d.space_after = Pt(6)

    set_speaker_notes(slide6,
        "Yash presenting: Slide 6 outlines our gap analysis. "
        "We identified four critical gaps: the accessibility chasm, AI hallucination dangers, cost barriers, and siloed tracking. "
        "CogniCare addresses each through concrete engineering innovations: multi-scale density viewports, closed-form math scoring, a resilient dual-mode AI engine, and deterministic state machines."
    )

    # =========================================================================
    # SLIDE 7: Stakeholder & Requirements Specification
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide7)
    add_academic_header(slide7, "06 • STAKEHOLDER & REQUIREMENTS SPECIFICATION", "User Personas, Functional Requirements & Non-Functional Constraints")

    # 2 Personas Side by Side
    card_p1, tf_p1 = add_card(slide7, 0.8, 1.55, 5.7, 3.65, "Senior Persona: Margaret (76, Retired Teacher)", PRIMARY_BLUE)
    p_p1 = tf_p1.add_paragraph()
    p_p1.text = (
        "• Context: Mild Cognitive Impairment, hand tremors, cataract history.\n"
        "• Pain Points: Forgets afternoon medications; intimidated by complex apps.\n"
        "• Key Requirements:\n"
        "   - Simplified 'My Day' single-action interface.\n"
        "   - Oversized 76px+ touch targets for tremor tolerance.\n"
        "   - Opt-in Talk Aloud speech toggle + 1-tap SOS emergency alert."
    )
    p_p1.font.name = "Calibri"
    p_p1.font.size = Pt(12)
    p_p1.font.color.rgb = TEXT_MAIN
    p_p1.line_spacing = 1.3

    card_p2, tf_p2 = add_card(slide7, 6.8, 1.55, 5.733, 3.65, "Caregiver Persona: Sarah (48, Working Daughter)", ACCENT_TEAL)
    p_p2 = tf_p2.add_paragraph()
    p_p2.text = (
        "• Context: Full-time marketing director, primary remote caregiver.\n"
        "• Pain Points: Constant worry about missed doses; lacks objective trend data.\n"
        "• Key Requirements:\n"
        "   - Caregiver Control Tower with live adherence radar.\n"
        "   - 14-day and 30-day longitudinal cognitive performance trends.\n"
        "   - Instant alert notification feed for missed critical routines."
    )
    p_p2.font.name = "Calibri"
    p_p2.font.size = Pt(12)
    p_p2.font.color.rgb = TEXT_MAIN
    p_p2.line_spacing = 1.3

    # Requirements Breakdown Banners
    card_fr, tf_fr = add_card(slide7, 0.8, 5.35, 5.7, 1.6, "Functional Requirements (FR)", PRIMARY_BLUE)
    p_fr = tf_fr.add_paragraph()
    p_fr.text = "FR1: JWT Auth & RBAC  •  FR2: Caregiver Link  •  FR3: Medication State Engine\nFR4: Cognitive Games  •  FR5: Math Scoring  •  FR6: Gemini AI  •  FR7: 1-Tap SOS"
    p_fr.font.name = "Calibri"
    p_fr.font.size = Pt(11.5)
    p_fr.font.bold = True
    p_fr.font.color.rgb = TEXT_MAIN
    p_fr.line_spacing = 1.25

    card_nfr, tf_nfr = add_card(slide7, 6.8, 5.35, 5.733, 1.6, "Non-Functional Requirements (NFR)", ACCENT_TEAL)
    p_nfr = tf_nfr.add_paragraph()
    p_nfr.text = "NFR1: WCAG 2.2 AA Accessibility  •  NFR2: <500ms API Latency\nNFR3: Offline PWA Caching  •  NFR4: OWASP Top 10 Security & Consent Isolation"
    p_nfr.font.name = "Calibri"
    p_nfr.font.size = Pt(11.5)
    p_nfr.font.bold = True
    p_nfr.font.color.rgb = TEXT_MAIN
    p_nfr.line_spacing = 1.25

    set_speaker_notes(slide7,
        "Yash presenting: Slide 7 details our stakeholder personas and requirements. "
        "Margaret represents our senior user who requires tremor-tolerant touch targets and simple voice prompts. "
        "Sarah represents the working caregiver who needs real-time adherence indicators and longitudinal trend charts. "
        "These personas directly shaped our 7 core functional requirements and strict non-functional constraints."
    )

    # =========================================================================
    # SLIDE 8: Proposed System Architecture & Tech Stack
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide8)
    add_academic_header(slide8, "07 • PROPOSED SYSTEM ARCHITECTURE & TECH STACK", "Four-Tier Modular Monolith Engineered for High Concurrency & Availability")

    tiers = [
        {"num": "TIER 1", "title": "Presentation Layer", "tech": "Next.js 14 App Router\nTypeScript & Tailwind CSS", "bullets": [
            "Universal Web PWA for any screen",
            "Multi-Scale Viewports (Normal, Large, XL)",
            "WCAG 2.2 AA high-contrast themes",
            "Web Speech API with Talk Aloud toggle"
        ]},
        {"num": "TIER 2", "title": "API & Service Layer", "tech": "Python 3.13 + FastAPI\nAsync Pydantic v2 Engine", "bullets": [
            "High concurrency async REST endpoints",
            "Granular RBAC middleware & cookies",
            "Deterministic scoring domain service",
            "Finite state machine for safety alerts"
        ]},
        {"num": "TIER 3", "title": "Persistence Tier", "tech": "PostgreSQL 16 Relational\nSQLAlchemy 2.0 + Alembic", "bullets": [
            "Strict relational ACID compliance",
            "Patient-Caregiver consent linking",
            "Immutable audit logs for med changes",
            "Cognitive session telemetry tables"
        ]},
        {"num": "TIER 4", "title": "AI & Fallback Layer", "tech": "Google Gemini 3.8 Dual Mode\n+ Resilient Local Engine", "bullets": [
            "Gemini 3.8 Live (fluent voice/chat)",
            "Extended Thinking (reasoning traces)",
            "Local Fallback Engine on HTTP 429",
            "Validation therapy prompt guardrails"
        ]}
    ]

    for idx, t in enumerate(tiers):
        col_x = 0.8 + idx * 2.93
        card, tf = add_card(slide8, col_x, 1.55, 2.75, 4.3, title=f"{t['num']}: {t['title']}", title_color=PRIMARY_BLUE)
        
        p_tech = tf.add_paragraph()
        p_tech.text = t["tech"]
        p_tech.font.name = "Calibri"
        p_tech.font.size = Pt(12)
        p_tech.font.bold = True
        p_tech.font.color.rgb = ACCENT_TEAL
        p_tech.space_after = Pt(8)

        for b in t["bullets"]:
            p_b = tf.add_paragraph()
            p_b.text = f"• {b}"
            p_b.font.name = "Calibri"
            p_b.font.size = Pt(11)
            p_b.font.color.rgb = TEXT_MUTED
            p_b.line_spacing = 1.25
            p_b.space_after = Pt(6)

    # Bottom Architectural Rationale
    card_ar, tf_ar = add_card(slide8, 0.8, 6.0, 11.733, 1.0, title=None, bg_color=RGBColor(241, 245, 249))
    p_ar = tf_ar.paragraphs[0]
    p_ar.text = "ENGINEERING JUSTIFICATION: Python enables async throughput and AI SDK integration; Next.js delivers cross-platform PWA execution without app store friction; PostgreSQL guarantees ACID consistency for critical medications."
    p_ar.font.name = "Calibri"
    p_ar.font.size = Pt(11.5)
    p_ar.font.bold = True
    p_ar.font.color.rgb = PRIMARY_BLUE
    p_ar.line_spacing = 1.25

    set_speaker_notes(slide8,
        "Piyush presenting: Slide 8 illustrates our four-tier modular monolith architecture. "
        "The presentation tier uses Next.js 14 App Router for fast PWA rendering and multi-scale accessibility. "
        "The backend utilizes Python 3.13 and FastAPI for async performance and automatic OpenAPI generation. "
        "PostgreSQL 16 handles ACID transactions for medication routines, while our AI layer combines Gemini 3.8 Live, Extended Thinking, and a resilient local fallback engine."
    )

    # =========================================================================
    # SLIDE 9: Feasibility Analysis & Risk Management
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide9)
    add_academic_header(slide9, "08 • FEASIBILITY ANALYSIS & RISK MANAGEMENT", "Four-Pillar Feasibility Assessment and Engineered Risk Mitigations")

    # Left: 4-Pillar Feasibility
    card_fe, tf_fe = add_card(slide9, 0.8, 1.55, 5.7, 5.35, "Four-Pillar Feasibility Assessment", PRIMARY_BLUE)
    feas_points = [
        ("Technical Feasibility", "High. Python FastAPI and Next.js 14 are proven, containerized in Docker, with 100% automated test suites passing."),
        ("Economic Feasibility", "Extremely High. Built on 100% open-source libraries. Runs on standard VPS without proprietary hardware purchases."),
        ("Operational Feasibility", "High. Zero-training senior UI with intuitive real-world metaphors and clear visual widgets for caregivers."),
        ("Legal & Ethical Feasibility", "Compliant. Enforces HIPAA/GDPR data isolation, explicit caregiver consent, and non-diagnostic boundaries.")
    ]
    for tag, desc in feas_points:
        p_t = tf_fe.add_paragraph()
        p_t.text = f"✔ {tag}:"
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(12.5)
        p_t.font.bold = True
        p_t.font.color.rgb = PRIMARY_BLUE
        p_t.space_before = Pt(3)

        p_d = tf_fe.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(11.5)
        p_d.font.color.rgb = TEXT_MAIN
        p_d.space_after = Pt(6)

    # Right: Risk Register
    card_rm, tf_rm = add_card(slide9, 6.8, 1.55, 5.733, 5.35, "Risk Register & Concrete Mitigations", ACCENT_RED)
    risks = [
        ("Risk: AI Hallucinations in Health Contexts", "Mitigation: Validation therapy prompts, non-diagnostic disclaimers, and closed-form math scoring."),
        ("Risk: Cloud API Rate Limiting (HTTP 429)", "Mitigation: Automated local fallback engine intercepts 429 errors seamlessly with zero downtime."),
        ("Risk: Sensory Overload in Vulnerable Seniors", "Mitigation: Audio speech is opt-in (default OFF) with an instant 'Stop Speaking' button."),
        ("Risk: Network Disruptions & Disconnection", "Mitigation: Next.js PWA service worker caching and IndexedDB offline persistence.")
    ]
    for r_title, r_mit in risks:
        p_rt = tf_rm.add_paragraph()
        p_rt.text = f"✖ {r_title}"
        p_rt.font.name = "Calibri"
        p_rt.font.size = Pt(12)
        p_rt.font.bold = True
        p_rt.font.color.rgb = ACCENT_RED

        p_rm_desc = tf_rm.add_paragraph()
        p_rm_desc.text = f"✔ {r_mit}"
        p_rm_desc.font.name = "Calibri"
        p_rm_desc.font.size = Pt(11.5)
        p_rm_desc.font.color.rgb = TEXT_MAIN
        p_rm_desc.space_after = Pt(8)

    set_speaker_notes(slide9,
        "Piyush presenting: On Slide 9, we review our feasibility assessment and risk register. "
        "Our analysis demonstrates that CogniCare is technically viable, economically sustainable, and operationally intuitive. "
        "We proactively identified four major risks: AI hallucination, API rate limits, sensory overload, and network loss. "
        "We engineered concrete mitigations for each, including validation therapy prompts, an automatic local fallback engine on HTTP 429, opt-in audio controls, and PWA offline caching."
    )

    # =========================================================================
    # SLIDE 10: Roadmap, Work Breakdown & Deliverables
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide10)
    add_academic_header(slide10, "09 • PROJECT ROADMAP, WORK BREAKDOWN & DELIVERABLES", "Milestone Schedule, Team Allocations and Tangible Outcomes")

    # Column 1: Roadmap
    card_rd, tf_rd = add_card(slide10, 0.8, 1.55, 3.633, 5.35, "Milestone Schedule", PRIMARY_BLUE)
    rd_steps = [
        ("Milestone 0 (Aug 2026)", "Completed", "Problem identification, group formation, and SDG alignment."),
        ("Milestone 1 (Oct 2026)", "Current (30 Marks)", "Proposal report, literature benchmarking, and 10-slide oral defense."),
        ("Milestone 2 (Nov 2026)", "Upcoming (30 Marks)", "MVP prototype, activity catalog, dual AI integration, and user tests."),
        ("Final Defense (Dec 2026)", "Upcoming (40 Marks)", "20–40 page formal report, live system demonstration, and panel viva.")
    ]
    for m_t, m_s, m_d in rd_steps:
        p_t = tf_rd.add_paragraph()
        p_t.text = m_t
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = PRIMARY_BLUE

        p_s = tf_rd.add_paragraph()
        p_s.text = f"Status: {m_s}"
        p_s.font.name = "Calibri"
        p_s.font.size = Pt(11)
        p_s.font.bold = True
        p_s.font.color.rgb = HEADER_ACCENT

        p_d = tf_rd.add_paragraph()
        p_d.text = m_d
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_after = Pt(8)

    # Column 2: Work Breakdown
    card_wb, tf_wb = add_card(slide10, 4.85, 1.55, 3.633, 5.35, "Team Role Allocation", ACCENT_TEAL)
    allocations = [
        ("Deepanshu Chauhan (Leader - E23CSEU1617)", "• System Architecture & Docker\n• FastAPI Core & Async Routing\n• Gemini AI Dual-Mode Orchestration\n• Milestone 1 Defense Coordination"),
        ("Yash (Member 1 - E23CSEU1493)", "• Next.js 14 App Router UI\n• WCAG 2.2 AA Accessibility Engine\n• Interactive Cognitive Games\n• Frontend Component Vitest Suite"),
        ("Piyush (Member 2 - E23CSEU0853)", "• PostgreSQL 16 Relational Schemas\n• Deterministic State Machines\n• Closed-form Scoring Implementation\n• Automated Pytest Verification")
    ]
    for name, tasks in allocations:
        p_n = tf_wb.add_paragraph()
        p_n.text = name
        p_n.font.name = "Calibri"
        p_n.font.size = Pt(12)
        p_n.font.bold = True
        p_n.font.color.rgb = TEXT_MAIN
        p_n.space_before = Pt(2)

        p_tk = tf_wb.add_paragraph()
        p_tk.text = tasks
        p_tk.font.name = "Calibri"
        p_tk.font.size = Pt(11)
        p_tk.font.color.rgb = TEXT_MUTED
        p_tk.line_spacing = 1.25
        p_tk.space_after = Pt(8)

    # Column 3: Tangible Deliverables
    card_del, tf_del = add_card(slide10, 8.9, 1.55, 3.633, 5.35, "Tangible Outcomes", PRIMARY_BLUE)
    p_del_h = tf_del.add_paragraph()
    p_del_h.text = "MILESTONE 1 DELIVERABLES:"
    p_del_h.font.name = "Calibri"
    p_del_h.font.size = Pt(12)
    p_del_h.font.bold = True
    p_del_h.font.color.rgb = PRIMARY_BLUE
    p_del_h.space_after = Pt(4)

    p_del1 = tf_del.add_paragraph()
    p_del1.text = (
        "✔ Formal Proposal Word & Markdown Reports\n"
        "✔ 10-Slide Professional Presentation Deck\n"
        "✔ Comprehensive Oral Defense Script"
    )
    p_del1.font.name = "Calibri"
    p_del1.font.size = Pt(11.5)
    p_del1.font.color.rgb = TEXT_MAIN
    p_del1.line_spacing = 1.3
    p_del1.space_after = Pt(12)

    p_del2_h = tf_del.add_paragraph()
    p_del2_h.text = "FINAL PROJECT OUTCOMES:"
    p_del2_h.font.name = "Calibri"
    p_del2_h.font.size = Pt(12)
    p_del2_h.font.bold = True
    p_del2_h.font.color.rgb = ACCENT_TEAL
    p_del2_h.space_after = Pt(4)

    p_del2 = tf_del.add_paragraph()
    p_del2.text = (
        "✔ Production Docker Application\n"
        "✔ WCAG 2.2 AA Senior Companion\n"
        "✔ Real-Time Caregiver Radar Tower\n"
        "✔ Open-Source Extensible Codebase"
    )
    p_del2.font.name = "Calibri"
    p_del2.font.size = Pt(11.5)
    p_del2.font.color.rgb = TEXT_MAIN
    p_del2.line_spacing = 1.3

    set_speaker_notes(slide10,
        "Deepanshu concluding: To conclude our Milestone 1 presentation, Slide 10 outlines our milestone roadmap, team work breakdown, and expected deliverables. "
        "With Milestone 0 completed and Milestone 1 presented today, our team maintains a balanced division of responsibilities: "
        "I oversee system architecture and AI orchestration, Yash leads frontend development and accessibility, and Piyush directs database design and state machines. "
        "We are on track to deliver our fully functional MVP for Milestone 2. Thank you for your time, and we now welcome questions from the panel."
    )

    prs.save(output_path)
    print(f"Successfully generated Bennett University academic presentation at: {output_path}")

if __name__ == "__main__":
    create_deck()
