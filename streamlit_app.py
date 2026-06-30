

import streamlit as st
import subprocess
import os
import io
import tempfile
from PIL import Image

os.makedirs("dna_storage", exist_ok=True)
os.makedirs("input_data", exist_ok=True)
os.makedirs("output", exist_ok=True)
# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="DNA Storage System",
    page_icon="🧬",
    layout="wide"
)

# ==========================================
# CUSTOM CSS (PROFESSIONAL LIGHT THEME)
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{
    --bg:        #f6f8fb;   /* app background */
    --bg2:       #ffffff;   /* cards */
    --bg3:       #f1f4f9;   /* input / stat-cell fields */
    --bg4:       #e7ecf3;   /* hover */
    --border:    #dde3ec;
    --accent:    #2e9e5b;   /* green  - primary action (encode) */
    --accent2:   #21804a;   /* green darker */
    --blue:      #2f7de1;   /* decode actions */
    --orange:    #d9772b;   /* warnings / analysis */
    --red:       #d6453d;   /* errors / simulation */
    --purple:    #8a5cd6;   /* G base color */
    --text:      #16202c;   /* primary text */
    --text2:     #5b6b7c;   /* secondary text */
    --text3:     #97a2af;   /* muted text */
}

html, body, [class*="css"]{
    font-family:'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.main{
    background:var(--bg);
}

.block-container{
    padding-top:42px;
    padding-left:44px;
    padding-right:44px;
    padding-bottom:40px;
    max-width:1320px;
}

h1,h2,h3{
    color:var(--text);
    font-weight:700;
    letter-spacing:-0.02em;
}

p, span, label, div{
    color:var(--text2);
}

/* ===== SIDEBAR (mirrors dark nav rail, kept dark for contrast) ===== */

section[data-testid="stSidebar"]{
    background:#10243E;
    border-right:1px solid #0B1B30;
}

section[data-testid="stSidebar"] *{
    color:#C7D2E3;
}

section[data-testid="stSidebar"] h1{
    color:#FFFFFF !important;
    font-size:19px;
    font-weight:700;
    padding-bottom:4px;
}

section[data-testid="stSidebar"] hr{
    border-color:rgba(255,255,255,0.12);
}

/* ===== CARDS ===== */

.card{
    background:var(--bg2);
    padding:24px 26px;
    border-radius:14px;
    border:1px solid var(--border);
    box-shadow:0 1px 3px rgba(16,24,40,0.05);
    margin-bottom:20px;
    transition:box-shadow 0.2s ease, transform 0.2s ease;
    position:relative;
    overflow:hidden;
}

.card::before{
    content:"";
    position:absolute;
    top:0;
    left:0;
    width:4px;
    height:100%;
    background:linear-gradient(180deg,var(--accent),var(--blue));
}

.card:hover{
    box-shadow:0 6px 16px rgba(16,24,40,0.08);
    transform:translateY(-2px);
}

.card h3{
    margin-top:0;
    font-size:15px;
    font-weight:700;
    letter-spacing:0.04em;
    text-transform:uppercase;
    color:var(--text);
    border-bottom:1px solid var(--bg3);
    padding-bottom:12px;
    margin-bottom:16px;
}

/* ===== METRIC / STAT CARDS (like .info-cell) ===== */

.metric{
    background:var(--bg3);
    border:1px solid var(--border);
    padding:20px 16px 18px 16px;
    border-radius:12px;
    text-align:center;
    box-shadow:none;
    position:relative;
    overflow:hidden;
    transition:box-shadow 0.2s ease, transform 0.2s ease, background 0.2s ease;
}

.metric::before{
    content:"";
    position:absolute;
    top:0;
    left:0;
    width:100%;
    height:3px;
    background:linear-gradient(90deg,var(--accent),var(--blue));
}

.metric:hover{
    background:var(--bg2);
    box-shadow:0 4px 14px rgba(16,24,40,0.07);
    transform:translateY(-2px);
}

.metric h3{
    font-size:26px;
    margin:4px 0 6px 0;
    color:var(--text);
}

.metric div{
    color:var(--text3);
    font-size:11px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.07em;
}

/* ===== TITLES ===== */

.title{
    font-size:30px;
    font-weight:800;
    color:var(--text);
    margin-bottom:8px;
}

.subtitle{
    color:var(--text2);
    font-size:16px;
}

/* ===== DNA BLOCK (monospace preview, matches log box) ===== */

.dna{
    background:var(--bg);
    border:1px solid var(--border);
    border-radius:10px;
    padding:16px;
    font-family:'Cascadia Code','SFMono-Regular', Consolas, monospace;
    font-size:13px;
    color:var(--accent2);
}

.small{
    color:var(--text3);
    font-size:13px;
}

/* ===== BUTTONS — clean light-mode style ===== */

.stButton > button{
    background:#FFFFFF !important;
    color:var(--accent2) !important;
    border:1.5px solid var(--accent) !important;
    border-radius:9px !important;
    height:46px !important;
    font-size:14px !important;
    font-weight:600 !important;
    letter-spacing:0.01em;
    width:100%;
    transition:background 0.15s ease, color 0.15s ease, transform 0.05s ease, box-shadow 0.15s ease;
    box-shadow:0 1px 2px rgba(16,24,40,0.04);
}

.stButton > button:hover{
    background:var(--accent) !important;
    color:#FFFFFF !important;
    border:1.5px solid var(--accent) !important;
    box-shadow:0 4px 10px rgba(46,158,91,0.22);
}

.stButton > button:active{
    transform:scale(0.98);
}

/* Sidebar buttons - dark nav-rail item look */
section[data-testid="stSidebar"] .stButton > button{
    background:transparent !important;
    color:#C7D2E3 !important;
    text-align:left !important;
    justify-content:flex-start !important;
    padding-left:14px !important;
    font-weight:500 !important;
    font-size:14px !important;
    border:1px solid transparent !important;
    border-radius:8px !important;
    box-shadow:none !important;
    height:42px !important;
}

section[data-testid="stSidebar"] .stButton > button:hover{
    background:rgba(63,185,80,0.12) !important;
    color:#FFFFFF !important;
    border:1px solid rgba(63,185,80,0.25) !important;
    box-shadow:none !important;
}

/* ===== INPUTS ===== */

.stTextArea textarea, .stTextInput input{
    background:var(--bg3) !important;
    border:1px solid var(--border) !important;
    border-radius:8px !important;
    color:var(--text) !important;
    font-family:'Cascadia Code', Consolas, monospace !important;
}

.stTextArea textarea:focus, .stTextInput input:focus{
    border-color:var(--accent) !important;
}

/* ===== TABS ===== */

.stTabs [data-baseweb="tab"]{
    font-weight:600;
    color:var(--text2);
}

.stTabs [aria-selected="true"]{
    color:var(--accent2) !important;
}

/* ===== CODE BLOCKS (DNA sequence previews) ===== */

.stCodeBlock, pre{
    border-radius:10px !important;
    border:1px solid var(--border) !important;
    background:var(--bg) !important;
}

.stCodeBlock code, pre code{
    color:var(--accent2) !important;
}

/* ===== ALERTS — colour-coded like log lines (ok/err/warn/info) ===== */

div[data-testid="stAlert"]{
    border-radius:10px;
    border:1px solid var(--border);
}

div[data-testid="stAlertContentSuccess"]{ color:var(--accent2) !important; }
div[data-testid="stAlertContentError"]{ color:var(--red) !important; }
div[data-testid="stAlertContentWarning"]{ color:var(--orange) !important; }
div[data-testid="stAlertContentInfo"]{ color:var(--blue) !important; }

/* ===== METRICS (st.metric widget) — give them card styling too ===== */

div[data-testid="stMetric"]{
    background:var(--bg3);
    border:1px solid var(--border);
    border-radius:12px;
    padding:14px 16px 10px 16px;
}

div[data-testid="stMetricLabel"]{
    color:var(--text3) !important;
    font-weight:700 !important;
    text-transform:uppercase;
    font-size:11px !important;
    letter-spacing:0.06em;
}

div[data-testid="stMetricValue"]{
    color:var(--text) !important;
    font-weight:700 !important;
}

/* ===== PROGRESS BAR (Analysis accuracy ring substitute) ===== */

div[data-testid="stProgress"] > div > div{
    background:linear-gradient(90deg,var(--accent),var(--blue)) !important;
}

/* ===== FILE UPLOADER ===== */

section[data-testid="stFileUploaderDropzone"]{
    background:var(--bg3) !important;
    border:1.5px dashed var(--border) !important;
    border-radius:10px !important;
}

/* ===== DIVIDER ===== */

hr{
    border-color:var(--border);
}

</style>
""",unsafe_allow_html=True)

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def run_python(script):

    result=subprocess.run(
        ["python",script],
        capture_output=True,
        text=True
    )

    return result


def read_file(path):

    if os.path.exists(path):

        with open(path,"r",encoding="utf-8") as f:
            return f.read()

    return ""


def save_uploaded(uploaded,path):

    with open(path,"wb") as f:
        f.write(uploaded.getbuffer())


def stat(title,value):

    st.markdown(f"""
    <div class="metric">

    <h3>{value}</h3>

    <div>{title}</div>

    </div>

    """,unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

if "page" not in st.session_state:

    st.session_state.page="Dashboard"

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🧬 DNA Storage")

    st.write("---")

    if st.button("🏠 Dashboard",use_container_width=True):
        st.session_state.page="Dashboard"

    if st.button("🖼 Image Encoding",use_container_width=True):
        st.session_state.page="Image Encoding"

    if st.button("📝 Text Encoding",use_container_width=True):
        st.session_state.page="Text Encoding"

    if st.button("🔬 Image Decoding",use_container_width=True):
        st.session_state.page="Image Decoding"

    if st.button("📄 Text Decoding",use_container_width=True):
        st.session_state.page="Text Decoding"

    if st.button("🦠 Error Simulation",use_container_width=True):
        st.session_state.page="Error Simulation"

    if st.button("📊 Analysis",use_container_width=True):
        st.session_state.page="Analysis"

    if st.button("ℹ About",use_container_width=True):
        st.session_state.page="About"

# ==========================================
# DASHBOARD
# ==========================================

if st.session_state.page=="Dashboard":

    st.markdown("""
<div style="
background:linear-gradient(135deg,#10243E 0%,#21804a 100%);
border-radius:16px;
padding:42px 40px;
margin-bottom:28px;
box-shadow:0 8px 24px rgba(16,36,62,0.18);
">

<h1 style="
color:#FFFFFF;
font-size:34px;
font-weight:800;
margin:0 0 8px 0;
letter-spacing:-0.02em;">
🧬 DNA-Based Digital Storage System
</h1>

<p style="
color:#cfe8da;
font-size:16px;
margin:0;
font-weight:400;">
Encode images & text into DNA · Simulate errors · Decode & recover data
</p>

</div>
""", unsafe_allow_html=True)

    # ================= QUICK ACCESS =================

    st.markdown('<p style="color:#5b6b7c;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:10px;">⚡ Quick Access</p>', unsafe_allow_html=True)

    tiles = [
        ("🖼", "Encode Image", "Image → Binary → DNA",  "#2e9e5b", "Image Encoding"),
        ("📝", "Encode Text",  "Text → Binary → DNA",   "#2e9e5b", "Text Encoding"),
        ("🔬", "Decode Image", "DNA → Binary → Image",  "#2f7de1", "Image Decoding"),
        ("📄", "Decode Text",  "DNA → Binary → Text",   "#2f7de1", "Text Decoding"),
        ("🦠", "Error Sim",    "Corrupt DNA bases",     "#d6453d", "Error Simulation"),
        ("📊", "Analysis",     "Accuracy & stats",      "#d9772b", "Analysis"),
    ]

    tile_cols = st.columns(6)

    for col, (icon, title, sub, color, target) in zip(tile_cols, tiles):
        with col:
            st.markdown(f"""
            <div style="
            background:#f1f4f9;
            border:1px solid #dde3ec;
            border-top:3px solid {color};
            border-radius:12px;
            padding:14px 10px 8px 10px;
            text-align:center;
            margin-bottom:8px;
            ">
            <div style="font-size:22px;">{icon}</div>
            <div style="font-size:13px;font-weight:700;color:#16202c;margin-top:4px;">{title}</div>
            <div style="font-size:11px;color:#5b6b7c;margin-top:2px;">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Open", key=f"tile_{target}", use_container_width=True):
                st.session_state.page = target
                st.rerun()

    st.write("")

    # ================= ENCODING MAP =================

    st.markdown("""
    <div class="card">
    <h3>🗺 Encoding Map · Binary ↔ DNA</h3>
    </div>
    """, unsafe_allow_html=True)

    map_cols = st.columns(4)
    for col, (bits, base, color) in zip(
        map_cols,
        [("00","A","#2e9e5b"), ("01","T","#2f7de1"), ("10","C","#d9772b"), ("11","G","#8a5cd6")]
    ):
        with col:
            st.markdown(f"""
            <div style="
            background:#f1f4f9;
            border:1px solid #dde3ec;
            border-radius:10px;
            text-align:center;
            padding:14px 0;
            margin-top:-14px;
            margin-bottom:14px;
            ">
            <div style="font-size:11px;color:#5b6b7c;">{bits}</div>
            <div style="font-size:24px;font-weight:800;font-family:'Cascadia Code',monospace;color:{color};">{base}</div>
            </div>
            """, unsafe_allow_html=True)

    # ================= SYSTEM STATUS =================

    st.markdown("""
    <div class="card">
    <h3>✅ System Status</h3>
    </div>
    """, unsafe_allow_html=True)

    status_items = [
        "Image Encoder", "Image Decoder",
        "Text Encoder", "Text Decoder",
        "Error Simulation", "Analysis",
    ]

    status_cols = st.columns(3)
    for i, item in enumerate(status_items):
        with status_cols[i % 3]:
            st.markdown(f"""
            <div style="
            background:#f1f4f9;
            border:1px solid #dde3ec;
            border-radius:8px;
            padding:10px 14px;
            margin-top:-10px;
            margin-bottom:10px;
            font-size:13px;
            font-weight:600;
            color:#2e9e5b;
            ">
            ✓ &nbsp; {item} Ready
            </div>
            """, unsafe_allow_html=True)

   
    # ====================================================
# IMAGE ENCODING
# ====================================================

elif st.session_state.page=="Image Encoding":

    st.title("🖼 Image Encoding")

    st.write("Convert an image into a DNA sequence.")

    uploaded = st.file_uploader(
        "Choose Image",
        type=["png","jpg","jpeg","bmp"]
    )

    if uploaded:

        image = Image.open(uploaded)

        st.image(
            image,
            width=400
        )

        col1,col2,col3 = st.columns(3)

        with col1:
            st.metric(
                "Width",
                image.size[0]
            )

        with col2:
            st.metric(
                "Height",
                image.size[1]
            )

        with col3:
            st.metric(
                "Size",
                f"{uploaded.size/1024:.1f} KB"
            )

        if st.button(
            "🧬 Encode Image",
            use_container_width=True
        ):

            os.makedirs(
                "input_data",
                exist_ok=True
            )

            extension = uploaded.name.split(".")[-1]

            temp_path = f"input_data/input_image.{extension}"
            # Delete old images
            for ext in ["png", "jpg", "jpeg", "bmp"]:
                old_file = f"input_data/input_image.{ext}"
                if os.path.exists(old_file):
                   os.remove(old_file)

            save_uploaded(
                uploaded,
                temp_path
            )

            with st.spinner("Encoding Image..."):

                result = subprocess.run(

                    [
                        "python",
                        "scripts/encoder.py",
                        temp_path
                    ],

                    capture_output=True,
                    text=True

                )

            if result.returncode==0:

                st.success("Encoding Complete")

                dna = read_file(
                    "dna_storage/dna_data.txt"
                )

                metadata = read_file(
                    "dna_storage/metadata.txt"
                )

                st.subheader("Image Metadata")

                col1, col2, col3 = st.columns(3)

                parts = metadata.strip().split(",")

                if len(parts) == 3:

                   with col1:
                        st.metric("Height", parts[0])

                   with col2:
                        st.metric("Width", parts[1])

                   with col3:
                        st.metric("Channels", parts[2])

                st.code(metadata)

                st.subheader("DNA Preview")

                st.code(
                    dna[:1000]+"..."
                )

                col1,col2=st.columns(2)

                with col1:

                    st.download_button(

                        "Download DNA",

                        dna,

                        file_name="dna_data.txt"

                    )

                with col2:

                    st.download_button(

                        "Download Metadata",

                        metadata,

                        file_name="metadata.txt"

                    )

            else:

                st.error(result.stderr)
                # ====================================================
# TEXT ENCODING
# ====================================================

elif st.session_state.page == "Text Encoding":

    st.title("📝 Text Encoding")
    st.write("Convert text into a DNA sequence.")

    tab1, tab2 = st.tabs(["✍️ Write Text", "📂 Upload Text File"])

    text_data = ""

    with tab1:
        text_data = st.text_area(
            "Enter Text",
            height=200,
            placeholder="Type your text here..."
        )

    with tab2:

        txt = st.file_uploader(
            "Upload TXT File",
            type=["txt"]
        )

        if txt is not None:
            text_data = txt.read().decode("utf-8")
            st.success("File Loaded Successfully")
            st.text_area(
                "Preview",
                text_data,
                height=200
            )

    if st.button(
        "🧬 Encode Text",
        use_container_width=True
    ):

        if text_data.strip() == "":
            st.warning("Please enter some text.")
            st.stop()

        os.makedirs(
            "input_data",
            exist_ok=True
        )

        with open(
            "input_data/sample.txt",
            "w",
            encoding="utf-8"
        ) as f:
            f.write(text_data)

        with st.spinner("Encoding Text..."):

            result = subprocess.run(
                [
                    "python",
                    "scripts/text_encoder.py"
                ],
                capture_output=True,
                text=True
            )

        if result.returncode == 0:

            st.success("Text Encoded Successfully")

            dna = read_file(
                "dna_storage/text_dna.txt"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Characters",
                    len(text_data)
                )

            with col2:
                st.metric(
                    "Words",
                    len(text_data.split())
                )

            with col3:
                st.metric(
                    "DNA Bases",
                    len(dna)
                )

            st.subheader("DNA Preview")

            st.code(
                dna[:1000] + "..."
            )

            st.download_button(
                "⬇ Download text_dna.txt",
                dna,
                file_name="text_dna.txt"
            )

        else:

            st.error(result.stderr)
# ====================================================
# IMAGE DECODING
# ====================================================

elif st.session_state.page == "Image Decoding":

    st.title("🔬 Image Decoding")
    st.write("Convert DNA sequence back into the original image.")
    if "loaded_dna" not in st.session_state:
        st.session_state.loaded_dna = ""

    if "loaded_metadata" not in st.session_state:
        st.session_state.loaded_metadata = ""

    dna_text = st.text_area(
    "DNA Sequence",
    value=st.session_state.loaded_dna,
    height=180
)

    metadata = st.text_input(
    "Metadata",
    value=st.session_state.loaded_metadata
)

    col1, col2 = st.columns(2)

    with col1:
        load_btn = st.button(
        "📂 Load Saved DNA",
        use_container_width=True
    )

    with col2:
        decode_btn = st.button(
        "🧬 Decode Image",
        use_container_width=True
    )
    
 
    if load_btn:

        try:
            st.session_state.loaded_dna = read_file("dna_storage/dna_data.txt")
            st.session_state.loaded_metadata = read_file("dna_storage/metadata.txt")

            st.success("DNA Loaded Successfully")

            st.rerun()

        except Exception:
            st.error("dna_data.txt or metadata.txt not found.")

    if decode_btn:

        if dna_text.strip() == "" or metadata.strip() == "":

            st.warning("Please enter DNA and metadata.")

        else:

            os.makedirs("dna_storage", exist_ok=True)
            os.makedirs("output", exist_ok=True)

            dna_text = dna_text.upper()

            dna_text = "".join(
    c for c in dna_text
    if c in "ATCG"
)

            with open("dna_storage/dna_data.txt", "w") as f:
                f.write(dna_text) 

            with open("dna_storage/metadata.txt", "w") as f:
                f.write(metadata)

            with st.spinner("Decoding Image..."):

                result = subprocess.run(
                    ["python", "scripts/decoder.py"],
                    capture_output=True,
                    text=True
                )

            if result.returncode == 0:

                image_path = "output/decoded_image.png"

                if os.path.exists(image_path):

                    import time
                    from PIL import Image

                    # force browser refresh
                    time.sleep(0.5)

                    img = Image.open(image_path).copy()

                    st.success("✅ Image Decoded Successfully")

                    st.image(
                        img,
                        caption=f"Decoded Image {time.time()}",
                        use_container_width=True
                    )

                    with open(image_path, "rb") as f:
                        st.download_button(
                            "⬇ Download Image",
                            f.read(),
                            file_name="decoded_image.png",
                            mime="image/png",
                            use_container_width=True
                        )

                else:
                       st.error("Decoder failed")

                       st.write("STDOUT")
                       st.code(result.stdout)

                       st.write("STDERR")
                       st.code(result.stderr)

            else:
                st.error("Decoder Error")
                st.code(result.stderr)
# ====================================================
# TEXT DECODING
# ====================================================

elif st.session_state.page == "Text Decoding":

    st.title("📄 Text Decoding")
    st.write("Recover the original text from a DNA sequence.")

    if "loaded_text_dna" not in st.session_state:
        st.session_state.loaded_text_dna = ""

    dna_text = st.text_area(
        "DNA Sequence",
        value=st.session_state.loaded_text_dna,
        height=220,
        placeholder="Paste DNA sequence here..."
    )

    col1, col2 = st.columns(2)

    with col1:
        load_btn = st.button(
            "📂 Load Saved DNA",
            use_container_width=True
        )

    with col2:
        decode_btn = st.button(
            "🧬 Decode Text",
            use_container_width=True
        )

    if load_btn:

        dna = read_file("dna_storage/text_dna.txt")

        if dna.strip() == "":
           st.error("text_dna.txt is empty.")
        else:
           st.session_state.loaded_text_dna = dna
           st.rerun()

    if decode_btn:

        if dna_text.strip() == "":

            st.warning("Please enter DNA sequence.")

        else:

            os.makedirs("dna_storage", exist_ok=True)

            dna = "".join(
                c for c in dna_text.upper()
                if c in "ATCG"
            )

            with open(
                "dna_storage/text_dna.txt",
                "w"
            ) as f:

                f.write(dna)

            with st.spinner("Decoding Text..."):

                result = subprocess.run(
                    [
                        "python",
                        "scripts/text_decoder.py"
                    ],
                    capture_output=True,
                    text=True
                )

            if result.returncode == 0:

                decoded = read_file(
                    "output/decoded_text.txt"
                )

                st.success("✅ Text Decoded Successfully")

                st.subheader("Recovered Text")

                st.text_area(
                    "",
                    decoded,
                    height=250
                )

                st.download_button(
                    "⬇ Download decoded_text.txt",
                    decoded,
                    file_name="decoded_text.txt"
                )

            else:

                st.error(result.stderr)
                # ====================================================
# ERROR SIMULATION
# ====================================================

elif st.session_state.page == "Error Simulation":

    st.title("🦠 Error Simulation")
    st.write("Introduce random mutations into the DNA sequence.")

    if "loaded_sim_dna" not in st.session_state:
        st.session_state.loaded_sim_dna = ""

    dna_text = st.text_area(
        "DNA Sequence",
        value=st.session_state.loaded_sim_dna,
        height=220,
        placeholder="Paste DNA sequence here..."
    )

    col1, col2 = st.columns(2)

    with col1:
        load_btn = st.button(
            "📂 Load Saved DNA",
            use_container_width=True
        )

    with col2:
        simulate_btn = st.button(
            "🦠 Simulate Errors",
            use_container_width=True
        )

    if load_btn:

        dna = read_file("dna_storage/dna_data.txt")

        if dna.strip() == "":
            st.error("dna_data.txt not found.")
        else:
            st.session_state.loaded_sim_dna = dna
            st.rerun()

    if simulate_btn:

        if dna_text.strip() == "":
            st.warning("Please load or paste a DNA sequence.")

        else:

            dna = "".join(
                c for c in dna_text.upper()
                if c in "ATCG"
            )

            os.makedirs("dna_storage", exist_ok=True)

            with open("dna_storage/dna_data.txt", "w") as f:
                f.write(dna)

            with st.spinner("Simulating Errors..."):

                result = subprocess.run(
                    [
                        "python",
                        "scripts/error_simulation.py"
                    ],
                    capture_output=True,
                    text=True
                )

            if result.returncode == 0:

                corrupted = read_file(
                    "dna_storage/corrupted_dna.txt"
                )

                st.success("✅ Error Simulation Completed")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Original Bases",
                        len(dna)
                    )

                with col2:
                    st.metric(
                        "Corrupted Bases",
                        len(corrupted)
                    )

                with col3:
                    errors = sum(
                        1 for a, b in zip(dna, corrupted)
                        if a != b
                    )
                    st.metric(
                        "Errors",
                        errors
                    )

                st.subheader("Corrupted DNA Preview")

                st.code(corrupted[:1000] + "...")

                st.download_button(
                    "⬇ Download corrupted_dna.txt",
                    corrupted,
                    file_name="corrupted_dna.txt"
                )

            else:

                st.error(result.stderr)
                # ====================================================
# ANALYSIS
# ====================================================

elif st.session_state.page == "Analysis":

    st.title("📊 Analysis")
    st.write("Compare the original DNA sequence with the corrupted DNA sequence.")

    col1, col2 = st.columns(2)

    with col1:
        load_btn = st.button(
            "📂 Load DNA Files",
            use_container_width=True
        )

    with col2:
        analyse_btn = st.button(
            "📊 Run Analysis",
            use_container_width=True
        )

    if load_btn:

        original = read_file("dna_storage/dna_data.txt")
        corrupted = read_file("dna_storage/corrupted_dna.txt")

        if original == "":
            st.error("dna_data.txt not found.")
        elif corrupted == "":
            st.error("corrupted_dna.txt not found.")
        else:
            st.session_state.analysis_original = original
            st.session_state.analysis_corrupted = corrupted
            st.success("DNA files loaded successfully.")

    if "analysis_original" not in st.session_state:
        st.session_state.analysis_original = ""

    if "analysis_corrupted" not in st.session_state:
        st.session_state.analysis_corrupted = ""

    original = st.text_area(
        "Original DNA",
        value=st.session_state.analysis_original,
        height=180
    )

    corrupted = st.text_area(
        "Corrupted DNA",
        value=st.session_state.analysis_corrupted,
        height=180
    )

    if analyse_btn:

        original = "".join(c for c in original.upper() if c in "ATCG")
        corrupted = "".join(c for c in corrupted.upper() if c in "ATCG")

        if original == "" or corrupted == "":
            st.warning("Please load both DNA sequences.")
            st.stop()

        total = min(len(original), len(corrupted))

        errors = 0

        for a, b in zip(original, corrupted):

            if a != b:
                errors += 1

        accuracy = ((total - errors) / total) * 100
        error_rate = (errors / total) * 100

        st.success("Analysis Complete")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Total Bases",
                total
            )

        with c2:
            st.metric(
                "Errors",
                errors
            )

        with c3:
            st.metric(
                "Accuracy",
                f"{accuracy:.4f}%"
            )

        with c4:
            st.metric(
                "Error Rate",
                f"{error_rate:.4f}%"
            )

        st.progress(accuracy / 100)

        report = f"""
DNA STORAGE ANALYSIS REPORT

Total DNA Bases : {total}

Errors Found : {errors}

Storage Accuracy : {accuracy:.4f} %

Error Rate : {error_rate:.4f} %

Status : ANALYSIS COMPLETE
"""

        st.subheader("Analysis Report")

        st.code(report)

        st.download_button(
            "⬇ Download analysis_report.txt",
            report,
            file_name="analysis_report.txt"
        )
        # ====================================================
# ABOUT
# ====================================================

elif st.session_state.page == "About":

    st.title("ℹ About Project")
    st.caption("DNA Data Storage System — encoding digital data into synthetic DNA sequences")

    # ============================================
    # WHAT IS DNA STORAGE — 4 INFO TILES
    # ============================================

    st.markdown('<div class="card"><h3>🧬 What is DNA Storage?</h3></div>', unsafe_allow_html=True)

    info_tiles = [
        ("🧬", "DNA Storage", "#2e9e5b",
         "Encodes digital information into synthetic DNA strands using four "
         "bases — A, T, C, G — as a quaternary coding system. Extremely high "
         "theoretical storage density per gram of DNA."),
        ("🖼", "Image Encoding", "#2f7de1",
         "Images → RGB pixel arrays → each byte (0–255) → 8 bits. Each 2-bit "
         "pair maps to one DNA base. Image shape is saved in metadata.txt."),
        ("📝", "Text Encoding", "#d9772b",
         "Characters → ASCII/Unicode → 8-bit binary. Each 2-bit pair maps to "
         "one base. The full sequence is stored in text_dna.txt."),
        ("🦠", "Error Simulation", "#d6453d",
         "Real DNA is subject to base substitution errors during synthesis "
         "and sequencing. The simulator randomly replaces bases to model "
         "storage degradation."),
    ]

    tile_rows = [info_tiles[0:2], info_tiles[2:4]]

    for row in tile_rows:
        cols = st.columns(2)
        for col, (icon, title, color, desc) in zip(cols, row):
            with col:
                st.markdown(f"""
                <div style="
                background:#f1f4f9;
                border:1px solid #dde3ec;
                border-radius:12px;
                padding:18px 20px;
                margin-top:-14px;
                margin-bottom:16px;
                height:165px;
                ">
                <div style="font-size:15px;font-weight:700;color:{color};margin-bottom:8px;">
                {icon}&nbsp; {title}
                </div>
                <div style="font-size:13px;color:#5b6b7c;line-height:1.6;">
                {desc}
                </div>
                </div>
                """, unsafe_allow_html=True)

    # ============================================
    # OBJECTIVES
    # ============================================

    st.subheader("🎯 Project Objectives")

    c1, c2 = st.columns(2)

    with c1:

        st.success("✔ Encode Images into DNA")

        st.success("✔ Encode Text into DNA")

        st.success("✔ Decode DNA back to Images")

    with c2:

        st.success("✔ Decode DNA back to Text")

        st.success("✔ Simulate DNA Mutations")

        st.success("✔ Analyse Storage Accuracy")

    st.write("")

    # ============================================
    # FEATURES
    # ============================================

    st.subheader("⚙ System Features")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info("🖼 Image Encoding")

        st.info("🔬 Image Decoding")

    with col2:

        st.info("📝 Text Encoding")

        st.info("📄 Text Decoding")

    with col3:

        st.info("🦠 Error Simulation")

        st.info("📊 Analysis")

    st.write("")

    # ============================================
    # WORKFLOW
    # ============================================

    st.subheader("🔄 Project Workflow")

    st.markdown("""
<div class="card">

<center>

Image / Text

⬇

Binary Conversion

⬇

DNA Encoding

⬇

DNA Storage

⬇

Error Simulation

⬇

DNA Decoding

⬇

Original Data Recovery

</center>

</div>
""", unsafe_allow_html=True)

    # ============================================
    # DNA MAP — matches CTk's Encoding Map card
    # ============================================

    st.markdown('<div class="card"><h3>🗺 Encoding Map</h3></div>', unsafe_allow_html=True)

    map_cols = st.columns(4)
    for col, (bits, base, color) in zip(
        map_cols,
        [("00","A","#2e9e5b"), ("01","T","#2f7de1"), ("10","C","#d9772b"), ("11","G","#8a5cd6")]
    ):
        with col:
            st.markdown(f"""
            <div style="
            background:#f1f4f9;
            border:1px solid #dde3ec;
            border-radius:10px;
            text-align:center;
            padding:14px 0;
            margin-top:-14px;
            margin-bottom:14px;
            ">
            <div style="font-size:11px;color:#5b6b7c;">{bits}</div>
            <div style="font-size:24px;font-weight:800;font-family:'Cascadia Code',monospace;color:{color};">{base}</div>
            </div>
            """, unsafe_allow_html=True)

    

    
    # ============================================
    # TECHNOLOGY
    # ============================================

    st.subheader("💻 Technologies Used")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.success("Python")

        st.success("Streamlit")

    with col2:

        st.success("NumPy")

        st.success("Pillow")

    with col3:

        st.success("Custom DNA Algorithm")

        st.success("Subprocess")

    st.write("")

    

    st.success("🎉 DNA-Based Digital Storage System is Ready for Demonstration.")