import streamlit as st
import pandas as pd

# 設置手機適應的最佳化版面
st.set_page_config(
    page_title="女友美食備忘錄 ❤️",
    page_icon="🍰",
    layout="centered"
)

# ---------------------------------------------------------
# 🎨 自訂米色背景與深色字體樣式 (CSS)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* 全體背景與字體顏色設定 */
    .stApp {
        background-color: #FDFBF7;
        color: #2D2A29;
    }
    
    /* 標題與文字顏色 */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #2D2A29 !important;
    }
    
    /* 輸入框與選擇器外觀優化 */
    div[data-baseweb="select"] > div, input, textarea {
        background-color: #F4EFEA !important;
        color: #2D2A29 !important;
        border-color: #D6CCC2 !important;
    }
    
    /* 按鈕樣式 */
    .stButton>button {
        background-color: #C5A880 !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #B0926A !important;
    }
    </style>
""", unsafe_allow_html=True)

# 標題區塊
st.markdown("<h1 style='text-align: center; color: #4A403A;'>✨ 女友專屬美食備忘錄 ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7B726C;'>記錄她的最愛、口袋名單與絕對不能踩的雷區（可自訂分類與項目）</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------------------------------------------------------
# 1. 初始化 Session State (記憶分類與筆記清單)
# ---------------------------------------------------------
if 'categories' not in st.session_state:
    st.session_state.categories = ["食物 (正餐)", "甜點", "零食", "飲料"]

if 'memo_data' not in st.session_state:
    st.session_state.memo_data = [
        {"category": "甜點", "item_name": "栗子蒙布朗", "preference": "❤️ 超級喜歡", "notes": "最愛信義區那家，不喜歡太甜"},
        {"category": "飲料", "item_name": "珍珠奶茶", "preference": "😋 還不錯 / 偶爾吃", "notes": "微糖微冰，珍珠要Q"},
        {"category": "食物 (正餐)", "item_name": "香菜與芋頭", "preference": "❌ 雷區 / 絕對不吃", "notes": "看到會生氣！"},
    ]

# ---------------------------------------------------------
# 2. 側邊欄：新增自訂分類
# ---------------------------------------------------------
st.sidebar.header("⚙️ 管理與設定")
with st.sidebar.expander("➕ 新增自訂分類項目"):
    new_cat = st.text_input("輸入新的分類名稱（例如：水果、宵夜）")
    if st.button("新增分類"):
        if new_cat.strip() and new_cat not in st.session_state.categories:
            st.session_state.categories.append(new_cat.strip())
            st.success(f"✅ 成功新增分類：{new_cat}")
            st.rerun()
        elif new_cat in st.session_state.categories:
            st.warning("⚠️ 該分類已經存在囉！")

# ---------------------------------------------------------
# 3. 新增美食記錄區塊（手機好操作的表單）
# ---------------------------------------------------------
st.subheader("➕ 新增美食筆記")

with st.form("add_memo_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("📂 選擇分類", st.session_state.categories)
    with col2:
        preference = st.selectbox("💖 喜愛程度", ["❤️ 超級喜歡", "😋 還不錯 / 偶爾吃", "❌ 雷區 / 絕對不吃"])
        
    item_name = st.text_input("✨ 品項名稱（例如：草莓蛋糕、無糖綠茶）")
    notes = st.text_area("📝 專屬備註（例如：喜歡哪家店、不加香菜、微糖微冰等）")
    
    submitted = st.form_submit_button("💾 儲存到備忘錄", use_container_width=True)
    if submitted:
        if item_name.strip() == "":
            st.warning("⚠️ 請至少輸入品項名稱喔！")
        else:
            st.session_state.memo_data.append({
                "category": category,
                "item_name": item_name,
                "preference": preference,
                "notes": notes
            })
            st.success(f"✅ 成功新增：【{item_name}】！")
            st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# 4. 篩選與檢視女友的清單
# ---------------------------------------------------------
st.subheader("📋 現有美食清單總覽")

if not st.session_state.memo_data:
    st.info("目前還沒有記錄任何美食，趕快在上方新增吧！")
else:
    df = pd.DataFrame(st.session_state.memo_data)
    
    filter_options = ["全部顯示"] + st.session_state.categories
    filter_cat = st.selectbox("🔍 依分類快速篩選", filter_options)
    
    if filter_cat != "全部顯示":
        filtered_df = df[df["category"] == filter_cat]
    else:
        filtered_df = df
        
    for index, row in filtered_df.iterrows():
        if "❤️" in row['preference']:
            box_color = "#F4D1AE"
        elif "❌" in row['preference']:
            box_color = "#E8C2C8"
        else:
            box_color = "#EFEAD8"
            
        st.markdown(f"""
        <div style="background-color: {box_color}; padding: 14px; border-radius: 12px; margin-bottom: 12px; color: #2D2A29; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <b>📂 【{row['category']}】 {row['item_name']}</b><br>
            <span>評語：{row['preference']}</span><br>
            <small>備註：{row['notes']}</small>
        </div>
        """, unsafe_allow_html=True)
        
    col_del1, col_del2 = st.columns(2)
    with col_del1:
        if st.button("🗑️ 刪除最後一筆記錄"):
            if len(st.session_state.memo_data) > 0:
                st.session_state.memo_data.pop()
                st.rerun()
    with col_del2:
        if st.button("🔄 清空全部記錄"):
            st.session_state.memo_data = []
            st.rerun()
