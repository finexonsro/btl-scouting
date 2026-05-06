import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="BTL · Scouting",
    page_icon="🔶",
    layout="wide",
    initial_sidebar_state="expanded"
)

def safe_val(val, default="—", fmt=None):
    try:
        if val is None or (isinstance(val, float) and np.isnan(val)):
            return default
        if fmt:
            return fmt.format(val)
        return val
    except:
        return default

# ── LOGO ──────────────────────────────────────────────────────────────────────
LOGO_B64_VAR = "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"

# ── COLORS ────────────────────────────────────────────────────────────────────
ORG  = "#E8560A"
ORG2 = "#B84000"
BG   = "#2A2A2A"
C1   = "#333333"
C2   = "#444444"
W    = "#FFFFFF"
W2   = "#F0F0F0"
MUT  = "#888888"

# ── POSITION CONFIG ───────────────────────────────────────────────────────────
POS_CONFIG = {
    "Winger": {
        "de": "Außenstürmer",
        "attrs": ["involvement","finishing","providing teammates",
                  "dribbling","passing quality","box threat","pressing","run quality"],
        "attrs_de": ["Spielbeteiligung","Abschluss","Vorlagenqualität",
                     "Dribbling","Passqualität","Strafraum-Gefahr","Pressing","Laufqualität"],
    },
    "Striker": {
        "de": "Mittelstürmer",
        "attrs": ["poaching","aerial threat","involvement","finishing",
                  "providing teammates","hold up play","pressing","run quality"],
        "attrs_de": ["Positionsspiel","Kopfballstärke","Spielbeteiligung","Abschluss",
                     "Vorlagenqualität","Ballbehauptung","Pressing","Laufqualität"],
    },
    "Midfielder": {
        "de": "Mittelfeldspieler",
        "attrs": ["intelligent defence","involvement","progression",
                  "providing teammates","passing quality","box threat","active defence"],
        "attrs_de": ["Int. Verteidigen","Spielbeteiligung","Spielverlagerung",
                     "Vorlagenqualität","Passqualität","Strafraum-Gefahr","Akt. Verteidigen"],
    },
    "Fullback": {
        "de": "Außenverteidiger",
        "attrs": ["territorial dominance","intelligent defence","involvement","progression",
                  "chance prevention","providing teammates","passing quality","active defence","run quality"],
        "attrs_de": ["Raumkontrolle","Int. Verteidigen","Spielbeteiligung","Spielverlagerung",
                     "Torverhinderung","Vorlagenqualität","Passqualität","Akt. Verteidigen","Laufqualität"],
    },
    "Central Defender": {
        "de": "Innenverteidiger",
        "attrs": ["territorial dominance","composure","aerial threat","intelligent defence",
                  "involvement","progression","chance prevention","defensive heading","active defence"],
        "attrs_de": ["Raumkontrolle","Ruhe am Ball","Kopfballstärke","Int. Verteidigen",
                     "Spielbeteiligung","Spielverlagerung","Torverhinderung","Kopfballduell","Akt. Verteidigen"],
    },
}

# ── LABEL SYSTEMS ─────────────────────────────────────────────────────────────
IFI_LABEL_STYLE = {
    "ELITE":   ("🔴 ELITE",   "#CC0000", "#FFFFFF"),
    "STRONG":  ("🟠 STRONG",  "#E8560A", "#FFFFFF"),
    "AVERAGE": ("🟡 AVERAGE", "#F0A500", "#1A1A1A"),
    "BELOW":   ("🔵 BELOW",   "#1565C0", "#FFFFFF"),
    "WEAK":    ("⚫ WEAK",    "#555555", "#AAAAAA"),
}

TIER_COLORS = {
    "🔥 ELITE TARGET": "#E8560A",
    "🟢 TOP TARGET":   "#1B5E20",
    "🔵 INTERESTING":  "#0D47A1",
    "🟡 WATCHLIST":    "#F0A500",
    "🔴 RISIKO":       "#4A0D0D",
}

SPEED_FLAGS = {
    "⚡ ELITE": "#E8560A",
    "🔵 HIGH":  "#1565C0",
    "🟡 FAST":  "#0288D1",
    "🟠 MEDIUM":"#B84000",
    "—":        "#444444",
}

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{{font-family:'DM Sans',sans-serif;background:{BG};color:{W2};}}
.main{{background:{BG};}} .block-container{{padding-top:2rem !important;}}
[data-testid="stHeader"]::after{{content:'';display:block;height:4px;
    background:linear-gradient(90deg,{ORG2},{ORG} 40%,#FFa040 60%,{ORG} 80%,{ORG2});
    position:fixed;top:0;left:0;right:0;z-index:9999;}}
[data-testid="stSidebar"]{{background:#222222;border-right:2px solid {ORG};}}
[data-testid="stSidebar"] label{{color:{W2} !important;font-size:11px !important;
    letter-spacing:0.08em;text-transform:uppercase;font-weight:500 !important;}}
[data-testid="stSidebar"] p,[data-testid="stSidebar"] span{{color:{W2} !important;}}
[data-testid="stSlider"] [role="progressbar"]{{background:{ORG} !important;}}
.stButton>button,.stDownloadButton>button{{background:{ORG} !important;color:{W} !important;
    border:none !important;border-radius:6px !important;font-weight:700 !important;}}
[role="tab"]{{color:{MUT} !important;font-size:13px;font-weight:500;border-bottom:2px solid transparent;}}
[role="tab"][aria-selected="true"]{{color:{ORG} !important;border-bottom:2px solid {ORG} !important;}}
[data-baseweb="tag"]{{background:{ORG2} !important;color:{W} !important;}}
.jcard{{background:{C1};border:1px solid {C2};border-top:3px solid {ORG};
    border-radius:8px;padding:14px 12px;text-align:center;margin-bottom:4px;}}
.jcard .val{{font-family:'DM Mono',monospace;font-size:22px;font-weight:600;color:{W};}}
.jcard .lbl{{font-size:10px;color:{MUT};letter-spacing:0.1em;text-transform:uppercase;margin-top:4px;}}
.sec{{font-family:'DM Mono',monospace;font-size:10px;color:{ORG};letter-spacing:0.15em;
    text-transform:uppercase;border-bottom:1px solid {C2};padding-bottom:4px;margin-bottom:10px;}}
.div{{height:1px;background:linear-gradient(90deg,{ORG}66,{C2});margin:10px 0;}}
.pbar-row{{display:flex;align-items:center;padding:6px 0;border-bottom:1px solid #3A3A3A;gap:12px;}}
.pbar-name{{font-size:12px;color:#CCC;min-width:155px;}}
.pbar-bg{{background:#3A3A3A;border-radius:4px;height:10px;flex:1;}}
.pbar-fill{{height:10px;border-radius:4px;}}
.pbar-info{{font-size:11px;color:#888;min-width:50px;text-align:right;font-family:DM Mono,monospace;}}
.stTextInput input{{background:#333 !important;color:#FFF !important;border:1px solid #555 !important;}}
.bm-row{{display:flex;align-items:center;gap:12px;padding:4px 0;font-size:12px;}}
.bm-label{{color:#888;min-width:80px;}}
.bm-val{{color:#FFF;font-family:DM Mono,monospace;min-width:40px;}}
.bm-delta-pos{{color:#81C784;font-family:DM Mono,monospace;font-weight:600;}}
.bm-delta-neg{{color:#EF9A9A;font-family:DM Mono,monospace;font-weight:600;}}
</style>
""", unsafe_allow_html=True)

# ── PASSWORD ──────────────────────────────────────────────────────────────────
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center;margin-bottom:24px;">
            <img src="data:image/png;base64,{LOGO_B64_VAR}" style="width:100px;filter:drop-shadow(0 0 12px #E8560A66);">
            <div style="font-size:22px;font-weight:800;color:#FFF;margin-top:12px;">Between The Lines</div>
            <div style="font-size:12px;color:#888;letter-spacing:0.15em;text-transform:uppercase;margin-top:4px;">Scouting Intelligence</div>
        </div>
        """, unsafe_allow_html=True)
        pwd = st.text_input("Passwort", type="password", placeholder="Passwort eingeben...")
        if st.button("Anmelden", use_container_width=True):
            if pwd == st.secrets.get("password", "btl2024"):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Falsches Passwort")
    return False

if not check_password():
    st.stop()

# ── DATA ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/btl_scouting_app_data.csv")
    df.columns = [c.lower().strip() for c in df.columns]
    if "age" in df.columns:
        df["age"] = pd.to_numeric(df["age"], errors="coerce").round(0).astype("Int64")
    df["markt"] = "DACH"
    has_sc  = df["sc_psv-99"].notna() if "sc_psv-99" in df.columns else pd.Series(False, index=df.index)
    has_ifi = df["pct_score"].notna()  if "pct_score"  in df.columns else pd.Series(False, index=df.index)
    df["datenquelle"] = "unbekannt"
    df.loc[ has_sc &  has_ifi, "datenquelle"] = "vollständig"
    df.loc[ has_sc & ~has_ifi, "datenquelle"] = "nur_physical"
    df.loc[~has_sc &  has_ifi, "datenquelle"] = "nur_ifi"
    if "minutes" not in df.columns and "sc_minutes" in df.columns:
        df["minutes"] = df["sc_minutes"]
    return df

df_raw = load_data()

# ── HELPERS ───────────────────────────────────────────────────────────────────
def speed_flag(psv):
    try:
        v = float(psv)
        if v >= 32:   return "⚡ ELITE"
        elif v >= 31: return "🔵 HIGH"
        elif v >= 30: return "🟡 FAST"
        elif v >= 29: return "🟠 MEDIUM"
        else:         return "—"
    except:
        return "—"

def ifi_label(pct):
    """pct is 0-100"""
    try:
        p = float(pct)
        if p >= 90:  return "ELITE"
        elif p >= 75: return "STRONG"
        elif p >= 50: return "AVERAGE"
        elif p >= 25: return "BELOW"
        else:         return "WEAK"
    except:
        return "—"

def physical_tier(ps):
    """ps is 0-100"""
    try:
        p = float(ps)
        if p >= 80:   return "🔥 ELITE TARGET",  ORG
        elif p >= 65: return "🟢 TOP TARGET",     "#1B5E20"
        elif p >= 50: return "🔵 INTERESTING",    "#0D47A1"
        elif p >= 35: return "🟡 WATCHLIST",      ORG2
        else:         return "🔴 RISIKO",         "#4A0D0D"
    except:
        return "—", "#555"

def calc_final_tier(row, ifi_lbl):
    ps = row.get("physical score", np.nan)
    has_physical = pd.notna(ps)
    has_ifi      = pd.notna(row.get("pct_score", np.nan))

    if not has_physical and not has_ifi:
        return "—"

    if not has_physical:
        return "⬜ NUR IFI"

    tier, _ = physical_tier(ps)
    order = ["🔥 ELITE TARGET","🟢 TOP TARGET","🔵 INTERESTING","🟡 WATCHLIST","🔴 RISIKO"]

    if ifi_lbl in ["BELOW","WEAK"] and tier in order:
        return order[max(order.index(tier), 3)]
    return tier

def recalc(df, weights, position):
    df = df.copy()
    pos_cfg = POS_CONFIG.get(position, {})
    attrs   = pos_cfg.get("attrs", [])
    active  = {a: w for a, w in weights.items() if w > 0}
    pct_cols = [f"pct_{a}" for a in attrs if f"pct_{a}" in df.columns and a in active]

    if pct_cols and active:
        tw = sum(active.get(c.replace("pct_",""), 0) for c in pct_cols)
        if tw > 0:
            raw = sum(df[c].fillna(0) * (active.get(c.replace("pct_",""), 1) / tw) for c in pct_cols)
            df["pct_score"] = raw.rank(pct=True) * 100

    df["ifi_label"]  = df["pct_score"].apply(ifi_label)
    df["speed_flag"] = df["sc_psv-99"].apply(speed_flag)
    df["final_tier"] = df.apply(lambda r: calc_final_tier(r, r.get("ifi_label","—")), axis=1)
    return df

# ── PHYSICAL BARS ─────────────────────────────────────────────────────────────
def render_physical_bars(row):
    ps     = float(row.get("physical score", 0) or 0)
    tier_l, tier_c = physical_tier(ps)

    comps = [
        ("⚡ Top-Speed",         row.get("pct_speed", 0),  ORG),
        ("🏃 Off-Ball Intensität", row.get("pct_otip",  0), "#E65100"),
        ("💥 Lauf-Intensität",    row.get("pct_bip",   0), "#1565C0"),
        ("🚀 Explosivität",       row.get("pct_burst", 0), "#2E7D32"),
    ]
    html = ""
    for name, val, color in comps:
        try:
            v = float(val or 0)
        except:
            v = 0
        html += f"""<div class="pbar-row">
            <div class="pbar-name">{name}</div>
            <div class="pbar-bg"><div class="pbar-fill" style="width:{v:.0f}%;background:{color};"></div></div>
            <div class="pbar-info">{v:.0f}%</div>
        </div>"""

    psv    = float(row.get("sc_psv-99", 0) or 0)
    sf     = row.get("speed_flag", "—")
    sf_c   = SPEED_FLAGS.get(sf, "#888")
    bm_bl  = row.get("benchmark_bl", np.nan)
    bm_3l  = row.get("benchmark_3liga", np.nan)
    d_bl   = row.get("δ_vs_bl", np.nan)
    d_3l   = row.get("δ_vs_3liga", np.nan)

    bm_html = ""
    if pd.notna(bm_bl):
        dc = "#81C784" if (d_bl or 0) >= 0 else "#EF9A9A"
        bm_html += f'<div class="bm-row"><span class="bm-label">vs BL:</span><span class="bm-val">{bm_bl:.1f}</span><span class="bm-delta-{"pos" if (d_bl or 0) >= 0 else "neg"}">{d_bl:+.1f}</span></div>'
    if pd.notna(bm_3l):
        dc = "#81C784" if (d_3l or 0) >= 0 else "#EF9A9A"
        bm_html += f'<div class="bm-row"><span class="bm-label">vs 3.Liga:</span><span class="bm-val">{bm_3l:.1f}</span><span class="bm-delta-{"pos" if (d_3l or 0) >= 0 else "neg"}">{d_3l:+.1f}</span></div>'

    html += f"""
    <div style="margin-top:10px;padding-top:8px;border-top:1px solid #3A3A3A;">
        <div style="font-size:12px;color:#888;margin-bottom:4px;">
            PSV-99: <b style="color:#FFF;">{psv:.2f} km/h</b>
            <span style="color:{sf_c};margin-left:8px;font-weight:700;">{sf}</span>
        </div>
        {bm_html}
    </div>"""
    return html

# ── RADAR CHART ───────────────────────────────────────────────────────────────
def make_radar(row, position):
    pos_cfg  = POS_CONFIG.get(position, {})
    attrs    = pos_cfg.get("attrs", [])
    attrs_de = pos_cfg.get("attrs_de", attrs)
    vals, labels = [], []
    for attr, attr_de in zip(attrs, attrs_de):
        col = f"pct_{attr}"
        if col in row.index and pd.notna(row[col]):
            vals.append(float(row[col]))
            labels.append(attr_de)
    if len(vals) < 3:
        return None

    ifi_lbl = row.get("ifi_label", "—")
    em, ic, _ = IFI_LABEL_STYLE.get(ifi_lbl, ("—", "#888", "#FFF"))

    vals_c   = vals + [vals[0]]
    labels_c = labels + [labels[0]]

    fig = go.Figure()
    for ring, op in [(100, 0.02), (75, 0.03), (50, 0.04), (25, 0.05)]:
        fig.add_trace(go.Scatterpolar(
            r=[ring]*(len(vals)+1), theta=labels_c, mode="lines",
            line=dict(color="#FFFFFF", width=0.5), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatterpolar(
        r=[50]*(len(vals)+1), theta=labels_c, mode="lines",
        line=dict(color="#666", width=1.5, dash="dot"),
        name="Median (50%)", hoverinfo="skip"))
    fig.add_trace(go.Scatterpolar(
        r=vals_c, theta=labels_c, fill="toself",
        fillcolor="rgba(232,86,10,0.18)",
        line=dict(color=ORG, width=2.5),
        name=f"IFI · {em}",
        hovertemplate="%{theta}: <b>%{r:.0f}%</b><extra></extra>"))
    fig.update_layout(
        polar=dict(bgcolor="#2A2A2A",
            radialaxis=dict(visible=True, range=[0,100],
                tickvals=[25,50,75,100], ticktext=["25%","50%","75%","100%"],
                tickfont=dict(color="#666", size=9), gridcolor="#3A3A3A", linecolor="#3A3A3A"),
            angularaxis=dict(tickfont=dict(color="#DDD", size=10),
                gridcolor="#3A3A3A", linecolor="#444", direction="clockwise")),
        paper_bgcolor=BG, font=dict(family="DM Sans", color="#CCC"),
        showlegend=True,
        legend=dict(bgcolor="#333", bordercolor="#444", borderwidth=1,
            font=dict(color="#888", size=10), orientation="h", y=-0.15, x=0.5, xanchor="center"),
        margin=dict(l=60, r=60, t=50, b=60), height=400,
        title=dict(text=f"IFI Radar · {em} · {row.get('pct_score',50):.0f}. Perzentil",
            font=dict(size=12, color=ic), x=0.5))
    return fig

# ── HTML REPORT ───────────────────────────────────────────────────────────────
def make_html_report(row, position):
    pos_cfg  = POS_CONFIG.get(position, {})
    attrs    = pos_cfg.get("attrs", [])
    attrs_de = pos_cfg.get("attrs_de", attrs)
    ifi_lbl  = row.get("ifi_label", "—")
    em, ic, _ = IFI_LABEL_STYLE.get(ifi_lbl, ("—","#888","#FFF"))
    ps        = float(row.get("physical score", 0) or 0)
    tier_l, tier_c = physical_tier(ps)
    t_bg      = TIER_COLORS.get(tier_l, "#333")
    ifi_pct   = float(row.get("pct_score", 50) or 50)
    psv       = float(row.get("sc_psv-99", 0) or 0)
    sf        = row.get("speed_flag", "—")
    bm_bl     = row.get("benchmark_bl", "—")
    bm_3l     = row.get("benchmark_3liga", "—")
    d_bl      = row.get("δ_vs_bl", "—")
    d_3l      = row.get("δ_vs_3liga", "—")

    phys_rows = ""
    for nm, val, color in [
        ("⚡ Top-Speed",          row.get("pct_speed", 0), "#E8560A"),
        ("🏃 Off-Ball Intensität", row.get("pct_otip",  0), "#E65100"),
        ("💥 Lauf-Intensität",    row.get("pct_bip",   0), "#1565C0"),
        ("🚀 Explosivität",       row.get("pct_burst", 0), "#2E7D32"),
    ]:
        try:
            v = float(val or 0)
        except:
            v = 0
        phys_rows += f"""<tr>
            <td style="padding:6px 8px;font-size:12px;">{nm}</td>
            <td style="padding:6px 8px;width:180px;">
                <div style="background:#eee;border-radius:4px;height:10px;">
                    <div style="background:{color};width:{v:.0f}%;height:10px;border-radius:4px;"></div>
                </div>
            </td>
            <td style="padding:6px 8px;font-size:12px;">{v:.0f}%</td>
        </tr>"""

    ifi_rows = ""
    for attr, attr_de in zip(attrs, attrs_de):
        col = f"pct_{attr}"
        if col not in row.index or pd.isna(row.get(col)):
            continue
        pct   = float(row[col])
        lbl   = ifi_label(pct)
        em2, c2, _ = IFI_LABEL_STYLE.get(lbl, ("—","#999","#FFF"))
        ifi_rows += f"""<tr>
            <td style="padding:5px 8px;font-size:12px;">{attr_de}</td>
            <td style="padding:5px 8px;width:180px;">
                <div style="background:#eee;border-radius:4px;height:8px;">
                    <div style="background:{c2};width:{pct:.0f}%;height:8px;border-radius:4px;"></div>
                </div>
            </td>
            <td style="padding:5px 8px;font-size:12px;color:{c2};font-weight:600;">{pct:.0f}% {em2}</td>
        </tr>"""

    try:
        d_bl_str  = f"{float(d_bl):+.1f}" if pd.notna(d_bl) else "—"
        d_3l_str  = f"{float(d_3l):+.1f}" if pd.notna(d_3l) else "—"
        bm_bl_str = f"{float(bm_bl):.1f}" if pd.notna(bm_bl) else "—"
        bm_3l_str = f"{float(bm_3l):.1f}" if pd.notna(bm_3l) else "—"
    except:
        d_bl_str = d_3l_str = bm_bl_str = bm_3l_str = "—"

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<title>Scouting Report – {row.get('name','—')}</title>
<style>
body{{font-family:Arial,sans-serif;margin:0;padding:24px;background:#fff;max-width:900px;margin:0 auto;}}
.header{{background:{t_bg};color:#fff;padding:20px 24px;border-radius:10px;margin-bottom:16px;}}
.header h1{{margin:0;font-size:22px;font-weight:800;}}
.header p{{margin:6px 0 0;opacity:0.85;font-size:13px;}}
.badge{{background:rgba(255,255,255,0.2);display:inline-block;padding:4px 12px;
    border-radius:20px;font-size:13px;font-weight:700;margin-top:10px;}}
.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px;}}
.card{{border:1px solid #ddd;border-top:3px solid {ORG};border-radius:8px;padding:12px;text-align:center;}}
.card .val{{font-size:20px;font-weight:700;color:#111;}}
.card .lbl{{font-size:10px;color:#888;text-transform:uppercase;letter-spacing:0.08em;margin-top:4px;}}
.section h2{{font-size:13px;color:{ORG};text-transform:uppercase;letter-spacing:0.1em;
    border-bottom:1px solid #eee;padding-bottom:5px;margin:16px 0 8px;}}
table{{width:100%;border-collapse:collapse;}}
</style></head><body>
<div class="header">
    <h1>{row.get('name','—')}</h1>
    <p>{row.get('team','—')} · {row.get('liga','—')} · {pos_cfg.get('de',position)} · {row.get('spielertyp','—')} · {safe_val(row.get('age'),'—')} J. · {safe_val(row.get('sc_minutes', row.get('minutes')),'—')} min</p>
    <div class="badge">{tier_l}</div>
</div>
<div class="cards">
    <div class="card"><div class="val">{ps:.0f}</div><div class="lbl">Physical Score /100</div></div>
    <div class="card"><div class="val" style="color:{tier_c};">{tier_l}</div><div class="lbl">Physical Tier</div></div>
    <div class="card"><div class="val">{ifi_pct:.0f}%</div><div class="lbl">IFI Perzentil</div></div>
    <div class="card"><div class="val" style="color:{ic};">{em}</div><div class="lbl">IFI Label</div></div>
</div>
<div class="cards">
    <div class="card"><div class="val">{psv:.2f} km/h</div><div class="lbl">PSV-99</div></div>
    <div class="card"><div class="val">{sf}</div><div class="lbl">Speed Flag</div></div>
    <div class="card"><div class="val">{bm_bl_str} ({d_bl_str})</div><div class="lbl">vs BL Benchmark</div></div>
    <div class="card"><div class="val">{bm_3l_str} ({d_3l_str})</div><div class="lbl">vs 3.Liga Benchmark</div></div>
</div>
<div class="section"><h2>⚡ Physical Breakdown</h2><table>{phys_rows}</table></div>
<div class="section"><h2>🎯 IFI Profil — {pos_cfg.get('de',position)}</h2><table>{ifi_rows}</table></div>
<div style="margin-top:20px;font-size:11px;color:#aaa;text-align:right;">
    Between The Lines Scouting Intelligence · {datetime.now().strftime('%d.%m.%Y')}
</div>
</body></html>"""

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:20px 0 14px;">
        <img src="data:image/png;base64,{LOGO_B64_VAR}" style="width:90px;filter:drop-shadow(0 0 14px {ORG}88);">
        <div style="font-size:14px;font-weight:800;color:#FFF;margin-top:10px;letter-spacing:0.06em;">BETWEEN THE LINES</div>
        <div style="font-size:10px;color:#888;letter-spacing:0.18em;text-transform:uppercase;margin-top:3px;">Scouting Intelligence</div>
    </div>
    <div class="div"></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec">Position</div>', unsafe_allow_html=True)
    avail_pos = ["Alle"] + [p for p in POS_CONFIG.keys() if "position" in df_raw.columns and p in df_raw["position"].unique()]
    sel_pos   = st.selectbox("Position", avail_pos, label_visibility="collapsed")

    st.markdown('<div class="sec" style="margin-top:10px;">Filter</div>', unsafe_allow_html=True)

    # Markt filter
    if "markt" in df_raw.columns:
        maerkte = sorted(df_raw["markt"].dropna().unique().tolist())
        sel_markt = st.multiselect("Markt", maerkte, default=maerkte)
    else:
        sel_markt = []
    # Datenquelle filter
    sel_src = st.multiselect("Datenquelle",
        ["vollständig","nur_physical","nur_ifi"],
        default=["vollständig","nur_physical","nur_ifi"],
        format_func=lambda x: {
            "vollständig":  "✅ Vollständig (SC + IFI)",
            "nur_physical": "⚡ Nur Physical (kein IFI)",
            "nur_ifi":      "🎯 Nur IFI (kein SC-Match)"
        }.get(x, x))

    if "liga" in df_raw.columns:
        ligen = sorted(df_raw["liga"].dropna().unique().tolist())
        sel_ligen = st.multiselect("Liga", ligen, default=ligen)
    else:
        sel_ligen = []

    psv_min = st.slider("PSV-99 Minimum (km/h)", 0.0, 33.0, 0.0, 0.5, format="%.1f")

    age_col = "age" if "age" in df_raw.columns else None
    if age_col:
        ar = st.slider("Alter", int(df_raw[age_col].min()), int(df_raw[age_col].max()), (15, int(df_raw[age_col].max())))
    else:
        ar = (15, 40)

    min_col = "sc_minutes" if "sc_minutes" in df_raw.columns else ("minutes" if "minutes" in df_raw.columns else None)
    if min_col:
        max_min = int(df_raw[min_col].max())
        mr = st.slider("Minuten", 0, max_min, (100, max_min), step=50)
    else:
        mr = (100, 5000)

    all_tiers = ["🔥 ELITE TARGET","🟢 TOP TARGET","🔵 INTERESTING","🟡 WATCHLIST","🔴 RISIKO","⬜ NUR IFI"]
    sel_final_tiers = st.multiselect("Final Tier", all_tiers, default=all_tiers)

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec">🎯 IFI Gewichtung</div>', unsafe_allow_html=True)
    pos_for_weights = sel_pos if sel_pos != "Alle" else "Winger"
    pos_cfg_w = POS_CONFIG.get(pos_for_weights, POS_CONFIG["Winger"])
    weights = {}
    for attr, attr_de in zip(pos_cfg_w["attrs"], pos_cfg_w["attrs_de"]):
        weights[attr] = st.slider(attr_de, 0, 3, 1, key=f"w_{attr}")
    active_n = sum(1 for w in weights.values() if w > 0)
    if active_n > 0:
        st.success(f"{active_n}/{len(weights)} aktiv")
    else:
        st.warning("Alle deaktiviert")

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    sort_options = ["physical score","sc_psv-99","pct_score","pct_speed","pct_otip","pct_bip","pct_burst","age"]
    sort_options = [c for c in sort_options if c in df_raw.columns]
    sort_col = st.selectbox("Sortieren nach", sort_options,
        format_func=lambda x: {
            "physical score": "Physical Score",
            "sc_psv-99": "PSV-99",
            "pct_score": "IFI Perzentil",
            "pct_speed": "Speed Pct",
            "pct_otip":  "OTIP Pct",
            "pct_bip":   "BIP Pct",
            "pct_burst": "Burst Pct",
            "age":       "Alter",
        }.get(x, x))

# ── FILTER & RECALC ───────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_pos != "Alle" and "position" in df.columns:
    df = df[df["position"] == sel_pos]

df = recalc(df, weights, pos_for_weights)

mask = pd.Series([True]*len(df), index=df.index)
if sel_ligen and "liga" in df.columns:
    mask = mask & df["liga"].isin(sel_ligen)
if sel_markt and "markt" in df.columns:
    mask = mask & df["markt"].isin(sel_markt)
if sel_src and "datenquelle" in df.columns:
    mask = mask & df["datenquelle"].isin(sel_src)
if "sc_psv-99" in df.columns:
    mask = mask & ((pd.to_numeric(df["sc_psv-99"], errors="coerce") >= psv_min) | df["sc_psv-99"].isna())
if age_col and age_col in df.columns:
    mask = mask & (df[age_col] >= ar[0]) & (df[age_col] <= ar[1])
if min_col and min_col in df.columns:
    mask = mask & (df[min_col] >= mr[0]) & (df[min_col] <= mr[1])
if sel_final_tiers and "final_tier" in df.columns:
    mask = mask & df["final_tier"].isin(sel_final_tiers)

df_f = df[mask].sort_values(sort_col, ascending=False, na_position="last").reset_index(drop=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
cL, cT = st.columns([1,12])
with cL:
    st.markdown(f'<div style="padding-top:6px;"><img src="data:image/png;base64,{LOGO_B64_VAR}" style="width:48px;filter:drop-shadow(0 2px 6px {ORG}66);"></div>', unsafe_allow_html=True)
with cT:
    pos_label = f" · {POS_CONFIG[sel_pos]['de']}" if sel_pos != "Alle" else ""
    st.markdown(f'<div style="padding-top:8px;"><span style="font-size:22px;font-weight:800;color:#FFF;">Scouting Dashboard</span><span style="font-size:13px;color:#777;margin-left:12px;">Between The Lines{pos_label} &nbsp;·&nbsp;<span style="color:{ORG};font-weight:700;">{len(df_f)} Spieler</span> nach Filter</span></div>', unsafe_allow_html=True)

st.markdown('<div class="div" style="margin:10px 0 16px;"></div>', unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
kpi_cols = st.columns(6)
elite_top = len(df_f[df_f.get("final_tier", pd.Series(dtype=str)).isin(["🔥 ELITE TARGET","🟢 TOP TARGET"])]) if "final_tier" in df_f.columns else 0
ifi_elite = len(df_f[df_f.get("ifi_label", pd.Series(dtype=str)) == "ELITE"]) if "ifi_label" in df_f.columns else 0
max_psv   = f'{df_f["sc_psv-99"].max():.2f}' if "sc_psv-99" in df_f.columns and len(df_f) > 0 else "—"
max_ps    = f'{df_f["physical score"].max():.0f}' if "physical score" in df_f.columns and len(df_f) > 0 else "—"
med_age   = f'{int(df_f["age"].median())}' if "age" in df_f.columns and len(df_f) > 0 else "—"
kpis = [
    (len(df_f),  "Spieler gesamt"),
    (elite_top,  "Elite + Top"),
    (ifi_elite,  "IFI Elite 🔴"),
    (max_psv,    "Höchste PSV-99"),
    (max_ps,     "Bester Physical"),
    (med_age,    "Median Alter"),
]
for col, (val, lbl) in zip(kpi_cols, kpis):
    with col:
        st.markdown(f'<div class="jcard"><div class="val">{val}</div><div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📋 Spieler-Liste","🏟️ Team-Suche","📊 Scatter-Plot","📖 Info"])

# ── TAB 1: SPIELER-LISTE ──────────────────────────────────────────────────────
with tab1:
    global_search = st.text_input("🔍 Spieler suchen (Filter ignoriert)",
        placeholder="Name eingeben...", key="gsearch")

    def normalize(s):
        return (str(s).lower()
            .replace("ä","ae").replace("ö","oe").replace("ü","ue")
            .replace("ß","ss").replace("á","a").replace("é","e")
            .replace("ó","o").replace("ú","u").replace("ń","n"))

    if global_search:
        sn = normalize(global_search)
        df_display = df[df["name"].apply(lambda x: sn in normalize(x) if pd.notna(x) else False)]
        st.markdown(f'<div style="font-size:11px;color:{ORG};font-family:DM Mono;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px;">🔍 {len(df_display)} Treffer · Filter ignoriert</div>', unsafe_allow_html=True)
    else:
        df_display = df_f
        st.markdown(f'<div style="font-size:11px;color:#666;font-family:DM Mono;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px;">{len(df_display)} Spieler · Sortiert nach {sort_col}</div>', unsafe_allow_html=True)

    if df_display.empty:
        st.info("Keine Spieler mit diesen Filtern.")
    else:
        show_cols = [c for c in [
            "name","team","liga","position","spielertyp","markt","age",
            "physical score","final_tier","ifi_label",
            "speed_flag","sc_psv-99",
            "pct_score","pct_speed","pct_otip","pct_bip","pct_burst",
            "benchmark_bl","δ_vs_bl","benchmark_3liga","δ_vs_3liga",
        ] if c in df_display.columns]

        disp = df_display[show_cols].copy()
        disp = disp.rename(columns={
            "name":           "Spieler",
            "team":           "Verein",
            "liga":           "Liga",
            "position":       "Position",
            "spielertyp":     "Spielertyp",
            "markt":          "Markt",
            "age":            "Alter",
            "physical score": "Physical Score",
            "final_tier":     "Final Tier",
            "ifi_label":      "IFI Label",
            "speed_flag":     "Speed Flag",
            "sc_psv-99":      "PSV-99",
            "pct_score":      "IFI Pct",
            "pct_speed":      "Speed Pct",
            "pct_otip":       "OTIP Pct",
            "pct_bip":        "BIP Pct",
            "pct_burst":      "Burst Pct",
            "benchmark_bl":   "BM BL",
            "δ_vs_bl":        "Δ vs BL",
            "benchmark_3liga":"BM 3.Liga",
            "δ_vs_3liga":     "Δ vs 3L",
        })

        # Styling functions
        tier_bg = lambda v: {
            "🔥 ELITE TARGET": "background-color:#4A1500;color:#FFB380;font-weight:700",
            "🟢 TOP TARGET":   "background-color:#0A1F0A;color:#81C784;font-weight:700",
            "🔵 INTERESTING":  "background-color:#060E22;color:#90CAF9;font-weight:700",
            "🟡 WATCHLIST":    "background-color:#2A1A00;color:#FFCC80;font-weight:700",
            "🔴 RISIKO":       "background-color:#1A0000;color:#EF9A9A;font-weight:700",
        }.get(v, "")

        ifi_bg = lambda v: {
            "ELITE":   "background-color:#4A1500;color:#FFB380;font-weight:700",
            "STRONG":  "background-color:#2A1200;color:#FFCC80;font-weight:700",
            "AVERAGE": "background-color:#1A1A00;color:#FFF59D",
            "BELOW":   "background-color:#060E22;color:#90CAF9",
            "WEAK":    "color:#555",
        }.get(v, "")

        psv_bg = lambda v: ("" if pd.isna(v) else
            "background-color:#4A1500;color:#FFB380;font-weight:700" if v >= 32 else
            "background-color:#0D1F50;color:#90CAF9;font-weight:700" if v >= 31 else
            "background-color:#003344;color:#80DEEA;font-weight:700" if v >= 30 else
            "background-color:#2A1200;color:#FFCC80;font-weight:700" if v >= 29 else "color:#555")

        delta_style = lambda v: ("" if pd.isna(v) else
            "color:#81C784;font-weight:600" if v > 0 else
            "color:#EF9A9A;font-weight:600" if v < 0 else "")

        fmt = {k: v for k, v in {
            "PSV-99":       "{:.2f}",
            "Physical Score": "{:.0f}",
            "IFI Pct":      "{:.0f}",
            "Speed Pct":    "{:.0f}",
            "OTIP Pct":     "{:.0f}",
            "BIP Pct":      "{:.0f}",
            "Burst Pct":    "{:.0f}",
            "BM BL":        "{:.1f}",
            "Δ vs BL":      "{:+.1f}",
            "BM 3.Liga":    "{:.1f}",
            "Δ vs 3L":      "{:+.1f}",
        }.items() if k in disp.columns}

        styled = disp.style
        if "Final Tier" in disp.columns: styled = styled.map(tier_bg, subset=["Final Tier"])
        if "IFI Label"  in disp.columns: styled = styled.map(ifi_bg,  subset=["IFI Label"])
        if "PSV-99"     in disp.columns: styled = styled.map(psv_bg,  subset=["PSV-99"])
        if "Δ vs BL"    in disp.columns: styled = styled.map(delta_style, subset=["Δ vs BL"])
        if "Δ vs 3L"    in disp.columns: styled = styled.map(delta_style, subset=["Δ vs 3L"])
        styled = styled.format(fmt, na_rep="—")

        event = st.dataframe(styled, use_container_width=True, height=440,
                             on_select="rerun", selection_mode="single-row")

        sel_name = None
        if event and event.selection and event.selection.rows:
            idx = event.selection.rows[0]
            if idx < len(df_display):
                sel_name = df_display.iloc[idx]["name"]
        if global_search and len(df_display) == 1:
            sel_name = df_display.iloc[0]["name"]

        # Dropdown
        name_counts = df_display["name"].value_counts()
        def make_label(row):
            if name_counts.get(row["name"], 1) > 1:
                return f"{row['name']} ({row.get('position','?')})"
            return row["name"]
        display_labels = df_display.apply(make_label, axis=1).tolist()
        label_to_idx   = {lbl: i for i, lbl in enumerate(display_labels)}
        options        = ["— auswählen —"] + display_labels
        sel_default    = 0
        if sel_name:
            for i, lbl in enumerate(display_labels):
                if lbl.startswith(str(sel_name)):
                    sel_default = i + 1
                    break
        sel_dd = st.selectbox("Oder Spieler auswählen:", options, index=sel_default, key="dd")
        if sel_dd != "— auswählen —":
            row_idx  = label_to_idx.get(sel_dd, 0)
            sel_name = df_display.iloc[row_idx]["name"]
            sel_pos_row = df_display.iloc[row_idx].get("position", "Winger")
        else:
            sel_pos_row = ""

        # ── DETAIL ────────────────────────────────────────────────────────────
        if sel_name:
            row_m = df[df["name"] == sel_name]
            if not row_m.empty:
                row      = row_m.iloc[0]
                pos_row  = row.get("position", "Winger")
                tier_l, tier_c = physical_tier(row.get("physical score", 0) or 0)
                t_bg_val = TIER_COLORS.get(tier_l, "#333")
                ifi_lbl  = row.get("ifi_label", "—")
                em, ic, _ = IFI_LABEL_STYLE.get(ifi_lbl, ("—","#888","#FFF"))
                ps       = float(row.get("physical score", 0) or 0)
                ifi_pct  = float(row.get("pct_score", 0) or 0)
                mins     = safe_val(row.get("sc_minutes", row.get("minutes")), "—")
                has_physical = pd.notna(row.get("physical score"))
                has_ifi      = pd.notna(row.get("pct_score"))

                st.markdown("---")
                st.markdown(f"""
                <div style="background:#2E2E2E;border:1px solid #444;border-left:4px solid {ORG};
                            border-radius:8px;padding:16px 20px;margin-bottom:16px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="font-size:20px;font-weight:800;color:#FFF;">{row.get('name','—')}</div>
                            <div style="font-size:13px;color:#888;margin-top:4px;">
                                {row.get('team','—')} · {row.get('liga','—')} ·
                                {POS_CONFIG.get(pos_row,{}).get('de',pos_row)} ·
                                <span style="color:{ORG};">{row.get('spielertyp','—')}</span> ·
                                {safe_val(row.get('age'),'—')} J. · {mins} min
                            </div>
                        </div>
                        <div style="background:{t_bg_val};color:#FFF;padding:6px 14px;
                                    border-radius:20px;font-weight:700;font-size:13px;">{tier_l}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                d1, d2, d3, d4 = st.columns(4)
                with d1:
                    st.markdown(f'<div class="jcard"><div class="val">{ps:.0f}<span style="font-size:13px;color:#666;">/100</span></div><div class="lbl">Physical Score</div></div>', unsafe_allow_html=True)
                with d2:
                    st.markdown(f'<div class="jcard"><div class="val" style="font-size:16px;color:{tier_c};">{tier_l}</div><div class="lbl">Physical Tier</div></div>', unsafe_allow_html=True)
                with d3:
                    st.markdown(f'<div class="jcard"><div class="val">{ifi_pct:.0f}<span style="font-size:13px;color:#666;">%</span></div><div class="lbl">IFI Perzentil</div></div>', unsafe_allow_html=True)
                with d4:
                    st.markdown(f'<div class="jcard"><div class="val" style="font-size:16px;color:{ic};">{em}</div><div class="lbl">IFI Label</div></div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                ch1, ch2 = st.columns([1,1])
                with ch1:
                    if has_physical:
                        st.markdown("**⚡ Physical Breakdown**")
                        phys_html = render_physical_bars(row)
                        st.markdown(f'<div style="background:#2E2E2E;border:1px solid #444;border-radius:8px;padding:14px 16px;">{phys_html}</div>', unsafe_allow_html=True)
                    else:
                        st.info("⚡ Kein Physical Score — kein SkillCorner-Match")
                with ch2:
                    if has_ifi:
                        radar = make_radar(row, pos_row)
                        if radar:
                            st.plotly_chart(radar, use_container_width=True, key="radar")
                        else:
                            st.info("Keine IFI-Daten für diese Position")
                    else:
                        st.info("🎯 Kein IFI Profil — kein Twelve-Match")

                # TM Link + Downloads
                st.markdown("<br>", unsafe_allow_html=True)
                tm_q = str(row.get("name","")).replace(" ","+")
                st.markdown(f'<a href="https://www.transfermarkt.de/schnellsuche/ergebnis/schnellsuche?query={tm_q}" target="_blank" style="display:inline-block;background:#1a3c6e;color:#fff;padding:7px 16px;border-radius:6px;font-size:12px;font-weight:600;text-decoration:none;">🔗 Transfermarkt</a>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

                dl1, dl2, dl3 = st.columns(3)
                with dl1:
                    html_rep = make_html_report(row, pos_row)
                    st.download_button("📄 Profil HTML", html_rep.encode("utf-8"),
                        f"Profil_{str(row.get('name','player')).replace(' ','_')}.html",
                        "text/html", use_container_width=True)
                with dl2:
                    st.download_button("📊 Spieler CSV",
                        df[df["name"]==sel_name].to_csv(index=False).encode("utf-8"),
                        f"Daten_{str(row.get('name','player')).replace(' ','_')}.csv",
                        "text/csv", use_container_width=True)
                with dl3:
                    st.download_button("📋 Liste CSV",
                        df_f.to_csv(index=False).encode("utf-8"),
                        "btl_scouting.csv", "text/csv", use_container_width=True)

# ── TAB 2: TEAM-SUCHE ────────────────────────────────────────────────────────
with tab2:
    st.markdown("### 🏟️ Team-Suche")
    team_search = st.text_input("Vereinsname eingeben:", placeholder="z.B. Wolfsburg, Sturm Graz...", key="team_s")

    if team_search and "team" in df.columns:
        df_team = df[df["team"].str.contains(team_search, case=False, na=False)]
        if df_team.empty:
            st.info(f"Kein Verein gefunden für: {team_search}")
        else:
            vereine = df_team["team"].unique()
            for verein in vereine:
                df_v = df_team[df_team["team"]==verein].sort_values("physical score", ascending=False, na_position="last")
                liga  = df_v["liga"].iloc[0] if "liga" in df_v.columns else "—"
                markt = df_v["markt"].iloc[0] if "markt" in df_v.columns else "DACH"

                st.markdown(f"""
                <div style="background:#2E2E2E;border:1px solid #444;border-left:4px solid {ORG};
                            border-radius:8px;padding:12px 16px;margin-bottom:12px;">
                    <span style="font-size:16px;font-weight:700;color:#FFF;">{verein}</span>
                    <span style="font-size:12px;color:#888;margin-left:12px;">{liga} · {markt} · {len(df_v)} Spieler</span>
                </div>
                """, unsafe_allow_html=True)

                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    avg_ps = df_v["physical score"].mean() if "physical score" in df_v.columns else 0
                    st.markdown(f'<div class="jcard"><div class="val">{avg_ps:.0f}</div><div class="lbl">Ø Physical Score</div></div>', unsafe_allow_html=True)
                with m2:
                    max_psv = df_v["sc_psv-99"].max() if "sc_psv-99" in df_v.columns else 0
                    st.markdown(f'<div class="jcard"><div class="val">{max_psv:.2f}</div><div class="lbl">Max PSV-99</div></div>', unsafe_allow_html=True)
                with m3:
                    et = len(df_v[df_v.get("final_tier", pd.Series(dtype=str)).isin(["🔥 ELITE TARGET","🟢 TOP TARGET"])]) if "final_tier" in df_v.columns else 0
                    st.markdown(f'<div class="jcard"><div class="val">{et}</div><div class="lbl">Elite + Top</div></div>', unsafe_allow_html=True)
                with m4:
                    pos_dist = df_v["position"].value_counts().to_dict() if "position" in df_v.columns else {}
                    pos_str  = " · ".join([f"{p}: {n}" for p, n in pos_dist.items()])
                    st.markdown(f'<div class="jcard"><div class="val" style="font-size:12px;">{pos_str or "—"}</div><div class="lbl">Positionen</div></div>', unsafe_allow_html=True)

                show = [c for c in ["name","position","age","physical score","final_tier","ifi_label","sc_psv-99","speed_flag","spielertyp"] if c in df_v.columns]
                st.dataframe(df_v[show].rename(columns={
                    "name":"Spieler","position":"Position","age":"Alter",
                    "physical score":"Physical Score","final_tier":"Final Tier",
                    "ifi_label":"IFI Label","sc_psv-99":"PSV-99",
                    "speed_flag":"Speed Flag","spielertyp":"Spielertyp"
                }).reset_index(drop=True), use_container_width=True, height=200)
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#888;font-size:13px;">Vereinsnamen eingeben um alle Spieler dieses Teams anzuzeigen.</div>', unsafe_allow_html=True)

# ── TAB 3: SCATTER ────────────────────────────────────────────────────────────
with tab3:
    num_cols = [c for c in [
        "sc_psv-99","physical score","pct_score","pct_speed","pct_otip","pct_bip","pct_burst",
        "age","δ_vs_bl","δ_vs_3liga"
    ] if c in df_f.columns]

    col_labels = {
        "sc_psv-99":      "PSV-99",
        "physical score": "Physical Score",
        "pct_score":      "IFI Perzentil",
        "pct_speed":      "Speed Pct",
        "pct_otip":       "OTIP Pct",
        "pct_bip":        "BIP Pct",
        "pct_burst":      "Burst Pct",
        "age":            "Alter",
        "δ_vs_bl":        "Δ vs BL",
        "δ_vs_3liga":     "Δ vs 3.Liga",
    }

    c1, c2, c3, c4 = st.columns(4)
    with c1: x  = st.selectbox("X-Achse", num_cols, index=0, format_func=lambda v: col_labels.get(v,v))
    with c2: y  = st.selectbox("Y-Achse", num_cols, index=1, format_func=lambda v: col_labels.get(v,v))
    with c3: sz = st.selectbox("Größe", ["—"]+num_cols, index=0, format_func=lambda v: col_labels.get(v,v))
    with c4: cb = st.selectbox("Farbe", ["final_tier","speed_flag","ifi_label","position","markt","liga"], index=0,
                                format_func=lambda v: {"final_tier":"Final Tier","speed_flag":"Speed Flag",
                                    "ifi_label":"IFI Label","position":"Position","markt":"Markt","liga":"Liga"}.get(v,v))

    if not df_f.empty:
        try:
            pdf_p = df_f.dropna(subset=[x,y]).copy()
            cm    = TIER_COLORS if cb == "final_tier" else (SPEED_FLAGS if cb == "speed_flag" else None)
            sv    = None
            if sz != "—" and sz in pdf_p.columns:
                s  = pd.to_numeric(pdf_p[sz], errors="coerce").fillna(0)
                sv = (((s - s.min()) / (s.max() - s.min() + 0.001)) * 20 + 6).tolist()

            fig = px.scatter(pdf_p, x=x, y=y, color=cb, color_discrete_map=cm,
                hover_name="name",
                hover_data={c: True for c in ["team","liga","position","sc_psv-99"] if c in pdf_p.columns},
                size=sv, size_max=24, template="plotly_dark", height=520,
                labels={k: col_labels.get(k,k) for k in [x,y,cb]})

            if x == "sc_psv-99": fig.add_vline(x=29.0, line_dash="dash", line_color=ORG, annotation_text="PSV-99 29.0", annotation_font_size=11)
            if y == "sc_psv-99": fig.add_hline(y=29.0, line_dash="dash", line_color=ORG)

            fig.update_layout(
                paper_bgcolor=BG, plot_bgcolor="#333",
                font_family="DM Sans", font_color="#AAA",
                xaxis=dict(gridcolor="#3A3A3A", zeroline=False),
                yaxis=dict(gridcolor="#3A3A3A", zeroline=False),
                legend=dict(bgcolor="#333", bordercolor="#444", borderwidth=1),
                margin=dict(l=40,r=20,t=40,b=40))
            fig.update_traces(marker=dict(line=dict(width=0.5, color=BG)))
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Fehler: {e}")

# ── TAB 4: INFO ───────────────────────────────────────────────────────────────
with tab4:
    ca, cb_ = st.columns(2)
    with ca:
        st.markdown("### Physical Score /100")
        st.markdown("""
Peer-Perzentil pro Position + Liga — 100 = bester Spieler in seiner Liga und Position.

| Komponente | Winger | Striker | MF | FB | IV |
|---|---|---|---|---|---|
| ⚡ Speed (PSV-99) | ×2.0 | ×1.0 | ×0.5 | ×1.0 | ×0.5 |
| 🏃 OTIP (Off-Ball) | ×1.5 | ×1.0 | ×1.5 | ×2.5 | ×2.5 |
| 💥 BIP (Lauf-Int.) | ×0.5 | ×1.0 | ×1.5 | ×1.5 | ×1.5 |
| 🚀 Burst (Explo.)  | ×2.0 | ×1.0 | ×2.0 | ×0.5 | ×1.5 |

**Tiers:** ≥80 🔥 ELITE · ≥65 🟢 TOP · ≥50 🔵 INT · ≥35 🟡 WATCHLIST · <35 🔴 RISIKO

**Benchmarks:** BL-Median + 3.Liga-Median pro Position (Δ = Differenz zum Median)
        """)
    with cb_:
        st.markdown("### IFI System (IFI-Attribute)")
        st.markdown("""
Peer-Perzentil der Twelve-Attribute pro Position + Liga.

| Perzentil | Label |
|---|---|
| Top 10% | 🔴 ELITE |
| Top 25% | 🟠 STRONG |
| Top 50% | 🟡 AVERAGE |
| Top 75% | 🔵 BELOW |
| Rest | ⚫ WEAK |

**Speed Flags (absolut, positionsunabhängig):**
- ⚡ ELITE ≥ 32 km/h
- 🔵 HIGH ≥ 31 km/h
- 🟡 FAST ≥ 30 km/h
- 🟠 MEDIUM ≥ 29 km/h

**Rollenprofile:** Clustering auf allen Ligen (≥500 min) — BL als Qualitätsreferenz

**IFI-Attribute** werden über Twelve (Football Intelligence Platform) gemessen.
        """)

    st.markdown("---")
    st.markdown(f"<div style='text-align:center;color:#666;font-size:11px;'>Between The Lines Scouting Intelligence · {datetime.now().strftime('%Y')}</div>", unsafe_allow_html=True)
