import unicodedata
import streamlit as st
import openai
import os
import tempfile
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()
ai_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="MindDrift AI", layout="wide")
st.title("MindDrift AI")
st.caption("Collaborative Sci-Fi Story Writer")

def generate_ai_title(story_text):
    title_prompt = (
        "Give a creative, sci-fi inspired title for the following story. (max 5 words) "
        "It should be captivating and mysterious. Just output the title, no explanation.\n\n"
        f"Story:\n{story_text}"
    )
    try:
        client = openai.OpenAI(api_key=ai_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": title_prompt}],
            max_tokens=10,
            temperature=1.2,
        )
        title = response.choices[0].message.content.strip().removeprefix('"').removesuffix('"')
        return title
    except Exception as e:
        return "Story"


def clean_text(text):
    # Replace curly quotes, dashes, etc., with ASCII equivalents
    replacements = {
        '\u2018': "'", '\u2019': "'",  # single quotes
        '\u201c': '"', '\u201d': '"',  # double quotes
        '\u2013': '-', '\u2014': '-',  # dashes
        '\u2026': '...',               # ellipsis
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    # Normalize to remove other non-latin1 characters
    return unicodedata.normalize("NFKD", text).encode("latin-1", "ignore").decode("latin-1")


def text_to_pdf(title, body):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)
    title = clean_text(title)
    pdf.cell(0, 12, title, ln=True, align="C")
    pdf.ln(8)
    pdf.set_font("Arial", size=12)
    body = clean_text(body)
    for para in body.split("\n\n"):
        pdf.multi_cell(0, 8, para)
        pdf.ln(2)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        tmp_file.seek(0)
        pdf_bytes = tmp_file.read()
    return pdf_bytes

story_devices = [
    "Include a brief dialogue between characters.",
    "Describe a flashback or memory.",
    "Shift to a different character's perspective.",
    "Focus only on environmental description—no action or dialogue.",
    "Write as an internal monologue or stream of consciousness.",
    "Convey the action through a news report or data log.",
    "Describe the scene using questions or uncertainty.",
    "Use very short, staccato sentences.",
    "End this section with a twist, revelation, or reversal.",
    "Emphasize sensory details (sights, sounds, smells)."
]

story_theme = st.text_input("Story Theme", placeholder="e.g., 'A detective discovers their memories are artificial'")

st.markdown("### Story Parameters")
param_cols = st.columns(3)

hallucination_keywords = ["Realistic", "Vivid", "Imaginative", "Dreamlike", "Strange", "Bizarre", "Surreal", "Otherworldly", "Mind-Bending", "Hallucinatory"]
tone_keywords = ["Bright", "Neutral", "Balanced", "Mildly Dark", "Dark", "Gloomy", "Foreboding", "Bleak", "Ominous", "Nightmarish"]
surreal_keywords = ["Grounded", "Slightly Off", "Odd", "Bizarre", "Dreamy", "Fantastical", "Absurd", "Fragmented", "Abstract", "Unreal"]
emotion_keywords = ["Cold", "Reserved", "Subtle", "Wistful", "Tense", "Dramatic", "Intense", "Raw", "Overwhelming", "Gut-wrenching"]
pace_keywords = ["Introspective", "Slow", "Steady", "Balanced", "Pensive", "Brisk", "Fast-paced", "Thrilling", "Explosive", "Relentless"]

with param_cols[0]:
    hallucination_level = st.slider("Imagination", 1, 10, 7)
    st.caption(f"Selected: {hallucination_keywords[hallucination_level-1]}")
    clarity_level = st.slider("Clarity", 1, 10, 8)

with param_cols[1]:
    dark_tone = st.slider("Tone", 1, 10, 5)
    st.caption(f"Selected: {tone_keywords[dark_tone-1]}")
    surreal_factor = st.slider("Surreal", 1, 10, 7)
    st.caption(f"Selected: {surreal_keywords[surreal_factor-1]}")

with param_cols[2]:
    emotional_charge = st.slider("Emotion", 1, 10, 6)
    st.caption(f"Selected: {emotion_keywords[emotional_charge-1]}")
    action_vs_thought = st.slider("Pace", 1, 10, 5)
    st.caption(f"Selected: {pace_keywords[action_vs_thought-1]}")

def generate_ai_content(
    theme,
    previous_content="",
    hallucination_level=7,
    dark_tone=5,
    surreal_factor=7,
    clarity_level=8,
    emotional_charge=6,
    action_vs_thought=5,
    special_device="",
    avoid_repetition=True
):
    hallucination_kw = hallucination_keywords[hallucination_level-1]
    tone_kw = tone_keywords[dark_tone-1]
    surreal_kw = surreal_keywords[surreal_factor-1]
    emotion_kw = emotion_keywords[emotional_charge-1]
    pace_kw = pace_keywords[action_vs_thought-1]
    clarity_kw = "Simple, clear language." if clarity_level > 7 else "More poetic or complex language."

    variation_instruction = ""
    if avoid_repetition:
        variation_instruction += (
            "Do not repeat the sentence structure, narrative arc, or style of the previous section. "
            "Vary sentence length and focus, and surprise the reader by using a different storytelling device or perspective."
        )
    if special_device:
        variation_instruction += f" This section must: {special_device}"

    prompt = (
        f"You are an award-winning science fiction author collaborating with a human co-writer. "
        f"Theme: {theme}\n"
        f"Story so far: {previous_content}\n\n"
        f"Write the next part of this sci-fi story. "
        f"- Write a single paragraph (4 to 7 sentences).\n"
        f"- Advance the plot and deepen character or world development, referencing previous events.\n"
        f"- Imagination: {hallucination_kw}, tone: {tone_kw}, surrealism: {surreal_kw}.\n"
        f"- Emotional charge: {emotion_kw}.\n"
        f"- Pace: {pace_kw}.\n"
        f"- {clarity_kw}\n"
        f"{variation_instruction}\n"
        f"Maintain continuity with the previous text. Ensure this section feels cinematic, vivid, and emotionally resonant, never generic or formulaic. Make the reader feel something new or surprising."
    )
    try:
        client = openai.OpenAI(api_key=ai_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=1.1,
        )
        return response.choices[0].message.content.strip(), prompt
    except Exception as e:
        return f"Error generating content: {e}", prompt


# Session state
if 'story_parts' not in st.session_state:
    st.session_state.story_parts = ["" for _ in range(5)]
    st.session_state.prompts = ["" for _ in range(5)]
    st.session_state.keywords = ["" for _ in range(5)]
if 'generate_triggers' not in st.session_state:
    st.session_state.generate_triggers = [False for _ in range(5)]
if 'regenerate_triggers' not in st.session_state:
    st.session_state.regenerate_triggers = [False for _ in range(5)]
if 'ai_title' not in st.session_state:
    st.session_state.ai_title = ""
if 'user_title' not in st.session_state:
    st.session_state.user_title = ""

st.markdown("---")
st.subheader("Your Story")

for idx in range(5):
    st.markdown(f"#### Part {idx + 1}")
    colA, colB = st.columns([8, 2])
    if idx % 2 == 0:
        with colA:
            st.text_area(f"AI Part {idx + 1}", value=st.session_state.story_parts[idx], height=150, disabled=True)
            if st.session_state.keywords[idx]:
                st.caption(st.session_state.keywords[idx])
        with colB:
            if st.button(f"Generate AI Part {idx + 1}", key=f"generate_{idx}"):
                st.session_state.generate_triggers[idx] = True
                st.rerun()
            if st.button(f"Regenerate AI Part {idx + 1}", key=f"regen_{idx}"):
                st.session_state.regenerate_triggers[idx] = True
                st.rerun()
            if st.session_state.prompts[idx]:
                with st.expander("Show Prompt"):
                    st.write(st.session_state.prompts[idx])
    else:
        with colA:
            user_content = st.text_area(
                f"Your Part {idx + 1}",
                value=st.session_state.story_parts[idx],
                placeholder="Write your paragraph here...",
                height=150,
                key=f"user_{idx}"
            )
            st.session_state.story_parts[idx] = user_content
        with colB:
            pass

    if st.session_state.generate_triggers[idx]:
        previous_text = " ".join(st.session_state.story_parts[:idx])
        special_device = story_devices[idx % len(story_devices)]
        with st.spinner("Generating..."):
            ai_content, ai_prompt = generate_ai_content(
                story_theme,
                previous_text,
                hallucination_level,
                dark_tone,
                surreal_factor,
                clarity_level,
                emotional_charge,
                action_vs_thought,
                special_device=special_device
            )
        if ai_content.startswith("Error"):
            st.error(ai_content)
        else:
            st.session_state.story_parts[idx] = ai_content
            st.session_state.prompts[idx] = ai_prompt
            st.session_state.keywords[idx] = (
                f"Imagination: {hallucination_keywords[hallucination_level-1]}, "
                f"Tone: {tone_keywords[dark_tone-1]}, "
                f"Surreal: {surreal_keywords[surreal_factor-1]}, "
                f"Emotion: {emotion_keywords[emotional_charge-1]}, "
                f"Pace: {pace_keywords[action_vs_thought-1]}, "
                f"Clarity: {clarity_level}/10, "
                f"Device: {special_device}"
            )
        st.session_state.generate_triggers[idx] = False
        st.rerun()
    if st.session_state.regenerate_triggers[idx]:
        # Same logic as above
        ...

# Recalculate complete story dynamically
complete_story = "\n\n".join([part for part in st.session_state.story_parts if part.strip()])

# Auto-generate title if all parts are filled
all_filled = all(p.strip() for p in st.session_state.story_parts)
ai_title_ready = st.session_state.get("ai_title", "")
user_titled = st.session_state.get("user_title", "").strip()

if all_filled and not ai_title_ready and not user_titled:
    ai_title = generate_ai_title(complete_story)
    st.session_state.ai_title = ai_title
    st.session_state.user_title = ai_title
    st.experimental_rerun()

st.markdown("---")
st.subheader("Complete Story")

title_col, button_col = st.columns([5, 2])
with title_col:
    user_title = st.text_input("Story Title", value=st.session_state.user_title, max_chars=50, key="title_input")
    st.session_state.user_title = user_title
with button_col:
    if st.button("AI Generate Title"):
        with st.spinner("Generating..."):
            ai_title = generate_ai_title(complete_story)
            st.session_state.ai_title = ai_title
            st.session_state.user_title = ai_title
            st.rerun()

final_title = st.session_state.user_title.strip() or st.session_state.ai_title.strip() or "Story"
st.markdown(f"**Title:** {final_title}")
st.text_area("", value=complete_story, height=800, disabled=True)



if st.button("Download as PDF"):
    if complete_story.strip():
        pdf_bytes = text_to_pdf(final_title, complete_story)
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name=f"{final_title}.pdf",
            mime="application/pdf"
        )

if st.button("Download Story as TXT"):
    if complete_story.strip():
        st.download_button("Download", data=complete_story, file_name=f"{final_title}.txt")
