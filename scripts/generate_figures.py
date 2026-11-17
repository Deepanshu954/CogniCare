import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_system_architecture(out_path):
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_facecolor('#0f172a')
    fig.patch.set_facecolor('#0f172a')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Title
    ax.text(7, 7.5, 'CogniCare: 4-Tier Decoupled System Architecture', ha='center', va='center',
            fontsize=16, fontweight='bold', color='#f8fafc', fontfamily='sans-serif')
    ax.text(7, 7.1, 'Separation of Deterministic System of Record from Generative AI Services', ha='center', va='center',
            fontsize=11, color='#94a3b8', fontfamily='sans-serif')

    # Tier 1: Client Layer
    box_t1 = patches.FancyBboxPatch((0.5, 4.8), 3.8, 1.8, boxstyle="round,pad=0.15",
                                    ec="#38bdf8", fc="#1e293b", lw=2)
    ax.add_patch(box_t1)
    ax.text(2.4, 6.3, 'Tier 1: Accessible Presentation Layer', ha='center', fontsize=11, fontweight='bold', color='#38bdf8')
    ax.text(2.4, 5.8, '• Next.js 14 App Router (React, TypeScript)\n• Accessible Senior UI (72px+ touch, AAA contrast)\n• Caregiver Command Tower (Recharts, Alerts)\n• Service Worker PWA (Offline Asset Caching)',
            ha='center', va='center', fontsize=9, color='#e2e8f0')

    # Tier 2: API Gateway & Security
    box_t2 = patches.FancyBboxPatch((5.1, 4.8), 3.8, 1.8, boxstyle="round,pad=0.15",
                                    ec="#818cf8", fc="#1e293b", lw=2)
    ax.add_patch(box_t2)
    ax.text(7.0, 6.3, 'Tier 2: API Gateway & Security Layer', ha='center', fontsize=11, fontweight='bold', color='#818cf8')
    ax.text(7.0, 5.8, '• FastAPI REST Application Framework\n• Multi-Tenant RBAC & Consent Verifier\n• Rate Limiter (20 req/min for Auth)\n• Global RFC 7807 Exception Sanitizer',
            ha='center', va='center', fontsize=9, color='#e2e8f0')

    # Tier 3: Deterministic Core & Scoring
    box_t3 = patches.FancyBboxPatch((0.5, 1.8), 6.0, 2.4, boxstyle="round,pad=0.15",
                                    ec="#34d399", fc="#1e293b", lw=2)
    ax.add_patch(box_t3)
    ax.text(3.5, 3.8, 'Tier 3: Deterministic Business & Scoring Core', ha='center', fontsize=11, fontweight='bold', color='#34d399')
    ax.text(3.5, 2.9, '• Reminder & Escalation State Machine (Sched/Ack/Snooze/Skip/Missed)\n• Cognitive Activity Session Engine (4 Domains: Memory, Attention, Working, Spatial)\n• Longitudinal Trend & Baseline Analyzer (7d & 30d Rolling Windows, Z-Scores)\n• Safety & Alert Dispatch Engine (1-Click SOS, Caregiver Escalation)\n• Code-Calculated Adherence & Caregiver Weekly Report Builder',
            ha='center', va='center', fontsize=9, color='#e2e8f0')

    # Tier 4: Storage & AI Providers
    box_t4 = patches.FancyBboxPatch((7.5, 1.8), 6.0, 2.4, boxstyle="round,pad=0.15",
                                    ec="#f472b6", fc="#1e293b", lw=2)
    ax.add_patch(box_t4)
    ax.text(10.5, 3.8, 'Tier 4: Enterprise Persistence & AI Provider Layer', ha='center', fontsize=11, fontweight='bold', color='#f472b6')
    ax.text(10.5, 2.9, '• PostgreSQL 16 (Relational DB with ACID transactions)\n• SQLAlchemy 2.0 ORM & Automated Migrations\n• Audit Logging Repository (Actor traceability, UUIDs)\n• Gemini 1.5/2.0 AI Provider Adapter (Live API, Audio STT/TTS)\n• Strict Medical Safety Guardrail Filter (Rejects Diagnostic Claims)\n• Deterministic MockAIProvider (Offline/Testing Fallback)',
            ha='center', va='center', fontsize=9, color='#e2e8f0')

    # Tier 0: Deployment / Infra
    box_t0 = patches.FancyBboxPatch((0.5, 0.4), 13.0, 0.9, boxstyle="round,pad=0.1",
                                    ec="#64748b", fc="#1e293b", lw=1.5, ls="--")
    ax.add_patch(box_t0)
    ax.text(7.0, 0.85, 'Deployment & Containerization: Multi-Stage Docker Compose (PostgreSQL 16, Python 3.13, Next.js Standalone, Non-Root Users, CI/CD Pipeline)',
            ha='center', va='center', fontsize=9, fontweight='semibold', color='#cbd5e1')

    # Arrows
    arrow_props = dict(arrowstyle="->", lw=2, color="#38bdf8")
    ax.annotate("", xy=(5.0, 5.7), xytext=(4.4, 5.7), arrowprops=arrow_props)
    ax.annotate("", xy=(2.4, 4.3), xytext=(2.4, 4.7), arrowprops=dict(arrowstyle="->", lw=2, color="#818cf8"))
    ax.annotate("", xy=(7.0, 4.3), xytext=(7.0, 4.7), arrowprops=dict(arrowstyle="->", lw=2, color="#818cf8"))
    ax.annotate("", xy=(7.4, 3.0), xytext=(6.6, 3.0), arrowprops=dict(arrowstyle="<->", lw=2, color="#34d399"))

    plt.tight_layout()
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")

def draw_cognitive_scoring_pipeline(out_path):
    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
    ax.set_facecolor('#0f172a')
    fig.patch.set_facecolor('#0f172a')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Title
    ax.text(7, 6.5, 'Cognitive Activity Scoring & Longitudinal Trend Pipeline', ha='center', va='center',
            fontsize=15, fontweight='bold', color='#f8fafc')
    ax.text(7, 6.1, 'Mathematical, Deterministic Scoring Formula & Baseline Variance Analysis', ha='center', va='center',
            fontsize=10.5, color='#94a3b8')

    steps = [
        ('1. Raw Game Capture', '• Accuracy (0/1)\n• Latency (ms)\n• Attempts Count\n• Difficulty Weight', '#38bdf8', (0.5, 2.5)),
        ('2. Dimension Scoring', '• S_acc = Acc * 40\n• S_lat = Lat_eff * 30\n• S_comp = Comp * 20\n• S_diff = Diff * 10', '#818cf8', (3.8, 2.5)),
        ('3. Session Composite', 'S_session = \nSUM(Scores)\nRange: [0, 100]\nDomain Tagged', '#34d399', (7.1, 2.5)),
        ('4. Baseline & Trends', '• Rolling 7d & 30d Means\n• Variance & Z-Scores\n• Trend Direction: Stable,\n  Improving, Declining', '#f59e0b', (10.4, 2.5))
    ]

    for title, desc, color, (x, y) in steps:
        box = patches.FancyBboxPatch((x, y), 2.8, 2.6, boxstyle="round,pad=0.15",
                                     ec=color, fc="#1e293b", lw=2)
        ax.add_patch(box)
        ax.text(x + 1.4, y + 2.2, title, ha='center', fontsize=11, fontweight='bold', color=color)
        ax.text(x + 1.4, y + 1.0, desc, ha='center', va='center', fontsize=9, color='#e2e8f0')

    # Arrows between steps
    for x in [3.4, 6.7, 10.0]:
        ax.annotate("", xy=(x + 0.3, 3.8), xytext=(x, 3.8),
                    arrowprops=dict(arrowstyle="->", lw=2.5, color="#f8fafc"))

    # Bottom Clinical & Action Box
    box_action = patches.FancyBboxPatch((0.5, 0.5), 12.7, 1.4, boxstyle="round,pad=0.15",
                                       ec="#ef4444", fc="#1e293b", lw=1.5)
    ax.add_patch(box_action)
    ax.text(6.85, 1.5, 'Clinical Safety & Support Signal Decision Engine', ha='center', fontsize=11, fontweight='bold', color='#ef4444')
    ax.text(6.85, 0.95, 'IF score < baseline - 1.5 * sigma over 3 consecutive sessions:\n  -> Emit Support Signal (DECLINING_EFFICIENCY) to Caregiver Tower with objective empirical evidence.\n  -> Generate Plain-Language Narrative in Weekly Care Report WITHOUT Diagnostic Stigma.',
            ha='center', va='center', fontsize=9, color='#cbd5e1')

    plt.tight_layout()
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")

def draw_reminder_state_machine(out_path):
    fig, ax = plt.subplots(figsize=(13, 6.5), dpi=300)
    ax.set_facecolor('#0f172a')
    fig.patch.set_facecolor('#0f172a')
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    ax.text(6.5, 6.0, 'Reminder Lifecycle & Escalation State Machine', ha='center', va='center',
            fontsize=15, fontweight='bold', color='#f8fafc')
    ax.text(6.5, 5.6, 'Deterministic Care State Transitions & Missed Dose Alert Escalation', ha='center', va='center',
            fontsize=10.5, color='#94a3b8')

    states = [
        ('SCHEDULED', 'Initial State\nGenerated daily from\nPrescriptions & Routines', '#38bdf8', (0.8, 3.0)),
        ('SNOOZED', 'Temporary Pause\n15-min countdown\nRe-alerts senior', '#f59e0b', (4.8, 4.2)),
        ('ACKNOWLEDGED', 'Terminal State (Success)\nTimestamp captured\nAdherence logged', '#22c55e', (4.8, 1.8)),
        ('SKIPPED', 'Explicit Action\nCaregiver documented\nNon-adherence reason', '#a855f7', (8.8, 4.2)),
        ('MISSED / ESCALATED', 'Critical Warning\nThreshold exceeded\nCaregiver alert pushed', '#ef4444', (8.8, 1.8))
    ]

    for title, desc, color, (x, y) in states:
        box = patches.FancyBboxPatch((x, y), 2.8, 1.8, boxstyle="round,pad=0.12",
                                     ec=color, fc="#1e293b", lw=2)
        ax.add_patch(box)
        ax.text(x + 1.4, y + 1.45, title, ha='center', fontsize=10.5, fontweight='bold', color=color)
        ax.text(x + 1.4, y + 0.65, desc, ha='center', va='center', fontsize=8.5, color='#e2e8f0')

    # Transitions
    ax.annotate("Senior taps 'I did this'", xy=(4.7, 2.7), xytext=(3.7, 3.6),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#22c55e"), fontsize=8, color="#22c55e")
    ax.annotate("Senior taps 'Snooze'", xy=(4.7, 4.8), xytext=(3.7, 4.1),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#f59e0b"), fontsize=8, color="#f59e0b")
    ax.annotate("Senior taps 'Skip'", xy=(8.7, 4.8), xytext=(7.7, 4.8),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#a855f7"), fontsize=8, color="#a855f7")
    ax.annotate("Timeout (>60m)", xy=(8.7, 2.7), xytext=(7.7, 2.7),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#ef4444"), fontsize=8, color="#ef4444")

    # Legend / Note
    box_legend = patches.FancyBboxPatch((0.8, 0.5), 11.4, 0.8, boxstyle="round,pad=0.1",
                                        ec="#64748b", fc="#1e293b", lw=1)
    ax.add_patch(box_legend)
    ax.text(6.5, 0.9, 'All state changes generate an immutable AuditLog entry recording Actor ID, timestamp, and transition context.',
            ha='center', va='center', fontsize=9, color='#94a3b8')

    plt.tight_layout()
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")

def draw_test_verification_matrix(out_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    fig.patch.set_facecolor('#0f172a')
    for ax in [ax1, ax2]:
        ax.set_facecolor('#1e293b')
        ax.tick_params(colors='#e2e8f0', labelsize=9)
        for spine in ax.spines.values():
            spine.set_color('#334155')

    fig.suptitle('CogniCare: Automated Test Verification & Statement Coverage', fontsize=15, fontweight='bold', color='#f8fafc', y=0.98)

    # Left: Coverage by Subsystem
    modules = ['Cognition API', 'Reports API', 'Care Service', 'Patients API', 'Safety API', 'Assistant Service', 'Overall Core']
    coverage = [100, 100, 89, 95, 90, 84, 87]
    bars = ax1.barh(modules, coverage, color='#38bdf8', edgecolor='#0284c7', height=0.6)
    ax1.set_xlim(0, 110)
    ax1.axvline(70, color='#ef4444', linestyle='--', linewidth=1.5, label='Target Minimum (70%)')
    ax1.set_xlabel('Statement Coverage (%)', color='#e2e8f0', fontweight='bold', fontsize=10)
    ax1.set_title('Backend Test Coverage by Router & Service', color='#f8fafc', fontsize=12, fontweight='bold', pad=10)
    ax1.legend(loc='lower right', facecolor='#0f172a', edgecolor='#334155', labelcolor='#e2e8f0')

    for bar, val in zip(bars, coverage):
        ax1.text(val + 1.5, bar.get_y() + bar.get_height()/2, f'{val}%', va='center', color='#f8fafc', fontweight='bold', fontsize=8.5)

    # Right: Test Suite Pass Matrix
    suites = ['Backend Pytest', 'Frontend Vitest', 'Docker Compose', 'Security OWASP', 'E2E Flakiness (3x)']
    pass_rates = [100, 100, 100, 100, 100]
    bars2 = ax2.bar(suites, pass_rates, color=['#34d399', '#818cf8', '#f59e0b', '#ec4899', '#06b6d4'], edgecolor='#0f172a', width=0.5)
    ax2.set_ylim(0, 115)
    ax2.set_ylabel('Verification Pass Rate (%)', color='#e2e8f0', fontweight='bold', fontsize=10)
    ax2.set_title('Test Suite Execution & Determinism (100% Pass)', color='#f8fafc', fontsize=12, fontweight='bold', pad=10)
    plt.setp(ax2.get_xticklabels(), rotation=15, ha='right')

    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval + 2, 'PASS (100%)', ha='center', va='bottom', color='#f8fafc', fontweight='bold', fontsize=8.5)

    plt.tight_layout()
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")

if __name__ == '__main__':
    for d in ['milestone 2/figures', 'final_submission/figures']:
        draw_system_architecture(os.path.join(d, 'figure1_system_architecture.png'))
        draw_cognitive_scoring_pipeline(os.path.join(d, 'figure2_cognitive_scoring_pipeline.png'))
        draw_reminder_state_machine(os.path.join(d, 'figure3_reminder_state_machine.png'))
        draw_test_verification_matrix(os.path.join(d, 'figure4_test_verification_matrix.png'))
