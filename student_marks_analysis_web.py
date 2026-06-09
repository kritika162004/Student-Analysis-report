"""
Student Performance Analysis  ·  Analysis + Live Web Dashboard
==============================================================
  1. Average Marks per Subject
  2. Top-Performing Students
  + Launches a beautiful HTML dashboard in your browser
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import base64, io, webbrowser, tempfile, os

# ──────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────
CSV_PATH = r"C:/Users/Dell/Downloads/student_dataset.csv"
SUBJECTS = ["Math", "Physics", "Chemistry", "English"]

PALETTE = {
    "bg":      "#F7F9FC", "card":    "#FFFFFF",
    "grid":    "#E4EAF2", "text":    "#1A202C", "muted":   "#718096",
    "math":    "#4361EE", "physics": "#F72585",
    "chem":    "#4CC9F0", "english": "#F9C74F",
    "gold":    "#F4A261", "silver":  "#A8DADC",
    "bronze":  "#E76F51", "p4":      "#8338EC", "p5":      "#06D6A0",
}
SUB_COLORS = [PALETTE["math"], PALETTE["physics"], PALETTE["chem"], PALETTE["english"]]
TOP_COLORS = [PALETTE["gold"], PALETTE["silver"], PALETTE["bronze"], PALETTE["p4"], PALETTE["p5"]]


# ══════════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════════
df = pd.read_csv(CSV_PATH)
print(f"  Loaded {len(df)} students × {len(df.columns)} columns")


# ══════════════════════════════════════════════════════════════════
# ANALYSIS 1 — AVERAGE MARKS PER SUBJECT
# ══════════════════════════════════════════════════════════════════
sub_avg = df[SUBJECTS].mean().round(2)
sub_std = df[SUBJECTS].std().round(2)
sub_min = df[SUBJECTS].min()
sub_max = df[SUBJECTS].max()
sub_med = df[SUBJECTS].median()

print("\n" + "=" * 52)
print("  1. AVERAGE MARKS PER SUBJECT")
print("=" * 52)
stats_df = pd.DataFrame({"Mean": sub_avg, "Median": sub_med,
                          "Std": sub_std, "Min": sub_min, "Max": sub_max})
print(stats_df.to_string())
print(f"\n  Strongest : {sub_avg.idxmax()} ({sub_avg.max()})")
print(f"  Weakest   : {sub_avg.idxmin()} ({sub_avg.min()})")


# ══════════════════════════════════════════════════════════════════
# ANALYSIS 2 — TOP-PERFORMING STUDENTS
# ══════════════════════════════════════════════════════════════════
df["Study_Norm"] = (df["Study_Hours"] / df["Study_Hours"].max()) * 100
df["Composite"]  = (
    0.60 * df["Percentage"] +
    0.20 * df["Attendance"] +
    0.20 * df["Study_Norm"]
).round(2)

toppers = df.sort_values("Composite", ascending=False).head(5).reset_index(drop=True)

print("\n" + "=" * 52)
print("  2. TOP-PERFORMING STUDENTS")
print("=" * 52)
print("  Formula: 60% Score + 20% Attendance + 20% Study\n")
medals_txt = ["Gold", "Silver", "Bronze", "4th", "5th"]
for i, row in toppers.iterrows():
    print(f"  [{medals_txt[i]:<7}] {row['Name']:<10} "
          f"Score:{row['Percentage']:>5.1f}%  Att:{row['Attendance']:>3}%  "
          f"Study:{row['Study_Hours']:>4}h  → Composite:{row['Composite']:>6.1f}")

print(f"\n  Class average : {df['Percentage'].mean():.1f}%")
print(f"  Grade-A count : {(df['Grade'] == 'A').sum()} students")


# ══════════════════════════════════════════════════════════════════
# MATPLOTLIB CHARTS → base64 PNGs for embedding in HTML
# ══════════════════════════════════════════════════════════════════
def fig_to_b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                facecolor=PALETTE["bg"])
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

def style_ax(ax, title, ylabel=""):
    ax.set_facecolor(PALETTE["bg"])
    ax.set_title(title, fontweight="bold", color=PALETTE["text"],
                 fontsize=10, pad=8, loc="left")
    ax.set_ylabel(ylabel, color=PALETTE["muted"], fontsize=8)
    ax.tick_params(colors=PALETTE["muted"], labelsize=8)
    ax.grid(color=PALETTE["grid"], linestyle="--", linewidth=0.6, axis="y")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(PALETTE["grid"])

print("\n  Generating charts …")

# ── Chart A: Grouped bar — avg marks per subject ─────────────────
fig1, ax1 = plt.subplots(figsize=(7, 3.8), facecolor=PALETTE["bg"])
x, w = np.arange(len(SUBJECTS)), 0.20
for (label, vals, alpha), offs in zip(
        [("Mean", sub_avg, 1.0), ("Median", sub_med, 0.6),
         ("Min", sub_min, 0.35), ("Max", sub_max, 0.2)],
        [-1.5, -0.5, 0.5, 1.5]):
    ax1.bar(x + offs * w, vals, width=w, color=SUB_COLORS,
            alpha=alpha, edgecolor="white", linewidth=0.5)
mean_bars = ax1.bar(x - 1.5 * w, sub_avg, width=w,
                    color=SUB_COLORS, edgecolor="white", linewidth=0.5)
for bar, val in zip(mean_bars, sub_avg):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
             f"{val:.1f}", ha="center", va="bottom", fontsize=8,
             fontweight="bold", color=PALETTE["text"])
ax1.set_xticks(x); ax1.set_xticklabels(SUBJECTS); ax1.set_ylim(40, 110)
ax1.legend(["Mean", "Median", "Min", "Max"], fontsize=7.5, ncol=4,
           framealpha=0, labelcolor=PALETTE["muted"], loc="upper right")
style_ax(ax1, "Average Marks per Subject", "Marks")
plt.tight_layout()
chart_a = fig_to_b64(fig1); plt.close(fig1)

# ── Chart B: Error-bar — mean ± std ──────────────────────────────
fig2, ax2 = plt.subplots(figsize=(3.6, 3.8), facecolor=PALETTE["bg"])
xp = np.arange(len(SUBJECTS))
ax2.bar(xp, sub_avg, color=SUB_COLORS, alpha=0.75,
        edgecolor="white", linewidth=0.6, width=0.52)
ax2.errorbar(xp, sub_avg, yerr=sub_std, fmt="none",
             ecolor=PALETTE["text"], elinewidth=1.6, capsize=5, capthick=1.6)
ax2.set_xticks(xp); ax2.set_xticklabels(SUBJECTS); ax2.set_ylim(50, 108)
style_ax(ax2, "Mean ± Std Dev", "Marks")
plt.tight_layout()
chart_b = fig_to_b64(fig2); plt.close(fig2)

# ── Chart C: Radar — top-3 subject profile ───────────────────────
fig3 = plt.figure(figsize=(3.8, 3.8), facecolor=PALETTE["bg"])
ax3  = fig3.add_subplot(111, polar=True)
angles = np.linspace(0, 2 * np.pi, len(SUBJECTS), endpoint=False).tolist()
angles += angles[:1]
ax3.set_facecolor(PALETTE["bg"])
ax3.set_theta_offset(np.pi / 2); ax3.set_theta_direction(-1)
ax3.set_xticks(angles[:-1]); ax3.set_xticklabels(SUBJECTS, color=PALETTE["muted"], fontsize=8)
ax3.set_ylim(50, 100); ax3.set_yticks([60, 75, 90])
ax3.set_yticklabels(["60", "75", "90"], color=PALETTE["muted"], fontsize=6.5)
ax3.grid(color=PALETTE["grid"], linewidth=0.6)
ax3.spines["polar"].set_visible(False)
for i, row in toppers.head(3).iterrows():
    vals = [row[s] for s in SUBJECTS] + [row[SUBJECTS[0]]]
    ax3.plot(angles, vals, color=TOP_COLORS[i], linewidth=1.8)
    ax3.fill(angles, vals, color=TOP_COLORS[i], alpha=0.12)
ax3.set_title("Top-3 Subject Profile", fontweight="bold",
              color=PALETTE["text"], fontsize=10, pad=14)
ax3.legend(toppers.head(3)["Name"].tolist(), fontsize=7.5,
           framealpha=0, labelcolor=PALETTE["muted"],
           loc="lower right", bbox_to_anchor=(1.4, -0.05))
plt.tight_layout()
chart_c = fig_to_b64(fig3); plt.close(fig3)

# ── Chart D: Horizontal bar — composite ranking ───────────────────
fig4, ax4 = plt.subplots(figsize=(11, 3.2), facecolor=PALETTE["bg"])
names_r  = toppers["Name"].tolist()[::-1]
scores_r = toppers["Composite"].tolist()[::-1]
h_bars   = ax4.barh(names_r, scores_r, color=TOP_COLORS[::-1],
                    edgecolor="white", linewidth=0.8, height=0.48)
for bar, val, row in zip(h_bars, scores_r, toppers.iloc[::-1].itertuples()):
    ax4.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
             f"{val:.1f}", va="center", fontsize=9.5,
             fontweight="bold", color=PALETTE["text"])
    ax4.text(1.0, bar.get_y() + bar.get_height() / 2,
             f"Score: {row.Percentage:.0f}%    Attendance: {row.Attendance}%"
             f"    Study: {row.Study_Hours}h/day    Grade: {row.Grade}",
             va="center", fontsize=8.5, color="white", fontweight="bold")
ax4.set_xlim(0, 110); ax4.set_facecolor(PALETTE["bg"])
ax4.grid(color=PALETTE["grid"], linestyle="--", linewidth=0.6, axis="x")
ax4.spines[["top", "right"]].set_visible(False)
ax4.spines[["left", "bottom"]].set_color(PALETTE["grid"])
ax4.tick_params(colors=PALETTE["muted"], labelsize=9)
ax4.set_title("Top-Performing Students — Composite Score Ranking",
              fontweight="bold", color=PALETTE["text"], fontsize=10, pad=8, loc="left")
plt.tight_layout()
chart_d = fig_to_b64(fig4); plt.close(fig4)

# ── Chart E: Box plot ─────────────────────────────────────────────
fig5, ax5 = plt.subplots(figsize=(3.6, 3.8), facecolor=PALETTE["bg"])
bp = ax5.boxplot([df[s] for s in SUBJECTS], patch_artist=True, widths=0.44,
                 medianprops=dict(color=PALETTE["text"], linewidth=2),
                 whiskerprops=dict(color=PALETTE["muted"], linewidth=1),
                 capprops=dict(color=PALETTE["muted"], linewidth=1.4),
                 flierprops=dict(marker="o", markersize=3.5,
                                 markerfacecolor=PALETTE["muted"], alpha=0.6))
for patch, col in zip(bp["boxes"], SUB_COLORS):
    patch.set_facecolor(col); patch.set_alpha(0.75); patch.set_edgecolor("white")
ax5.set_xticklabels(SUBJECTS)
style_ax(ax5, "Score Distribution", "Marks")
plt.tight_layout()
chart_e = fig_to_b64(fig5); plt.close(fig5)

# ── Chart F: Strip / scatter ──────────────────────────────────────
fig6, ax6 = plt.subplots(figsize=(3.6, 3.8), facecolor=PALETTE["bg"])
for i, subj in enumerate(SUBJECTS):
    y_vals = df[subj].values
    x_vals = np.full(len(y_vals), i) + np.random.uniform(-0.12, 0.12, len(y_vals))
    ax6.scatter(x_vals, y_vals, color=SUB_COLORS[i],
                s=34, alpha=0.8, edgecolors="white", linewidth=0.4, zorder=3)
    ax6.hlines(sub_avg[subj], i - 0.28, i + 0.28,
               colors=SUB_COLORS[i], linewidth=2.2, zorder=4)
ax6.set_xticks(range(len(SUBJECTS))); ax6.set_xticklabels(SUBJECTS)
ax6.set_ylim(40, 105)
style_ax(ax6, "Individual Scores", "Marks")
plt.tight_layout()
chart_f = fig_to_b64(fig6); plt.close(fig6)

print("  Charts ready.")


# ══════════════════════════════════════════════════════════════════
# COMPUTE SUMMARY STATS FOR FRONTEND CARDS
# ══════════════════════════════════════════════════════════════════
class_avg  = round(df["Percentage"].mean(), 1)
top_score  = df["Percentage"].max()
top_name   = df.loc[df["Percentage"].idxmax(), "Name"]
grade_a    = int((df["Grade"] == "A").sum())
total_stu  = len(df)

# Subject stat cards
sub_cards_html = ""
sub_icons = ["&#9650;", "&#128267;", "&#128149;", "&#128218;"]
for subj, icon, col in zip(SUBJECTS, sub_icons, SUB_COLORS):
    sub_cards_html += f"""
      <div class="sub-card" style="border-top: 3px solid {col}">
        <div class="sub-icon" style="color:{col}">{icon}</div>
        <div class="sub-name">{subj}</div>
        <div class="sub-avg" style="color:{col}">{sub_avg[subj]}</div>
        <div class="sub-meta">
          <span>Min {int(sub_min[subj])}</span>
          <span>Max {int(sub_max[subj])}</span>
          <span>σ {sub_std[subj]}</span>
        </div>
      </div>"""

# Topper cards
medal_emojis = ["🥇", "🥈", "🥉", "4", "5"]
topper_cards_html = ""
for i, row in toppers.iterrows():
    pct_bar = int(row["Composite"])
    topper_cards_html += f"""
      <div class="topper-card" style="border-left: 4px solid {TOP_COLORS[i]}">
        <div class="topper-rank" style="color:{TOP_COLORS[i]}">{medal_emojis[i]}</div>
        <div class="topper-info">
          <div class="topper-name">{row['Name']}</div>
          <div class="topper-grade" style="background:{TOP_COLORS[i]}22;color:{TOP_COLORS[i]}">
            Grade {row['Grade']}
          </div>
        </div>
        <div class="topper-stats">
          <span>Score <b>{row['Percentage']:.1f}%</b></span>
          <span>Att <b>{row['Attendance']}%</b></span>
          <span>Study <b>{row['Study_Hours']}h</b></span>
        </div>
        <div class="topper-bar-wrap">
          <div class="topper-bar" style="width:{pct_bar}%;background:{TOP_COLORS[i]}"></div>
        </div>
        <div class="topper-composite" style="color:{TOP_COLORS[i]}">{row['Composite']}</div>
      </div>"""


# ══════════════════════════════════════════════════════════════════
# BUILD HTML PAGE
# ══════════════════════════════════════════════════════════════════
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Student Performance Dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet"/>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  :root {{
    --bg:        #0F1117;
    --surface:   #181C27;
    --surface2:  #1E2333;
    --border:    rgba(255,255,255,0.07);
    --text:      #E8EAF0;
    --muted:     #7A8299;
    --math:      #4361EE;
    --physics:   #F72585;
    --chem:      #4CC9F0;
    --english:   #F9C74F;
    --gold:      #F4A261;
    --silver:    #A8DADC;
    --bronze:    #E76F51;
  }}

  body {{
    font-family: 'DM Sans', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 0 0 60px;
  }}

  /* ── HEADER ─────────────────────────────────────────── */
  .header {{
    background: linear-gradient(135deg, #0F1117 0%, #1a1f35 100%);
    border-bottom: 1px solid var(--border);
    padding: 36px 48px 32px;
    position: relative;
    overflow: hidden;
  }}
  .header::before {{
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 60% 80% at 80% 50%,
                rgba(67,97,238,0.12) 0%, transparent 70%);
    pointer-events: none;
  }}
  .header-inner {{ max-width: 1200px; margin: 0 auto; position: relative; }}
  .header-label {{
    font-size: 11px; font-weight: 500; letter-spacing: 0.14em;
    text-transform: uppercase; color: var(--muted); margin-bottom: 10px;
  }}
  .header h1 {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(24px, 4vw, 38px); font-weight: 700;
    color: var(--text); line-height: 1.15; margin-bottom: 8px;
  }}
  .header h1 span {{ color: #4361EE; }}
  .header-sub {{ font-size: 14px; color: var(--muted); }}

  /* ── MAIN WRAP ───────────────────────────────────────── */
  .wrap {{ max-width: 1200px; margin: 0 auto; padding: 40px 24px 0; }}

  /* ── STAT SUMMARY CARDS ──────────────────────────────── */
  .stat-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 36px; }}
  .stat-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px; padding: 20px 22px;
  }}
  .stat-label {{ font-size: 11px; color: var(--muted); text-transform: uppercase;
                letter-spacing: 0.1em; margin-bottom: 8px; }}
  .stat-value {{ font-family: 'Space Grotesk', sans-serif; font-size: 28px;
                font-weight: 700; color: var(--text); line-height: 1; }}
  .stat-sub {{ font-size: 12px; color: var(--muted); margin-top: 5px; }}
  .stat-accent {{ color: #4361EE; }}

  /* ── SECTION TITLE ───────────────────────────────────── */
  .section-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px; font-weight: 600; color: var(--text);
    margin-bottom: 16px; display: flex; align-items: center; gap: 10px;
  }}
  .section-title::after {{
    content: ''; flex: 1; height: 1px; background: var(--border);
  }}

  /* ── SUBJECT CARDS ───────────────────────────────────── */
  .sub-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 36px; }}
  .sub-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px; padding: 20px 18px;
    transition: transform 0.2s;
  }}
  .sub-card:hover {{ transform: translateY(-3px); }}
  .sub-icon {{ font-size: 22px; margin-bottom: 10px; }}
  .sub-name {{ font-size: 12px; color: var(--muted); text-transform: uppercase;
              letter-spacing: 0.1em; margin-bottom: 6px; }}
  .sub-avg {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px; font-weight: 700; line-height: 1; margin-bottom: 10px;
  }}
  .sub-meta {{ display: flex; gap: 10px; font-size: 11px; color: var(--muted); }}

  /* ── CHART PANELS ────────────────────────────────────── */
  .chart-panel {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px; padding: 24px;
    margin-bottom: 20px;
  }}
  .chart-panel img {{ width: 100%; border-radius: 8px; display: block; }}
  .chart-grid-2 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 18px; margin-bottom: 20px; }}
  .chart-grid-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 18px; margin-bottom: 36px; }}
  .panel-label {{
    font-size: 11px; font-weight: 500; text-transform: uppercase;
    letter-spacing: 0.1em; color: var(--muted); margin-bottom: 14px;
  }}

  /* ── TOPPER CARDS ────────────────────────────────────── */
  .topper-list {{ display: flex; flex-direction: column; gap: 12px; margin-bottom: 40px; }}
  .topper-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px; padding: 16px 20px;
    display: grid;
    grid-template-columns: 36px 1fr auto 200px 52px;
    align-items: center; gap: 16px;
    transition: background 0.2s;
  }}
  .topper-card:hover {{ background: var(--surface2); }}
  .topper-rank {{ font-size: 20px; text-align: center; }}
  .topper-info {{ display: flex; align-items: center; gap: 10px; }}
  .topper-name {{ font-family: 'Space Grotesk', sans-serif; font-size: 15px; font-weight: 600; }}
  .topper-grade {{
    font-size: 11px; font-weight: 600; padding: 2px 10px;
    border-radius: 99px; white-space: nowrap;
  }}
  .topper-stats {{ display: flex; gap: 16px; font-size: 12px; color: var(--muted); }}
  .topper-stats b {{ color: var(--text); font-weight: 600; }}
  .topper-bar-wrap {{
    height: 6px; background: rgba(255,255,255,0.07);
    border-radius: 99px; overflow: hidden;
  }}
  .topper-bar {{ height: 100%; border-radius: 99px;
                transition: width 1s cubic-bezier(.4,0,.2,1); }}
  .topper-composite {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 17px; font-weight: 700; text-align: right;
  }}

  /* ── FORMULA NOTE ────────────────────────────────────── */
  .formula-note {{
    font-size: 12px; color: var(--muted); margin-bottom: 16px;
    padding: 10px 16px; border-radius: 8px;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    display: inline-block;
  }}
  .formula-note b {{ color: var(--text); }}

  /* ── FOOTER ──────────────────────────────────────────── */
  .footer {{
    text-align: center; font-size: 12px; color: var(--muted);
    margin-top: 40px; padding-top: 24px;
    border-top: 1px solid var(--border);
  }}

  @media (max-width: 768px) {{
    .stat-row, .sub-grid {{ grid-template-columns: 1fr 1fr; }}
    .chart-grid-2, .chart-grid-3 {{ grid-template-columns: 1fr; }}
    .topper-card {{ grid-template-columns: 36px 1fr; }}
    .topper-stats, .topper-bar-wrap, .topper-composite {{ display: none; }}
    .header {{ padding: 24px 20px; }}
    .wrap {{ padding: 24px 16px 0; }}
  }}
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <div class="header-inner">
    <div class="header-label">Academic Analytics · {total_stu} Students</div>
    <h1>Student <span>Performance</span> Dashboard</h1>
    <div class="header-sub">Average Marks per Subject &nbsp;·&nbsp; Top-Performing Students</div>
  </div>
</div>

<div class="wrap">

  <!-- SUMMARY STAT CARDS -->
  <div class="stat-row">
    <div class="stat-card">
      <div class="stat-label">Total Students</div>
      <div class="stat-value">{total_stu}</div>
      <div class="stat-sub">Across all subjects</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Class Average</div>
      <div class="stat-value stat-accent">{class_avg}%</div>
      <div class="stat-sub">Overall percentage</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Top Scorer</div>
      <div class="stat-value" style="font-size:22px">{top_name}</div>
      <div class="stat-sub">{top_score:.1f}% — highest in class</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Grade A Students</div>
      <div class="stat-value" style="color:var(--gold)">{grade_a}</div>
      <div class="stat-sub">Out of {total_stu} students</div>
    </div>
  </div>

  <!-- SUBJECT AVERAGE CARDS -->
  <div class="section-title">Average Marks per Subject</div>
  <div class="sub-grid">
    {sub_cards_html}
  </div>

  <!-- CHART ROW 1: grouped bar (wide) -->
  <div class="chart-panel">
    <div class="panel-label">Grouped Comparison — Mean · Median · Min · Max</div>
    <img src="data:image/png;base64,{chart_a}" alt="grouped bar chart"/>
  </div>

  <!-- CHART ROW 2: error bar + radar + scatter -->
  <div class="chart-grid-3">
    <div class="chart-panel" style="margin-bottom:0">
      <div class="panel-label">Mean ± Std Deviation</div>
      <img src="data:image/png;base64,{chart_b}" alt="error bar"/>
    </div>
    <div class="chart-panel" style="margin-bottom:0">
      <div class="panel-label">Top-3 Subject Profile</div>
      <img src="data:image/png;base64,{chart_c}" alt="radar chart"/>
    </div>
    <div class="chart-panel" style="margin-bottom:0">
      <div class="panel-label">Individual Scores · Strip Plot</div>
      <img src="data:image/png;base64,{chart_f}" alt="scatter"/>
    </div>
  </div>
  <div style="margin-bottom:36px"></div>

  <!-- TOP PERFORMING STUDENTS -->
  <div class="section-title">Top-Performing Students</div>
  <div class="formula-note">
    Composite Score = <b>60%</b> Academic Score + <b>20%</b> Attendance + <b>20%</b> Study Hours
  </div>

  <!-- horizontal bar chart -->
  <div class="chart-panel">
    <div class="panel-label">Composite Score Ranking</div>
    <img src="data:image/png;base64,{chart_d}" alt="topper ranking bar"/>
  </div>

  <!-- topper cards -->
  <div class="topper-list">
    {topper_cards_html}
  </div>

  <!-- bottom charts: box + distribution -->
  <div class="section-title">Score Distribution</div>
  <div class="chart-grid-2" style="grid-template-columns:1fr 1fr">
    <div class="chart-panel" style="margin-bottom:0">
      <div class="panel-label">Box Plot — Spread per Subject</div>
      <img src="data:image/png;base64,{chart_e}" alt="box plot"/>
    </div>
    <div class="chart-panel" style="margin-bottom:0">
      <div class="panel-label">Individual Scores per Subject</div>
      <img src="data:image/png;base64,{chart_f}" alt="scatter"/>
    </div>
  </div>

  <div class="footer">
    Generated by Student Performance Analysis Script &nbsp;·&nbsp;
    Data: {total_stu} students · {len(SUBJECTS)} subjects
  </div>

</div>
</body>
</html>"""


# ══════════════════════════════════════════════════════════════════
# SAVE HTML & OPEN IN BROWSER
# ══════════════════════════════════════════════════════════════════
html_path = os.path.join(tempfile.gettempdir(), "student_dashboard.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n  Dashboard saved → {html_path}")
print("  Opening in browser …")
webbrowser.open(f"file:///{html_path.replace(os.sep, '/')}")
print("  Done.")
