"""
Life Choices: The Decision Maze
--------------------------------
Single-file Flask app. Just run:
    python app.py
Then open http://localhost:5000
"""

from flask import Flask, render_template_string, jsonify, request, session
import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np
import json
import random

app = Flask(__name__)
app.secret_key = 'decision_maze_2024'

# ─────────────────────────────────────────────
# CHART HELPERS  (Plotly.js-compatible JSON)
# ─────────────────────────────────────────────

def _layout(height=240):
    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor":  "rgba(0,0,0,0)",
        "font": {"color": "#f5d878", "family": "Georgia,serif"},
        "margin": {"t": 10, "b": 36, "l": 40, "r": 10},
        "height": height,
        "xaxis": {"gridcolor": "rgba(200,144,26,0.15)", "showgrid": False,
                  "tickfont": {"color": "#f5d878"}},
        "yaxis": {"gridcolor": "rgba(200,144,26,0.2)",
                  "tickfont": {"color": "#c8901a"}},
        "legend": {"bgcolor": "rgba(0,0,0,0.5)",
                   "bordercolor": "#c8901a", "borderwidth": 1},
    }

def bar_chart(names, values, colors, height=230):
    traces = [{"type":"bar","name":n,"x":[n],"y":[v],
               "marker":{"color":c,"line":{"color":"rgba(0,0,0,.3)","width":2}}}
              for n,v,c in zip(names,values,colors)]
    lay = _layout(height)
    lay["showlegend"] = False
    lay["yaxis"]["title"] = "Insight Tokens"
    return json.dumps({"data":traces,"layout":lay})

def grouped_bar_line(cats, bars1, bars2, line_vals, height=255):
    BAR_COLORS = ["#4a7828","#8b5a1a","#5a2a7a","#1a4a78"]
    BAR2_COLORS = ["#6a9840","#ab7a2a","#7a4a9a","#3a6a98"]
    traces = [
        {"type":"bar","name":"Total Spaces","x":cats,"y":bars1,
         "marker":{"color":BAR_COLORS,"line":{"color":"rgba(200,144,26,.5)","width":1.5}}},
        {"type":"bar","name":"Leaf Spaces","x":cats,"y":bars2,
         "marker":{"color":BAR2_COLORS,"line":{"color":"rgba(200,144,26,.5)","width":1.5}}},
        {"type":"scatter","name":"Reward Potential","x":cats,"y":line_vals,
         "mode":"lines+markers",
         "line":{"color":"#f5d878","width":2.5},
         "marker":{"size":10,"color":"#e8b050",
                   "line":{"color":"#c8901a","width":1.5}}},
    ]
    lay = _layout(height)
    lay["barmode"] = "group"
    lay["xaxis"]["title"] = "Path"
    lay["yaxis"]["title"] = "Count / Score"
    return json.dumps({"data":traces,"layout":lay})

def radar_chart(player_names, player_values, player_colors, height=280):
    cats = ["Insight","Spaces","Cards","Risk"]
    traces = []
    for name, vals, col in zip(player_names, player_values, player_colors):
        hx = col.lstrip("#")
        r,g,b = int(hx[0:2],16), int(hx[2:4],16), int(hx[4:6],16)
        traces.append({
            "type":"scatterpolar",
            "r": vals + [vals[0]],
            "theta": cats + [cats[0]],
            "fill":"toself","name":name,
            "line":{"color":col},
            "fillcolor":f"rgba({r},{g},{b},0.15)",
        })
    lay = {
        "paper_bgcolor":"rgba(0,0,0,0)",
        "font":{"color":"#f5d878","family":"Georgia,serif"},
        "polar":{"bgcolor":"rgba(0,0,0,0)",
                 "radialaxis":{"visible":True,"gridcolor":"rgba(200,144,26,.3)","color":"#c8901a"},
                 "angularaxis":{"gridcolor":"rgba(200,144,26,.3)","color":"#f5d878"}},
        "showlegend":True,
        "legend":{"bgcolor":"rgba(0,0,0,.5)","bordercolor":"#c8901a","borderwidth":1},
        "margin":{"t":20,"b":20,"l":20,"r":20},
        "height":height,
    }
    return json.dumps({"data":traces,"layout":lay})

# ─────────────────────────────────────────────
# GAME DATA
# ─────────────────────────────────────────────

CARDS = [
    {"id":1,"quote":"Looked down one as far as I could",
     "action":"You pause to carefully plan your journey.",
     "effect":"insight","value":1,"icon":"👁️"},
    {"id":2,"quote":"Because it was grassy and wanted wear",
     "action":"Take a risky route — even roll: +2 spaces, odd roll: −1 space.",
     "effect":"roll","value":0,"icon":"🎲"},
    {"id":3,"quote":"Oh, I kept the first for another day!",
     "action":"You spend too much time thinking about a path not taken.",
     "effect":"lose_insight","value":-1,"icon":"💭"},
    {"id":4,"quote":"Leaves no step had trodden black",
     "action":"You discover a completely new direction.",
     "effect":"insight","value":2,"icon":"🍃"},
    {"id":5,"quote":"Way leads on to way",
     "action":"One decision quickly leads to another.",
     "effect":"move","value":2,"icon":"🛤️"},
    {"id":6,"quote":"I shall be telling this with a sigh",
     "action":"A moment of regret slows your progress.",
     "effect":"move","value":-2,"icon":"😔"},
    {"id":7,"quote":"Sorry I could not travel both",
     "action":"Indecision stops you for a moment.",
     "effect":"skip","value":0,"icon":"⏸️"},
    {"id":8,"quote":"Bent in the undergrowth",
     "action":"You encounter an unexpected obstacle.",
     "effect":"move_lose","value":-1,"icon":"🌿"},
    {"id":9,"quote":"Perhaps the better claim",
     "action":"You feel confident about your decision.",
     "effect":"insight_move","value":1,"icon":"✨"},
    {"id":10,"quote":"Worn them really about the same",
     "action":"Everyone is navigating their own journey — ALL players gain 1 token.",
     "effect":"all_insight","value":1,"icon":"🤝"},
    {"id":11,"quote":"I doubted if I should ever come back",
     "action":"You fully commit. Gain 2 tokens + Shield (blocks next penalty).",
     "effect":"insight_shield","value":2,"icon":"🛡️"},
    {"id":12,"quote":"Somewhere ages and ages hence",
     "action":"Peek at the top 3 cards, reorder them, and gain 1 token.",
     "effect":"peek","value":1,"icon":"🔮"},
    {"id":13,"quote":"Two roads diverged in a wood",
     "action":"Challenge another player — higher roll wins 2 tokens.",
     "effect":"duel","value":2,"icon":"⚔️"},
    {"id":14,"quote":"I took the one less traveled by",
     "action":"You confidently choose a unique path.",
     "effect":"insight","value":3,"icon":"🌟"},
    {"id":15,"quote":"And that has made all the difference",
     "action":"Your decisions bring you closer to success.",
     "effect":"move","value":3,"icon":"🎯"},
]

PATHS = {
    "A":{"name":"Path A – The Safe Road",
         "desc":"Shorter, safer, fewer opportunities but steady progress.",
         "spaces":6,"leaf_spaces":[2,5],"color":"#3a7828","icon":"🌿"},
    "B":{"name":"Path B – The Winding Way",
         "desc":"Medium length with moderate risks and rewards.",
         "spaces":8,"leaf_spaces":[1,3,5,7],"color":"#8b5a1a","icon":"🍂"},
    "C":{"name":"Path C – The Forest Deep",
         "desc":"Long and mysterious — high insight potential.",
         "spaces":9,"leaf_spaces":[1,3,4,6,8],"color":"#6a2a9a","icon":"🔮"},
    "D":{"name":"Path D – The Wild Trail",
         "desc":"Longest, riskiest, greatest chance for wisdom.",
         "spaces":11,"leaf_spaces":[1,2,4,6,8,10],"color":"#1a5a9a","icon":"⚡"},
}

PLAYER_COLORS = ["#e8b050","#c85018","#3a9830","#1a6ab8","#8a28a8","#18a898"]
PLAYER_PAWNS  = ["🦊","🐺","🦌","🦅","🐻","🦁"]

# ─────────────────────────────────────────────
# ANALYTICS
# ─────────────────────────────────────────────

def game_stats(players):
    if not players:
        return {}
    df = pd.DataFrame(players)

    ins_chart = bar_chart(
        names=list(df["name"]),
        values=list(df["insight"].astype(int)),
        colors=list(df.get("color", ["#e8b050"]*len(df))),
    )

    rad_chart = radar_chart(
        player_names=list(df["name"]),
        player_values=[
            [int(r["insight"]), int(r.get("position",0)),
             int(r.get("cards_drawn",0)), int(r.get("risk_score",0))]
            for _,r in df.iterrows()
        ],
        player_colors=list(df.get("color",["#e8b050"]*len(df))),
    )

    anomalies = []
    if len(players) >= 3:
        X = np.array([[p.get("insight",0), p.get("cards_drawn",0)] for p in players])
        labels = IsolationForest(contamination=0.1, random_state=42).fit_predict(X)
        anomalies = [players[i]["name"] for i,l in enumerate(labels) if l==-1]

    leader = df.loc[df["insight"].idxmax(), "name"]
    total  = int(df["cards_drawn"].sum()) if "cards_drawn" in df.columns else 0
    return {"insight_chart":ins_chart,"radar_chart":rad_chart,
            "anomalies":anomalies,"leader":leader,"total_cards":total}

def path_chart():
    df = pd.DataFrame([
        {"Path":k,"Spaces":v["spaces"],"Leaf":len(v["leaf_spaces"]),
         "Reward":round(len(v["leaf_spaces"])*1.8,1)}
        for k,v in PATHS.items()
    ])
    return grouped_bar_line(list(df["Path"]),list(df["Spaces"]),
                            list(df["Leaf"]),list(df["Reward"]))

# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route("/")
def index():
    return render_template_string(HTML,
        cards=CARDS, paths=PATHS,
        path_chart_json=path_chart())

@app.route("/api/new", methods=["POST"])
def api_new():
    names = request.json.get("players", ["Player 1","Player 2"])
    players = [
        {"id":i,"name":n,"insight":2,"position":0,"path":None,
         "at_crossroad":False,"finished":False,"cards_drawn":0,
         "risk_score":0,"shield":False,"skip_next":False,
         "color":PLAYER_COLORS[i%len(PLAYER_COLORS)],
         "pawn":PLAYER_PAWNS[i%len(PLAYER_PAWNS)],"history":[]}
        for i,n in enumerate(names)
    ]
    deck = list(range(15)); random.shuffle(deck)
    session["g"] = {"players":players,"cur":0,"deck":deck,"turn":1,
                    "log":["🎮 Journey begins! May your path bring wisdom."],
                    "phase":"roll","winner":None}
    return jsonify({"ok":True,"g":session["g"]})

@app.route("/api/roll", methods=["POST"])
def api_roll():
    g = session.get("g")
    if not g: return jsonify({"error":"no game"}),400
    roll = random.randint(1,6)
    cp   = g["cur"]
    pl   = g["players"][cp]

    if pl["skip_next"]:
        pl["skip_next"] = False
        g["log"].insert(0,f"⏸️ {pl['pawn']} {pl['name']} skips their turn!")
        g["cur"] = (cp+1)%len(g["players"])
        g["phase"] = "roll"
        session["g"] = g
        return jsonify({"roll":0,"skipped":True,"g":g})

    if pl["path"] is None and not pl["at_crossroad"]:
        pl["position"] += roll
        if pl["position"] >= 4:
            pl["position"] = 4
            pl["at_crossroad"] = True
            g["phase"] = "path_choice"
            msg = f"🎲 {pl['pawn']} {pl['name']} rolled {roll} → reached the CROSSROAD! Choose your path!"
        elif pl["position"] in [2,3]:
            g["phase"] = "draw_card"
            msg = f"🎲 {pl['pawn']} {pl['name']} rolled {roll} → 🍂 Leaf Space!"
        else:
            g["phase"] = "roll"
            g["cur"] = (cp+1)%len(g["players"])
            msg = f"🎲 {pl['pawn']} {pl['name']} rolled {roll} → space {pl['position']}"
    elif pl["path"] and not pl["finished"]:
        pd_data = PATHS[pl["path"]]
        pl["position"] = min(pl["position"]+roll, pd_data["spaces"])
        if pl["position"] >= pd_data["spaces"]:
            pl["finished"] = True; pl["insight"] += 3
            if not g["winner"]: g["winner"] = pl["name"]
            g["phase"] = "finished_player"
            msg = f"🏆 {pl['pawn']} {pl['name']} FINISHED! +3 bonus tokens! Total: {pl['insight']}"
        elif pl["position"] in pd_data["leaf_spaces"]:
            g["phase"] = "draw_card"
            msg = f"🎲 {pl['pawn']} {pl['name']} rolled {roll} → 🍂 Leaf Space on Path {pl['path']}!"
        else:
            g["phase"] = "roll"
            g["cur"] = (cp+1)%len(g["players"])
            msg = f"🎲 {pl['pawn']} {pl['name']} rolled {roll} → space {pl['position']} on Path {pl['path']}"
    else:
        g["cur"] = (cp+1)%len(g["players"])
        msg = f"✅ {pl['pawn']} {pl['name']} has already finished."
        g["phase"] = "roll"

    pl["history"].append({"turn":g["turn"],"roll":roll,"insight":pl["insight"]})
    g["log"].insert(0,msg); g["log"] = g["log"][:25]
    g["turn"] += 1
    session["g"] = g
    return jsonify({"roll":roll,"g":g})

@app.route("/api/choose_path", methods=["POST"])
def api_choose_path():
    g = session.get("g")
    if not g: return jsonify({"error":"no game"}),400
    path = request.json.get("path","A")
    cp = g["cur"]; pl = g["players"][cp]
    pl["path"] = path; pl["at_crossroad"] = False
    pl["position"] = 0; pl["risk_score"] = len(PATHS[path]["leaf_spaces"])
    g["log"].insert(0,f"🛤️ {pl['pawn']} {pl['name']} chose {PATHS[path]['name']}!")
    g["phase"] = "roll"; g["cur"] = (cp+1)%len(g["players"])
    session["g"] = g
    return jsonify({"g":g})

@app.route("/api/draw_card", methods=["POST"])
def api_draw_card():
    g = session.get("g")
    if not g: return jsonify({"error":"no game"}),400
    if not g["deck"]:
        g["deck"] = list(range(15)); random.shuffle(g["deck"])
    card = CARDS[g["deck"].pop(0)]
    cp = g["cur"]; pl = g["players"][cp]
    pl["cards_drawn"] += 1
    eff = card["effect"]; val = card["value"]

    result = ""
    if   eff == "insight":      pl["insight"] += val; result = f"+{val} Insight Token{'s' if val>1 else ''}!"
    elif eff == "lose_insight":
        if pl["shield"]: pl["shield"]=False; result="🛡️ Shield blocked the loss!"
        else: pl["insight"]=max(0,pl["insight"]+val); result=f"{val} Insight Token!"
    elif eff == "move":
        pl["position"]=max(0,pl["position"]+val)
        result=(f"+{val} spaces!" if val>0 else f"{val} spaces!")
    elif eff == "skip":         pl["skip_next"]=True; result="Skip your next turn!"
    elif eff == "move_lose":
        if pl["shield"]: pl["shield"]=False; result="🛡️ Shield blocked the penalty!"
        else: pl["position"]=max(0,pl["position"]-1); pl["insight"]=max(0,pl["insight"]-1); result="-1 space, -1 token!"
    elif eff == "insight_move": pl["insight"]+=1; pl["position"]+=1; result="+1 token and +1 space!"
    elif eff == "all_insight":
        for p in g["players"]: p["insight"]+=1
        result="ALL players gain 1 token!"
    elif eff == "insight_shield": pl["insight"]+=2; pl["shield"]=True; result="+2 tokens + Shield!"
    elif eff == "peek":         pl["insight"]+=1; result="+1 token! You peeked at upcoming cards."
    elif eff == "duel":         result="Challenge another player — higher roll wins 2 tokens!"
    elif eff == "roll":
        r2=random.randint(1,6)
        if r2%2==0: pl["position"]+=2; result=f"Rerolled {r2} (even) → +2 spaces!"
        else: pl["position"]=max(0,pl["position"]-1); result=f"Rerolled {r2} (odd) → −1 space!"

    g["log"].insert(0,f"{card['icon']} {pl['pawn']} {pl['name']}: \"{card['quote']}\" — {result}")
    g["log"] = g["log"][:25]
    g["phase"]="roll"; g["cur"]=(cp+1)%len(g["players"])
    session["g"] = g
    return jsonify({"card":card,"result":result,"g":g})

@app.route("/api/stats")
def api_stats():
    g = session.get("g")
    if not g: return jsonify({})
    return jsonify(game_stats(g["players"]))

# ─────────────────────────────────────────────
# HTML  (embedded — no templates/ folder needed)
# ─────────────────────────────────────────────

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Life Choices: The Decision Maze</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;900&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>
:root{
  --gold:#e8b050;--gl:#f5d878;--gd:#c8901a;
  --bd:#1a0a00;--bdk:#3a1a04;--bm:#5a3008;--bl:#8b5a1a;
  --pc:#f0e2b8;--pd:#d4b870;--cr:#f8f0d8;
  --lo:#c85018;--shadow:rgba(0,0,0,.6);
}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Crimson Text',Georgia,serif;background:var(--bd);color:var(--pc);min-height:100vh;overflow-x:hidden}
/* HEADER */
.hdr{background:linear-gradient(180deg,#080300 0%,#2a1204 50%,#3a1a04 100%);border-bottom:3px solid var(--gd);box-shadow:0 4px 30px rgba(200,144,26,.3);text-align:center;position:relative;overflow:hidden}
.hdr-bg{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 0%,rgba(200,144,26,.1) 0%,transparent 60%);pointer-events:none}
.hdr-inner{position:relative;z-index:1;padding:20px 20px 0}
.site-title{font-family:'Cinzel',serif;font-size:clamp(26px,5vw,54px);font-weight:900;color:var(--gl);text-shadow:0 0 40px rgba(232,176,80,.6),3px 3px 8px rgba(0,0,0,.8);letter-spacing:4px}
.site-sub{font-family:'Cinzel',serif;font-size:clamp(12px,2vw,18px);color:var(--gold);letter-spacing:6px;margin-top:4px}
.frost{font-style:italic;font-size:13px;color:var(--pd);margin:6px 0 0;opacity:.8}
.nav{display:flex;justify-content:center;flex-wrap:wrap;border-top:1px solid rgba(200,144,26,.25);margin-top:16px;background:rgba(0,0,0,.25)}
.ntab{padding:11px 22px;font-family:'Cinzel',serif;font-size:12px;letter-spacing:2px;color:var(--pd);cursor:pointer;border:none;background:transparent;border-right:1px solid rgba(200,144,26,.15);transition:all .25s;position:relative}
.ntab:hover{color:var(--gl);background:rgba(200,144,26,.08)}
.ntab.on{color:var(--gl);background:rgba(200,144,26,.14)}
.ntab.on::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:var(--gold)}
/* LAYOUT */
.wrap{max-width:1380px;margin:0 auto;padding:18px 14px}
.page{display:none;animation:fadeIn .35s ease-out}
.page.on{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
/* PANELS */
.panel{background:linear-gradient(135deg,rgba(58,26,4,.96),rgba(32,14,0,.99));border:1px solid rgba(200,144,26,.3);border-radius:12px;padding:18px;position:relative;overflow:hidden}
.ptitle{font-family:'Cinzel',serif;font-size:15px;font-weight:600;color:var(--gl);letter-spacing:2px;margin-bottom:12px;padding-bottom:9px;border-bottom:1px solid rgba(200,144,26,.25);display:flex;align-items:center;gap:7px}
/* BUTTONS */
.btn{font-family:'Cinzel',serif;font-size:12px;letter-spacing:2px;font-weight:600;padding:11px 26px;border-radius:8px;border:none;cursor:pointer;transition:all .22s;text-transform:uppercase;position:relative}
.btn-p{background:linear-gradient(135deg,#c8901a,#7a500a);color:var(--gl);border:1px solid var(--gold);box-shadow:0 4px 14px rgba(200,144,26,.35)}
.btn-p:hover{transform:translateY(-2px);box-shadow:0 6px 22px rgba(200,144,26,.5);background:linear-gradient(135deg,#e8a820,#9a6010)}
.btn-s{background:linear-gradient(135deg,rgba(58,26,4,.9),rgba(26,10,0,.95));color:var(--pc);border:1px solid rgba(200,144,26,.35)}
.btn-s:hover{border-color:var(--gold);color:var(--gl)}
.btn:disabled{opacity:.35;cursor:not-allowed;transform:none!important}
.btn-block{width:100%}
/* GRID HELPERS */
.g2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
@media(max-width:900px){.g4{grid-template-columns:1fr 1fr}.g3{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.g2,.g3,.g4{grid-template-columns:1fr}}
/* HOME */
.hero{text-align:center;padding:32px 16px;background:linear-gradient(135deg,rgba(40,16,0,.98),rgba(20,8,0,1));border:1px solid rgba(200,144,26,.35);border-radius:14px;margin-bottom:18px;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 50% 0%,rgba(200,144,26,.1) 0%,transparent 55%)}
.shimmer{background:linear-gradient(90deg,var(--gd),var(--gl),var(--gd));background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:shimmer 3s linear infinite}
@keyframes shimmer{0%{background-position:-200% center}100%{background-position:200% center}}
.board-wrap{border:2px solid rgba(200,144,26,.35);border-radius:10px;overflow:hidden;box-shadow:0 8px 40px rgba(0,0,0,.6),0 0 60px rgba(200,144,26,.08);max-width:860px;margin:16px auto}
/* PATH CARDS */
.path-card{padding:16px 12px;border-radius:10px;border:1.5px solid;cursor:pointer;text-align:center;transition:transform .22s,box-shadow .22s;background:linear-gradient(135deg,rgba(42,18,2,.95),rgba(26,10,0,.98))}
.path-card:hover{transform:translateY(-4px);box-shadow:0 8px 24px rgba(0,0,0,.5)}
/* GAME */
.game-grid{display:grid;grid-template-columns:260px 1fr 240px;gap:14px;align-items:start}
@media(max-width:1060px){.game-grid{grid-template-columns:1fr 1fr}.gcenter{grid-column:1/-1;order:-1}}
@media(max-width:640px){.game-grid{grid-template-columns:1fr}}
/* PLAYER CARD */
.pcard{padding:13px;border-radius:10px;border:1.5px solid rgba(200,144,26,.25);background:linear-gradient(135deg,rgba(42,18,2,.95),rgba(26,10,0,.98));margin-bottom:9px;transition:border-color .3s,box-shadow .3s;position:relative}
.pcard.active{border-color:var(--gold);box-shadow:0 0 18px rgba(232,176,80,.28)}
.pcard.active::after{content:'▶ TURN';position:absolute;top:6px;right:8px;font-family:'Cinzel',serif;font-size:8px;color:var(--gold);letter-spacing:1px;animation:pulse 1.4s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.token-row{display:flex;flex-wrap:wrap;gap:3px;margin-top:6px}
.token{width:15px;height:15px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#f5d878,#c8901a);border:1px solid #7a4818;box-shadow:0 1px 3px rgba(0,0,0,.4)}
/* DICE */
.dice-wrap{margin:14px 0;display:flex;flex-direction:column;align-items:center;gap:11px}
.dice{width:76px;height:76px;background:linear-gradient(135deg,#f0e2b8,#d4b870);border:3px solid var(--bm);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:900;color:var(--bd);box-shadow:4px 4px 12px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.3);font-family:'Cinzel',serif;transition:transform .1s}
@keyframes diceRoll{0%{transform:rotate(0) scale(1)}25%{transform:rotate(18deg) scale(1.1)}50%{transform:rotate(-12deg) scale(.95)}75%{transform:rotate(6deg) scale(1.05)}100%{transform:rotate(0) scale(1)}}
.dice.rolling{animation:diceRoll .5s ease-out}
/* LOG */
.log-box{max-height:260px;overflow-y:auto;padding:3px 0;scrollbar-width:thin;scrollbar-color:var(--bm) transparent}
.log-entry{padding:6px 9px;font-size:12px;color:var(--pd);border-bottom:1px solid rgba(200,144,26,.07);line-height:1.4}
.log-entry:first-child{color:var(--gl);font-size:13px}
/* MODALS */
.overlay{position:fixed;inset:0;background:rgba(0,0,0,.87);z-index:1000;display:flex;align-items:center;justify-content:center;backdrop-filter:blur(4px);opacity:0;pointer-events:none;transition:opacity .28s}
.overlay.open{opacity:1;pointer-events:all}
.modal{background:linear-gradient(135deg,#3a1a04,#28100000);border:2px solid var(--gd);border-radius:14px;padding:28px;max-width:680px;width:92%;box-shadow:0 20px 60px rgba(0,0,0,.8),0 0 60px rgba(200,144,26,.12);transform:scale(.9);transition:transform .28s}
.modal{background:linear-gradient(135deg,#3a1a04,#1e0e00)}
.overlay.open .modal{transform:scale(1)}
.mtitle{font-family:'Cinzel',serif;font-size:20px;font-weight:700;color:var(--gl);text-align:center;margin-bottom:6px;letter-spacing:2px}
.msub{text-align:center;color:var(--pd);font-style:italic;margin-bottom:18px;font-size:13px}
.path-grid{display:grid;grid-template-columns:1fr 1fr;gap:11px}
.pbtn{padding:16px 12px;border-radius:10px;border:2px solid;cursor:pointer;text-align:center;transition:transform .2s;background:linear-gradient(135deg,rgba(26,10,0,.95),rgba(42,18,2,.98))}
.pbtn:hover{transform:translateY(-3px)}
/* CARD MODAL */
.card-face{background:linear-gradient(160deg,#f0e2b8,#d4b870);border:3px solid var(--bm);border-radius:14px;padding:26px 20px;margin:14px 0;box-shadow:5px 5px 18px rgba(0,0,0,.5);position:relative}
.card-face::before{content:'';position:absolute;inset:5px;border:1px solid rgba(90,48,8,.25);border-radius:9px;pointer-events:none}
.cq{font-style:italic;font-size:19px;color:#2a1200;font-weight:600;text-align:center;margin-bottom:8px;line-height:1.4}
.ca{font-size:12px;color:#5a3008;text-align:center;line-height:1.5;padding:8px;background:rgba(90,48,8,.06);border-radius:6px;margin-bottom:8px}
.cr{font-family:'Cinzel',serif;font-size:15px;font-weight:700;color:#8a1800;text-align:center;padding:7px 14px;border-radius:7px;background:rgba(200,80,24,.08);border:1px solid rgba(200,80,24,.25)}
/* CHOICE CARDS PAGE */
.cc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:15px}
.cc{background:linear-gradient(160deg,#f0e2b8,#d4b870);border:2px solid #8b5a1a;border-radius:13px;padding:18px 14px;position:relative;box-shadow:3px 3px 14px rgba(0,0,0,.4);cursor:pointer;transition:transform .22s,box-shadow .22s}
.cc:hover{transform:translateY(-5px) rotate(-.5deg);box-shadow:7px 11px 22px rgba(0,0,0,.5)}
.cc::before{content:'';position:absolute;inset:4px;border:1px solid rgba(139,90,26,.25);border-radius:9px;pointer-events:none}
.cc-num{position:absolute;top:7px;left:11px;font-family:'Cinzel',serif;font-size:9px;color:var(--bl);letter-spacing:1px}
.cc-ico{font-size:34px;text-align:center;margin:4px 0 9px;display:block}
.cc-q{font-style:italic;font-size:13.5px;color:#2a1200;font-weight:600;text-align:center;margin-bottom:7px;line-height:1.4}
.cc-hr{height:1px;background:rgba(90,48,8,.18);margin:6px 0}
.cc-a{font-size:11px;color:#5a3008;text-align:center;line-height:1.5}
.tag{display:inline-block;padding:2px 7px;border-radius:20px;font-size:10px;font-family:'Cinzel',serif;letter-spacing:1px;margin-top:8px}
.ti{background:rgba(232,176,80,.12);border:1px solid rgba(232,176,80,.35);color:var(--gl)}
.td{background:rgba(200,80,24,.12);border:1px solid rgba(200,80,24,.35);color:#f09060}
.tm{background:rgba(74,120,40,.12);border:1px solid rgba(74,120,40,.35);color:#8aaa50}
/* RULES */
.ri{display:flex;gap:9px;margin-bottom:9px;padding:9px;background:rgba(0,0,0,.2);border-radius:7px;border-left:3px solid var(--gd);font-size:13px;line-height:1.5}
.rico{font-size:18px;flex-shrink:0}
/* ANALYTICS */
.stat{padding:18px;border-radius:9px;text-align:center;background:linear-gradient(135deg,rgba(42,18,2,.95),rgba(26,10,0,.98));border:1px solid rgba(200,144,26,.22)}
.sv{font-family:'Cinzel',serif;font-size:34px;font-weight:900;color:var(--gl);text-shadow:0 0 20px rgba(232,176,80,.35)}
.sl{font-size:11px;color:var(--pd);letter-spacing:2px;font-family:'Cinzel',serif;margin-top:3px}
.abadge{display:inline-block;padding:3px 11px;background:rgba(200,80,24,.18);border:1px solid #c85018;border-radius:20px;font-size:12px;color:#f09060;margin:3px}
/* WINNER */
.woverlay{position:fixed;inset:0;background:rgba(0,0,0,.93);z-index:2000;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity .5s}
.woverlay.show{opacity:1;pointer-events:all}
.wcard{background:linear-gradient(135deg,#2a1200,#3a1a04);border:3px solid var(--gold);border-radius:18px;padding:44px 36px;text-align:center;max-width:460px;width:90%;box-shadow:0 0 80px rgba(200,144,26,.4)}
.wcrown{font-size:68px;margin-bottom:10px;animation:float 2s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.wt{font-family:'Cinzel',serif;font-size:28px;font-weight:900;color:var(--gl);text-shadow:0 0 30px rgba(232,176,80,.5);margin-bottom:6px}
.wn{font-family:'Cinzel',serif;font-size:22px;color:var(--gold);margin-bottom:14px}
/* SETUP */
.pinput{flex:1;background:rgba(26,10,0,.85);border:1px solid rgba(200,144,26,.3);border-radius:8px;padding:9px 13px;color:var(--pc);font-family:'Crimson Text',serif;font-size:15px;outline:none;transition:border-color .2s}
.pinput:focus{border-color:var(--gold);box-shadow:0 0 10px rgba(232,176,80,.18)}
.pinput::placeholder{color:rgba(212,184,112,.35)}
.addrow{background:none;border:1.5px dashed rgba(200,144,26,.35);border-radius:8px;padding:9px;color:var(--pd);cursor:pointer;width:100%;font-family:'Cinzel',serif;font-size:11px;letter-spacing:2px;transition:all .2s;margin-top:5px}
.addrow:hover{border-color:var(--gold);color:var(--gl)}
/* LEAF PARTICLES */
@keyframes leafFall{0%{transform:translateY(-20px) rotate(0);opacity:0}10%{opacity:1}90%{opacity:1}100%{transform:translateY(100vh) rotate(360deg);opacity:0}}
.lp{position:fixed;pointer-events:none;z-index:9999;animation:leafFall linear forwards}
/* TOAST */
.toast{position:fixed;bottom:22px;right:22px;background:linear-gradient(135deg,#3a1a04,#1e0800);border:1px solid var(--gd);border-radius:9px;padding:12px 18px;font-family:'Cinzel',serif;font-size:12px;color:var(--gl);box-shadow:0 8px 24px rgba(0,0,0,.6);z-index:3000;transform:translateX(120%);transition:transform .38s cubic-bezier(.34,1.56,.64,1);max-width:280px}
.toast.show{transform:translateX(0)}
/* DIVIDER */
.div{height:1px;background:linear-gradient(90deg,transparent,rgba(200,144,26,.35),transparent);margin:16px 0}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:rgba(26,10,0,.4)}
::-webkit-scrollbar-thumb{background:var(--bm);border-radius:3px}
</style>
</head>
<body>

<div id="lp"></div>

<!-- HEADER -->
<header class="hdr">
  <div class="hdr-bg"></div>
  <div class="hdr-inner">
    <div class="site-title">LIFE CHOICES</div>
    <div class="site-sub">The Decision Maze</div>
    <div class="frost">"Two roads diverged in a wood, and I — I took the one less traveled by, and that has made all the difference."</div>
  </div>
  <nav class="nav">
    <button class="ntab on"  onclick="show('home')">🏠 Home</button>
    <button class="ntab"     onclick="show('setup')">⚙️ New Game</button>
    <button class="ntab"     onclick="show('play')">🎮 Play</button>
    <button class="ntab"     onclick="show('cards')">🃏 Card Deck</button>
    <button class="ntab"     onclick="show('rules')">📜 Rules</button>
    <button class="ntab"     onclick="show('analytics')">📊 Analytics</button>
  </nav>
</header>

<main class="wrap">

<!-- ══════════ HOME ══════════ -->
<div id="pg-home" class="page on">
  <div class="hero">
    <div style="position:relative;z-index:1">
      <div style="font-family:'Cinzel',serif;font-size:12px;letter-spacing:3px;color:var(--gd);margin-bottom:6px">INSPIRED BY</div>
      <div class="shimmer" style="font-family:'Cinzel',serif;font-size:clamp(13px,3vw,26px);font-weight:700;margin-bottom:14px;letter-spacing:2px">The Road Not Taken — Robert Frost</div>
      <p style="max-width:640px;margin:0 auto 22px;font-size:15px;color:var(--pd);line-height:1.8;font-style:italic">
        Navigate the Decision Maze. Every choice shapes your journey.
        Collect Insight Tokens. Make your path meaningful.
      </p>
      <div class="board-wrap"><canvas id="homeCanvas" width="860" height="490"></canvas></div>
      <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:18px">
        <button class="btn btn-p" onclick="show('setup')">⚔️ Start New Game</button>
        <button class="btn btn-s" onclick="show('rules')">📜 How to Play</button>
        <button class="btn btn-s" onclick="show('cards')">🃏 View Cards</button>
      </div>
    </div>
  </div>

  <div class="panel" style="margin-bottom:16px">
    <div class="ptitle">🛤️ The Four Paths</div>
    <div class="g4">
      {% for k,p in paths.items() %}
      <div class="path-card" style="border-color:{{p.color}}">
        <div style="font-size:28px;margin-bottom:6px">{{p.icon}}</div>
        <div style="font-family:'Cinzel',serif;font-size:12px;font-weight:600;color:{{p.color}};margin-bottom:4px">PATH {{k}}</div>
        <div style="font-size:11px;color:var(--pd);line-height:1.4">{{p.desc}}</div>
        <div style="margin-top:8px;font-size:11px;display:flex;justify-content:center;gap:7px">
          <span style="padding:2px 7px;border-radius:20px;background:rgba(0,0,0,.35)">{{p.spaces}} spaces</span>
          <span style="padding:2px 7px;border-radius:20px;background:rgba(0,0,0,.35)">{{p.leaf_spaces|length}} 🍂</span>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>

  <div class="panel">
    <div class="ptitle">📊 Path Comparison</div>
    <div id="homeChart"></div>
  </div>
</div>

<!-- ══════════ SETUP ══════════ -->
<div id="pg-setup" class="page">
  <div style="max-width:820px;margin:0 auto">
    <div class="panel">
      <div class="ptitle" style="font-size:19px;justify-content:center;padding-bottom:14px">⚔️ Assemble Your Travelers</div>
      <div class="g2">
        <div>
          <div style="font-family:'Cinzel',serif;font-size:13px;color:var(--gold);margin-bottom:11px;letter-spacing:2px">👥 PLAYER NAMES</div>
          <div id="pInputs">
            <div class="player-row" style="display:flex;align-items:center;gap:9px;margin-bottom:9px">
              <span style="font-size:22px">🦊</span>
              <input class="pinput" placeholder="Player 1…" value="Player 1">
              <button onclick="delRow(this)" style="background:none;border:none;color:#c85018;cursor:pointer;font-size:17px;padding:4px">✕</button>
            </div>
            <div class="player-row" style="display:flex;align-items:center;gap:9px;margin-bottom:9px">
              <span style="font-size:22px">🐺</span>
              <input class="pinput" placeholder="Player 2…" value="Player 2">
              <button onclick="delRow(this)" style="background:none;border:none;color:#c85018;cursor:pointer;font-size:17px;padding:4px">✕</button>
            </div>
          </div>
          <button class="addrow" onclick="addRow()">+ Add Player (max 6)</button>
        </div>
        <div>
          <div style="font-family:'Cinzel',serif;font-size:13px;color:var(--gold);margin-bottom:11px;letter-spacing:2px">📋 QUICK RULES</div>
          <div class="ri"><span class="rico">🎲</span><div>Roll the die to move forward through the maze.</div></div>
          <div class="ri"><span class="rico">🍂</span><div>Land on a <strong style="color:var(--gl)">Leaf Space</strong> → draw a Choice Card.</div></div>
          <div class="ri"><span class="rico">✦</span><div>At <strong style="color:var(--gl)">Space 4</strong> choose Path A, B, C, or D — permanently.</div></div>
          <div class="ri"><span class="rico">🏆</span><div>Most <strong style="color:var(--gl)">Insight Tokens</strong> wins. First to finish gets +3 bonus!</div></div>
        </div>
      </div>
      <div class="div"></div>
      <div style="text-align:center">
        <button class="btn btn-p" style="font-size:15px;padding:13px 46px" onclick="startGame()">🎮 Begin the Journey</button>
      </div>
    </div>
  </div>
</div>

<!-- ══════════ PLAY ══════════ -->
<div id="pg-play" class="page">
  <div id="noGame" style="text-align:center;padding:60px 16px">
    <div style="font-size:60px;margin-bottom:14px">🌲</div>
    <div style="font-family:'Cinzel',serif;font-size:18px;color:var(--gold);margin-bottom:10px">No Game in Progress</div>
    <div style="color:var(--pd);margin-bottom:18px">Set up a new game to begin.</div>
    <button class="btn btn-p" onclick="show('setup')">⚙️ Set Up Game</button>
  </div>
  <div id="gameArea" style="display:none">
    <div class="game-grid">
      <!-- LEFT -->
      <div class="gleft">
        <div style="font-family:'Cinzel',serif;font-size:13px;color:var(--gold);letter-spacing:2px;margin-bottom:9px">👥 PLAYERS</div>
        <div id="pCards"></div>
        <div class="panel" style="margin-top:10px">
          <div class="ptitle" style="font-size:11px">📜 Game Log</div>
          <div class="log-box" id="gLog"></div>
        </div>
      </div>
      <!-- CENTER -->
      <div class="gcenter">
        <div class="panel" style="margin-bottom:14px;text-align:center">
          <canvas id="gameCanvas" width="780" height="440" style="width:100%;border-radius:7px"></canvas>
        </div>
        <div class="panel" style="text-align:center">
          <div id="turnDisplay" style="font-family:'Cinzel',serif;font-size:13px;color:var(--gold);margin-bottom:11px;letter-spacing:2px">⏳ Set up a game to play…</div>
          <div class="dice-wrap">
            <div class="dice" id="diceEl">🎲</div>
            <button class="btn btn-p" id="rollBtn" onclick="rollDice()">🎲 Roll Dice</button>
          </div>
        </div>
      </div>
      <!-- RIGHT -->
      <div class="gright">
        <div class="panel" style="margin-bottom:12px">
          <div class="ptitle" style="font-size:11px">🛤️ Paths</div>
          {% for k,p in paths.items() %}
          <div style="padding:7px;border-radius:7px;border-left:3px solid {{p.color}};margin-bottom:7px;background:rgba(0,0,0,.2)">
            <div style="font-family:'Cinzel',serif;font-size:10px;color:{{p.color}};margin-bottom:2px">{{p.icon}} PATH {{k}}</div>
            <div style="font-size:11px;color:var(--pd)">{{p.spaces}} spaces · {{p.leaf_spaces|length}} 🍂</div>
          </div>
          {% endfor %}
        </div>
        <div class="panel">
          <div class="ptitle" style="font-size:11px">💡 Token Guide</div>
          <div style="font-size:11px;color:var(--pd);line-height:1.9">
            <div>🟡 Start with 2 tokens each</div>
            <div>⭐ First finish: +3 bonus</div>
            <div>🃏 Leaf spaces → draw card</div>
            <div>🛡️ Shield blocks one penalty</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ══════════ CARDS ══════════ -->
<div id="pg-cards" class="page">
  <div class="panel" style="margin-bottom:14px">
    <div class="ptitle">🃏 The Choice Deck — 15 Cards of Wisdom & Challenge</div>
    <div style="font-style:italic;color:var(--pd);font-size:13px">Each card quotes a line from Robert Frost's poem and carries a unique effect on your journey through the maze.</div>
  </div>
  <div class="cc-grid">
    {% for c in cards %}
    <div class="cc">
      <div class="cc-num">CARD {{ c.id }}</div>
      <div class="cc-ico">{{ c.icon }}</div>
      <div class="cc-q">"{{ c.quote }}"</div>
      <div class="cc-hr"></div>
      <div class="cc-a">{{ c.action }}</div>
      <div style="text-align:center">
        {% if 'insight' in c.effect %}<span class="tag ti">+INSIGHT</span>
        {% elif 'lose' in c.effect or c.effect=='skip' %}<span class="tag td">PENALTY</span>
        {% elif 'move' in c.effect %}<span class="tag tm">MOVEMENT</span>
        {% else %}<span class="tag ti">SPECIAL</span>{% endif %}
      </div>
    </div>
    {% endfor %}
  </div>
</div>

<!-- ══════════ RULES ══════════ -->
<div id="pg-rules" class="page">
  <div class="g2" style="margin-bottom:16px">
    <div class="panel">
      <div class="ptitle">🏁 Objective</div>
      <p style="font-size:14px;line-height:1.8;color:var(--pd)">Navigate the Decision Maze. The goal is not just to reach the end, but to make <strong style="color:var(--gl)">thoughtful decisions</strong> that earn the most Insight Tokens. Most tokens wins.</p>
      <div class="div"></div>
      <div style="font-family:'Cinzel',serif;font-size:13px;color:var(--gold);margin-bottom:10px;letter-spacing:2px">SETUP</div>
      <div class="ri"><span class="rico">🪙</span><div>Each player starts with <strong>2 Insight Tokens</strong>.</div></div>
      <div class="ri"><span class="rico">🎯</span><div>All pawns begin at the <strong>START</strong> space.</div></div>
      <div class="ri"><span class="rico">🃏</span><div>Shuffle the 15 Choice Cards and place face-down.</div></div>
    </div>
    <div class="panel">
      <div class="ptitle">🎲 On Your Turn</div>
      <div class="ri"><span class="rico">1️⃣</span><div><strong>Roll the die</strong> and move your pawn forward.</div></div>
      <div class="ri"><span class="rico">2️⃣</span><div>Land on a <strong>Path Space</strong> → turn ends normally.</div></div>
      <div class="ri"><span class="rico">3️⃣</span><div>Land on a <strong>🍂 Leaf Space</strong> → draw a Choice Card immediately.</div></div>
      <div class="ri"><span class="rico">4️⃣</span><div>Reach <strong>Space 4 (Crossroad)</strong> → permanently choose Path A, B, C, or D.</div></div>
    </div>
    <div class="panel">
      <div class="ptitle">🛤️ The Four Paths</div>
      <div class="ri" style="border-left-color:#3a7828"><span class="rico">🌿</span><div><strong style="color:#5aaa38">Path A</strong> — Shortest & safest. Fewer leaf spaces.</div></div>
      <div class="ri" style="border-left-color:#8b5a1a"><span class="rico">🍂</span><div><strong style="color:#c87820">Path B</strong> — Medium length, balanced risk and reward.</div></div>
      <div class="ri" style="border-left-color:#6a2a9a"><span class="rico">🔮</span><div><strong style="color:#a060d0">Path C</strong> — Long, many leaf spaces, high insight.</div></div>
      <div class="ri" style="border-left-color:#1a5a9a"><span class="rico">⚡</span><div><strong style="color:#4090d0">Path D</strong> — Longest & riskiest. Most leaf spaces.</div></div>
    </div>
    <div class="panel">
      <div class="ptitle">🏆 Winning</div>
      <div class="ri"><span class="rico">🥇</span><div>First to finish gets <strong>+3 Bonus Tokens</strong>.</div></div>
      <div class="ri"><span class="rico">🧮</span><div>All players count tokens. <strong>Most wins</strong>.</div></div>
      <div class="ri"><span class="rico">🤝</span><div>Tie → player on the longer path wins.</div></div>
    </div>
  </div>
  <div class="panel">
    <div class="ptitle">📖 Connection to "The Road Not Taken"</div>
    <div class="g2">
      <div>
        <p style="font-size:14px;line-height:1.9;color:var(--pd);font-style:italic">"Two roads diverged in a yellow wood, And sorry I could not travel both And be one traveler, long I stood And looked down one as far as I could…"</p>
      </div>
      <div>
        <div class="ri"><span class="rico">🍃</span><div>The <strong>Maze Crossroad</strong> mirrors the poem's fork in the wood.</div></div>
        <div class="ri"><span class="rico">💭</span><div><strong>Insight Tokens</strong> represent wisdom gained from each choice.</div></div>
        <div class="ri"><span class="rico">✨</span><div>All 15 cards quote lines from the poem directly.</div></div>
      </div>
    </div>
  </div>
</div>

<!-- ══════════ ANALYTICS ══════════ -->
<div id="pg-analytics" class="page">
  <div id="analyticsContent">
    <div style="text-align:center;padding:60px 16px">
      <div style="font-size:46px;margin-bottom:12px">📊</div>
      <div style="font-family:'Cinzel',serif;font-size:17px;color:var(--gold);margin-bottom:8px">Analytics Dashboard</div>
      <div style="color:var(--pd);margin-bottom:18px">Start a game to unlock live Pandas + Plotly + Scikit-learn analytics.</div>
      <button class="btn btn-p" onclick="show('setup')">Start a Game</button>
    </div>
  </div>
</div>

</main>

<!-- ══════ PATH CHOICE MODAL ══════ -->
<div class="overlay" id="pathOverlay">
  <div class="modal">
    <div class="mtitle">🌲 The Crossroad Awaits</div>
    <div class="msub">Choose your path wisely — this decision is permanent.</div>
    <div class="path-grid">
      {% for k,p in paths.items() %}
      <div class="pbtn" style="border-color:{{p.color}}" onclick="choosePath('{{k}}')">
        <div style="font-size:30px;margin-bottom:5px">{{p.icon}}</div>
        <div style="font-family:'Cinzel',serif;font-size:12px;font-weight:600;color:{{p.color}};margin-bottom:3px">PATH {{k}}</div>
        <div style="font-size:11px;color:var(--pd);line-height:1.4">{{p.desc}}</div>
        <div style="margin-top:7px;font-size:10px;color:var(--pd)">{{p.spaces}} spaces · {{p.leaf_spaces|length}} 🍂</div>
      </div>
      {% endfor %}
    </div>
  </div>
</div>

<!-- ══════ CARD MODAL ══════ -->
<div class="overlay" id="cardOverlay">
  <div class="modal" style="max-width:440px;text-align:center">
    <div class="mtitle">🍂 Choice Card Drawn!</div>
    <div class="card-face">
      <div style="font-size:44px;margin-bottom:6px" id="cIcon">🍂</div>
      <div style="font-family:'Cinzel',serif;font-size:9px;color:var(--bl);letter-spacing:1px;margin-bottom:7px" id="cNum">CARD —</div>
      <div class="cq" id="cQ">"…"</div>
      <div class="ca" id="cA"></div>
      <div class="cr" id="cR"></div>
    </div>
    <button class="btn btn-p btn-block" onclick="closeCard()">Continue Journey →</button>
  </div>
</div>

<!-- ══════ WINNER MODAL ══════ -->
<div class="woverlay" id="wOverlay">
  <div class="wcard">
    <div class="wcrown">👑</div>
    <div class="wt">JOURNEY COMPLETE!</div>
    <div class="wn" id="wName">The Traveler</div>
    <div style="font-size:16px;color:var(--pc);margin-bottom:6px" id="wScore"></div>
    <div style="font-style:italic;font-size:14px;color:var(--pd);margin:14px 0">"And that has made all the difference."<br><em>— Robert Frost</em></div>
    <div style="display:flex;gap:10px;justify-content:center;margin-top:18px">
      <button class="btn btn-p" onclick="newGame()">🎮 Play Again</button>
      <button class="btn btn-s" onclick="showAnalytics()">📊 Analytics</button>
    </div>
  </div>
</div>

<!-- ══════ TOAST ══════ -->
<div class="toast" id="toast"></div>

<script>
// ─── PATHS DATA (from Flask) ───
const PATHS = {{ paths | tojson }};
const PATH_CHART = {{ path_chart_json | safe }};

// ─── PAGE NAVIGATION ───
const PAGES = ['home','setup','play','cards','rules','analytics'];
function show(name) {
  PAGES.forEach(p => {
    document.getElementById('pg-'+p).classList.remove('on');
  });
  document.querySelectorAll('.ntab').forEach((t,i) => {
    t.classList.toggle('on', PAGES[i]===name);
  });
  document.getElementById('pg-'+name).classList.add('on');
  if (name==='home')      { setTimeout(drawHome,80); renderHomeChart(); }
  if (name==='play' && G) { updateUI(); setTimeout(drawGame,80); }
  if (name==='analytics' && G) loadAnalytics();
}

// ─── TOAST ───
function toast(msg, ms=3000) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  setTimeout(()=>el.classList.remove('show'), ms);
}

// ─── LEAF PARTICLES ───
function leaf() {
  const lp = document.getElementById('lp');
  const el = document.createElement('div');
  el.className = 'lp';
  el.textContent = ['🍂','🍁','🍃'][Math.floor(Math.random()*3)];
  el.style.left = Math.random()*100+'vw';
  el.style.top = '-30px';
  const d = 6 + Math.random()*7;
  el.style.animationDuration = d+'s';
  el.style.fontSize = (14+Math.random()*14)+'px';
  lp.appendChild(el);
  setTimeout(()=>el.remove(), d*1000);
}
setInterval(leaf, 2800);

// ─── DRAW HOME CANVAS ───
function drawHome() {
  const cv = document.getElementById('homeCanvas');
  if (!cv) return;
  const ctx = cv.getContext('2d');
  const W=860, H=490; cv.width=W; cv.height=H;

  // bg
  ctx.fillStyle='#1a0a00'; ctx.fillRect(0,0,W,H);

  // sky
  let g=ctx.createLinearGradient(0,0,0,H*.5);
  g.addColorStop(0,'#c0d8e8'); g.addColorStop(1,'#d0e8c0');
  ctx.beginPath(); ctx.ellipse(W/2,H/2,W*.46,H*.46,0,0,Math.PI*2);
  ctx.fillStyle=g; ctx.fill();

  // grass
  g=ctx.createRadialGradient(W/2,H*.75,30,W/2,H*.55,H*.4);
  g.addColorStop(0,'#80a030'); g.addColorStop(1,'#3a4e10');
  ctx.beginPath(); ctx.ellipse(W/2,H*.6,W*.44,H*.36,0,0,Math.PI*2);
  ctx.fillStyle=g; ctx.fill();

  // frame
  [[W*.495,H*.495,'#3a1a04',22],[W*.495,H*.495,'#c8901a',3],[W*.495,H*.495,'#e8b840',1],
   [W*.475,H*.475,'#5a3008',32],[W*.475,H*.475,'#f0e2b8',24],[W*.475,H*.475,'#c8a860',1.5]]
  .forEach(([rx,ry,col,lw])=>{
    ctx.beginPath(); ctx.ellipse(W/2,H/2,rx,ry,0,0,Math.PI*2);
    ctx.strokeStyle=col; ctx.lineWidth=lw; ctx.stroke();
  });

  // middle ring
  [[W*.30,H*.30,'#5a3008',32],[W*.30,H*.30,'#f0e2b8',24],[W*.30,H*.30,'#c8a860',1.2]]
  .forEach(([rx,ry,col,lw])=>{
    ctx.beginPath(); ctx.ellipse(W/2,H/2,rx,ry,0,0,Math.PI*2);
    ctx.strokeStyle=col; ctx.lineWidth=lw; ctx.stroke();
  });

  // 4 inner paths
  const pXs=[210,330,530,650], pCols=['#3a7828','#8b5a1a','#6a2a9a','#1a5a9a'];
  pXs.forEach((px,i)=>{
    const sx=W/2, sy=H*.78, ey=H*.14, cv2=W/2+(px-W/2)*.45;
    ctx.beginPath(); ctx.moveTo(sx,sy);
    ctx.bezierCurveTo(sx+(px-sx)*.25,sy-60,cv2,ey+70,px,ey);
    ctx.strokeStyle='#5a3008'; ctx.lineWidth=28; ctx.lineCap='round'; ctx.stroke();
    ctx.beginPath(); ctx.moveTo(sx,sy);
    ctx.bezierCurveTo(sx+(px-sx)*.25,sy-60,cv2,ey+70,px,ey);
    ctx.strokeStyle='#f0e2b8'; ctx.lineWidth=22; ctx.stroke();
  });

  // trees
  function mTree(x,y,r,c1,c2){
    ctx.beginPath(); ctx.roundRect(x-4,y,8,r*.65,2);
    ctx.fillStyle='#5a3008'; ctx.fill();
    ctx.beginPath(); ctx.ellipse(x,y-r*.2,r,r*1.05,0,0,Math.PI*2);
    const gr=ctx.createRadialGradient(x,y-r*.55,r*.1,x,y-r*.2,r);
    gr.addColorStop(0,c1); gr.addColorStop(1,c2);
    ctx.fillStyle=gr; ctx.fill();
  }
  [[130,200,30,'#e07818','#7a3005'],[165,230,26,'#d06010','#602808'],
   [200,185,28,'#c89020','#705010'],[680,190,30,'#e07818','#703008'],
   [720,218,26,'#d06818','#603008'],[740,185,28,'#c07018','#583008'],
   [410,280,22,'#d87018','#683008'],[450,268,20,'#c06010','#582808'],
   [118,340,28,'#e08020','#703808'],[795,335,28,'#d07018','#603008']]
  .forEach(t=>mTree(...t));

  // signpost
  ctx.beginPath(); ctx.roundRect(W/2-3,H*.52,6,28,2); ctx.fillStyle='#7a4818'; ctx.fill();
  [[-1,'#b89040','A  B'],[1,'#6a4010','C  D']].forEach(([d,c,lbl])=>{
    ctx.beginPath();
    ctx.moveTo(W/2,H*.52+4); ctx.lineTo(W/2+d*55,H*.52-4);
    ctx.lineTo(W/2+d*60,H*.52+4); ctx.lineTo(W/2+d*55,H*.52+12); ctx.lineTo(W/2,H*.52+4);
    ctx.fillStyle=c; ctx.fill();
    ctx.font='bold 9px Cinzel,Georgia,serif'; ctx.fillStyle='#f5d878';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(lbl,W/2+d*30,H*.52+4);
  });

  // START banner
  ctx.beginPath(); ctx.roundRect(W/2-55,H*.85,110,32,4);
  ctx.fillStyle='#3a1a00'; ctx.fill(); ctx.strokeStyle='#c8901a'; ctx.lineWidth=1.5; ctx.stroke();
  ctx.font='bold 14px Cinzel,Georgia,serif'; ctx.fillStyle='#f5d878';
  ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText('START',W/2,H*.864+2);

  // title ribbon
  ctx.beginPath(); ctx.moveTo(190,10);
  ctx.quadraticCurveTo(W/2,-4,670,10); ctx.lineTo(674,44);
  ctx.quadraticCurveTo(W/2,58,186,44); ctx.closePath();
  const tg=ctx.createLinearGradient(190,10,670,10);
  tg.addColorStop(0,'#1a0a00'); tg.addColorStop(.4,'#7a4010');
  tg.addColorStop(.6,'#7a4010'); tg.addColorStop(1,'#1a0a00');
  ctx.fillStyle=tg; ctx.fill(); ctx.strokeStyle='#e8b840'; ctx.lineWidth=1.5; ctx.stroke();
  ctx.font='bold 15px Cinzel,Georgia,serif'; ctx.fillStyle='#f5d878';
  ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText('LIFE CHOICES: THE DECISION MAZE',W/2,26);
}

function renderHomeChart() {
  if (document.getElementById('homeChart') && PATH_CHART) {
    Plotly.newPlot('homeChart', PATH_CHART.data, PATH_CHART.layout, {displayModeBar:false,responsive:true});
  }
}

// ─── DRAW GAME CANVAS ───
function drawGame() {
  const cv = document.getElementById('gameCanvas');
  if (!cv || !G) return;
  const ctx = cv.getContext('2d');
  const W=780, H=440; cv.width=W; cv.height=H;

  const bg=ctx.createRadialGradient(W/2,H/2,40,W/2,H/2,W*.6);
  bg.addColorStop(0,'#3a2010'); bg.addColorStop(1,'#180600');
  ctx.fillStyle=bg; ctx.fillRect(0,0,W,H);

  const cx=W/2, stemTop=H*.48, stemBot=H*.86;
  const pXs={A:160,B:300,C:480,D:620};

  // stem lanes
  [cx-34,cx+34].forEach(lx=>{
    ctx.beginPath(); ctx.moveTo(lx,stemBot); ctx.lineTo(lx,stemTop);
    ctx.strokeStyle='#5a3008'; ctx.lineWidth=34; ctx.lineCap='square'; ctx.stroke();
    ctx.beginPath(); ctx.moveTo(lx,stemBot); ctx.lineTo(lx,stemTop);
    ctx.strokeStyle='#f0e2b8'; ctx.lineWidth=26; ctx.stroke();
  });
  ctx.beginPath(); ctx.moveTo(cx,stemBot); ctx.lineTo(cx,stemTop);
  ctx.strokeStyle='#c8a860'; ctx.lineWidth=1.5; ctx.stroke();
  for (let y=stemTop+4;y<stemBot;y+=34){
    ctx.beginPath(); ctx.moveTo(cx-47,y); ctx.lineTo(cx+47,y);
    ctx.strokeStyle='#8b5a18'; ctx.lineWidth=1.2; ctx.stroke();
  }

  // 4 paths
  Object.entries(pXs).forEach(([k,px])=>{
    const cv2=cx+(px-cx)*.4, ey=H*.10;
    ctx.beginPath(); ctx.moveTo(cx,stemTop);
    ctx.bezierCurveTo(cx+(px-cx)*.2,stemTop-40,cv2,ey+70,px,ey);
    ctx.strokeStyle='#5a3008'; ctx.lineWidth=34; ctx.lineCap='round'; ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx,stemTop);
    ctx.bezierCurveTo(cx+(px-cx)*.2,stemTop-40,cv2,ey+70,px,ey);
    ctx.strokeStyle='#f0e2b8'; ctx.lineWidth=26; ctx.stroke();
    ctx.font='bold 10px Cinzel,Georgia,serif'; ctx.fillStyle=PATHS[k].color;
    ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText('PATH '+k,px,ey-14);
  });

  // crossroad platform
  ctx.beginPath(); ctx.roundRect(cx-80,stemTop-4,160,36,6);
  ctx.fillStyle='#e8d4a0'; ctx.fill(); ctx.strokeStyle='#8b5a18'; ctx.lineWidth=2; ctx.stroke();
  ctx.font='bold 9px Cinzel,Georgia,serif'; ctx.fillStyle='#5a3008';
  ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.fillText('CROSSROAD — Choose Your Path',cx,stemTop+14);

  // leaf spaces
  const leafY=[stemTop+(stemBot-stemTop)*.32, stemTop+(stemBot-stemTop)*.65];
  leafY.forEach(ly=>{
    [cx-34,cx+34].forEach(lx=>{
      ctx.beginPath(); ctx.arc(lx,ly,9,0,Math.PI*2);
      ctx.fillStyle='#c85018'; ctx.fill(); ctx.strokeStyle='#7a2808'; ctx.lineWidth=1.5; ctx.stroke();
      ctx.font='10px serif'; ctx.fillStyle='#f5e090';
      ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText('🍂',lx,ly);
    });
  });

  // START
  ctx.beginPath(); ctx.roundRect(cx-52,stemBot+6,104,28,4);
  ctx.fillStyle='#3a1a00'; ctx.fill(); ctx.strokeStyle='#c8901a'; ctx.lineWidth=1.5; ctx.stroke();
  ctx.font='bold 12px Cinzel,Georgia,serif'; ctx.fillStyle='#f5d878';
  ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText('START',cx,stemBot+20);

  // finish flags
  Object.values(pXs).forEach(px=>{
    ctx.font='14px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText('🏁',px,H*.055);
  });

  // player pawns
  G.players.forEach((pl,idx)=>{
    let px=cx, py=stemBot-10;
    if (pl.finished) { px=30+idx*35; py=22; }
    else if (pl.at_crossroad) { px=cx+(idx-G.players.length/2+.5)*16; py=stemTop-18; }
    else if (pl.path) {
      const epx=pXs[pl.path], ey=H*.10, cv2=cx+(epx-cx)*.4;
      const t=pl.position/PATHS[pl.path].spaces;
      const mt=t*.99;
      px=Math.round((1-mt)*(1-mt)*(1-mt)*cx + 3*(1-mt)*(1-mt)*mt*(cx+(epx-cx)*.2) + 3*(1-mt)*mt*mt*cv2 + mt*mt*mt*epx);
      py=Math.round((1-mt)*(1-mt)*(1-mt)*stemTop + 3*(1-mt)*(1-mt)*mt*(stemTop-40) + 3*(1-mt)*mt*mt*(ey+70) + mt*mt*mt*ey);
    } else {
      const lx=idx%2===0?cx-34:cx+34;
      py=stemBot - (pl.position/4)*(stemBot-stemTop) - 10;
      px=lx;
    }
    if (idx===G.cur) { ctx.shadowColor='#f5d878'; ctx.shadowBlur=18; }
    ctx.font='20px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(pl.pawn,px,py);
    ctx.shadowBlur=0;
  });
}

// ─── GAME STATE ───
let G = null;

// ─── SETUP ───
let rowCount = 2;
const PAWNS = ['🦊','🐺','🦌','🦅','🐻','🦁'];
function addRow() {
  if (rowCount >= 6) { toast('Maximum 6 players!'); return; }
  rowCount++;
  const d = document.createElement('div');
  d.className = 'player-row';
  d.style.cssText = 'display:flex;align-items:center;gap:9px;margin-bottom:9px';
  d.innerHTML = `<span style="font-size:22px">${PAWNS[rowCount-1]}</span>
    <input class="pinput" placeholder="Player ${rowCount}…" value="Player ${rowCount}">
    <button onclick="delRow(this)" style="background:none;border:none;color:#c85018;cursor:pointer;font-size:17px;padding:4px">✕</button>`;
  document.getElementById('pInputs').appendChild(d);
}
function delRow(btn) {
  const rows = document.querySelectorAll('.player-row');
  if (rows.length <= 2) { toast('Minimum 2 players!'); return; }
  btn.closest('.player-row').remove(); rowCount--;
}

// ─── START GAME ───
async function startGame() {
  const names = [...document.querySelectorAll('.pinput')].map(i=>i.value.trim()||'Traveler');
  const res = await fetch('/api/new',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({players:names})});
  const d = await res.json();
  if (d.ok) {
    G = d.g;
    show('play'); updateUI(); toast('🎮 Journey begins! Good luck, travelers!');
  }
}

// ─── ROLL ───
async function rollDice() {
  if (!G) return;
  document.getElementById('rollBtn').disabled = true;
  const dEl = document.getElementById('diceEl');
  dEl.classList.add('rolling');
  const faces=['⚀','⚁','⚂','⚃','⚄','⚅'];
  let i=0; const anim=setInterval(()=>{ dEl.textContent=faces[i++%6]; },80);
  const res = await fetch('/api/roll',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});
  const d = await res.json();
  setTimeout(()=>{
    clearInterval(anim); dEl.classList.remove('rolling');
    dEl.textContent = d.roll || '⏸';
    G = d.g; updateUI(); drawGame();
    document.getElementById('rollBtn').disabled = false;
    if (d.skipped) toast('⏸ Turn skipped!');
    else if (G.phase==='path_choice') document.getElementById('pathOverlay').classList.add('open');
    else if (G.phase==='draw_card') setTimeout(drawCard,400);
    else if (G.phase==='finished_player' && G.winner) showWinner();
    leaf(); leaf();
  },620);
}

// ─── DRAW CARD ───
async function drawCard() {
  const res=await fetch('/api/draw_card',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});
  const d=await res.json();
  G=d.g;
  document.getElementById('cIcon').textContent=d.card.icon;
  document.getElementById('cNum').textContent=`CARD ${d.card.id} OF 15`;
  document.getElementById('cQ').textContent=`"${d.card.quote}"`;
  document.getElementById('cA').textContent=d.card.action;
  document.getElementById('cR').textContent=d.result;
  document.getElementById('cardOverlay').classList.add('open');
}
function closeCard() {
  document.getElementById('cardOverlay').classList.remove('open');
  updateUI(); drawGame();
}

// ─── CHOOSE PATH ───
async function choosePath(path) {
  document.getElementById('pathOverlay').classList.remove('open');
  const res=await fetch('/api/choose_path',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({path})});
  const d=await res.json();
  G=d.g; updateUI(); drawGame();
  toast(`${PATHS[path].icon} Path ${path} chosen!`);
}

// ─── UPDATE UI ───
function updateUI() {
  if (!G) return;
  document.getElementById('noGame').style.display='none';
  document.getElementById('gameArea').style.display='block';
  const cp=G.players[G.cur];
  document.getElementById('turnDisplay').innerHTML=`${cp.pawn} <span style="color:${cp.color}">${cp.name}</span>'s Turn — Turn ${G.turn}`;
  // player cards
  const cont=document.getElementById('pCards'); cont.innerHTML='';
  G.players.forEach((pl,i)=>{
    const active=i===G.cur;
    const tokens=Array(Math.max(0,pl.insight)).fill('<div class="token"></div>').join('');
    let badge='';
    if (pl.finished) badge=`<span style="display:inline-block;padding:2px 8px;border-radius:20px;background:rgba(232,176,80,.15);border:1px solid var(--gold);color:var(--gl);font-size:10px;font-family:'Cinzel',serif">🏆 Finished</span>`;
    else if (pl.at_crossroad) badge=`<span style="display:inline-block;padding:2px 8px;border-radius:20px;background:rgba(200,80,24,.15);border:1px solid #c85018;color:#f09060;font-size:10px;font-family:'Cinzel',serif">✦ Crossroad!</span>`;
    else if (pl.path) badge=`<span style="display:inline-block;padding:2px 8px;border-radius:20px;background:rgba(0,0,0,.3);border:1px solid rgba(200,144,26,.25);color:var(--pd);font-size:10px;font-family:'Cinzel',serif">Path ${pl.path}</span>`;
    cont.innerHTML+=`
      <div class="pcard${active?' active':''}">
        <div style="display:flex;align-items:center;gap:9px">
          <span style="font-size:26px">${pl.pawn}</span>
          <div>
            <div style="font-family:'Cinzel',serif;font-size:12px;font-weight:600;color:${pl.color}">${pl.name}</div>
            <div style="display:flex;align-items:center;gap:5px;margin-top:4px">
              <span style="font-size:18px;font-weight:600;color:${pl.color}">${pl.insight}</span>
              <span style="font-size:11px;color:var(--pd)">tokens</span>
              ${pl.shield?'<span title="Shield active" style="color:#5aaa50">🛡️</span>':''}
            </div>
          </div>
        </div>
        <div class="token-row">${tokens}</div>
        ${badge}
        <div style="font-size:10px;color:var(--pd);margin-top:4px">Pos ${pl.position} · ${pl.cards_drawn} cards drawn</div>
      </div>`;
  });
  // log
  document.getElementById('gLog').innerHTML=G.log.map(e=>`<div class="log-entry">${e}</div>`).join('');
}

// ─── WINNER ───
function showWinner() {
  setTimeout(()=>{
    const w=G.players.reduce((a,b)=>a.insight>b.insight?a:b);
    document.getElementById('wName').textContent=`${w.pawn} ${w.name}`;
    document.getElementById('wScore').textContent=`${w.insight} Insight Tokens${w.path?' · Path '+w.path:''}`;
    document.getElementById('wOverlay').classList.add('show');
    for(let i=0;i<12;i++) setTimeout(leaf,i*180);
  },900);
}
function newGame(){
  document.getElementById('wOverlay').classList.remove('show');
  show('setup');
}
function showAnalytics(){
  document.getElementById('wOverlay').classList.remove('show');
  show('analytics');
}

// ─── ANALYTICS ───
async function loadAnalytics() {
  if (!G) return;
  const res=await fetch('/api/stats');
  const s=await res.json();
  document.getElementById('analyticsContent').innerHTML=`
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:14px">
      ${[['PLAYERS',G.players.length],['TURNS',G.turn],['CARDS DRAWN',s.total_cards||0],['LEADING',s.leader||'—']]
        .map(([l,v])=>`<div class="stat"><div class="sv" style="${typeof v==='string'&&v.length>4?'font-size:20px':''}">
          ${v}</div><div class="sl">${l}</div></div>`).join('')}
    </div>
    ${s.anomalies&&s.anomalies.length?`
    <div class="panel" style="margin-bottom:14px">
      <div class="ptitle">🔬 IsolationForest Anomaly Detection</div>
      <div style="font-size:12px;color:var(--pd);margin-bottom:7px">Players with unusual score patterns (Scikit-learn):</div>
      ${s.anomalies.map(a=>`<span class="abadge">⚠️ ${a}</span>`).join('')}
    </div>`:''}
    <div class="g2" style="margin-bottom:14px">
      <div class="panel"><div class="ptitle">📊 Insight Distribution</div><div id="iChart"></div></div>
      <div class="panel"><div class="ptitle">🕸️ Player Radar</div><div id="rChart"></div></div>
    </div>
    <div class="panel">
      <div class="ptitle">🛤️ Path Comparison</div>
      <div id="pChart"></div>
    </div>`;
  if (s.insight_chart) Plotly.newPlot('iChart',JSON.parse(s.insight_chart).data,JSON.parse(s.insight_chart).layout,{displayModeBar:false,responsive:true});
  if (s.radar_chart)   Plotly.newPlot('rChart',JSON.parse(s.radar_chart).data,JSON.parse(s.radar_chart).layout,{displayModeBar:false,responsive:true});
  Plotly.newPlot('pChart',PATH_CHART.data,PATH_CHART.layout,{displayModeBar:false,responsive:true});
}

// ─── INIT ───
window.addEventListener('load',()=>{
  drawHome();
  renderHomeChart();
});
</script>
</body>
</html>"""

if __name__ == "__main__":
    print("\n  Life Choices: The Decision Maze")
    print("  ─────────────────────────────────")
    print("  Running at  →  http://localhost:5000\n")
    app.run(debug=True, port=5000)