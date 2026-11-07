"""
Graphify Pipeline: Project Knowledge Graph Engine
Generates:
1. GraphRAG-ready JSON (nodes, edges, communities, metadata)
2. Interactive standalone HTML graph viewer (vis.js)
3. Quantitative GRAPH_REPORT.md audit
"""

import json
import re
from pathlib import Path
import networkx as nx

def build_project_knowledge_graph(root_dir: str = ".") -> nx.DiGraph:
    root = Path(root_dir).resolve()
    G = nx.DiGraph()

    out_dir = root / "data" / "knowledge_graph"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Ingest Python Code Modules
    src_dir = root / "src"
    if src_dir.exists():
        for py_file in src_dir.rglob("*.py"):
            mod_id = f"mod_{py_file.stem}"
            rel_path = py_file.relative_to(root).as_posix()
            G.add_node(mod_id, label=py_file.name, type="CodeModule", path=rel_path, group="code")

            # Parse classes/functions via regex
            content = py_file.read_text(encoding="utf-8", errors="ignore")
            classes = re.findall(r"class\s+([A-Za-z0-9_]+)", content)
            functions = re.findall(r"def\s+([A-Za-z0-9_]+)", content)

            for cls in classes:
                cls_id = f"cls_{cls}"
                G.add_node(cls_id, label=cls, type="ClassSchema", source=mod_id, group="schema")
                G.add_edge(mod_id, cls_id, relationship="DEFINES_CLASS")

            for fn in functions:
                if not fn.startswith("__"):
                    fn_id = f"fn_{py_file.stem}_{fn}"
                    G.add_node(fn_id, label=f"{fn}()", type="Function", source=mod_id, group="code")
                    G.add_edge(mod_id, fn_id, relationship="DEFINES_FUNC")

    # 2. Ingest Production Shot Decks
    decks_dir = root / "data" / "shot_decks"
    if decks_dir.exists():
        for json_file in decks_dir.glob("*.json"):
            deck_id = f"deck_{json_file.stem}"
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                title = data.get("title", json_file.stem)
                aspect = data.get("aspect_ratio", "9:16")
                duration = data.get("target_total_duration_sec", 0.0)

                G.add_node(deck_id, label=f"Deck: {title}", type="ShotDeck", aspect_ratio=aspect, duration=duration, group="narrative")

                # Characters
                bible = data.get("character_bible", {})
                for char_name, desc in bible.items():
                    char_id = f"char_{char_name.lower()}"
                    G.add_node(char_id, label=f"Character: {char_name}", type="Character", description=desc, group="character")
                    G.add_edge(deck_id, char_id, relationship="FEATURES_CHARACTER")

                # Shots
                shots = data.get("shots", [])
                prev_shot_id = None
                for shot in shots:
                    sid = f"shot_{shot.get('shot_id')}"
                    s_label = f"Shot {shot.get('shot_id')} [{shot.get('narrative_beat')}] ({shot.get('duration_sec')}s)"
                    G.add_node(sid, label=s_label, type="Shot", duration=shot.get("duration_sec"), group="shot")
                    G.add_edge(deck_id, sid, relationship="CONTAINS_SHOT")

                    if prev_shot_id:
                        G.add_edge(prev_shot_id, sid, relationship="SEQUENTIAL_CUT")
                    prev_shot_id = sid

                    # Link active characters to shot
                    for cname in shot.get("visual", {}).get("characters_present", []):
                        cid = f"char_{cname.lower()}"
                        if cid in G:
                            G.add_edge(sid, cid, relationship="CHARACTERS_IN_FRAME")

                    # Link dialogue & audio
                    dia = shot.get("dialogue")
                    if dia:
                        dia_id = f"dia_shot_{shot.get('shot_id')}"
                        G.add_node(dia_id, label=f"Line: \"{dia.get('line')[:35]}...\"", type="Dialogue", speaker=dia.get("speaker"), group="audio")
                        G.add_edge(sid, dia_id, relationship="SPOKEN_DIALOGUE")

            except Exception as e:
                print(f"Error parsing {json_file}: {e}")

    # 3. Ingest Audio Assets
    audio_dir = root / "data" / "audio"
    if audio_dir.exists():
        for audio_file in audio_dir.glob("*.mp3"):
            aid = f"audio_{audio_file.stem}"
            G.add_node(aid, label=audio_file.name, type="AudioAsset", group="audio")
            # Connect to matching shot
            for node in list(G.nodes):
                if node.startswith("shot_") and node.replace("shot_", "") in audio_file.stem:
                    G.add_edge(node, aid, relationship="SYNTHESIZED_VOICEOVER")

    # 4. Ingest Keyframe Assets
    keyframe_dir = root / "data" / "keyframes"
    if keyframe_dir.exists():
        for kf_file in keyframe_dir.glob("*.png"):
            kid = f"kf_{kf_file.stem}"
            G.add_node(kid, label=kf_file.name, type="KeyframeAsset", group="keyframe")
            for node in list(G.nodes):
                if node.startswith("shot_") and node.replace("shot_", "") in kf_file.stem:
                    G.add_edge(node, kid, relationship="RENDERED_KEYFRAME")

    # 5. Ingest Video Clip Assets
    video_dir = root / "data" / "video_clips"
    if video_dir.exists():
        for vid_file in video_dir.glob("*.mp4"):
            vid_id = f"vid_{vid_file.stem}"
            G.add_node(vid_id, label=vid_file.name, type="VideoClipAsset", group="video")
            for node in list(G.nodes):
                if node.startswith("shot_") and node.replace("shot_", "") in vid_file.stem:
                    G.add_edge(node, vid_id, relationship="SYNTHESIZED_MOTION_CLIP")

    # 6. Ingest Final Master Video Assets
    final_dir = root / "data" / "final"
    if final_dir.exists():
        for master_file in final_dir.glob("*.mp4"):
            m_id = f"master_{master_file.stem}"
            G.add_node(m_id, label=f"Master: {master_file.name}", type="MasterVideoAsset", group="master")
            # Connect all video clips to master video
            for node in list(G.nodes):
                if node.startswith("vid_shot_"):
                    G.add_edge(node, m_id, relationship="ASSEMBLED_INTO_MASTER")

    # 7. Ingest Social Scheduling Campaigns
    schedules_dir = root / "data" / "schedules"
    if schedules_dir.exists():
        for sched_file in schedules_dir.glob("*.json"):
            try:
                s_data = json.loads(sched_file.read_text(encoding="utf-8"))
                batches = s_data if isinstance(s_data, list) else [s_data]
                for b in batches:
                    b_id = f"campaign_{b.get('batch_id', 'batch')}"
                    G.add_node(b_id, label=f"Campaign: {b.get('project_title', 'Social Batch')}", type="ScheduledCampaign", group="distribution")
                    for job in b.get("jobs", []):
                        jid = f"job_{job.get('job_id', 'job')}"
                        p_label = job.get("platform", "platform").replace("_", " ").title()
                        G.add_node(jid, label=f"Post: {p_label}", type="PlatformDispatchJob", group="distribution", url=job.get("remote_url"))
                        G.add_edge(b_id, jid, relationship="DISPATCH_CHANNEL")
            except Exception:
                pass

    # 8. Ingest Skills & Agents
    skills_dir = root / ".agents" / "skills"
    if skills_dir.exists():
        for skill_folder in skills_dir.iterdir():
            if skill_folder.is_dir():
                sk_id = f"skill_{skill_folder.name}"
                G.add_node(sk_id, label=f"Skill: {skill_folder.name}", type="AgentSkill", group="skill")

    # Save Graph JSON
    graph_data = {
        "nodes": [{"id": n, **G.nodes[n]} for n in G.nodes],
        "edges": [{"from": u, "to": v, **G.edges[u, v]} for u, v in G.edges],
        "metrics": {
            "node_count": G.number_of_nodes(),
            "edge_count": G.number_of_edges(),
            "density": nx.density(G)
        }
    }
    json_path = out_dir / "pipeline_graph.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2)

    # Save Interactive HTML Vis.js Viewer
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <title>Autonomous Video Pipeline Knowledge Graph</title>
  <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    body {{ margin: 0; background-color: #0f172a; color: #f8fafc; font-family: ui-sans-serif, system-ui, sans-serif; }}
    #header {{ padding: 12px 20px; background: #1e293b; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }}
    #header h1 {{ margin: 0; font-size: 1.1rem; color: #38bdf8; }}
    #network {{ width: 100vw; height: calc(100vh - 50px); }}
  </style>
</head>
<body>
  <div id="header">
    <h1>Autonomous Video Pipeline Knowledge Graph</h1>
    <span>Nodes: {G.number_of_nodes()} | Edges: {G.number_of_edges()}</span>
  </div>
  <div id="network"></div>
  <script type="text/javascript">
    const rawData = {json.dumps(graph_data)};
    const colorMap = {{
      code: "#3b82f6",
      schema: "#10b981",
      narrative: "#f59e0b",
      character: "#ec4899",
      shot: "#8b5cf6",
      audio: "#06b6d4",
      skill: "#e11d48"
    }};

    const nodes = rawData.nodes.map(n => ({{
      id: n.id,
      label: n.label,
      color: colorMap[n.group] || "#64748b",
      font: {{ color: "#ffffff", size: 13 }}
    }}));

    const edges = rawData.edges.map(e => ({{
      from: e.from,
      to: e.to,
      label: e.relationship,
      font: {{ size: 9, color: "#94a3b8", align: "middle" }},
      arrows: "to",
      color: {{ color: "#475569" }}
    }}));

    const container = document.getElementById("network");
    const data = {{ nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) }};
    const options = {{
      physics: {{ stabilization: true, barnesHut: {{ springLength: 120, damping: 0.1 }} }},
      nodes: {{ shape: "box", margin: 10, shadow: true }},
      edges: {{ smooth: {{ type: "cubicBezier" }} }}
    }};
    new vis.Network(container, data, options);
  </script>
</body>
</html>
"""
    html_path = out_dir / "graph_viewer.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Save Markdown Audit Report
    report = f"""# 🕸️ Pipeline Knowledge Graph Audit Report

- **Total Entities (Nodes):** {G.number_of_nodes()}
- **Total Relationships (Edges):** {G.number_of_edges()}
- **Graph Density:** {nx.density(G):.4f}

## Node Distribution by Domain
"""
    counts = {}
    for n in G.nodes:
        grp = G.nodes[n].get("group", "other")
        counts[grp] = counts.get(grp, 0) + 1

    for grp, cnt in sorted(counts.items(), key=lambda x: -x[1]):
        report += f"- **{grp.capitalize()}:** {cnt} nodes\n"

    report += f"\nInteractive Graph Viewer generated at: `{html_path}`\n"

    report_path = out_dir / "GRAPH_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ Built Knowledge Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")
    print(f"📊 Graph report: {report_path}")
    print(f"🌐 Visual viewer: {html_path}")
    return G

if __name__ == "__main__":
    build_project_knowledge_graph()
