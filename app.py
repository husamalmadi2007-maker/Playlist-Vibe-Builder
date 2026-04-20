import gradio as gr
import json

# ─────────────────────────────────────────────
# Default sample playlist data
# ─────────────────────────────────────────────
DEFAULT_SONGS = [
    {"title": "Blinding Lights",   "artist": "The Weeknd",       "energy": 87, "duration": 200},
    {"title": "Levitating",        "artist": "Dua Lipa",         "energy": 82, "duration": 203},
    {"title": "Stay",              "artist": "The Kid LAROI",    "energy": 60, "duration": 141},
    {"title": "Peaches",           "artist": "Justin Bieber",    "energy": 55, "duration": 198},
    {"title": "drivers license",   "artist": "Olivia Rodrigo",   "energy": 43, "duration": 242},
    {"title": "Good 4 U",          "artist": "Olivia Rodrigo",   "energy": 91, "duration": 178},
    {"title": "Montero",           "artist": "Lil Nas X",        "energy": 76, "duration": 137},
    {"title": "Watermelon Sugar",  "artist": "Harry Styles",     "energy": 82, "duration": 174},
]

def merge_sort(songs, key, steps):
    if len(songs) <= 1:
        return songs
    mid = len(songs) // 2
    left_sorted  = merge_sort(songs[:mid], key, steps)
    right_sorted = merge_sort(songs[mid:], key, steps)
    return merge(left_sorted, right_sorted, key, steps)

def merge(left, right, key, steps):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        left_val  = left[i][key]
        right_val = right[j][key]
        if left_val <= right_val:
            steps.append({"action": "compare & take LEFT", "taken": left[i]["title"], "left_val": left_val, "right_val": right_val, "key": key})
            result.append(left[i]); i += 1
        else:
            steps.append({"action": "compare & take RIGHT", "taken": right[j]["title"], "left_val": left_val, "right_val": right_val, "key": key})
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    steps.append({"action": "merge complete", "result": [s["title"] for s in result]})
    return result

def fmt_duration(seconds):
    return f"{seconds // 60}:{seconds % 60:02d}"

def validate_songs(songs):
    if not songs:
        return False, "❌ Playlist is empty. Add at least two songs."
    if len(songs) < 2:
        return False, "❌ Need at least 2 songs to sort."
    for s in songs:
        if not isinstance(s.get("title"), str) or not s["title"].strip():
            return False, f"❌ Missing or invalid title in: {s}"
        if not isinstance(s.get("artist"), str) or not s["artist"].strip():
            return False, f"❌ Missing or invalid artist in: {s}"
        try:
            e = int(s["energy"])
            if not (0 <= e <= 100):
                return False, f"❌ Energy must be 0-100. Got {e} for '{s['title']}'"
        except (ValueError, TypeError):
            return False, f"❌ Energy must be a number for '{s['title']}'"
        try:
            d = int(s["duration"])
            if d <= 0:
                return False, f"❌ Duration must be positive. Got {d} for '{s['title']}'"
        except (ValueError, TypeError):
            return False, f"❌ Duration must be a number for '{s['title']}'"
    return True, "ok"

def parse_playlist(json_text):
    try:
        data = json.loads(json_text)
        if not isinstance(data, list):
            return None, "❌ Input must be a JSON array [ ... ]"
        for s in data:
            s["energy"]   = int(s.get("energy",   0))
            s["duration"] = int(s.get("duration", 0))
        return data, "ok"
    except json.JSONDecodeError as e:
        return None, f"❌ JSON parse error: {e}"

def sort_playlist(json_input, sort_key):
    songs, msg = parse_playlist(json_input)
    if songs is None:
        return msg, "", ""
    ok, msg = validate_songs(songs)
    if not ok:
        return msg, "", ""
    steps = []
    sorted_songs = merge_sort(songs, sort_key, steps)
    key_label = "Energy (0-100)" if sort_key == "energy" else "Duration"
    header = f"{'#':<4} {'Title':<25} {'Artist':<20} {key_label}\n" + "-" * 65 + "\n"
    rows = ""
    for i, s in enumerate(sorted_songs, 1):
        val = s["energy"] if sort_key == "energy" else fmt_duration(s["duration"])
        rows += f"{i:<4} {s['title']:<25} {s['artist']:<20} {val}\n"
    playlist_out = header + rows
    log_lines = [f"Sorting {len(songs)} songs by {sort_key} using Merge Sort\n" + "=" * 50]
    for idx, step in enumerate(steps, 1):
        if step["action"] == "merge complete":
            log_lines.append(f"Step {idx:>3}: Merge complete -> [{', '.join(step['result'])}]")
        else:
            direction = "LEFT " if "LEFT" in step["action"] else "RIGHT"
            log_lines.append(f"Step {idx:>3}: Take {direction} '{step['taken']}' ({step['key']}={step['left_val']} vs {step['right_val']})")
    log_out = "\n".join(log_lines)
    summary = (
        f"Sorted {len(sorted_songs)} songs by {sort_key}.\n"
        f"Total merge steps: {len(steps)}\n\n"
        f"Top song:    {sorted_songs[-1]['title']} by {sorted_songs[-1]['artist']} ({sort_key} = {sorted_songs[-1][sort_key]})\n"
        f"Bottom song: {sorted_songs[0]['title']} by {sorted_songs[0]['artist']} ({sort_key} = {sorted_songs[0][sort_key]})\n"
    )
    return summary, playlist_out, log_out

DEFAULT_JSON = json.dumps(DEFAULT_SONGS, indent=2)

with gr.Blocks(title="Playlist Vibe Builder - Merge Sort", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Playlist Vibe Builder")
    gr.Markdown("Sort your playlist by **energy** or **duration** using **Merge Sort**. Watch every comparison and merge step unfold.")
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### Your Playlist (JSON)")
            gr.Markdown("Each song needs: `title`, `artist`, `energy` (0-100), `duration` (seconds).")
            playlist_input = gr.Textbox(value=DEFAULT_JSON, lines=20, label="Playlist JSON")
        with gr.Column(scale=1):
            gr.Markdown("### Sort Settings")
            sort_key = gr.Radio(choices=["energy", "duration"], value="energy", label="Sort by", info="Energy = vibe intensity (0-100). Duration = song length in seconds.")
            sort_btn = gr.Button("Sort My Playlist", variant="primary", size="lg")
            gr.Markdown("### Summary")
            summary_out = gr.Textbox(label="Result Summary", lines=6, interactive=False)
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Sorted Playlist")
            gr.Markdown("Songs ordered lowest to highest. Bottom = most intense / longest.")
            playlist_out = gr.Textbox(label="Sorted Order (lowest to highest)", lines=12, interactive=False)
        with gr.Column():
            gr.Markdown("### Step-by-Step Merge Log")
            log_out = gr.Textbox(label="Algorithm Steps", lines=12, interactive=False)
    sort_btn.click(fn=sort_playlist, inputs=[playlist_input, sort_key], outputs=[summary_out, playlist_out, log_out])
    gr.Markdown("---\n**CISC 121 Project · Queen's University · W26** | Algorithm: Merge Sort | Problem: Playlist Vibe Builder")

if __name__ == "__main__":
    demo.launch()
