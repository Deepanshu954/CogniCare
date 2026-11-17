import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_milestone_2_pptx(out_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    BG_DARK = RGBColor(15, 23, 42)      # Slate 900
    BG_CARD = RGBColor(30, 41, 59)      # Slate 800
    TEXT_LIGHT = RGBColor(248, 250, 252) # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184) # Slate 400
    ACCENT_SKY = RGBColor(56, 189, 248)  # Sky 400
    ACCENT_INDIGO = RGBColor(129, 140, 248) # Indigo 400
    ACCENT_GREEN = RGBColor(52, 211, 153) # Emerald 400
    ACCENT_RED = RGBColor(248, 113, 113)  # Red 400

    def add_header(slide, title, subtitle):
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()

        # Header Box
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT

        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.size = Pt(13)
        p2.font.color.rgb = ACCENT_SKY

        # Accent Bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.04))
        bar.fill.solid()
        bar.fill.fore_color.rgb = ACCENT_SKY
        bar.line.fill.background()

    def add_card(slide, left, top, width, height, title, items, color=ACCENT_SKY):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = BG_CARD
        box.line.color.rgb = color
        box.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = color

        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = f"• {it}"
            p_it.font.size = Pt(12)
            p_it.font.color.rgb = TEXT_LIGHT

    # --- Slide 1: Title ---
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_DARK
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "BENNETT UNIVERSITY\nSchool of Computer Science Engineering & Technology"
    p.font.size = Pt(16)
    p.font.color.rgb = TEXT_MUTED

    p = tf1.add_paragraph()
    p.text = "CSET400C – CAPSTONE PROJECT (Semester VII • 2026–27)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO

    p = tf1.add_paragraph()
    p.text = "\nCogniCare: An Ambient AI-Powered Cognitive Care & Routine Monitoring Companion"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT

    p = tf1.add_paragraph()
    p.text = "Milestone-2: System Design, MVP Implementation & Initial Validation (30 Marks)\n"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_SKY

    p = tf1.add_paragraph()
    p.text = "Team Leader: Deepanshu Chauhan (E23CSEU1617) | Members: Yash (E23CSEU1493), Piyush (E23CSEU0853)\nProject Guide: Amit Chauhan | Course Coordinator: Dr. Jabir Ali"
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # --- Slide 2: The Healthcare Challenge ---
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "The Healthcare Problem: Dementia & Caregiver Burnout", "Global scale, clinical challenges, and the assistive care gap")
    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "The Cognitive Decline Crisis", [
        "55+ million individuals worldwide live with dementia (WHO).",
        "Projected to reach 139 million by 2050.",
        "Early Mild Cognitive Impairment (MCI) causes routine forgetfulness and disorientation.",
        "Existing solutions are complex, inaccessible, or clinical in nature.",
        "Seniors feel stigmatized by traditional cognitive test batteries."
    ], ACCENT_RED)
    add_card(s2, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0), "Informal Family Caregiver Strain", [
        "Family caregivers provide 80%+ of dementia care worldwide.",
        "Constant anxiety over missed critical medications (Donepezil, Memantine).",
        "Lack of objective longitudinal visibility into cognitive performance trajectories.",
        "Caregivers experience severe burnout, stress, and career interruptions.",
        "Need for an ambient, non-intrusive companion that connects loved ones safely."
    ], ACCENT_SKY)

    # --- Slide 3: System Philosophy ---
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "System Philosophy: Deterministic vs. Generative Separation", "The fundamental architectural principle governing CogniCare")
    add_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Deterministic Core (System of Record)", [
        "FastAPI backend microservices & PostgreSQL 16 persistence.",
        "Reminder State Machine: Scheduled, Acknowledged, Snoozed, Skipped, Missed.",
        "Mathematical Scoring: Accuracy (40%), Latency (30%), Completion (20%), Level (10%).",
        "Deterministic adherence percentage calculation from confirmed database logs.",
        "Immutable AuditLog recording actor IDs and timestamps."
    ], ACCENT_GREEN)
    add_card(s3, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0), "Generative AI Companion (Service Adapter)", [
        "Powered by Google Gemini 1.5/2.0 API with Web Speech STT/TTS.",
        "Strictly grounded in daily database context via get_today_tasks tool.",
        "Medical Guardrail Filter: categorical refusal of diagnostic or medication alteration requests.",
        "Provides empathetic companionship, navigation aid, and weekly plain-language summaries.",
        "Architecturally barred from modifying clinical schedules or medical records."
    ], ACCENT_INDIGO)

    # --- Slide 4: 4-Tier Architecture ---
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "System Architecture: 4-Tier Decoupled Clean Design", "High modularity, clear separation of concerns, and containerized deployment")
    add_card(s4, Inches(0.8), Inches(1.8), Inches(2.7), Inches(5.0), "Tier 1: Presentation", [
        "Next.js 14 App Router",
        "TypeScript & Tailwind",
        "72px+ touch targets",
        "WCAG AAA contrast",
        "Lucide React icons",
        "Service Worker PWA"
    ], ACCENT_SKY)
    add_card(s4, Inches(3.8), Inches(1.8), Inches(2.7), Inches(5.0), "Tier 2: API Gateway", [
        "FastAPI ASGI (Uvicorn)",
        "JWT HS256 auth",
        "BCrypt 12 rounds",
        "Multi-tenant RBAC",
        "Auth rate limiting",
        "RFC 7807 exceptions"
    ], ACCENT_INDIGO)
    add_card(s4, Inches(6.8), Inches(1.8), Inches(2.7), Inches(5.0), "Tier 3: Domain Core", [
        "Reminder State Engine",
        "Cognitive Activity Suite",
        "Math Scoring Engine",
        "Rolling 7d/30d baselines",
        "Support signal triggers",
        "Weekly report builder"
    ], ACCENT_GREEN)
    add_card(s4, Inches(9.8), Inches(1.8), Inches(2.7), Inches(5.0), "Tier 4: Storage & AI", [
        "PostgreSQL 16 ACID",
        "SQLAlchemy 2.0 ORM",
        "Immutable Audit Logs",
        "Gemini Provider Adapter",
        "Context Tool Calling",
        "Deterministic Mock AI"
    ], ACCENT_RED)

    # --- Slide 5: Elderly Experience ---
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Senior Companion Experience: Accessible 'My Day' UI", "Human-centered design tailored for seniors with cognitive decline")
    add_card(s5, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0), "Oversized 'Next Up' Hero", [
        "Single most urgent pending item.",
        "Eliminates decision paralysis.",
        "Massive 72px green tap target: 'I did this!'.",
        "Instant positive feedback.",
        "Automatic caregiver sync."
    ], ACCENT_GREEN)
    add_card(s5, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0), "Care Routine Checklist", [
        "High-contrast color badges.",
        "Prescriptions, meals, hydration.",
        "Snooze (15 min) & Skip options.",
        "Clear visual state indicators.",
        "Zero nested menus or clutter."
    ], ACCENT_SKY)
    add_card(s5, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0), "Accessibility Features", [
        "3 dynamic display modes: Normal, Large, XL Senior.",
        "Web Speech audio feedback.",
        "High-legibility typography.",
        "5-second protected SOS trigger.",
        "Offline caching resilience."
    ], ACCENT_INDIGO)

    # --- Slide 6: Cognitive Activity Suite ---
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Interactive Cognitive Suite: 4 Neuropsychological Domains", "Empirical game modules capturing accuracy, latency, and consistency")
    add_card(s6, Inches(0.8), Inches(1.8), Inches(2.7), Inches(5.0), "1. Visual Memory", [
        "Pattern recall game.",
        "Vintage household items.",
        "5-second study window.",
        "Distractor identification.",
        "Evaluates visual retention."
    ], ACCENT_SKY)
    add_card(s6, Inches(3.8), Inches(1.8), Inches(2.7), Inches(5.0), "2. Working Memory", [
        "Number sequence recall.",
        "Forward & reverse spans.",
        "Graduated span lengths.",
        "Assesses executive memory.",
        "Calm retry mechanism."
    ], ACCENT_INDIGO)
    add_card(s6, Inches(6.8), Inches(1.8), Inches(2.7), Inches(5.0), "3. Attention Stroop", [
        "Classic Stroop color test.",
        "Conflicting ink & word stimuli.",
        "Measures inhibitory control.",
        "Latency recorded in ms.",
        "Standardized cognitive trial."
    ], ACCENT_RED)
    add_card(s6, Inches(9.8), Inches(1.8), Inches(2.7), Inches(5.0), "4. Spatial Clock", [
        "Clock orientation matching.",
        "Visual hour/minute angles.",
        "Compass directional tasks.",
        "Spatial reasoning index.",
        "Clear celebratory modals."
    ], ACCENT_GREEN)

    # --- Slide 7: Mathematical Scoring Pipeline ---
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Mathematical Cognitive Scoring & Longitudinal Baselines", "Reproducible evaluation formula independent of LLM hallucinations")
    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "4-Factor Scoring Formula", [
        "Accuracy Score: S_acc = (C_correct / C_total) * 40",
        "Latency Efficiency: S_lat = max(0, 1 - (T_resp - T_target) / (T_max - T_target)) * 30",
        "Completion Rate: S_comp = (N_answered / N_expected) * 20",
        "Difficulty Weight: S_diff = (Level / 3) * 10",
        "Total Composite Score: S_session = S_acc + S_lat + S_comp + S_diff in [0, 100]",
        "Objective, mathematical, 100% deterministic."
    ], ACCENT_SKY)
    add_card(s7, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0), "Longitudinal Baseline & Signals", [
        "Rolling 7-day and 30-day baseline averages (mu and sigma).",
        "Calculates individual performance variance.",
        "Trend Classification: STABLE, IMPROVING, VARIABLE, DECLINING.",
        "Support Signal: emitted when score < mu - 1.5 * sigma over 3 consecutive trials.",
        "Alerts caregiver to review care plan without alarming the senior."
    ], ACCENT_GREEN)

    # --- Slide 8: Caregiver Command Tower ---
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Caregiver Command Tower: Oversight & Analytical Intelligence", "Real-time compliance monitoring, trend visualization, and alert triage")
    add_card(s8, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0), "Adherence Gauge", [
        "Live SVG radial progress gauge.",
        "Calculates exact % compliance.",
        "Updates instantly upon acknowledgment.",
        "Tracks medication doses taken.",
        "Distinguishes snoozed vs missed."
    ], ACCENT_GREEN)
    add_card(s8, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0), "30-Day Trend Curves", [
        "Interactive Recharts SVG curves.",
        "Plots composite scores vs baseline.",
        "Filterable by domain (Memory, Attention).",
        "Identifies subtle longitudinal trends.",
        "Empirical evidence for doctor visits."
    ], ACCENT_SKY)
    add_card(s8, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0), "Alert Resolution & Reports", [
        "Real-time triage feed (SOS, Missed).",
        "1-click acknowledge & resolve.",
        "Mandatory clinical resolution notes.",
        "Weekly AI report generator.",
        "Clean print/PDF export layout."
    ], ACCENT_INDIGO)

    # --- Slide 9: AI Companion & Safety Guardrails ---
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "AI Assistant: Grounded Context & Medical Guardrails", "Empathetic conversational companion with strict safety boundaries")
    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Context-Grounded Tool Execution", [
        "Integrated via Google Gemini 1.5/2.0 API Live connection.",
        "Structured tool calling: get_today_tasks, get_upcoming_reminders.",
        "Senior can ask: 'What pills do I take tonight?'",
        "Assistant queries live database and replies with exact scheduled names and times.",
        "Empathetic tone designed to soothe anxious seniors."
    ], ACCENT_SKY)
    add_card(s9, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0), "Strict Medical Safety Filter", [
        "Categorical refusal of diagnostic inquiries ('Do I have Alzheimer's?').",
        "Categorical refusal to modify prescriptions or dosages.",
        "Standardized safety refusal message advising physician contact.",
        "Zero write permissions to healthcare tables.",
        "100% verified in automated test suite (test_assistant.py)."
    ], ACCENT_RED)

    # --- Slide 10: Testing & Verification ---
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Automated Testing & Quality Verification", "Rigorous verification: 100% test pass rate across backend and frontend")
    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Backend Pytest Integration Suite", [
        "15 automated test scenarios executed with Pytest.",
        "100% pass rate (15/15 passed).",
        "87% overall statement coverage (target >= 70%).",
        "Cognition API: 100% | Reports API: 100% | Patients: 95%.",
        "Safety API: 90% | Care API: 89% | Assistant: 84%.",
        "Verified across 3 consecutive runs with 0 flakiness."
    ], ACCENT_GREEN)
    add_card(s10, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0), "Frontend Vitest Unit Suite", [
        "11 test specifications with 23 individual tests.",
        "100% pass rate (23/23 passed).",
        "Tested: SosButton, PatientHeader, TrendChart, AdherenceGauge, TodayCard, Navbar, uiScaleContext.",
        "Next.js ESLint verified with 0 warnings & 0 errors.",
        "Next.js 14 production build compiled all 12 routes cleanly."
    ], ACCENT_INDIGO)

    # --- Slide 11: Containerization & Deployment ---
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Containerization & Deployment Architecture", "Production-ready Docker Compose topology with non-root containers")
    add_card(s11, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0), "cognicare-db", [
        "PostgreSQL 16 Alpine image.",
        "Persistent volume: pgdata.",
        "Internal port 5432.",
        "Healthcheck: pg_isready.",
        "ACID guarantees & auto-seed."
    ], ACCENT_SKY)
    add_card(s11, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0), "cognicare-backend", [
        "Multi-stage Python 3.13 image.",
        "Non-root 'appuser' account.",
        "Exposes port 8000.",
        "Liveness check: /health/live.",
        "Uncompressed size: 456 MB."
    ], ACCENT_INDIGO)
    add_card(s11, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0), "cognicare-frontend", [
        "Multi-stage Next.js 14 image.",
        "Standalone Node.js output.",
        "Non-root 'nextjs' user.",
        "Exposes port 3000.",
        "Uncompressed size: 234 MB (< 300MB target)."
    ], ACCENT_GREEN)

    # --- Slide 12: Live Demonstration Flow ---
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Demonstration Flow: 4-Step Live Walkthrough", "Sequential scenario demonstrating elderly and caregiver interactions")
    add_card(s12, Inches(0.8), Inches(1.8), Inches(2.7), Inches(5.0), "Step 1: Senior Login", [
        "1-click quick login as Margaret.",
        "Role-based routing to /app/my-day.",
        "High-contrast banner & greeting.",
        "Next Up hero displays evening Donepezil (10mg)."
    ], ACCENT_SKY)
    add_card(s12, Inches(3.8), Inches(1.8), Inches(2.7), Inches(5.0), "Step 2: Log Adherence", [
        "Senior taps massive 'I did this!' button.",
        "Card transitions to checked.",
        "Database updates reminder status to ACKNOWLEDGED.",
        "AuditLog entry written."
    ], ACCENT_GREEN)
    add_card(s12, Inches(6.8), Inches(1.8), Inches(2.7), Inches(5.0), "Step 3: Play Game", [
        "Senior navigates to /app/activities.",
        "Launches Visual Memory Pairs.",
        "5s study window & choice recall.",
        "Score (92/100) computed mathematically and stored."
    ], ACCENT_INDIGO)
    add_card(s12, Inches(9.8), Inches(1.8), Inches(2.7), Inches(5.0), "Step 4: Caregiver", [
        "Caregiver logs into /caregiver/dashboard.",
        "Observes 100% adherence gauge.",
        "Inspects 30-day cognitive trend curve.",
        "Generates weekly report with AI summary."
    ], ACCENT_RED)

    # --- Slide 13: Conclusion & Next Steps ---
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Conclusion & Roadmap to Final Evaluation", "Milestone-2 completed successfully (30/30 Marks Target)")
    add_card(s13, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Milestone-2 Achievements", [
        "All 13 required syllabus deliverables 100% completed.",
        "Fully functional, demonstrable MVP with elderly & caregiver portals.",
        "Compiler-grade test suite: 15 backend tests (87% cov), 23 frontend tests.",
        "Mathematical scoring formula & rolling variance engine operational.",
        "Production-ready multi-stage Docker containerization."
    ], ACCENT_GREEN)
    add_card(s13, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0), "Roadmap to Final Evaluation (40 Marks)", [
        "Extend multi-week longitudinal data simulation for sensitivity analysis.",
        "Finalize 30-page Final Capstone Mini-Report per Chapter 12 guidelines.",
        "Conduct team mock viva-voce technical defense sessions.",
        "Package public demo and live deployment URLs.",
        "Ready for final panel demonstration and defense."
    ], ACCENT_SKY)

    prs.save(out_path)
    print(f"Generated PPTX: {out_path}")

if __name__ == '__main__':
    create_milestone_2_pptx('milestone 2/CogniCare_Milestone_2_Presentation.pptx')
    create_milestone_2_pptx('final_submission/CogniCare_Final_Presentation.pptx')
