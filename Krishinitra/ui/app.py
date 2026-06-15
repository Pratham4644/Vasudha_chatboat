# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import streamlit as st
# from streamlit_mic_recorder import mic_recorder
# from utils.temp_index import build_temp_index
# from utils.retriever import retrieve_combined
# from utils.main_kb import main_index, main_metadata
# from utils.generator import stream_answer

# st.set_page_config(
#     page_title="Vasudha",
#     page_icon="🌱",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

# *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

# html, body,
# [data-testid="stApp"],
# [data-testid="stAppViewContainer"] {
#     background: #f0f7f2 !important;
#     color: #2d5016 !important;
#     font-family: 'Inter', sans-serif;
#     font-size: 14px;
# }

# header[data-testid="stHeader"],
# footer, [data-testid="stToolbar"],
# .stDeployButton, #MainMenu { display: none !important; }

# /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
# [data-testid="stSidebar"] {
#     background: #ffffff !important;
#     border-right: 1px solid #d4e8c2 !important;
#     min-width: 230px !important;
#     max-width: 230px !important;
# }
# [data-testid="stSidebar"] > div:first-child {
#     padding: 0 !important;
# }

# /* Brand row */
# .sb-brand {
#     display: flex; align-items: center; gap: 10px;
#     padding: 14px 16px 12px;
# }
# .sb-brand-icon {
#     width: 34px; height: 34px;
#     background: #3a6b10;
#     border-radius: 8px;
#     display: flex; align-items: center; justify-content: center;
#     font-size: 18px; flex-shrink: 0;
# }
# .sb-brand-name {
#     font-size: 1.05rem; font-weight: 700;
#     color: #2d5016;
# }

# /* New Chat button */
# [data-testid="stSidebar"] .stButton button {
#     background: #3a6b10 !important;
#     border: none !important;
#     color: #ffffff !important;
#     border-radius: 8px !important;
#     font-family: 'Inter', sans-serif !important;
#     font-size: 0.85rem !important;
#     font-weight: 600 !important;
#     padding: 10px 14px !important;
#     width: 100% !important;
#     transition: background 0.15s !important;
#     letter-spacing: 0.01em !important;
# }
# [data-testid="stSidebar"] .stButton button:hover {
#     background: #2d5016 !important;
# }

# /* User card */
# .sb-user {
#     display: flex; align-items: center; gap: 10px;
#     padding: 9px 12px;
#     background: #eaf4e0;
#     margin: 8px 10px 4px;
#     border-radius: 8px;
# }
# .sb-user-avatar {
#     width: 30px; height: 30px;
#     background: #4a8520;
#     border-radius: 50%;
#     display: flex; align-items: center; justify-content: center;
#     font-size: 11px; font-weight: 700; color: #fff; flex-shrink: 0;
# }
# .sb-user-name { font-size: 0.83rem; font-weight: 600; color: #2d5016; line-height: 1.3; }
# .sb-user-role { font-size: 0.70rem; color: #6a9940; }

# /* Section label */
# .sb-section {
#     padding: 12px 14px 4px;
#     font-size: 0.68rem; font-weight: 700;
#     color: #6a9940; letter-spacing: 0.07em; text-transform: uppercase;
# }

# /* History items */
# .sb-item {
#     padding: 7px 14px;
#     font-size: 0.78rem; color: #4a7020;
#     cursor: pointer; border-radius: 6px; margin: 1px 8px;
#     white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
#     transition: background 0.12s;
# }
# .sb-item:hover { background: #eaf4e0; }
# .sb-item.active {
#     background: #ddf0c8;
#     font-weight: 500; color: #2d5016;
#     border-radius: 6px;
# }

# /* Upload expander */
# [data-testid="stSidebar"] [data-testid="stExpander"] {
#     background: transparent !important;
#     border: 1px dashed #b8d99a !important;
#     border-radius: 8px !important;
#     margin: 8px 10px 10px !important;
# }
# [data-testid="stSidebar"] [data-testid="stExpander"] summary {
#     color: #6a9940 !important;
#     font-size: 0.78rem !important;
#     padding: 9px 12px !important;
# }

# /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    TOP BAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
# .top-bar {
#     display: flex; align-items: center; justify-content: space-between;
#     padding: 12px 28px;
#     background: #ffffff;
#     border-bottom: 1px solid #d4e8c2;
# }
# .top-bar-title { font-size: 0.88rem; font-weight: 500; color: #2d5016; }
# .online-badge {
#     display: flex; align-items: center; gap: 5px;
#     font-size: 0.75rem; color: #4a8520;
# }
# .online-dot {
#     width: 7px; height: 7px; border-radius: 50%;
#     background: #4a8520; display: inline-block;
# }

# /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    MAIN BLOCK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
# .main .block-container {
#     max-width: 900px !important;
#     margin: 0 auto !important;
#     padding: 0 2.5rem 260px !important;
# }

# /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    WELCOME SCREEN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
# .welcome-wrap {
#     padding: 9vh 0 2.5rem;
#     text-align: center;
# }
# .welcome-icon-box {
#     width: 60px; height: 60px;
#     background: #ddf0c8;
#     border: 1.5px solid #b8d99a;
#     border-radius: 18px;
#     display: flex; align-items: center; justify-content: center;
#     font-size: 30px;
#     margin: 0 auto 18px;
# }
# .welcome-title {
#     font-size: 1.75rem; font-weight: 700;
#     color: #2d5016; margin-bottom: 8px;
# }
# .welcome-sub {
#     font-size: 0.84rem; color: #6a9940;
#     margin-bottom: 2.5rem; line-height: 1.6;
# }

# /* Suggestion cards */
# [data-testid="stMainBlockContainer"] [data-testid="stColumns"] .stButton button {
#     background: #ffffff !important;
#     border: 1.5px solid #c8e0a8 !important;
#     color: #3a6b10 !important;
#     border-radius: 10px !important;
#     font-family: 'Inter', sans-serif !important;
#     font-size: 0.82rem !important;
#     padding: 14px 18px !important;
#     text-align: left !important;
#     height: auto !important;
#     line-height: 1.5 !important;
#     transition: all 0.18s !important;
#     font-weight: 400 !important;
# }
# [data-testid="stMainBlockContainer"] [data-testid="stColumns"] .stButton button:hover {
#     border-color: #3a6b10 !important;
#     background: #eaf4e0 !important;
# }

# /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    CHAT MESSAGES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
# .chat-feed { display: flex; flex-direction: column; padding-top: 1.5rem; }

# .user-avatar-wrap {
#     display: flex; align-items: flex-start; gap: 10px;
#     justify-content: flex-end; margin-bottom: 18px;
# }
# .user-card {
#     background: #ffffff;
#     border: 1.5px solid #c8e0a8;
#     border-radius: 12px;
#     padding: 13px 17px;
#     max-width: 70%;
# }
# .user-card-label {
#     font-size: 0.67rem; font-weight: 700;
#     color: #6a9940; letter-spacing: 0.07em;
#     text-transform: uppercase; margin-bottom: 5px;
# }
# .user-card-text { font-size: 0.87rem; color: #2d5016; line-height: 1.65; }
# .user-avatar-icon {
#     width: 32px; height: 32px;
#     background: #4a8520; border-radius: 50%;
#     display: flex; align-items: center; justify-content: center;
#     font-size: 11px; font-weight: 700; color: #fff;
#     flex-shrink: 0; margin-top: 2px;
# }

# .ai-turn { display: flex; gap: 12px; margin-bottom: 22px; align-items: flex-start; }
# .ai-avatar {
#     width: 32px; height: 32px;
#     background: #3a6b10;
#     border-radius: 50%;
#     display: flex; align-items: center; justify-content: center;
#     font-size: 16px; flex-shrink: 0; margin-top: 2px;
# }
# .ai-card {
#     flex: 1; min-width: 0;
#     background: #ffffff;
#     border: 1.5px solid #c8e0a8;
#     border-radius: 12px;
#     padding: 15px 20px;
# }
# .ai-card-name { font-size: 0.8rem; font-weight: 700; color: #3a6b10; margin-bottom: 10px; }
# .ai-card-text { font-size: 0.87rem; color: #2d5016; line-height: 1.85; }
# .ai-card-text b, .ai-card-text strong { color: #1e3a08; }
# .ai-card-text ul { padding-left: 18px; margin: 8px 0; }
# .ai-card-text li { margin-bottom: 5px; }

# .sources-row { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px; }
# .src-pill {
#     font-size: 0.68rem; padding: 4px 11px; border-radius: 20px;
#     background: #eaf4e0; color: #3a6b10;
#     border: 1px solid #b8d99a;
#     display: inline-flex; align-items: center; gap: 4px;
# }

# /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    FIXED INPUT AREA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
# .input-backdrop {
#     position: fixed; bottom: 0; left: 0; right: 0;
#     background: linear-gradient(to top, #f0f7f2 65%, transparent);
#     z-index: 300;
# }
# .input-shell {
#     max-width: 900px; margin: 0 auto;
#     padding: 0 2.5rem 1.4rem;
# }

# /* Toolbar row ABOVE the textarea */
# .input-toolbar-row {
#     display: flex; align-items: center; gap: 5px;
#     margin-bottom: 6px;
#     padding: 0 2px;
# }
# .tb-btn {
#     background: #fff; border: 1px solid #c8e0a8;
#     cursor: pointer; color: #4a7020;
#     font-size: 12px; font-weight: 700;
#     padding: 4px 9px; border-radius: 6px;
#     font-family: 'Inter', sans-serif; line-height: 1.4;
#     transition: background 0.12s;
# }
# .tb-btn:hover { background: #eaf4e0; }

# /* Textarea + buttons row */
# .input-row {
#     display: flex; align-items: flex-end; gap: 8px;
# }
# .input-box-wrap {
#     flex: 1;
#     background: #ffffff;
#     border: 1.5px solid #c8e0a8;
#     border-radius: 10px;
#     overflow: hidden;
# }
# .input-box-wrap [data-testid="stTextArea"] { margin: 0 !important; }
# .input-box-wrap [data-testid="stTextArea"] > div {
#     border: none !important; background: transparent !important;
#     box-shadow: none !important; padding: 0 !important;
# }
# .input-box-wrap [data-testid="stTextArea"] textarea {
#     background: transparent !important;
#     border: none !important; box-shadow: none !important;
#     color: #2d5016 !important;
#     font-family: 'Inter', sans-serif !important;
#     font-size: 0.88rem !important;
#     padding: 14px 16px !important;
#     line-height: 1.6 !important;
#     resize: none !important;
#     caret-color: #3a6b10;
# }
# .input-box-wrap [data-testid="stTextArea"] textarea::placeholder {
#     color: #9fc87a !important;
# }

# /* Attach button */
# .attach-wrap .stButton button {
#     background: #f0f7f2 !important;
#     border: 1.5px solid #c8e0a8 !important;
#     border-radius: 8px !important;
#     padding: 0 !important;
#     color: #4a7020 !important;
#     font-size: 1rem !important;
#     width: 40px !important; height: 40px !important;
#     min-width: 40px !important;
#     display: flex !important; align-items: center !important;
#     justify-content: center !important;
#     transition: background 0.12s !important;
# }
# .attach-wrap .stButton button:hover {
#     background: #ddf0c8 !important; color: #2d5016 !important;
# }

# /* Send button */
# .send-wrap .stButton button {
#     background: #3a6b10 !important;
#     border: none !important;
#     border-radius: 8px !important;
#     padding: 0 18px !important;
#     color: #fff !important;
#     font-family: 'Inter', sans-serif !important;
#     font-size: 0.85rem !important;
#     font-weight: 600 !important;
#     height: 40px !important;
#     min-width: 88px !important;
#     transition: background 0.15s !important;
#     letter-spacing: 0.01em !important;
# }
# .send-wrap .stButton button:hover { background: #2d5016 !important; }

# .input-footer {
#     text-align: center; font-size: 0.65rem;
#     color: #9fc87a; padding: 5px 0 8px;
# }

# /* Alerts & file uploader */
# [data-testid="stAlert"] {
#     background: #eaf4e0 !important;
#     border: 1px solid #b8d99a !important;
#     color: #3a6b10 !important; border-radius: 8px !important;
#     font-size: 0.8rem !important;
# }
# [data-testid="stFileUploader"] {
#     background: transparent !important;
#     border: 1px dashed #b8d99a !important;
#     border-radius: 8px !important;
# }
# [data-testid="stFileUploader"] label { color: #6a9940 !important; font-size: 0.75rem !important; }

# /* Upload panel */
# .upload-panel {
#     background: #f5fbef;
#     border: 1.5px solid #c8e0a8;
#     border-radius: 10px 10px 0 0;
#     border-bottom: none;
#     padding: 10px 14px 8px;
#     margin-bottom: 0;
# }
# .upload-panel-title {
#     font-size: 0.71rem; font-weight: 600;
#     color: #6a9940; letter-spacing: 0.05em;
#     text-transform: uppercase; margin-bottom: 8px;
# }
# .file-chips { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 5px; }
# .file-chip, .file-chip-strip {
#     display: inline-flex; align-items: center; gap: 4px;
#     background: #eaf4e0; border: 1px solid #b8d99a;
#     border-radius: 20px; padding: 3px 10px;
#     font-size: 0.71rem; color: #3a6b10;
# }
# .files-strip { display: flex; flex-wrap: wrap; gap: 5px; padding: 6px 0 2px; }

# ::-webkit-scrollbar { width: 4px; }
# ::-webkit-scrollbar-track { background: transparent; }
# ::-webkit-scrollbar-thumb { background: #b8d99a; border-radius: 4px; }
# </style>
# """, unsafe_allow_html=True)

# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# # SESSION STATE
# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# for key, val in {
#     "messages": [],
#     "uploaded_docs": [],
#     "temp_index": None,
#     "temp_metadata": None,
#     "pending_question": "",
#     "input_key": 0,
#     "user_name": "Prof. Sharma",
#     "show_upload": False,
# }.items():
#     if key not in st.session_state:
#         st.session_state[key] = val

# SUGGESTIONS = [
#     ("🌾", "Best crops for loamy soil in Kharif season?"),
#     ("🍃", "How to identify and treat leaf blight?"),
#     ("💧", "Drip irrigation tips for summer crops"),
#     ("🌿", "Fertilizer schedule for wheat cultivation"),
# ]

# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# # SIDEBAR
# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# with st.sidebar:
#     st.markdown("""
#     <div class="sb-brand">
#         <div class="sb-brand-icon">🌱</div>
#         <div class="sb-brand-name">Vasudha</div>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("<div style='padding:6px 10px 8px;'>", unsafe_allow_html=True)
#     if st.button("＋  New Chat", key="new_chat"):
#         st.session_state.messages = []
#         st.session_state.uploaded_docs = []
#         st.session_state.temp_index = None
#         st.session_state.temp_metadata = None
#         st.session_state.input_key += 1
#         st.rerun()
#     st.markdown("</div>", unsafe_allow_html=True)

#     initials = "".join([w[0].upper() for w in st.session_state.user_name.split()][:2])
#     st.markdown(f"""
#     <div class="sb-user">
#         <div class="sb-user-avatar">{initials}</div>
#         <div>
#             <div class="sb-user-name">Prathamesh Shinde</div>
#             <div class="sb-user-role">Farmer · Sangli</div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     # Recent chats
#     user_msgs = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
#     if user_msgs:
#         st.markdown('<div class="sb-section">Recent</div>', unsafe_allow_html=True)
#         for i, msg in enumerate(reversed(user_msgs[-6:])):
#             preview = msg[:32] + "…" if len(msg) > 32 else msg
#             cls = "sb-item active" if i == 0 else "sb-item"
#             st.markdown(f'<div class="{cls}">{preview}</div>', unsafe_allow_html=True)
#     else:
#         st.markdown("""
#         <div class="sb-section">Recent</div>
#         <div class="sb-item active">Crops for loamy soil in Kharif...</div>
#         <div class="sb-item">Wheat fertilizer schedule</div>
#         <div class="sb-item">Drip irrigation for cotton</div>
#         """, unsafe_allow_html=True)

#     st.markdown("<div style='margin-top:auto;padding-top:20px;'>", unsafe_allow_html=True)
#     with st.expander("📂  Upload farm documents", expanded=False):
#         uploaded_files = st.file_uploader(
#             "docs", type=["pdf", "txt", "docx"],
#             accept_multiple_files=True,
#             label_visibility="collapsed",
#             key="doc_uploader",
#         )
#         if uploaded_files:
#             st.session_state.uploaded_docs = uploaded_files
#             with st.spinner("Indexing…"):
#                 st.session_state.temp_index, st.session_state.temp_metadata = build_temp_index(uploaded_files)
#             st.success(f"✅ {len(uploaded_files)} file(s) indexed")
#     st.markdown("</div>", unsafe_allow_html=True)


# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# # TOP BAR
# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# st.markdown("""
# <div class="top-bar">
#     <span class="top-bar-title">Vasudha — Agricultural Assistant</span>
#     <span class="online-badge">
#         <span class="online-dot"></span> Online
#     </span>
# </div>
# """, unsafe_allow_html=True)


# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# # MAIN CHAT / WELCOME
# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# if not st.session_state.messages:
#     st.markdown("""
#     <div class="welcome-wrap">
#         <div class="welcome-icon-box">🌱</div>
#         <div class="welcome-title">Welcome to Vasudha</div>
#         <div class="welcome-sub">Your AI-powered agricultural assistant.<br>Ask about crops, soil, pests, or farming.</div>
#     </div>
#     """, unsafe_allow_html=True)

#     col1, col2 = st.columns(2)
#     for i, (icon, text) in enumerate(SUGGESTIONS):
#         with (col1 if i % 2 == 0 else col2):
#             if st.button(f"{icon}  {text}", key=f"sugg_{i}", use_container_width=True):
#                 st.session_state.pending_question = text
#                 st.rerun()
# else:
#     parts = ['<div class="chat-feed">']
#     for msg in st.session_state.messages:
#         if msg["role"] == "user":
#             parts.append(f"""
#             <div class="user-avatar-wrap">
#                 <div class="user-card">
#                     <div class="user-card-label">You</div>
#                     <div class="user-card-text">{msg["content"]}</div>
#                 </div>
#                 <div class="user-avatar-icon">{initials}</div>
#             </div>""")
#         else:
#             sources_html = ""
#             if msg.get("sources"):
#                 pills = "".join(f'<span class="src-pill">📄 {s}</span>' for s in msg["sources"])
#                 sources_html = f'<div class="sources-row">{pills}</div>'
#             parts.append(f"""
#             <div class="ai-turn">
#                 <div class="ai-avatar">🌱</div>
#                 <div class="ai-card">
#                     <div class="ai-card-name">Vasudha</div>
#                     <div class="ai-card-text">{msg["content"]}</div>
#                     {sources_html}
#                 </div>
#             </div>""")
#     parts.append("</div>")
#     st.markdown("".join(parts), unsafe_allow_html=True)


# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# # STREAM RESPONSE
# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# def stream_response(user_q: str):
#     context_text, sources = retrieve_combined(
#         user_q, main_index(), main_metadata(),
#         st.session_state.temp_index, st.session_state.temp_metadata,
#     )
#     st.markdown("""
#     <div class="ai-turn">
#         <div class="ai-avatar">🌱</div>
#         <div class="ai-card">
#             <div class="ai-card-name">Vasudha</div>
#     """, unsafe_allow_html=True)

#     placeholder = st.empty()
#     full_response = ""
#     for token in stream_answer(context_text, user_q):
#         full_response += token
#         placeholder.markdown(
#             f'<div class="ai-card-text">{full_response}▌</div>',
#             unsafe_allow_html=True,
#         )
#     placeholder.markdown(
#         f'<div class="ai-card-text">{full_response}</div>',
#         unsafe_allow_html=True,
#     )
#     if sources:
#         pills = "".join(f'<span class="src-pill">📄 {s}</span>' for s in sources)
#         st.markdown(f'<div class="sources-row">{pills}</div>', unsafe_allow_html=True)
#     st.markdown("</div></div>", unsafe_allow_html=True)

#     if not full_response:
#         full_response = "⚠️ No response received. Please make sure Ollama is running."
#     st.session_state.messages.append({
#         "role": "assistant", "content": full_response, "sources": sources,
#     })


# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# # FIXED INPUT BAR  — toolbar ABOVE textarea (matches screenshot)
# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# st.markdown('<div class="input-backdrop"><div class="input-shell">', unsafe_allow_html=True)

# # PDF upload panel
# if st.session_state.show_upload:
#     st.markdown('<div class="upload-panel">', unsafe_allow_html=True)
#     st.markdown('<div class="upload-panel-title">📄 Upload Farm Report / PDF</div>', unsafe_allow_html=True)
#     up_files = st.file_uploader(
#         "Upload files", type=["pdf", "txt", "docx"],
#         accept_multiple_files=True,
#         key=f"inline_uploader_{st.session_state.input_key}",
#         label_visibility="collapsed",
#     )
#     if up_files:
#         st.session_state.uploaded_docs = up_files
#         with st.spinner("Indexing…"):
#             st.session_state.temp_index, st.session_state.temp_metadata = build_temp_index(up_files)
#         chips = "".join(f'<span class="file-chip">📄 {f.name}</span>' for f in up_files)
#         st.markdown(f'<div class="file-chips">{chips}</div>', unsafe_allow_html=True)
#         st.success(f"✅ {len(up_files)} file(s) ready")
#     st.markdown('</div>', unsafe_allow_html=True)

# # File strip when panel closed
# if st.session_state.uploaded_docs and not st.session_state.show_upload:
#     chips = "".join(f'<span class="file-chip-strip">📄 {f.name}</span>' for f in st.session_state.uploaded_docs)
#     st.markdown(f'<div class="files-strip">{chips}</div>', unsafe_allow_html=True)

# # Formatting toolbar (above textarea)
# st.markdown("""
# <div class="input-toolbar-row">
#     <button class="tb-btn"><b>B</b></button>
#     <button class="tb-btn"><i>I</i></button>
#     <button class="tb-btn"><u>U</u></button>
#     <button class="tb-btn" style="font-family:monospace;">&#60;/&#62;</button>
# </div>
# """, unsafe_allow_html=True)

# # Textarea + mic + attach + send on same row
# radius = "0 0 10px 10px" if st.session_state.show_upload else "10px"
# input_col, mic_col, attach_col, send_col = st.columns([9, 1, 1, 1.4])

# with input_col:
#     st.markdown(f'<div class="input-box-wrap" style="border-radius:{radius}">', unsafe_allow_html=True)
#     user_input = st.text_area(
#         label="msg",
#         placeholder="Message Vasudha... (attach a PDF report)",
#         label_visibility="collapsed",
#         key=f"prompt_{st.session_state.input_key}",
#         height=56,
#     )
#     st.markdown('</div>', unsafe_allow_html=True)

# with mic_col:
#     st.markdown('<div class="attach-wrap">', unsafe_allow_html=True)
#     audio = mic_recorder(start_prompt="🎤", stop_prompt="⏹️", key="recorder")
#     if audio:
#         try:
#             with st.spinner("🎤 Transcribing..."):
#                 # Save audio to temp file
#                 temp_file = "temp_audio.wav"
#                 with open(temp_file, "wb") as f:
#                     f.write(audio['bytes'])
#                 # Transcribe
#                 from utils.speech_to_text import transcribe_audio
#                 transcribed_text = transcribe_audio(temp_file)
#                 # Clean up
#                 if os.path.exists(temp_file):
#                     os.remove(temp_file)
#                 # Set the text directly in the session state key that the text_area uses
#                 st.session_state[f"prompt_{st.session_state.input_key}"] = transcribed_text
#                 st.success("✅ Text captured!")
#                 st.rerun()
#         except Exception as e:
#             st.error(f"Error transcribing audio: {str(e)}")
#     st.markdown('</div>', unsafe_allow_html=True)

# with attach_col:
#     st.markdown('<div class="attach-wrap">', unsafe_allow_html=True)
#     if st.button("↑", key="attach_btn", help="Upload PDF"):
#         st.session_state.show_upload = not st.session_state.show_upload
#         st.rerun()
#     st.markdown('</div>', unsafe_allow_html=True)

# with send_col:
#     st.markdown('<div class="send-wrap">', unsafe_allow_html=True)
#     send_clicked = st.button("→  Send", key="send_btn")
#     st.markdown('</div>', unsafe_allow_html=True)

# st.markdown(
#     '<div class="input-footer">Powered by Vasudha Agronomy Model v1.2</div>',
#     unsafe_allow_html=True,
# )
# st.markdown('</div></div>', unsafe_allow_html=True)

# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# # HANDLE SUBMIT
# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# user_q = ""

# if send_clicked and user_input and user_input.strip():
#     user_q = user_input.strip()
#     st.session_state.input_key += 1
# elif st.session_state.pending_question:
#     user_q = st.session_state.pending_question
#     st.session_state.pending_question = ""

# if user_q:
#     st.session_state.messages.append({"role": "user", "content": user_q})
#     stream_response(user_q)
#     st.rerun()






import sys
import os
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from streamlit_mic_recorder import mic_recorder

from utils.temp_index import build_temp_index
from utils.retriever import retrieve_combined
from utils.main_kb import main_index, main_metadata
from utils.generator import stream_answer

# ── Optional: Whisper speech-to-text (graceful fallback if missing) ──
try:
    import whisper as _whisper
    _WHISPER_MODEL = _whisper.load_model("base")
    WHISPER_OK = True
except Exception:
    WHISPER_OK = False

def transcribe_audio(path: str) -> str:
    """Transcribe a WAV file using Whisper. Returns empty string on failure."""
    if not WHISPER_OK:
        return ""
    try:
        result = _WHISPER_MODEL.transcribe(path)
        return result.get("text", "").strip()
    except Exception:
        return ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="Vasudha",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CSS — exact match to screenshot
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"] {
    background: #eef7ee !important;
    color: #2d5016 !important;
    font-family: 'Inter', sans-serif;
    font-size: 14px;
}

header[data-testid="stHeader"],
footer, [data-testid="stToolbar"],
.stDeployButton, #MainMenu { display: none !important; }

/* ══════════════════════════════
   SIDEBAR
══════════════════════════════ */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #cde8b0 !important;
    min-width: 228px !important;
    max-width: 228px !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }

.sb-brand {
    display: flex; align-items: center; gap: 10px;
    padding: 15px 16px 13px;
    border-bottom: 1px solid #e2f0d0;
}
.sb-brand-icon {
    width: 34px; height: 34px;
    background: #3a6b10;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
}
.sb-brand-name { font-size: 1.05rem; font-weight: 700; color: #2d5016; }

/* All sidebar Streamlit buttons (New Chat) */
[data-testid="stSidebar"] .stButton button {
    background: #3a6b10 !important;
    border: none !important;
    color: #fff !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    padding: 10px 14px !important;
    width: 100% !important;
    transition: background 0.15s !important;
}
[data-testid="stSidebar"] .stButton button:hover { background: #2d5016 !important; }

.sb-user {
    display: flex; align-items: center; gap: 10px;
    padding: 9px 12px;
    background: #eaf4e0;
    margin: 8px 10px 2px;
    border-radius: 8px;
}
.sb-user-avatar {
    width: 30px; height: 30px;
    background: #4a8520; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700; color: #fff; flex-shrink: 0;
}
.sb-user-name  { font-size: 0.83rem; font-weight: 600; color: #2d5016; line-height: 1.3; }
.sb-user-role  { font-size: 0.70rem; color: #6a9940; }

.sb-section {
    padding: 10px 14px 3px;
    font-size: 0.67rem; font-weight: 700;
    color: #6a9940; letter-spacing: 0.07em; text-transform: uppercase;
}

.sb-item {
    padding: 6px 14px;
    font-size: 0.78rem; color: #4a7020;
    cursor: pointer; border-radius: 6px; margin: 1px 8px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    transition: background 0.12s;
}
.sb-item:hover { background: #eaf4e0; }
.sb-item.active { background: #d6edb8; font-weight: 500; color: #2d5016; }

[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: transparent !important;
    border: 1px dashed #b0d490 !important;
    border-radius: 8px !important;
    margin: 6px 10px 8px !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    color: #6a9940 !important; font-size: 0.78rem !important; padding: 9px 12px !important;
}

/* ══════════════════════════════
   TOP BAR
══════════════════════════════ */
.top-bar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 11px 28px;
    background: #ffffff;
    border-bottom: 1px solid #cde8b0;
    position: sticky; top: 0; z-index: 200;
}
.top-bar-title { font-size: 0.87rem; font-weight: 500; color: #2d5016; }
.online-badge  { display: flex; align-items: center; gap: 5px; font-size: 0.74rem; color: #4a8520; }
.online-dot    { width: 7px; height: 7px; border-radius: 50%; background: #4a8520; display: inline-block; }

/* ══════════════════════════════
   MAIN BLOCK
══════════════════════════════ */
.main .block-container {
    max-width: 920px !important;
    margin: 0 auto !important;
    padding: 0 2.5rem 260px !important;
}

/* ══════════════════════════════
   WELCOME
══════════════════════════════ */
.welcome-wrap { padding: 9vh 0 2.5rem; text-align: center; }
.welcome-icon-box {
    width: 62px; height: 62px;
    background: #d9efc0; border: 1.5px solid #b0d490;
    border-radius: 20px;
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; margin: 0 auto 18px;
}
.welcome-title { font-size: 1.75rem; font-weight: 700; color: #2d5016; margin-bottom: 8px; }
.welcome-sub   { font-size: 0.84rem; color: #6a9940; margin-bottom: 2.5rem; line-height: 1.6; }

/* Suggestion chip buttons */
[data-testid="stMainBlockContainer"] [data-testid="stColumns"] .stButton button,
[data-testid="stMainBlockContainer"] [data-testid="stColumns"] .stButton > button,
[data-testid="stMainBlockContainer"] [data-testid="stColumns"] button {
    background: #ffffff !important;
    border: 1.5px solid #c2df9e !important;
    color: #2d5016 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    padding: 13px 18px !important;
    text-align: left !important;
    height: auto !important;
    line-height: 1.5 !important;
    font-weight: 400 !important;
    box-shadow: none !important;
    transition: all 0.18s !important;
}
[data-testid="stMainBlockContainer"] [data-testid="stColumns"] .stButton button:hover,
[data-testid="stMainBlockContainer"] [data-testid="stColumns"] .stButton > button:hover,
[data-testid="stMainBlockContainer"] [data-testid="stColumns"] button:hover {
    border-color: #3a6b10 !important;
    background: #eaf4e0 !important;
}

/* ══════════════════════════════
   CHAT MESSAGES
══════════════════════════════ */
.chat-feed { display: flex; flex-direction: column; padding-top: 1.5rem; }

.user-avatar-wrap {
    display: flex; align-items: flex-start; gap: 10px;
    justify-content: flex-end; margin-bottom: 18px;
}
.user-card {
    background: #ffffff; border: 1.5px solid #c2df9e;
    border-radius: 12px; padding: 13px 17px; max-width: 70%;
}
.user-card-label {
    font-size: 0.67rem; font-weight: 700; color: #6a9940;
    letter-spacing: 0.07em; text-transform: uppercase; margin-bottom: 5px;
}
.user-card-text { font-size: 0.87rem; color: #2d5016; line-height: 1.65; }
.user-avatar-icon {
    width: 32px; height: 32px; background: #4a8520; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700; color: #fff; flex-shrink: 0; margin-top: 2px;
}

.ai-turn { display: flex; gap: 12px; margin-bottom: 22px; align-items: flex-start; }
.ai-avatar {
    width: 32px; height: 32px; background: #3a6b10; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0; margin-top: 2px;
}
.ai-card {
    flex: 1; min-width: 0; background: #ffffff;
    border: 1.5px solid #c2df9e; border-radius: 12px; padding: 15px 20px;
}
.ai-card-name  { font-size: 0.8rem; font-weight: 700; color: #3a6b10; margin-bottom: 10px; }
.ai-card-text  { font-size: 0.87rem; color: #2d5016; line-height: 1.85; }
.ai-card-text b, .ai-card-text strong { color: #1e3a08; }
.ai-card-text ul { padding-left: 18px; margin: 8px 0; }
.ai-card-text li { margin-bottom: 5px; }

.sources-row { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px; }
.src-pill {
    font-size: 0.68rem; padding: 4px 11px; border-radius: 20px;
    background: #eaf4e0; color: #3a6b10; border: 1px solid #b0d490;
    display: inline-flex; align-items: center; gap: 4px;
}

/* ══════════════════════════════
   FIXED INPUT AREA
══════════════════════════════ */
.input-backdrop {
    position: fixed; bottom: 0; left: 0; right: 0;
    background: linear-gradient(to top, #eef7ee 65%, transparent);
    z-index: 300;
}
.input-shell { max-width: 920px; margin: 0 auto; padding: 0 2.5rem 1.3rem; }

/* Toolbar row ABOVE textarea */
.input-toolbar-row {
    display: flex; align-items: center; gap: 5px;
    margin-bottom: 6px; padding: 0 2px;
}
.tb-btn {
    background: #fff; border: 1px solid #c2df9e; cursor: pointer;
    color: #4a7020; font-size: 12px; font-weight: 700;
    padding: 4px 9px; border-radius: 6px;
    font-family: 'Inter', sans-serif; line-height: 1.4;
    transition: background 0.12s;
}
.tb-btn:hover { background: #eaf4e0; }

/* Textarea wrapper */
.input-box-wrap {
    background: #ffffff; border: 1.5px solid #c2df9e;
    overflow: hidden;
}
.input-box-wrap [data-testid="stTextArea"] { margin: 0 !important; }
.input-box-wrap [data-testid="stTextArea"] > div {
    border: none !important; background: transparent !important;
    box-shadow: none !important; padding: 0 !important;
}
.input-box-wrap [data-testid="stTextArea"] textarea {
    background: transparent !important; border: none !important;
    box-shadow: none !important; color: #2d5016 !important;
    font-family: 'Inter', sans-serif !important; font-size: 0.88rem !important;
    padding: 14px 16px !important; line-height: 1.6 !important;
    resize: none !important; caret-color: #3a6b10;
}
.input-box-wrap [data-testid="stTextArea"] textarea::placeholder { color: #98c078 !important; }

/* ── icon buttons (mic / attach) ── */
.icon-wrap .stButton button {
    background: #f2f9ec !important;
    border: 1.5px solid #c2df9e !important;
    border-radius: 8px !important;
    padding: 0 !important;
    color: #4a7020 !important;
    font-size: 1.05rem !important;
    width: 40px !important; height: 40px !important; min-width: 40px !important;
    display: flex !important; align-items: center !important; justify-content: center !important;
    transition: background 0.12s !important;
}
.icon-wrap .stButton button:hover { background: #d9efc0 !important; color: #2d5016 !important; }

/* mic recorder widget — match icon button style */
.icon-wrap div[data-testid="stAudio"],
.icon-wrap audio { display: none; }
.icon-wrap .stButton > button[kind="secondary"] {
    background: #f2f9ec !important; border: 1.5px solid #c2df9e !important;
    border-radius: 8px !important; width: 40px !important; height: 40px !important;
    color: #4a7020 !important; font-size: 1rem !important;
}

/* Send button */
.send-wrap .stButton button {
    background: #3a6b10 !important; border: none !important;
    border-radius: 8px !important; padding: 0 18px !important;
    color: #fff !important; font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important; font-weight: 600 !important;
    height: 40px !important; min-width: 90px !important;
    transition: background 0.15s !important;
}
.send-wrap .stButton button:hover { background: #2d5016 !important; }

.input-footer {
    text-align: center; font-size: 0.65rem; color: #98c078; padding: 5px 0 7px;
}

/* Alerts */
[data-testid="stAlert"] {
    background: #eaf4e0 !important; border: 1px solid #b0d490 !important;
    color: #3a6b10 !important; border-radius: 8px !important; font-size: 0.8rem !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: transparent !important; border: 1px dashed #b0d490 !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploader"] label { color: #6a9940 !important; font-size: 0.75rem !important; }

/* Upload panel */
.upload-panel {
    background: #f5fbef; border: 1.5px solid #c2df9e;
    border-radius: 10px 10px 0 0; border-bottom: none;
    padding: 10px 14px 8px;
}
.upload-panel-title {
    font-size: 0.71rem; font-weight: 600; color: #6a9940;
    letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 8px;
}
.file-chips, .files-strip { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 5px; }
.file-chip, .file-chip-strip {
    display: inline-flex; align-items: center; gap: 4px;
    background: #eaf4e0; border: 1px solid #b0d490;
    border-radius: 20px; padding: 3px 10px;
    font-size: 0.71rem; color: #3a6b10;
}

/* Spinner */
[data-testid="stSpinner"] { color: #3a6b10 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #b0d490; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SESSION STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_DEFAULTS = {
    "messages":        [],
    "uploaded_docs":   [],
    "temp_index":      None,
    "temp_metadata":   None,
    "pending_question":"",
    "input_key":       0,
    "user_name":       "Prathamesh Shinde",
    "user_role":       "Farmer · Sangli",
    "show_upload":     False,
    "mic_transcript":  "",
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

SUGGESTIONS = [
    ("🌾", "Best crops for loamy soil in Kharif season?"),
    ("🍃", "How to identify and treat leaf blight?"),
    ("💧", "Drip irrigation tips for summer crops"),
    ("🌿", "Fertilizer schedule for wheat cultivation"),
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
initials = "".join([w[0].upper() for w in st.session_state.user_name.split()][:2])

with st.sidebar:
    # Brand
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-brand-icon">🌱</div>
        <div class="sb-brand-name">Vasudha</div>
    </div>
    """, unsafe_allow_html=True)

    # New Chat
    st.markdown("<div style='padding:8px 10px 6px;'>", unsafe_allow_html=True)
    if st.button("＋  New Chat", key="new_chat"):
        for k in ["messages", "uploaded_docs", "temp_index", "temp_metadata", "mic_transcript"]:
            st.session_state[k] = [] if isinstance(_DEFAULTS[k], list) else None
        st.session_state.input_key += 1
        st.session_state.show_upload = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # User card
    st.markdown(f"""
    <div class="sb-user">
        <div class="sb-user-avatar">{initials}</div>
        <div>
            <div class="sb-user-name">{st.session_state.user_name}</div>
            <div class="sb-user-role">{st.session_state.user_role}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Recent chats
    user_msgs = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
    st.markdown('<div class="sb-section">Recent</div>', unsafe_allow_html=True)
    if user_msgs:
        for i, msg in enumerate(reversed(user_msgs[-6:])):
            preview = msg[:30] + "…" if len(msg) > 30 else msg
            cls = "sb-item active" if i == 0 else "sb-item"
            st.markdown(f'<div class="{cls}">{preview}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="sb-item active">Crops for loamy soil in Kharif...</div>
        <div class="sb-item">Wheat fertilizer schedule</div>
        <div class="sb-item">Drip irrigation for cotton</div>
        """, unsafe_allow_html=True)

    # Spacer + Upload expander at bottom
    st.markdown("<div style='flex:1;min-height:30px'></div>", unsafe_allow_html=True)
    with st.expander("📂  Upload farm documents", expanded=False):
        sb_files = st.file_uploader(
            "docs", type=["pdf", "txt", "docx"],
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="doc_uploader",
        )
        if sb_files:
            st.session_state.uploaded_docs = sb_files
            with st.spinner("Indexing…"):
                st.session_state.temp_index, st.session_state.temp_metadata = \
                    build_temp_index(sb_files)
            st.success(f"✅ {len(sb_files)} file(s) indexed")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOP BAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<div class="top-bar">
    <span class="top-bar-title">Vasudha — Agricultural Assistant</span>
    <span class="online-badge"><span class="online-dot"></span> Online</span>
</div>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN CHAT / WELCOME
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-wrap">
        <div class="welcome-icon-box">🌱</div>
        <div class="welcome-title">Welcome to Vasudha</div>
        <div class="welcome-sub">Your AI-powered agricultural assistant.<br>
        Ask about crops, soil, pests, or farming.</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    for i, (icon, text) in enumerate(SUGGESTIONS):
        with (c1 if i % 2 == 0 else c2):
            if st.button(f"{icon}  {text}", key=f"sugg_{i}", use_container_width=True):
                st.session_state.pending_question = text
                st.rerun()
else:
    parts = ['<div class="chat-feed">']
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            parts.append(f"""
            <div class="user-avatar-wrap">
                <div class="user-card">
                    <div class="user-card-label">You</div>
                    <div class="user-card-text">{msg["content"]}</div>
                </div>
                <div class="user-avatar-icon">{initials}</div>
            </div>""")
        else:
            src_html = ""
            if msg.get("sources"):
                pills = "".join(f'<span class="src-pill">📄 {s}</span>'
                                for s in msg["sources"])
                src_html = f'<div class="sources-row">{pills}</div>'
            parts.append(f"""
            <div class="ai-turn">
                <div class="ai-avatar">🌱</div>
                <div class="ai-card">
                    <div class="ai-card-name">Vasudha</div>
                    <div class="ai-card-text">{msg["content"]}</div>
                    {src_html}
                </div>
            </div>""")
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STREAM RESPONSE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def stream_response(user_q: str):
    context_text, sources = retrieve_combined(
        user_q, main_index(), main_metadata(),
        st.session_state.temp_index, st.session_state.temp_metadata,
    )
    st.markdown("""
    <div class="ai-turn">
        <div class="ai-avatar">🌱</div>
        <div class="ai-card">
            <div class="ai-card-name">Vasudha</div>
    """, unsafe_allow_html=True)

    placeholder = st.empty()
    full = ""
    for token in stream_answer(context_text, user_q):
        full += token
        placeholder.markdown(f'<div class="ai-card-text">{full}▌</div>',
                             unsafe_allow_html=True)
    placeholder.markdown(f'<div class="ai-card-text">{full}</div>',
                         unsafe_allow_html=True)

    if sources:
        pills = "".join(f'<span class="src-pill">📄 {s}</span>' for s in sources)
        st.markdown(f'<div class="sources-row">{pills}</div>', unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    if not full:
        full = "⚠️ No response received. Please make sure Ollama is running."
    st.session_state.messages.append(
        {"role": "assistant", "content": full, "sources": sources}
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FIXED INPUT BAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown('<div class="input-backdrop"><div class="input-shell">', unsafe_allow_html=True)

# ── PDF upload panel (shown when toggled) ────────────────────────────
if st.session_state.show_upload:
    st.markdown('<div class="upload-panel">', unsafe_allow_html=True)
    st.markdown('<div class="upload-panel-title">📄 Upload Farm Report / PDF</div>', unsafe_allow_html=True)
    up_files = st.file_uploader(
        "Upload files", type=["pdf", "txt", "docx"],
        accept_multiple_files=True,
        key=f"inline_uploader_{st.session_state.input_key}",
        label_visibility="collapsed",
    )
    if up_files:
        st.session_state.uploaded_docs = up_files
        with st.spinner("Indexing documents…"):
            st.session_state.temp_index, st.session_state.temp_metadata = \
                build_temp_index(up_files)
        chips = "".join(f'<span class="file-chip">📄 {f.name}</span>' for f in up_files)
        st.markdown(f'<div class="file-chips">{chips}</div>', unsafe_allow_html=True)
        st.success(f"✅ {len(up_files)} file(s) ready")
    st.markdown('</div>', unsafe_allow_html=True)

# ── File chip strip when panel closed ───────────────────────────────
if st.session_state.uploaded_docs and not st.session_state.show_upload:
    chips = "".join(
        f'<span class="file-chip-strip">📄 {f.name}</span>'
        for f in st.session_state.uploaded_docs
    )
    st.markdown(f'<div class="files-strip">{chips}</div>', unsafe_allow_html=True)

# ── Formatting toolbar ───────────────────────────────────────────────
st.markdown("""
<div class="input-toolbar-row">
    <button class="tb-btn"><b>B</b></button>
    <button class="tb-btn"><i>I</i></button>
    <button class="tb-btn"><u>U</u></button>
    <button class="tb-btn" style="font-family:monospace;">&#60;/&#62;</button>
</div>
""", unsafe_allow_html=True)

# ── Textarea + mic + attach + send row ──────────────────────────────
radius = "0 0 10px 10px" if st.session_state.show_upload else "10px"
input_col, mic_col, attach_col, send_col = st.columns([9.5, 1, 1, 1.5])

with input_col:
    st.markdown(
        f'<div class="input-box-wrap" style="border-radius:{radius}">',
        unsafe_allow_html=True,
    )
    # Pre-fill textarea with mic transcript if available
    default_val = st.session_state.pop("mic_transcript", "") or ""
    user_input = st.text_area(
        label="msg",
        value=default_val,
        placeholder="Message Vasudha... (attach a PDF report)",
        label_visibility="collapsed",
        key=f"prompt_{st.session_state.input_key}",
        height=56,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ── Mic button ───────────────────────────────────────────────────────
with mic_col:
    st.markdown('<div class="icon-wrap">', unsafe_allow_html=True)
    audio = mic_recorder(
        start_prompt="🎤",
        stop_prompt="⏹️",
        just_once=True,
        key=f"mic_{st.session_state.input_key}",
    )
    if audio and audio.get("bytes"):
        with st.spinner("Transcribing…"):
            try:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                tmp.write(audio["bytes"])
                tmp.close()
                text = transcribe_audio(tmp.name)
                os.unlink(tmp.name)
                if text:
                    st.session_state.mic_transcript = text
                    st.session_state.input_key += 1   # force textarea refresh
                    st.rerun()
                else:
                    st.warning("Could not transcribe. Please type instead.")
            except Exception as e:
                st.error(f"Mic error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Attach (PDF toggle) ──────────────────────────────────────────────
with attach_col:
    st.markdown('<div class="icon-wrap">', unsafe_allow_html=True)
    attach_label = "📎✓" if st.session_state.show_upload else "↑"
    if st.button(attach_label, key="attach_btn", help="Upload PDF / Report"):
        st.session_state.show_upload = not st.session_state.show_upload
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── Send ─────────────────────────────────────────────────────────────
with send_col:
    st.markdown('<div class="send-wrap">', unsafe_allow_html=True)
    send_clicked = st.button("→  Send", key="send_btn")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="input-footer">Powered by Vasudha Agronomy Model v1.2</div>',
    unsafe_allow_html=True,
)
st.markdown('</div></div>', unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HANDLE SUBMIT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
user_q = ""

if send_clicked and user_input and user_input.strip():
    user_q = user_input.strip()
    st.session_state.input_key += 1          # clears the textarea
elif st.session_state.pending_question:
    user_q = st.session_state.pending_question
    st.session_state.pending_question = ""

if user_q:
    st.session_state.messages.append({"role": "user", "content": user_q})
    stream_response(user_q)
    st.rerun()