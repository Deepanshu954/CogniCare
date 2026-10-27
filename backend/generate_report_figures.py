import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("milestone 1/figures", exist_ok=True)

# -------------------------------------------------------------
# Figure 1: Proposed CogniCare Architecture
# -------------------------------------------------------------
def generate_figure1():
    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')

    # Title
    ax.text(50, 57, "Proposed CogniCare Architecture", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#0F2C59', fontfamily='serif')

    # Layer 1: Presentation Layer
    p1 = patches.FancyBboxPatch((25, 44), 50, 10, boxstyle="round,pad=0.8,rounding_size=2",
                                facecolor='#F8FAFC', edgecolor='#0F2C59', linewidth=1.5)
    ax.add_patch(p1)
    ax.text(50, 51.5, "PRESENTATION LAYER", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0F2C59')
    ax.text(50, 48.5, "Senior PWA: My Day, reminders, games, SOS", ha='center', va='center', fontsize=8, color='#334155')
    ax.text(50, 46.0, "Caregiver dashboard: routines, alerts, trends\nNext.js App Router • TypeScript • accessible UI",
            ha='center', va='center', fontsize=7.5, color='#475569')

    # Arrow 1 -> 2
    ax.annotate('', xy=(50, 37.5), xytext=(50, 44),
                arrowprops=dict(arrowstyle="->", color='#0F2C59', lw=1.2))
    ax.text(50, 40.5, "HTTPS / JSON", ha='center', va='center', fontsize=7.5, color='#0D6E85', fontweight='bold',
            bbox=dict(boxstyle='square,pad=0.2', facecolor='white', edgecolor='none'))

    # Layer 2: API & Routing Layer
    p2 = patches.FancyBboxPatch((25, 29), 50, 8.5, boxstyle="round,pad=0.8,rounding_size=2",
                                facecolor='#F8FAFC', edgecolor='#0F2C59', linewidth=1.5)
    ax.add_patch(p2)
    ax.text(50, 35.2, "API & ROUTING LAYER", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0F2C59')
    ax.text(50, 32.5, "FastAPI • REST /api/v1 • Pydantic validation", ha='center', va='center', fontsize=8, color='#334155')
    ax.text(50, 30.2, "Authentication / authorization • request limits", ha='center', va='center', fontsize=7.5, color='#475569')

    # Arrow 2 -> 3
    ax.annotate('', xy=(50, 22.5), xytext=(50, 29),
                arrowprops=dict(arrowstyle="->", color='#0F2C59', lw=1.2))
    ax.text(50, 25.5, "validated requests", ha='center', va='center', fontsize=7.5, color='#0D6E85',
            bbox=dict(boxstyle='square,pad=0.2', facecolor='white', edgecolor='none'))

    # Layer 3: Domain / Application Services
    p3 = patches.FancyBboxPatch((22, 13), 56, 9.5, boxstyle="round,pad=0.8,rounding_size=2",
                                facecolor='#F8FAFC', edgecolor='#0F2C59', linewidth=1.5)
    ax.add_patch(p3)
    ax.text(50, 20.2, "DOMAIN / APPLICATION SERVICES", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0F2C59')
    ax.text(50, 17.5, "Routine scheduler & reminder state machine", ha='center', va='center', fontsize=8, color='#334155')
    ax.text(50, 15.3, "Consent and role access • deterministic scoring", ha='center', va='center', fontsize=8, color='#334155')
    ax.text(50, 13.5, "Caregiver alerts • audit events • AI orchestration", ha='center', va='center', fontsize=7.5, color='#475569')

    # Bottom Split: Layer 4 Left (Data & Integration) & Right (Safety Boundary)
    # Down arrow left
    ax.annotate('', xy=(24, 8.5), xytext=(35, 13),
                arrowprops=dict(arrowstyle="->", color='#0F2C59', lw=1.2))
    ax.text(28, 10.5, "transactions / provider adapters", ha='center', va='center', fontsize=7, color='#0D6E85')

    # Up arrow right
    ax.annotate('', xy=(65, 13), xytext=(65, 8.5),
                arrowprops=dict(arrowstyle="->", color='#0F2C59', lw=1.2))
    ax.text(67, 10.5, "results / provider status", ha='center', va='center', fontsize=7, color='#0D6E85')

    # Layer 4 Left: Data & Integration Boundary
    p4 = patches.FancyBboxPatch((2, 1), 44, 7.5, boxstyle="round,pad=0.6,rounding_size=1.5",
                                facecolor='#F8FAFC', edgecolor='#0F2C59', linewidth=1.2)
    ax.add_patch(p4)
    ax.text(24, 6.8, "DATA & INTEGRATION BOUNDARY", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F2C59')
    ax.text(24, 4.8, "PostgreSQL • SQLAlchemy • Alembic migrations", ha='center', va='center', fontsize=7.5, color='#334155')
    ax.text(24, 3.2, "Notification adapter • Gemini Live API adapter", ha='center', va='center', fontsize=7.5, color='#334155')
    ax.text(24, 1.8, "Rule-based local response fallback", ha='center', va='center', fontsize=7.5, color='#475569')

    # Layer 4 Right: Safety Boundary Callout
    p5 = patches.FancyBboxPatch((50, 1), 48, 7.5, boxstyle="round,pad=0.6,rounding_size=1.5",
                                facecolor='#FFFBEB', edgecolor='#D97706', linewidth=1.2)
    ax.add_patch(p5)
    ax.text(74, 6.5, "Safety boundary: AI does not decide medication states,", ha='center', va='center',
            fontsize=7.5, fontweight='bold', color='#92400E')
    ax.text(74, 4.8, "calculate scores, diagnose, or change treatment.", ha='center', va='center',
            fontsize=7.5, fontweight='bold', color='#92400E')
    ax.text(74, 3.0, "Local fallback supports only bounded, pre-approved responses;", ha='center', va='center',
            fontsize=7.2, color='#78350F')
    ax.text(74, 1.5, "cloud AI and live alerts require connectivity.", ha='center', va='center',
            fontsize=7.2, color='#78350F')

    plt.tight_layout()
    output_path = "milestone 1/figures/figure1_architecture.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated Figure 1 at {output_path}")

# -------------------------------------------------------------
# Figure 2: Proposed Reminder State Machine
# -------------------------------------------------------------
def generate_figure2():
    fig, ax = plt.subplots(figsize=(8.5, 3.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 45)
    ax.axis('off')

    # Title
    ax.text(50, 42, "Proposed Reminder State Machine", ha='center', va='center',
            fontsize=11.5, fontweight='bold', color='#0F2C59', fontfamily='serif')

    # State: SCHEDULED
    p_sch = patches.FancyBboxPatch((4, 21), 15, 6, boxstyle="round,pad=0.5,rounding_size=3",
                                  facecolor='#F1F5F9', edgecolor='#0F2C59', linewidth=1.4)
    ax.add_patch(p_sch)
    ax.text(11.5, 24, "SCHEDULED", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F2C59')

    # Arrow SCHEDULED -> TRIGGERED
    ax.annotate('', xy=(31, 24), xytext=(19, 24),
                arrowprops=dict(arrowstyle="->", color='#0F2C59', lw=1.2))
    ax.text(25, 26, "due time", ha='center', va='center', fontsize=7.5, color='#475569')

    # State: TRIGGERED
    p_trg = patches.FancyBboxPatch((31, 21), 15, 6, boxstyle="round,pad=0.5,rounding_size=3",
                                  facecolor='#F1F5F9', edgecolor='#0F2C59', linewidth=1.4)
    ax.add_patch(p_trg)
    ax.text(38.5, 24, "TRIGGERED", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F2C59')

    # State: SNOOZED (above)
    p_snz = patches.FancyBboxPatch((44, 32), 15, 6, boxstyle="round,pad=0.5,rounding_size=3",
                                  facecolor='#F1F5F9', edgecolor='#0F2C59', linewidth=1.4)
    ax.add_patch(p_snz)
    ax.text(51.5, 35, "SNOOZED", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F2C59')

    # TRIGGERED -> SNOOZED
    ax.annotate('', xy=(44, 35), xytext=(38.5, 27),
                arrowprops=dict(arrowstyle="->", color='#0F2C59', lw=1.1, connectionstyle="arc3,rad=-0.15"))
    ax.text(38, 33, "snooze", ha='center', va='center', fontsize=7, color='#475569')

    # SNOOZED -> TRIGGERED
    ax.annotate('', xy=(42, 27), xytext=(48, 32),
                arrowprops=dict(arrowstyle="->", color='#0F2C59', lw=1.1, connectionstyle="arc3,rad=-0.15"))
    ax.text(48, 28, "snooze ends", ha='center', va='center', fontsize=7, color='#475569')

    # State: ACKNOWLEDGED (center-right)
    p_ack = patches.FancyBboxPatch((55, 20.5), 18, 7, boxstyle="round,pad=0.5,rounding_size=3",
                                  facecolor='#ECFDF5', edgecolor='#059669', linewidth=1.4)
    ax.add_patch(p_ack)
    ax.text(64, 25, "ACKNOWLEDGED", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#065F46')
    ax.text(64, 22.5, "(user-reported)", ha='center', va='center', fontsize=7.2, fontstyle='italic', color='#047857')

    # TRIGGERED -> ACKNOWLEDGED
    ax.annotate('', xy=(55, 24), xytext=(46, 24),
                arrowprops=dict(arrowstyle="->", color='#059669', lw=1.2))
    ax.text(50.5, 22.5, "confirm", ha='center', va='center', fontsize=7.5, color='#047857')

    # State: MISSED (lower right)
    p_msd = patches.FancyBboxPatch((68, 8), 12, 6, boxstyle="round,pad=0.5,rounding_size=3",
                                  facecolor='#FEF2F2', edgecolor='#DC2626', linewidth=1.4)
    ax.add_patch(p_msd)
    ax.text(74, 11, "MISSED", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#991B1B')

    # TRIGGERED -> MISSED
    ax.annotate('', xy=(68, 12), xytext=(44, 21),
                arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.1, connectionstyle="arc3,rad=0.2"))
    ax.text(53, 14, "deadline expires", ha='center', va='center', fontsize=7, color='#DC2626')

    # SNOOZED -> MISSED
    ax.annotate('', xy=(72, 14), xytext=(59, 34),
                arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.1, connectionstyle="arc3,rad=-0.1"))
    ax.text(67, 28, "final deadline expires", ha='center', va='center', fontsize=7, color='#DC2626')

    # State: CAREGIVER ALERT (far right)
    p_alr = patches.FancyBboxPatch((84, 7.5), 15, 7, boxstyle="round,pad=0.5,rounding_size=3",
                                  facecolor='#FEF2F2', edgecolor='#B91C1C', linewidth=1.4)
    ax.add_patch(p_alr)
    ax.text(91.5, 12, "CAREGIVER ALERT", ha='center', va='center', fontsize=8, fontweight='bold', color='#991B1B')
    ax.text(91.5, 9.5, "(delivery status logged)", ha='center', va='center', fontsize=6.8, fontstyle='italic', color='#7F1D1D')

    # MISSED -> CAREGIVER ALERT
    ax.annotate('', xy=(84, 11), xytext=(80, 11),
                arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.2))
    ax.text(82, 13, "critical schedule / policy", ha='center', va='center', fontsize=6.5, color='#991B1B')

    plt.tight_layout()
    output_path = "milestone 1/figures/figure2_state_machine.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated Figure 2 at {output_path}")

if __name__ == "__main__":
    generate_figure1()
    generate_figure2()
