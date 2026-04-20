# Playlist Vibe Builder — Merge Sort

## Chosen Problem

Given a playlist of songs (title, artist, energy score, duration), sort it by either **energy** or **duration** using Merge Sort, so users can build the perfect vibe — from chill to hype, or shortest to longest.

## Chosen Algorithm

**Merge Sort** — a divide-and-conquer algorithm with O(n log n) time complexity.

Merge Sort fits this problem because:
- It is a stable, comparison-based sort — two songs with the same energy keep their original relative order.
- The dataset is small (5–50 songs), so the clear recursive structure makes the steps easy to visualise step by step.
- Unlike Quick Sort, Merge Sort's worst case is still O(n log n) — no risk of slow performance on already-sorted playlists.

**Preconditions enforced by the app:**
- Input must be valid JSON (array of objects).
- Each song must have a non-empty `title` and `artist` (strings), `energy` (integer 0–100), and `duration` (positive integer in seconds).
- At least 2 songs must be provided.
- All checks happen before sorting — helpful error messages are shown if anything fails.

**What the user sees during the simulation:**
- A **Summary panel** — how many songs sorted, total merge steps, top and bottom song.
- A **Sorted playlist table** — songs in ascending order (lowest energy/duration first).
- A **Step-by-step merge log** — every comparison and merge completion, fully traceable.

## Demo

<img width="1251" height="838" alt="Screenshot 2026-04-20 at 12 27 17 AM" src="https://github.com/user-attachments/assets/7832278f-8042-4b49-94e7-8b23804d3d41" />


Example output — sort by **energy**, default 8-song playlist:

```
#    Title                     Artist               Energy (0-100)
-----------------------------------------------------------------
1    drivers license           Olivia Rodrigo       43
2    Peaches                   Justin Bieber        55
3    Stay                      The Kid LAROI        60
4    Montero                   Lil Nas X            76
5    Levitating                Dua Lipa             82
6    Watermelon Sugar          Harry Styles         82
7    Blinding Lights           The Weeknd           87
8    Good 4 U                  Olivia Rodrigo       91
```

Top song: **Good 4 U** (energy = 91) · Bottom song: **drivers license** (energy = 43)

## Problem Breakdown & Computational Thinking

### Flowchart

>

### Four Pillars of Computational Thinking

- **Decomposition** — The task is broken into four steps: (1) parse and validate the JSON input, (2) recursively split the song list in half, (3) merge sorted halves by comparing front elements, (4) format and display three output panels (summary, table, step log).

- **Pattern Recognition** — Merge Sort repeats the same pattern at every level: compare the front element of the left half against the front of the right half, take whichever is smaller, and advance that pointer. This comparison-and-take cycle is the only thing that reorders songs.

- **Abstraction** — Shown to the user: each comparison (which song was taken and why), each merge completion, the final ranked order, and a plain-English summary. Hidden from the user: list slicing, pointer arithmetic, the recursion call stack, and raw Python dict structures — these are internal details that do not help the user understand the sort.

- **Algorithm Design** — Input: a JSON array of song objects entered in a Gradio Textbox, plus a radio button for the sort key. Processing: `parse_playlist` → `validate_songs` → `merge_sort` (with a `steps` list collecting every comparison). Output: three Textbox widgets showing the summary, sorted table, and step log. Data types: Python `list` of `dict` objects, with `int` values for the sort key.

## Steps to Run

### Requirements

```
gradio
```

Save as `requirements.txt` in the same folder as `app.py`.

### Local setup

```bash
# 1. Clone the repo
git clone https://github.com/husamalmadi2007-maker/Playlist-Vibe-Builder.git
cd Playlist-Vibe-Builder

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Launch the app
python3 app.py
```

Open `http://127.0.0.1:7860` in your browser.

### How to use

1. Leave the default playlist or paste your own JSON in the left panel.
2. Choose **energy** or **duration** as the sort key.
3. Click **Sort My Playlist**.
4. Read the Summary, Sorted Playlist, and Step-by-Step Merge Log.

## Hugging Face Link

https://huggingface.co/spaces/husamalmadi2007-maker/playlist-vibe-builder

## Testing

| Test case | Input | Expected | Actual | Pass? |
|-----------|-------|----------|--------|-------|
| Default playlist, sort by energy | 8 songs, energy key | Ascending energy (43 → 91) | Correct, 23 merge steps | √ |
| Default playlist, sort by duration | 8 songs, duration key | Ascending duration (137s → 242s) | Correct | √ |
| Two songs only | 2 songs | Sorted by 1 comparison | Works | √ |
| Already sorted input | Songs in ascending order | Same order returned | Stable, preserved | √ |
| Reverse-sorted input | Songs in descending order | Fully reversed | Correctly sorted | √ |
| All same energy | All energy=50 | Original order preserved | Preserved | √ |
| Missing field | Song with no `energy` key | Clear error message | "X Energy must be a number…" | √ |
| Energy out of range | `"energy": 150` | Clear error message | "X Energy must be 0–100. Got 150" | √ |
| Invalid JSON | `{not valid}` | JSON parse error | "X JSON parse error: …" | √ |
| Only 1 song | Single song array | Error shown | "X Need at least 2 songs to sort." | √ |
| Empty array | `[]` | Error shown | "X Playlist is empty." | √ 

## Author & AI Acknowledgment

**Author:** Husam Almadi — CISC 121, Queen's University, Winter 2026

**AI use (Level 4):** Claude (Anthropic) was used to help write comments in `app.py`, generate the README structure, and produce the flowchart. All algorithm logic (`merge_sort`, `merge`, `validate_songs`) was written and understood by the author. All AI-generated content was reviewed and edited before submission.

**Sources:**
- Gradio documentation: https://gradio.app/docs
- Hugging Face Spaces guide: https://huggingface.co/docs/hub/spaces
- Cormen et al., *Introduction to Algorithms* — Merge Sort
