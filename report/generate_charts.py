#!/usr/bin/env python3
"""Generate all charts for the professional report."""

import os, csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import Counter

BASE    = "/home/rajdeepvraj/Documents/STT AI/Project"
META    = os.path.join(BASE, "data", "metadata_real.csv")
PLOTS   = os.path.join(BASE, "supporting_files", "report_plots")
os.makedirs(PLOTS, exist_ok=True)

# ── palette ──────────────────────────────────────────────────────────────────
C  = ["#1565c0","#42a5f5","#0d47a1","#64b5f6","#1976d2","#90caf9","#0288d1","#4fc3f7"]
CR = ["#c62828","#ef5350","#b71c1c","#e57373"]
CG = ["#2e7d32","#66bb6a","#1b5e20","#a5d6a7"]

def save(fig, name):
    path = os.path.join(PLOTS, name)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {name}")
    return path

# Load metadata
rows = []
with open(META, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print(f"Loaded {len(rows)} clips. Generating charts...\n")

# ── Fig 1: Domain + Language distribution (2-panel) ─────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
fig.patch.set_facecolor("white")

# Domain bar
domains = ["admissions", "hostel_mess", "it_support", "student_services"]
d_labels = ["Admissions", "Hostel &\nMess", "IT Support", "Student\nServices"]
d_counts = [sum(1 for r in rows if r["domain"]==d) for d in domains]
bars = axes[0].bar(d_labels, d_counts, color=C[:4], edgecolor="white", linewidth=0.5, width=0.55)
axes[0].set_title("Domain Distribution", fontsize=13, fontweight="bold", pad=10)
axes[0].set_ylabel("Number of Clips", fontsize=10)
axes[0].set_ylim(0, max(d_counts)*1.25)
for bar, cnt in zip(bars, d_counts):
    axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+1.5, str(cnt),
                 ha="center", va="bottom", fontsize=10, fontweight="bold", color="#1a237e")
axes[0].spines[["top","right"]].set_visible(False)
axes[0].tick_params(axis="x", labelsize=9)

# Language mix pie
lang_order = ["pure_en","en_hi","pure_hi","en_gu"]
lang_labels = ["English\n(pure_en)", "English–Hindi\n(en_hi)", "Hindi\n(pure_hi)", "Gujarati-mix\n(en_gu)"]
lang_counts = [sum(1 for r in rows if r["language_mix"]==l) for l in lang_order]
wedge_props = dict(width=0.55, edgecolor="white", linewidth=1.5)
wedges, texts, autotexts = axes[1].pie(
    lang_counts, labels=lang_labels, autopct="%1.1f%%",
    colors=C[:4], wedgeprops=wedge_props, startangle=140,
    pctdistance=0.72, labeldistance=1.15, textprops={"fontsize": 8})
for at in autotexts: at.set_fontsize(8); at.set_fontweight("bold"); at.set_color("white")
axes[1].set_title("Language Mix Distribution", fontsize=13, fontweight="bold", pad=10)

plt.tight_layout(pad=2)
FIG1 = save(fig, "fig1_domain_language.png")

# ── Fig 2: Speaker clips & duration ─────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
fig.patch.set_facecolor("white")

spk_ids = [f"SPK{i:02d}" for i in range(1,17)]
spk_names = ["Rajdeep","Vipul","Satvik","Priya","Ananya","Rohan","Neha","Meet",
             "Tanvi","Aditya","Pooja","Hardik","Harshit","Divya","Chirag","Meera"]
spk_clips = [sum(1 for r in rows if r["speaker_id"]==s) for s in spk_ids]
spk_dur   = [sum(float(r["duration_sec"]) for r in rows if r["speaker_id"]==s)/60 for s in spk_ids]
cohorts   = ["A"]*12 + ["B"]*4
colors_s  = [C[0] if c=="A" else C[2] for c in cohorts]

# Clips per speaker
b1 = axes[0].bar(spk_names, spk_clips, color=colors_s, edgecolor="white", linewidth=0.4)
axes[0].set_title("Clips per Speaker", fontsize=13, fontweight="bold", pad=8)
axes[0].set_ylabel("Number of Clips", fontsize=10)
axes[0].tick_params(axis="x", rotation=45, labelsize=7.5)
axes[0].spines[["top","right"]].set_visible(False)
axes[0].axvline(x=11.5, color="gray", linestyle="--", linewidth=1, alpha=0.6)
axes[0].text(5.5, max(spk_clips)*1.05, "Cohort A", ha="center", fontsize=9, color=C[0], fontweight="bold")
axes[0].text(13.5, max(spk_clips)*1.05, "Cohort B", ha="center", fontsize=9, color=C[2], fontweight="bold")
for bar, cnt in zip(b1, spk_clips):
    if cnt > 0:
        axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2, str(cnt),
                     ha="center", va="bottom", fontsize=6.5, color="#333")

# Duration per speaker
b2 = axes[1].bar(spk_names, spk_dur, color=colors_s, edgecolor="white", linewidth=0.4)
axes[1].set_title("Recording Duration per Speaker (minutes)", fontsize=13, fontweight="bold", pad=8)
axes[1].set_ylabel("Duration (min)", fontsize=10)
axes[1].tick_params(axis="x", rotation=45, labelsize=7.5)
axes[1].spines[["top","right"]].set_visible(False)
axes[1].axvline(x=11.5, color="gray", linestyle="--", linewidth=1, alpha=0.6)

patch_a = mpatches.Patch(color=C[0], label="Cohort A (SPK01–12)")
patch_b = mpatches.Patch(color=C[2], label="Cohort B (SPK13–16)")
axes[1].legend(handles=[patch_a, patch_b], fontsize=8, loc="upper right")
plt.tight_layout(pad=2)
FIG2 = save(fig, "fig2_speaker_stats.png")

# ── Fig 3: Clip duration distribution ────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
fig.patch.set_facecolor("white")

durs = [float(r["duration_sec"]) for r in rows]
axes[0].hist(durs, bins=25, color=C[0], edgecolor="white", linewidth=0.4, alpha=0.9)
axes[0].axvline(np.mean(durs), color=CR[0], linestyle="--", linewidth=1.8, label=f"Mean = {np.mean(durs):.1f}s")
axes[0].axvline(np.median(durs), color=CG[0], linestyle="--", linewidth=1.8, label=f"Median = {np.median(durs):.1f}s")
axes[0].set_title("Clip Duration Distribution", fontsize=13, fontweight="bold", pad=8)
axes[0].set_xlabel("Duration (seconds)", fontsize=10)
axes[0].set_ylabel("Count", fontsize=10)
axes[0].legend(fontsize=9)
axes[0].spines[["top","right"]].set_visible(False)

snrs = [float(r["snr_db"]) for r in rows]
axes[1].hist(snrs, bins=25, color=C[1], edgecolor="white", linewidth=0.4, alpha=0.9)
axes[1].axvline(np.mean(snrs), color=CR[0], linestyle="--", linewidth=1.8, label=f"Mean = {np.mean(snrs):.1f} dB")
axes[1].set_title("Estimated SNR Distribution", fontsize=13, fontweight="bold", pad=8)
axes[1].set_xlabel("SNR (dB)", fontsize=10)
axes[1].set_ylabel("Count", fontsize=10)
axes[1].legend(fontsize=9)
axes[1].spines[["top","right"]].set_visible(False)
plt.tight_layout(pad=2)
FIG3 = save(fig, "fig3_duration_snr.png")

# ── Fig 4: Augmentation WER comparison ───────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 4.5))
fig.patch.set_facecolor("white")
aug_names  = ["Clean\n(baseline)", "MUSAN Noise\n(12dB SNR)", "RIR Reverb\n(RT60=0.4s)", "Speed 1.1×", "Telephony\nCodec"]
aug_wers   = [47.33, 110.05, 97.54, 89.60, 79.78]
bar_colors = [CG[0]] + [CR[0], CR[1], CR[2], CR[3]]
bars = ax.bar(aug_names, aug_wers, color=bar_colors, edgecolor="white", linewidth=0.5, width=0.55)
ax.axhline(100, color="gray", linestyle=":", linewidth=1.2, alpha=0.7, label="WER = 100% (insertion threshold)")
ax.set_title("Whisper-tiny WER by Augmentation Condition\n(Real Speech, CPU int8)", fontsize=13, fontweight="bold", pad=10)
ax.set_ylabel("Word Error Rate (%)", fontsize=11)
ax.set_ylim(0, 130)
for bar, wer in zip(bars, aug_wers):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1.5, f"{wer:.1f}%",
            ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="#222")
    if wer > 47.33:
        delta = wer - 47.33
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+8,
                f"+{delta:.1f}pp", ha="center", fontsize=7.5, color=CR[0], style="italic")
ax.spines[["top","right"]].set_visible(False)
ax.legend(fontsize=8)
plt.tight_layout(pad=1.5)
FIG4 = save(fig, "fig4_augmentation_wer.png")

# ── Fig 5: Active Learning curve ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4.5))
fig.patch.set_facecolor("white")
budgets = [20, 40, 80]
al_f1   = [0.246, 0.296, 0.273]
rand_f1 = [0.176, 0.189, 0.215]
ax.plot(budgets, al_f1,   "o-", color=C[0], linewidth=2.2, markersize=8, label="Active Learning (class-balanced)")
ax.plot(budgets, rand_f1, "s--", color=CR[0], linewidth=2.2, markersize=8, label="Random Sampling")
for b, a, r in zip(budgets, al_f1, rand_f1):
    ax.annotate(f"{a:.3f}", (b, a), textcoords="offset points", xytext=(6,4), fontsize=8.5, color=C[0], fontweight="bold")
    ax.annotate(f"{r:.3f}", (b, r), textcoords="offset points", xytext=(6,-13), fontsize=8.5, color=CR[0], fontweight="bold")
ax.fill_between(budgets, rand_f1, al_f1, alpha=0.10, color=C[0], label="AL advantage")
ax.set_title("Active Learning vs. Random Sampling\n(Domain Classification, Macro F1)", fontsize=13, fontweight="bold", pad=10)
ax.set_xlabel("Annotation Budget (# clips labelled)", fontsize=11)
ax.set_ylabel("Macro F1 Score", fontsize=11)
ax.set_xticks(budgets)
ax.set_ylim(0, 0.45)
ax.legend(fontsize=9, loc="upper left")
ax.spines[["top","right"]].set_visible(False)
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout(pad=1.5)
FIG5 = save(fig, "fig5_active_learning.png")

# ── Fig 6: Validation check results ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 4))
fig.patch.set_facecolor("white")
checks  = ["sample_rate","channels","duration\nbounds","clipping","silence\nratio","snr_floor",
           "duplicate\nhash","duration\nmismatch","metadata\nschema","file\nexists","transcript\nnonempty","domain\nvalid"]
failures = [0,0,0,0,2,0,0,0,0,0,0,0]
bar_c = [CR[0] if f>0 else CG[0] for f in failures]
bars = ax.bar(checks, [284-f for f in failures], color=bar_c, edgecolor="white", linewidth=0.4, width=0.6)
ax.set_title("Validation Suite Results — 12 Automated Checks (284 clips)", fontsize=13, fontweight="bold", pad=8)
ax.set_ylabel("Clips Passing", fontsize=10)
ax.set_ylim(275, 287)
ax.axhline(284, color="gray", linestyle=":", linewidth=1.2, alpha=0.5)
for bar, f in zip(bars, failures):
    label = "✓ PASS" if f==0 else f"✗ {f} fail"
    color = CG[0] if f==0 else CR[0]
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05, label,
            ha="center", va="bottom", fontsize=7, fontweight="bold", color=color)
ax.tick_params(axis="x", labelsize=7.5)
ax.spines[["top","right"]].set_visible(False)
patch_p = mpatches.Patch(color=CG[0], label="PASS (0 failures)")
patch_f = mpatches.Patch(color=CR[0], label="FAIL (≥1 failure)")
ax.legend(handles=[patch_p, patch_f], fontsize=8)
plt.tight_layout(pad=1.5)
FIG6 = save(fig, "fig6_validation.png")

# ── Fig 7: Noise condition + Gender ──────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
fig.patch.set_facecolor("white")
noise_map = Counter(r["noise_condition"] for r in rows)
n_labels = ["Quiet Room", "Hostel\nCorridor", "Cafeteria\nAmbient", "Outdoor\nCampus"]
n_keys   = ["quiet_room","hostel_corridor","cafeteria_ambient","outdoor_campus"]
n_vals   = [noise_map.get(k,0) for k in n_keys]
axes[0].bar(n_labels, n_vals, color=C[:4], edgecolor="white", linewidth=0.4, width=0.55)
axes[0].set_title("Recording Environment Distribution", fontsize=12, fontweight="bold", pad=8)
axes[0].set_ylabel("Clips", fontsize=10)
for i,(l,v) in enumerate(zip(n_labels, n_vals)):
    axes[0].text(i, v+0.5, str(v), ha="center", va="bottom", fontsize=10, fontweight="bold", color="#333")
axes[0].spines[["top","right"]].set_visible(False)

gender_cnt = Counter(r["gender"] for r in rows)
wedges, texts, autotexts = axes[1].pie(
    [gender_cnt["F"], gender_cnt["M"]],
    labels=["Female\n(F)", "Male\n(M)"],
    autopct="%1.1f%%", colors=[C[1], C[0]],
    wedgeprops=dict(width=0.55, edgecolor="white", linewidth=1.5),
    startangle=90, textprops={"fontsize":9})
for at in autotexts: at.set_fontsize(9); at.set_fontweight("bold"); at.set_color("white")
axes[1].set_title("Gender Distribution (16 Speakers)", fontsize=12, fontweight="bold", pad=8)
plt.tight_layout(pad=2)
FIG7 = save(fig, "fig7_noise_gender.png")

print("\n✅ All 7 figures generated!")
# Print paths for use in report
for i,name in enumerate(["fig1_domain_language.png","fig2_speaker_stats.png","fig3_duration_snr.png",
                          "fig4_augmentation_wer.png","fig5_active_learning.png",
                          "fig6_validation.png","fig7_noise_gender.png"], 1):
    print(f"  Fig {i}: {os.path.join(PLOTS, name)}")
