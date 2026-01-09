import streamlit as st
import json

st.set_page_config(page_title="線上文字編輯器", page_icon="📝", layout="wide")

st.title("📝 線上文字編輯器")
st.markdown("支援 **MD**、**TXT**、**JSON** 檔案的上傳、檢視、編輯和下載")

uploaded_file = st.sidebar.file_uploader("📁 上傳檔案", type=["md", "txt", "json"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()

    try:
        file_content = uploaded_file.getvalue().decode("utf-8")
    except UnicodeDecodeError:
        file_content = uploaded_file.getvalue().decode("latin-1")

    st.session_state[f"content_{uploaded_file.name}"] = file_content
    st.session_state[f"original_name_{uploaded_file.name}"] = uploaded_file.name

if uploaded_file is not None and f"content_{uploaded_file.name}" in st.session_state:
    current_content = st.session_state[f"content_{uploaded_file.name}"]
    original_name = st.session_state[f"original_name_{uploaded_file.name}"]

    tab1, tab2 = st.tabs(["📖 檢視", "✏️ 編輯"])

    with tab1:
        if file_type == "md":
            st.markdown(current_content)
        elif file_type == "json":
            try:
                parsed_json = json.loads(current_content)
                st.json(parsed_json)
            except json.JSONDecodeError:
                st.error("JSON 格式錯誤")
                st.text(current_content)
        else:
            st.text(current_content)

    with tab2:
        edited_content = st.text_area(
            "編輯內容",
            value=current_content,
            height=400,
            key=f"editor_{uploaded_file.name}",
        )

        if edited_content != current_content:
            st.warning("⚠️ 內容已修改")

        col1, col2 = st.columns([1, 4])
        with col1:
            st.download_button(
                label="💾 下載檔案",
                data=edited_content,
                file_name=original_name,
                mime=f"text/{file_type}"
                if file_type in ["txt", "md"]
                else "application/json",
            )
else:
    st.info("👈 請從側邊欄上傳一個檔案開始")

    st.markdown("---")
    st.markdown("### 範例預覽")
    st.info("支援的格式：.md、.txt、.json")
