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

def safe_int(val, default=0):
    try:
        import math
        if val is None or (isinstance(val,float) and math.isnan(val)): return default
        return int(val or default)
    except: return default

# ── PASSWORT-SCHUTZ ───────────────────────────────────────────────────────────
LOGO_B64_VAR = "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"

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
            <div style="font-size:22px;font-weight:800;color:#FFF;margin-top:12px;">
                Between The Lines
            </div>
            <div style="font-size:12px;color:#888;letter-spacing:0.15em;
                        text-transform:uppercase;margin-top:4px;">
                Scouting Intelligence
            </div>
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

LOGO_B64_VAR = "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"

# Colors
ORG  = "#E8560A"   # BTL Orange
ORG2 = "#B84000"   # Darker orange
BG   = "#2A2A2A"   # Dark background (like ecosystem slide)
C1   = "#333333"   # Card background
C2   = "#444444"   # Border
W    = "#FFFFFF"
W2   = "#F0F0F0"
MUT  = "#888888"

# Position configs
POS_CONFIG = {
    "Winger": {
        "de": "Außenstürmer",
        "attrs": ["Involvement","Finishing","Providing teammates",
                  "Dribbling","Passing quality","Box threat","Pressing","Run quality"],
        "attrs_de": ["Spielbeteiligung","Abschluss","Vorlagenqualität",
                     "Dribbling","Passqualität","Strafraum-Gefahr","Pressing","Laufqualität"],
    },
    "Striker": {
        "de": "Mittelstürmer",
        "attrs": ["Poaching","Aerial threat","Involvement","Finishing",
                  "Providing teammates","Hold-up play","Pressing","Run quality"],
        "attrs_de": ["Positionsspiel","Kopfballstärke","Spielbeteiligung","Abschluss",
                     "Vorlagenqualität","Ballbehauptung","Pressing","Laufqualität"],
    },
    "Midfielder": {
        "de": "Mittelfeldspieler",
        "attrs": ["Intelligent defence","Involvement","Progression",
                  "Providing teammates","Passing quality","Box threat","Active defence"],
        "attrs_de": ["Int. Verteidigen","Spielbeteiligung","Spielverlagerung",
                     "Vorlagenqualität","Passqualität","Strafraum-Gefahr","Akt. Verteidigen"],
    },
    "Fullback": {
        "de": "Außenverteidiger",
        "attrs": ["Territorial dominance","Intelligent defence","Involvement","Progression",
                  "Chance prevention","Providing teammates","Passing quality","Active defence","Run quality"],
        "attrs_de": ["Raumkontrolle","Int. Verteidigen","Spielbeteiligung","Spielverlagerung",
                     "Torverhinderung","Vorlagenqualität","Passqualität","Akt. Verteidigen","Laufqualität"],
    },
    "Central Defender": {
        "de": "Innenverteidiger",
        "attrs": ["Territorial dominance","Composure","Aerial threat","Intelligent defence",
                  "Involvement","Progression","Chance prevention","Defensive heading","Active defence"],
        "attrs_de": ["Raumkontrolle","Ruhe am Ball","Kopfballstärke","Int. Verteidigen",
                     "Spielbeteiligung","Spielverlagerung","Torverhinderung","Kopfballduell","Akt. Verteidigen"],
    },
}

LABEL_STYLE = {
    "ELITE":   ("🔴 ELITE",   "#CC0000","#FFFFFF"),
    "STRONG":  ("🟠 STRONG",  "#E8560A","#FFFFFF"),
    "AVERAGE": ("🟡 AVERAGE", "#F0A500","#1A1A1A"),
    "BELOW":   ("🔵 BELOW",   "#1565C0","#FFFFFF"),
    "WEAK":    ("⚫ WEAK",    "#555555","#AAAAAA"),
}
TIER_COLORS = {
    "🔥 ELITE TARGET":"#E8560A","🟢 TOP TARGET":"#1B5E20",
    "🔵 INTERESTING":"#0D47A1","🟡 WATCHLIST":"#F0A500","🔴 RISIKO":"#4A0D0D",
    "⬜ NUR IFI":"#444444",
}
SPEED_COLORS = {
    "⚡ ELITE":"#E8560A","🔵 HIGH":"#1565C0",
    "🟡 FAST":"#0288D1","🟠 MEDIUM":"#B84000","—":"#444444",
}

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
.pbar-info{{font-size:11px;color:#888;min-width:40px;text-align:right;font-family:DM Mono,monospace;}}
.ifi-row{{display:flex;align-items:center;padding:5px 0;border-bottom:1px solid #3A3A3A;gap:10px;}}
.ifi-name{{font-size:12px;color:#CCC;min-width:150px;}}
.ifi-bg{{background:#3A3A3A;border-radius:4px;height:8px;flex:1;}}
.ifi-info{{font-size:11px;min-width:100px;text-align:right;font-family:DM Mono,monospace;}}
.src-badge{{display:inline-block;padding:2px 8px;border-radius:12px;font-size:10px;font-weight:600;}}
.stTextInput input{{background:#333 !important;color:#FFF !important;border:1px solid #555 !important;}}
</style>
""", unsafe_allow_html=True)

if not check_password():
    st.stop()

# ── DATA ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/btl_scouting_app_data.csv")
    return df

B = dict(psv_med=29.45)
df_raw = load_data()

def recalc_ifi(df, weights, position):
    df = df.copy()
    pos_cfg = POS_CONFIG.get(position, {})
    attrs = pos_cfg.get("attrs", [])
    active = {a:w for a,w in weights.items() if w>0}
    pct_cols = [f"Pct_{a}" for a in attrs if f"Pct_{a}" in df.columns and a in active]

    if pct_cols:
        tw = sum(active.get(a.replace("Pct_",""),0) for a in pct_cols)
        if tw > 0:
            raw = sum(df[c].fillna(0)*(active.get(c.replace("Pct_",""),1)/tw) for c in pct_cols)
            df["IFI Percentile"] = raw.rank(pct=True).round(3)
        else:
            df["IFI Percentile"] = df["IFI Percentile"] if "IFI Percentile" in df.columns else 0.5
    elif "IFI Percentile" in df.columns:
        pass

    pct_labels = dict(elite=0.90, strong=0.75, average=0.50, below=0.25)
    df["IFI Label"] = df["IFI Percentile"].apply(lambda p:
        "ELITE" if pd.notna(p) and p>=pct_labels["elite"] else
        "STRONG" if pd.notna(p) and p>=pct_labels["strong"] else
        "AVERAGE" if pd.notna(p) and p>=pct_labels["average"] else
        "BELOW" if pd.notna(p) and p>=pct_labels["below"] else
        "WEAK" if pd.notna(p) else "—")

    def _tier(r):
        ps = r["Physical Score"]
        if pd.isna(ps): return "⬜ NUR IFI"
        if   ps>=16: base="🔥 ELITE TARGET"
        elif ps>=14: base="🟢 TOP TARGET"
        elif ps>=12: base="🔵 INTERESTING"
        elif ps>=9:  base="🟡 WATCHLIST"
        else:        base="🔴 RISIKO"
        order=["🔥 ELITE TARGET","🟢 TOP TARGET","🔵 INTERESTING","🟡 WATCHLIST","🔴 RISIKO"]
        if r["IFI Label"] in ["BELOW","WEAK"] and base in order:
            return order[max(order.index(base),3)]
        return base
    df["Final Tier"] = df.apply(_tier, axis=1)
    return df

def physical_label(ps):
    if   ps>=16: return "🔥 ELITE",   ORG
    elif ps>=14: return "🟢 TOP",     "#1B5E20"
    elif ps>=12: return "🔵 INTERESTING","#0D47A1"
    elif ps>=9:  return "🟡 WATCHLIST",ORG2
    else:        return "🔴 RISIKO",  "#4A0D0D"

def render_physical_bars(row):
    comps = [
        ("⚡ Top-Speed", int(row.get("Speed Score",0) or 0), 4, ORG),
        ("🏃 Off-Ball Intensität",int(row.get("OTIP Score",0) or 0),  4, "#E65100"),
        ("💥 Lauf-Intensität",    int(row.get("BIP Score",0) or 0),   4, "#1565C0"),
        ("🚀 Explosivität",       int(row.get("Burst Score",0) or 0), 4, "#2E7D32"),
    ]
    html = ""
    for name,val,maxv,color in comps:
        pct = int(val/maxv*100) if maxv>0 else 0
        html += f"""<div class="pbar-row">
            <div class="pbar-name">{name}</div>
            <div class="pbar-bg"><div style="width:{pct}%;height:10px;border-radius:4px;background:{color};"></div></div>
            <div class="pbar-info">{val}/{maxv}</div>
        </div>"""
    sf  = str(row.get("Speed Flag","—"))
    dpv = float(row.get("Δ PSV-99",0) or 0)
    dc  = "#81C784" if dpv>0 else "#EF9A9A"
    sf_c= {ORG:"⚡","🔵 HIGH":"#1565C0","🟡 FAST":"#0288D1","🟠 MEDIUM":ORG2}.get(sf,"#888")
    html += f'<div style="margin-top:8px;font-size:12px;color:#888;">PSV-99: <b style="color:#FFF;">{row.get("PSV-99",0):.2f} km/h</b> <span style="color:{ORG};">{sf}</span> · Δ vs Benchmark: <b style="color:{dc};">{dpv:+.2f}</b></div>'
    return html

def make_radar(row, position):
    pos_cfg = POS_CONFIG.get(position, {})
    attrs    = pos_cfg.get("attrs", [])
    attrs_de = pos_cfg.get("attrs_de", attrs)
    vals, labels = [], []
    for attr, attr_de in zip(attrs, attrs_de):
        col = f"Pct_{attr}"
        if col in row.index and pd.notna(row[col]):
            vals.append(float(row[col])*100)
            labels.append(attr_de)
    if len(vals) < 3:
        return None
    vals_c   = vals + [vals[0]]
    labels_c = labels + [labels[0]]
    ifi_lbl  = row.get("IFI Label","—")
    em,ic,_  = LABEL_STYLE.get(ifi_lbl,("—","#888","#FFF"))
    fig = go.Figure()
    for ring,op in [(100,0.02),(75,0.03),(50,0.04),(25,0.05)]:
        fig.add_trace(go.Scatterpolar(
            r=[ring]*(len(vals)+1), theta=labels_c, mode="lines",
            line=dict(color="#FFFFFF",width=0.5), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatterpolar(
        r=[50]*(len(vals)+1), theta=labels_c, mode="lines",
        line=dict(color="#666",width=1.5,dash="dot"),
        name="Median (50%)", hoverinfo="skip"))
    fig.add_trace(go.Scatterpolar(
        r=vals_c, theta=labels_c, fill="toself",
        fillcolor=f"rgba(232,86,10,0.18)",
        line=dict(color=ORG,width=2.5),
        name=f"IFI · {em}",
        hovertemplate="%{theta}: <b>%{r:.0f}%</b><extra></extra>"))
    fig.update_layout(
        polar=dict(bgcolor="#2A2A2A",
            radialaxis=dict(visible=True,range=[0,100],
                tickvals=[25,50,75,100],ticktext=["25%","50%","75%","100%"],
                tickfont=dict(color="#666",size=9),gridcolor="#3A3A3A",linecolor="#3A3A3A"),
            angularaxis=dict(tickfont=dict(color="#DDD",size=10),
                gridcolor="#3A3A3A",linecolor="#444",direction="clockwise")),
        paper_bgcolor=BG, font=dict(family="DM Sans",color="#CCC"),
        showlegend=True,
        legend=dict(bgcolor="#333",bordercolor="#444",borderwidth=1,
            font=dict(color="#888",size=10),orientation="h",y=-0.15,x=0.5,xanchor="center"),
        margin=dict(l=60,r=60,t=50,b=60), height=400,
        title=dict(text=f"IFI Radar · {em} · {int(row.get('IFI Percentile',0.5)*100)}. Percentile",
            font=dict(size=12,color=ic),x=0.5))
    return fig

def make_pdf(row, position):
    pos_cfg  = POS_CONFIG.get(position,{})
    attrs    = pos_cfg.get("attrs",[])
    attrs_de = pos_cfg.get("attrs_de",attrs)
    ifi_lbl  = row.get("IFI Label","—")
    em,ic,_  = LABEL_STYLE.get(ifi_lbl,("—","#888","#FFF"))
    ps       = row.get("Physical Score",0) or 0
    pl,pc    = physical_label(ps)
    ifi_pct  = int((row.get("IFI Percentile",0.5) or 0.5)*100)
    tier_str = row.get("Final Tier","—")
    t_bg     = TIER_COLORS.get(tier_str,"#333")
    dpv      = float(row.get("Δ PSV-99",0) or 0)
    dc       = "#2E7D32" if dpv>0 else "#CC0000"
    src      = row.get("Datenquelle","vollständig")
    src_note = {"vollständig":"Physical + IFI","nur_physical":"Nur Physical Score",
                "nur_ifi":"Nur IFI Profil"}.get(src,src)

    phys_rows = ""
    for nm,val,maxv,wgt,color in [
        ("⚡ Top-Speed",int(row.get("Speed Score",0) or 0),4,2.0,ORG),
        ("🏃 Off-Ball Intensität",int(row.get("OTIP Score",0) or 0),4,1.5,"#E65100"),
        ("💥 Lauf-Intensität",int(row.get("BIP Score",0) or 0),4,1.0,"#1565C0"),
        ("🚀 Explosivität",int(row.get("Burst Score",0) or 0),4,0.5,"#2E7D32"),
    ]:
        pct = int(val/maxv*100) if maxv>0 else 0
        phys_rows += f"""<tr>
            <td style="padding:6px 8px;font-size:12px;color:#333;">{nm}</td>
            <td style="padding:6px 8px;width:180px;">
                <div style="background:#eee;border-radius:4px;height:10px;">
                    <div style="background:{color};width:{pct}%;height:10px;border-radius:4px;"></div>
                </div>
            </td>
            <td style="padding:6px 8px;font-size:12px;color:#555;">{val}/{maxv}</td>
        </tr>"""

    ifi_rows = ""
    for attr,attr_de in zip(attrs, attrs_de):
        pcol = f"Pct_{attr}"
        lcol = f"Lbl_{attr}"
        if pcol not in row.index or pd.isna(row.get(pcol)): continue
        pct = float(row[pcol])*100
        lbl = row.get(lcol,"—")
        em2,c2,_ = LABEL_STYLE.get(lbl,("—","#999","#FFF"))
        ifi_rows += f"""<tr>
            <td style="padding:5px 8px;font-size:12px;color:#333;">{attr_de}</td>
            <td style="padding:5px 8px;width:180px;">
                <div style="background:#eee;border-radius:4px;height:8px;">
                    <div style="background:{c2};width:{int(pct)}%;height:8px;border-radius:4px;"></div>
                </div>
            </td>
            <td style="padding:5px 8px;font-size:12px;color:{c2};font-weight:600;">{int(pct)}% {em2}</td>
        </tr>"""

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<title>Scouting Report – {row.get("Spieler","—")}</title>
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
.src{{font-size:11px;color:#888;text-align:right;margin-bottom:8px;}}
@media print{{body{{padding:10px;}}}}
</style></head><body>
<div class="header">
    <h1>{row.get("Spieler","—")}</h1>
    <p>{row.get("Verein","—")} · {row.get("Liga","—")} · {pos_cfg.get("de",position)} · {safe_int(row.get("Alter"))} J. · {safe_int(row.get("Minuten"))} min</p>
    <div class="badge">{tier_str}</div>
</div>
<div class="src">Daten: {src_note} | Between The Lines Scouting | {datetime.now().strftime("%d.%m.%Y")}</div>
<div class="cards">
    <div class="card"><div class="val">{ps:.1f}/20</div><div class="lbl">Physical Score</div></div>
    <div class="card"><div class="val" style="color:{pc};">{pl}</div><div class="lbl">Physical Label</div></div>
    <div class="card"><div class="val">{ifi_pct}%</div><div class="lbl">IFI Percentile</div></div>
    <div class="card"><div class="val" style="color:{ic};">{em}</div><div class="lbl">IFI Label</div></div>
</div>
<div class="cards">
    <div class="card"><div class="val">{row.get("PSV-99",0):.2f} km/h</div><div class="lbl">PSV-99</div></div>
    <div class="card"><div class="val" style="color:{dc};">{dpv:+.2f}</div><div class="lbl">Δ vs Benchmark</div></div>
    <div class="card"><div class="val">{row.get("Speed Flag","—")}</div><div class="lbl">Speed Flag</div></div>
    <div class="card"><div class="val">{row.get("Spielertyp","—")}</div><div class="lbl">Spielertyp</div></div>
</div>
<div class="section"><h2>⚡ Physical Breakdown</h2><table>{phys_rows}</table></div>
<div class="section"><h2>🎯 IFI Profil — {pos_cfg.get("de",position)}</h2><table>{ifi_rows}</table></div>
</body></html>"""

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:20px 0 14px;">
        <img src="data:image/png;base64,{LOGO_B64_VAR}" style="width:90px;filter:drop-shadow(0 0 14px {ORG}88);">
        <div style="font-size:14px;font-weight:800;color:#FFF;
                    margin-top:10px;letter-spacing:0.06em;">BETWEEN THE LINES</div>
        <div style="font-size:10px;color:#888;letter-spacing:0.18em;
                    text-transform:uppercase;margin-top:3px;">Scouting Intelligence</div>
    </div>
    <div class="div"></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec">Position</div>', unsafe_allow_html=True)
    all_pos = ["Alle"] + [p for p in POS_CONFIG.keys() if p in df_raw.get("Position", pd.Series()).unique().tolist()]
    if "Position" in df_raw.columns:
        avail_pos = ["Alle"] + [p for p in POS_CONFIG.keys() if p in df_raw["Position"].unique()]
    else:
        avail_pos = ["Alle"]
    sel_pos = st.selectbox("Position", avail_pos, label_visibility="collapsed")

    st.markdown('<div class="sec" style="margin-top:10px;">Filter</div>', unsafe_allow_html=True)

    # Markt filter
    if "Markt" in df_raw.columns:
        maerkte = ["Alle"] + sorted(df_raw["Markt"].dropna().unique().tolist())
        sel_markt = st.multiselect("Markt", maerkte[1:], default=maerkte[1:])
    else:
        sel_markt = []

    if "Liga" in df_raw.columns:
        ligen = sorted(df_raw["Liga"].dropna().unique().tolist())
        sel_ligen = st.multiselect("Liga", ligen, default=ligen)
    else:
        sel_ligen = []

    psv_min = st.slider("PSV-99 Minimum (km/h)", 0.0, 33.0, 0.0, 0.5, format="%.1f")
    ar = st.slider("Alter", int(df_raw["Alter"].min()) if "Alter" in df_raw.columns else 15,
                   int(df_raw["Alter"].max()) if "Alter" in df_raw.columns else 40,
                   (15, 35) if "Alter" not in df_raw.columns else
                   (int(df_raw["Alter"].min()), int(df_raw["Alter"].max())))
    mr = st.slider("Minuten", 0, int(df_raw["Minuten"].max()) if "Minuten" in df_raw.columns else 3000,
                   (100, int(df_raw["Minuten"].max()) if "Minuten" in df_raw.columns else 3000), step=50)

    all_tiers = ["🔥 ELITE TARGET","🟢 TOP TARGET","🔵 INTERESTING","🟡 WATCHLIST","🔴 RISIKO","⬜ NUR IFI"]
    sel_tiers = st.multiselect("Final Tier", all_tiers, default=all_tiers)
    otip_gate = st.checkbox("Nur Off-Ball Pass ✅ (OTIP ≥2)", value=False)

    # Datenquelle filter
    if "Datenquelle" in df_raw.columns:
        sel_src = st.multiselect("Datenquelle",
            ["vollständig","nur_physical","nur_ifi"],
            default=["vollständig","nur_physical","nur_ifi"])
    else:
        sel_src = []

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)

    # IFI weights — per position
    st.markdown('<div class="sec">🎯 IFI Gewichtung</div>', unsafe_allow_html=True)
    pos_for_weights = sel_pos if sel_pos != "Alle" else "Winger"
    pos_cfg_w = POS_CONFIG.get(pos_for_weights, POS_CONFIG["Winger"])
    weights = {}
    for attr, attr_de in zip(pos_cfg_w["attrs"], pos_cfg_w["attrs_de"]):
        weights[attr] = st.slider(attr_de, 0, 4, 1, 1, key=f"ifi_{attr}")
    active_n = sum(1 for w in weights.values() if w>0)
    if active_n > 0: st.success(f"{active_n}/{len(weights)} aktiv")
    else: st.warning("Alle deaktiviert")

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    sort_col = st.selectbox("Sortieren nach", [
        "Physical Score","PSV-99","IFI Percentile",
        "OTIP Score","BIP Score","Burst Score","Alter","Minuten"])

# ── FILTER & RECALC ───────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_pos != "Alle" and "Position" in df.columns:
    df = df[df["Position"]==sel_pos]

df = recalc_ifi(df, weights, pos_for_weights)

mask = pd.Series([True]*len(df), index=df.index)
if sel_ligen and "Liga" in df.columns:
    mask = mask & (df["Liga"].isin(sel_ligen) | (df["Datenquelle"]=="nur_ifi") | df["Liga"].isna())
if sel_markt and "Markt" in df.columns:
    mask = mask & (df["Markt"].isin(sel_markt) | (df["Datenquelle"]=="nur_ifi") | df["Markt"].isna())
if "PSV-99" in df.columns:
    mask = mask & ((pd.to_numeric(df["PSV-99"],errors="coerce") >= psv_min) | (df["PSV-99"].isna()))
if "Alter" in df.columns:
    mask = mask & (df["Alter"]>=ar[0]) & (df["Alter"]<=ar[1])
if "Minuten" in df.columns:
    mask = mask & ((df["Minuten"]>=mr[0]) & (df["Minuten"]<=mr[1]) | (df["Minuten"]==0))
if sel_tiers:
    mask = mask & df["Final Tier"].isin(sel_tiers)
if sel_src and "Datenquelle" in df.columns:
    mask = mask & df["Datenquelle"].isin(sel_src)
if otip_gate and "OTIP Pass" in df.columns:
    mask = mask & (df["OTIP Pass"]=="✅ YES")

df_f = df[mask].sort_values(sort_col, ascending=False, na_position="last").reset_index(drop=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
cL,cT = st.columns([1,12])
with cL:
    st.markdown(f'<div style="padding-top:6px;"><img src="data:image/png;base64,{LOGO_B64_VAR}" style="width:48px;filter:drop-shadow(0 2px 6px {ORG}66);"></div>', unsafe_allow_html=True)
with cT:
    pos_label = f" · {POS_CONFIG[sel_pos]['de']}" if sel_pos != "Alle" else ""
    st.markdown(f'<div style="padding-top:8px;"><span style="font-size:22px;font-weight:800;color:#FFF;">Scouting Dashboard</span><span style="font-size:13px;color:#777;margin-left:12px;">Between The Lines{pos_label} &nbsp;·&nbsp;<span style="color:{ORG};font-weight:700;">{len(df_f)} Spieler</span> nach Filter</span></div>', unsafe_allow_html=True)

st.markdown('<div class="div" style="margin:10px 0 16px;"></div>', unsafe_allow_html=True)

# KPIs
kpi_cols = st.columns(6)
kpis = [
    (len(df_f), "Spieler gesamt"),
    (len(df_f[df_f["Final Tier"].isin(["🔥 ELITE TARGET","🟢 TOP TARGET"])]) if len(df_f)>0 else 0, "Elite + Top"),
    (len(df_f[df_f.get("IFI Label","—")=="ELITE"]) if "IFI Label" in df_f.columns else 0, "IFI Elite 🔴"),
    (f"{df_f['PSV-99'].max():.2f}" if len(df_f)>0 and "PSV-99" in df_f.columns else "—", "Höchste PSV-99"),
    (f"{df_f['Physical Score'].max():.1f}" if len(df_f)>0 and "Physical Score" in df_f.columns else "—", "Bester Physical /20"),
    (f"{int(df_f['Alter'].median())}" if len(df_f)>0 and "Alter" in df_f.columns else "—", "Median Alter"),
]
for col,(val,lbl) in zip(kpi_cols,kpis):
    with col:
        st.markdown(f'<div class="jcard"><div class="val">{val}</div><div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📋 Spieler-Liste","🏟️ Team-Suche","📊 Scatter-Plot","📖 Info"])

# ── TAB 1: Spieler-Liste ──────────────────────────────────────────────────────
with tab1:
    # Global search
    global_search = st.text_input("🔍 Spieler suchen (alle Spieler, Filter ignoriert)",
        placeholder="Name eingeben...", key="gsearch")

    if global_search:
        df_display = df[df["Spieler"].str.contains(global_search, case=False, na=False)]
        st.markdown(f'<div style="font-size:11px;color:{ORG};font-family:DM Mono,monospace;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px;">🔍 {len(df_display)} Treffer · Filter ignoriert</div>', unsafe_allow_html=True)
    else:
        df_display = df_f
        st.markdown(f'<div style="font-size:11px;color:#666;font-family:DM Mono,monospace;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px;">{len(df_display)} Spieler · Sortiert nach {sort_col}</div>', unsafe_allow_html=True)

    if df_display.empty:
        st.info("Keine Spieler mit diesen Filtern.")
    else:
        # Display columns
        show_cols = [c for c in [
            "Spieler","Verein","Liga","Position","Markt","Alter","Minuten",
            "Physical Score","Final Tier","IFI Label",
            "Speed Flag","PSV-99","Δ PSV-99",
            "OTIP Pass","OTIP Score","BIP Level","BIP Score",
            "Burst Score","Spielertyp","Datenquelle",
        ] if c in df_display.columns]

        disp = df_display[show_cols].copy()
        disp = disp.rename(columns={
            "OTIP Score":  "Off-Ball Int.",
            "BIP Score":   "Lauf-Int.",
            "BIP Level":   "Lauf-Int. Level",
            "Burst Score": "Explo.",
            "OTIP Pass":   "Off-Ball Pass",
            "Speed Flag":  "Top-Speed",
        })

        tier_bg = lambda v:{
            "🔥 ELITE TARGET":f"background-color:#4A1500;color:#FFB380;font-weight:700",
            "🟢 TOP TARGET":"background-color:#0A1F0A;color:#81C784;font-weight:700",
            "🔵 INTERESTING":"background-color:#060E22;color:#90CAF9;font-weight:700",
            "🟡 WATCHLIST":"background-color:#2A1A00;color:#FFCC80;font-weight:700",
            "🔴 RISIKO":"background-color:#1A0000;color:#EF9A9A;font-weight:700",
            "⬜ NUR IFI":"background-color:#2A2A2A;color:#AAAAAA",
        }.get(v,"")
        ifi_bg = lambda v:{
            "ELITE":f"background-color:#4A1500;color:#FFB380;font-weight:700",
            "STRONG":f"background-color:#2A1200;color:#FFCC80;font-weight:700",
            "AVERAGE":"background-color:#1A1A00;color:#FFF59D",
            "BELOW":"background-color:#060E22;color:#90CAF9",
            "WEAK":"color:#555",
        }.get(v,"")
        psv_bg = lambda v:("" if pd.isna(v) else
            f"background-color:#4A1500;color:#FFB380;font-weight:700" if v>=32 else
            "background-color:#0D1F50;color:#90CAF9;font-weight:700" if v>=31 else
            "background-color:#003344;color:#80DEEA;font-weight:700" if v>=30.5 else
            f"background-color:#2A1200;color:#FFCC80;font-weight:700" if v>=29.45 else "color:#555")
        pos_d = lambda v:"" if pd.isna(v) else(f"color:#81C784" if v>0 else("color:#EF9A9A" if v<0 else ""))
        src_style = lambda v:{
            "vollständig":"color:#81C784",
            "nur_physical":f"color:{ORG}",
            "nur_ifi":"color:#90CAF9",
        }.get(v,"color:#888")

        fmt = {
            "PSV-99":          "{:.2f}",
            "Physical Score":  "{:.1f}",
            "Δ PSV-99":        "{:+.2f}",
            "Off-Ball Int.":   "{:.0f}",
            "Lauf-Int.":       "{:.0f}",
            "Explo.":          "{:.0f}",
            "IFI Percentile":  "{:.0%}",
        }
        fmt = {k:v for k,v in fmt.items() if k in disp.columns}

        styled = disp.style
        if "Final Tier" in disp.columns: styled = styled.map(tier_bg, subset=["Final Tier"])
        if "IFI Label" in disp.columns:  styled = styled.map(ifi_bg,  subset=["IFI Label"])
        if "PSV-99" in disp.columns:     styled = styled.map(psv_bg,  subset=["PSV-99"])
        if "Δ PSV-99" in disp.columns:   styled = styled.map(pos_d,   subset=["Δ PSV-99"])
        if "Datenquelle" in disp.columns:styled = styled.map(src_style,subset=["Datenquelle"])
        styled = styled.format(fmt, na_rep="—")

        event = st.dataframe(styled, use_container_width=True, height=440,
                             on_select="rerun", selection_mode="single-row")

        sel_name = None
        if event and event.selection and event.selection.rows:
            idx = event.selection.rows[0]
            if idx < len(df_display):
                sel_name = df_display.iloc[idx]["Spieler"]
        if global_search and len(df_display)==1:
            sel_name = df_display.iloc[0]["Spieler"]

        options = ["— auswählen —"] + df_display["Spieler"].tolist()
        default_idx = options.index(sel_name) if sel_name in options else 0
        sel_dd = st.selectbox("Oder Spieler auswählen:", options, index=default_idx, key="dd")
        if sel_dd != "— auswählen —": sel_name = sel_dd

        # ── DETAIL ────────────────────────────────────────────────────────────
        if sel_name:
            row_m = df[df["Spieler"]==sel_name]
            if not row_m.empty:
                row = row_m.iloc[0]
                pos_row = row.get("Position","Winger") if "Position" in row.index else "Winger"
                tier_str = row.get("Final Tier","—")
                ifi_lbl  = row.get("IFI Label","—")
                em,ic,_  = LABEL_STYLE.get(ifi_lbl,("—","#888","#FFF"))
                t_bg_val = TIER_COLORS.get(tier_str,"#333")
                ps       = row.get("Physical Score",0) or 0
                pl,pc    = physical_label(ps)
                ifi_pct  = int((row.get("IFI Percentile",0.5) or 0.5)*100)
                src      = row.get("Datenquelle","vollständig")
                src_colors = {"vollständig":"#81C784","nur_physical":ORG,"nur_ifi":"#90CAF9"}
                src_c    = src_colors.get(src,"#888")

                st.markdown("---")
                st.markdown(f"""
                <div style="background:#2E2E2E;border:1px solid #444;border-left:4px solid {ORG};
                            border-radius:8px;padding:16px 20px;margin-bottom:16px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="font-size:20px;font-weight:800;color:#FFF;">{row.get("Spieler","—")}</div>
                            <div style="font-size:13px;color:#888;margin-top:4px;">
                                {row.get("Verein","—")} · {row.get("Liga","—")} ·
                                {POS_CONFIG.get(pos_row,{}).get("de",pos_row)} · {row.get('Spielertyp','—')} ·
                                {safe_int(row.get("Alter"))} J. · {safe_int(row.get("Minuten"))} min
                                &nbsp;<span style="color:#888;font-size:11px;">{row.get("Spielertyp","—")}</span>
                            </div>
                        </div>
                        <div style="background:{t_bg_val};color:#FFF;padding:6px 14px;
                                    border-radius:20px;font-weight:700;font-size:13px;">{tier_str}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                d1,d2,d3,d4 = st.columns(4)
                with d1: st.markdown(f'''<div class="jcard"><div class="val">{ps:.1f}<span style="font-size:13px;color:#666;">/20</span></div><div class="lbl">Physical Score</div></div>''',unsafe_allow_html=True)
                with d2: st.markdown(f'''<div class="jcard"><div class="val" style="font-size:16px;color:{pc};">{pl}</div><div class="lbl">Physical Label</div></div>''',unsafe_allow_html=True)
                with d3: st.markdown(f'''<div class="jcard"><div class="val">{ifi_pct}<span style="font-size:13px;color:#666;">%</span></div><div class="lbl">IFI Percentile</div></div>''',unsafe_allow_html=True)
                with d4: st.markdown(f'''<div class="jcard"><div class="val" style="font-size:16px;color:{ic};">{em}</div><div class="lbl">IFI Label</div></div>''',unsafe_allow_html=True)

                st.markdown("<br>",unsafe_allow_html=True)

                ch1,ch2 = st.columns([1,1])
                with ch1:
                    st.markdown("**⚡ Physical Breakdown**")
                    phys_html = render_physical_bars(row)
                    st.markdown(f'<div style="background:#2E2E2E;border:1px solid #444;border-radius:8px;padding:14px 16px;">{phys_html}</div>', unsafe_allow_html=True)
                with ch2:
                    radar = make_radar(row, pos_row)
                    if radar: st.plotly_chart(radar, use_container_width=True, key="radar")
                    else: st.info("Keine IFI-Daten für diese Position")

                # TM Link + Downloads
                st.markdown("<br>",unsafe_allow_html=True)
                tm_q = row.get("Spieler","").replace(" ","+")
                st.markdown(f'<a href="https://www.transfermarkt.de/schnellsuche/ergebnis/schnellsuche?query={tm_q}" target="_blank" style="display:inline-block;background:#1a3c6e;color:#fff;padding:7px 16px;border-radius:6px;font-size:12px;font-weight:600;text-decoration:none;">🔗 Transfermarkt</a>', unsafe_allow_html=True)
                st.markdown("<br>",unsafe_allow_html=True)

                dl1,dl2,dl3 = st.columns(3)
                with dl1:
                    html_rep = make_pdf(row, pos_row)
                    st.download_button("📄 Profil HTML",html_rep.encode("utf-8"),
                        f"Profil_{row.get('Spieler','player').replace(' ','_')}.html","text/html",use_container_width=True)
                with dl2:
                    st.download_button("📊 Spieler CSV",
                        df[df["Spieler"]==sel_name].to_csv(index=False).encode("utf-8"),
                        f"Daten_{row.get('Spieler','player').replace(' ','_')}.csv","text/csv",use_container_width=True)
                with dl3:
                    st.download_button("📋 Liste CSV",df_f.to_csv(index=False).encode("utf-8"),
                        "btl_scouting.csv","text/csv",use_container_width=True)

# ── TAB 2: Team-Suche ────────────────────────────────────────────────────────
with tab2:
    st.markdown("### 🏟️ Team-Suche")
    team_search = st.text_input("Vereinsname eingeben:", placeholder="z.B. Wolfsburg, Sturm Graz...", key="team_s")

    if team_search and "Verein" in df.columns:
        df_team = df[df["Verein"].str.contains(team_search, case=False, na=False)]
        if df_team.empty:
            st.info(f'Kein Verein gefunden für: {team_search}')
        else:
            vereine = df_team["Verein"].unique()
            for verein in vereine:
                df_v = df_team[df_team["Verein"]==verein].sort_values("Physical Score",ascending=False,na_position="last")
                liga = df_v["Liga"].iloc[0] if "Liga" in df_v.columns else "—"
                markt = df_v["Markt"].iloc[0] if "Markt" in df_v.columns else "—"

                st.markdown(f"""
                <div style="background:#2E2E2E;border:1px solid #444;border-left:4px solid {ORG};
                            border-radius:8px;padding:12px 16px;margin-bottom:12px;">
                    <span style="font-size:16px;font-weight:700;color:#FFF;">{verein}</span>
                    <span style="font-size:12px;color:#888;margin-left:12px;">{liga} · {markt} · {len(df_v)} Spieler</span>
                </div>
                """, unsafe_allow_html=True)

                # Team overview metrics
                m1,m2,m3,m4 = st.columns(4)
                with m1:
                    avg_ps = df_v["Physical Score"].mean() if "Physical Score" in df_v.columns else 0
                    st.markdown(f'<div class="jcard"><div class="val">{avg_ps:.1f}</div><div class="lbl">Ø Physical Score</div></div>', unsafe_allow_html=True)
                with m2:
                    max_psv = df_v["PSV-99"].max() if "PSV-99" in df_v.columns else 0
                    st.markdown(f'<div class="jcard"><div class="val">{max_psv:.2f}</div><div class="lbl">Max PSV-99</div></div>', unsafe_allow_html=True)
                with m3:
                    elite_top = len(df_v[df_v["Final Tier"].isin(["🔥 ELITE TARGET","🟢 TOP TARGET"])])
                    st.markdown(f'<div class="jcard"><div class="val">{elite_top}</div><div class="lbl">Elite + Top</div></div>', unsafe_allow_html=True)
                with m4:
                    pos_dist = df_v["Position"].value_counts().to_dict() if "Position" in df_v.columns else {}
                    pos_str = " · ".join([f"{p}: {n}" for p,n in pos_dist.items()])
                    st.markdown(f'<div class="jcard"><div class="val" style="font-size:12px;">{pos_str or "—"}</div><div class="lbl">Positionen</div></div>', unsafe_allow_html=True)

                # Player list
                show = [c for c in ["Spieler","Position","Alter","Minuten","Physical Score",
                                     "Final Tier","IFI Label","PSV-99","Speed Flag"] if c in df_v.columns]
                st.dataframe(df_v[show].reset_index(drop=True), use_container_width=True, height=200)
                st.markdown("<br>",unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#888;font-size:13px;">Vereinsnamen eingeben um alle Spieler dieses Teams anzuzeigen — unabhängig von Position und Liga.</div>', unsafe_allow_html=True)

# ── TAB 3: Scatter ───────────────────────────────────────────────────────────
with tab3:
    num_cols = [c for c in ["PSV-99","Physical Score","IFI Percentile","OTIP Score",
        "BIP Score","Burst Score","Speed Score","Alter","Minuten","Δ PSV-99"] if c in df_f.columns]
    c1,c2,c3,c4 = st.columns(4)
    with c1: x = st.selectbox("X-Achse",num_cols,index=0)
    with c2: y = st.selectbox("Y-Achse",num_cols,index=1)
    with c3: sz= st.selectbox("Größe",["—"]+num_cols,index=0)
    with c4: cb= st.selectbox("Farbe",["Final Tier","Speed Flag","IFI Label","Position","Markt","Liga"],index=0)

    if not df_f.empty:
        try:
            pdf_p = df_f.dropna(subset=[x,y]).copy()
            cm = TIER_COLORS if cb=="Final Tier" else(SPEED_COLORS if cb=="Speed Flag" else None)
            sv = None
            if sz!="—" and sz in pdf_p.columns:
                s = pd.to_numeric(pdf_p[sz],errors="coerce").fillna(0)
                sv = (((s-s.min())/(s.max()-s.min()+0.001))*20+6).tolist()
            fig = px.scatter(pdf_p,x=x,y=y,color=cb,color_discrete_map=cm,
                hover_name="Spieler",
                hover_data={c:True for c in ["Verein","Liga","Position","Markt","Alter","PSV-99"] if c in pdf_p.columns},
                size=sv,size_max=24,template="plotly_dark",height=520)
            if x=="PSV-99": fig.add_vline(x=29.45,line_dash="dash",line_color=ORG,annotation_text="Benchmark Median",annotation_font_size=11)
            if y=="PSV-99": fig.add_hline(y=29.45,line_dash="dash",line_color=ORG)
            fig.update_layout(
                paper_bgcolor=BG,plot_bgcolor="#333",font_family="DM Sans",font_color="#AAA",
                xaxis=dict(gridcolor="#3A3A3A",zeroline=False),
                yaxis=dict(gridcolor="#3A3A3A",zeroline=False),
                legend=dict(bgcolor="#333",bordercolor="#444",borderwidth=1),
                margin=dict(l=40,r=20,t=40,b=40))
            fig.update_traces(marker=dict(line=dict(width=0.5,color=BG)))
            st.plotly_chart(fig,use_container_width=True)
        except Exception as e:
            st.error(f"Fehler: {e}")

# ── TAB 4: Info ──────────────────────────────────────────────────────────────
with tab4:
    ca,cb_ = st.columns(2)
    with ca:
        st.markdown("### Physical Score /20")
        st.markdown("""
| Komponente | Faktor | Max |
|---|---|---|
| ⚡ Topgeschwindigkeit (0–4) | ×2.0 | 8 |
| 🏃 Pressing-Intensität (0–4) | ×1.5 | 6 |
| 💥 Lauf-Intensität (0–4) | ×1.0 | 4 |
| 🚀 Explosivität (0–4) | ×0.5 | 2 |

**Tiers:** ≥16 🔥 ELITE · ≥14 🟢 TOP · ≥12 🔵 INT · ≥9 🟡 WATCHLIST · <9 🔴 RISIKO

**IFI Gate:** BELOW/WEAK → max. WATCHLIST
        """)
    with cb_:
        st.markdown("### IFI System")
        st.markdown("""
| Percentile | Label |
|---|---|
| Top 10% | 🔴 ELITE |
| Top 25% | 🟠 STRONG |
| Top 50% | 🟡 AVERAGE |
| Top 75% | 🔵 BELOW |
| Rest | ⚫ WEAK |

**Datenquelle:**
- ✅ vollständig = Physical + IFI
- 🟠 nur_physical = kein Twelve-Match
- 🔵 nur_ifi = kein SC-Match
        """)

    st.markdown("---")
    st.markdown(f"<div style='text-align:center;color:#666;font-size:11px;'>Between The Lines Scouting Intelligence · {datetime.now().strftime('%Y')}</div>", unsafe_allow_html=True)
