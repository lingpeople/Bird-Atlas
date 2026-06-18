"""苏州鸟类图谱 - Streamlit 应用"""

import streamlit as st
import os
from bird_data import BIRDS_DATA

# 资源目录基于脚本所在路径，避免 streamlit server 工作目录不一致导致图片/音频加载失败
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, 'images')
AUDIO_DIR = os.path.join(BASE_DIR, 'audio')


def get_local_image_path(bird):
    """获取本地图片路径（绝对路径）"""
    # 尝试两种格式：序号_名字.jpg 或 名字.jpg
    for filename in [f"{bird['id']:02d}_{bird['name']}.jpg", f"{bird['name']}.jpg"]:
        local_path = os.path.join(IMAGES_DIR, filename)
        if os.path.exists(local_path):
            return local_path
    return None


def get_local_audio_path(bird):
    """获取本地音频路径（绝对路径，优先从audio文件夹）"""
    name = bird['name']
    # 常见后缀变体
    suffixes = ["", "鸟"]
    base_names = []
    for suffix in suffixes:
        base_names.extend([
            os.path.join(AUDIO_DIR, f"{bird['id']:02d}_{name}{suffix}"),
            os.path.join(AUDIO_DIR, f"{name}{suffix}"),
            os.path.join(BASE_DIR, 'videos', f"{bird['id']:02d}_{name}{suffix}"),
            os.path.join(BASE_DIR, 'videos', f"{name}{suffix}"),
        ])
    extensions = ['.mp3', '.mp4']
    for base in base_names:
        for ext in extensions:
            path = f"{base}{ext}"
            if os.path.exists(path):
                return path
    return None


# 页面配置
st.set_page_config(
    page_title="苏州鸟类图谱",
    page_icon="🦅",
    layout="wide"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .bird-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #4CAF50;
        cursor: pointer;
        transition: all 0.3s;
    }
    .bird-card:hover {
        background-color: #E8F5E9;
        transform: translateX(5px);
    }
    .bird-name {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1B5E20;
    }
    .pinyin {
        color: #888;
        font-size: 0.9rem;
    }
    .pinyin-char {
        color: #888;
        font-size: 0.9rem;
        display: inline-block;
        min-width: 2.5rem;
        text-align: center;
    }
    .char {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1B5E20;
        display: inline-block;
        min-width: 2.5rem;
        text-align: center;
    }
    .bird-name-space {
        display: inline-block;
        min-width: 3rem;
    }
    .scientific-name {
        font-style: italic;
        color: #666;
        font-size: 0.9rem;
    }
    .info-tag {
        display: inline-block;
        background-color: #E8F5E9;
        color: #2E7D32;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        margin-right: 0.3rem;
        font-size: 0.8rem;
    }
    .song-box {
        background-color: #FFF8E1;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
    }
    .song-phonetic {
        font-size: 1.3rem;
        color: #E65100;
        font-weight: bold;
    }
    .placeholder-img {
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        border-radius: 10px;
        height: 120px;
        font-size: 3rem;
    }
    .detail-img {
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        border-radius: 10px;
        height: 300px;
        font-size: 6rem;
    }
    /* 首页"今日鸟种 / 听音识鸟"统一卡片 */
    .feature-card {
        background: linear-gradient(135deg, #F1F8E9 0%, #DCEDC8 100%);
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.10);
        border-left: 4px solid #66BB6A;
        height: 100%;
    }
    .feature-card h3 {
        margin-top: 0;
        color: #1B5E20;
    }
    /* 趣味知识卡 */
    .fact-card {
        background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%);
        border-radius: 14px;
        padding: 1.2rem 1.6rem;
        box-shadow: 0 2px 8px rgba(255, 152, 0, 0.10);
        border-left: 4px solid #FFB300;
        font-size: 1.05rem;
        color: #5D4037;
    }
    /* 推箱子彩蛋页鸟类卡 */
    .rescue-card {
        background: #F1F8E9;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        text-align: center;
        transition: transform 0.25s, box-shadow 0.25s;
    }
    .rescue-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.18);
    }
    /* 详情页英雄头 */
    .detail-hero {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(76, 175, 80, 0.12);
    }
    /* 按钮全局 hover 提升 */
    .stButton > button {
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.12);
    }
</style>
""", unsafe_allow_html=True)


def display_card_list():
    """卡片列表页面 - 两列布局"""
    st.markdown('<div class="main-header">🦅 苏州鸟类图谱</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Suzhou Bird Atlas · 30种苏州常见鸟类</div>', unsafe_allow_html=True)
    
    # 筛选器
    with st.sidebar:
        st.title("🔍 筛选")
        
        categories = ["全部"] + sorted(list(set(b['category'] for b in BIRDS_DATA)))
        selected_category = st.selectbox("按目分类", categories)
        
        seasons = ["全部"] + sorted(list(set(b['season'] for b in BIRDS_DATA)))
        selected_season = st.selectbox("按居留类型", seasons)
        
        levels = ["全部", "三有保护动物", "省重点保护动物"]
        selected_level = st.selectbox("按保护级别", levels)
        
        common_levels = ["全部", "★★★★★", "★★★★", "★★★", "★★"]
        selected_common = st.selectbox("按常见程度", common_levels)
        
        search = st.text_input("🔎 搜索", "")
    
    # 筛选数据
    filtered_birds = BIRDS_DATA
    
    if selected_category != "全部":
        filtered_birds = [b for b in filtered_birds if b['category'] == selected_category]
    
    if selected_season != "全部":
        filtered_birds = [b for b in filtered_birds if b['season'] == selected_season]
    
    if selected_level != "全部":
        filtered_birds = [b for b in filtered_birds if b['conservation_level'] == selected_level]
    
    if selected_common != "全部":
        filtered_birds = [b for b in filtered_birds if b['common_level'] == selected_common]
    
    if search:
        filtered_birds = [b for b in filtered_birds 
                        if search.lower() in b['name'].lower() 
                        or search.lower() in b['scientific_name'].lower()]
    
    st.markdown(f"**共 {len(filtered_birds)} 种鸟类**")
    st.markdown("---")

    # 响应式布局：电脑端用两列，手机端自动堆叠为单列
    # 通过判断屏幕宽度在 CSS 中隐藏/显示列；这里用单一容器 + 卡片流式排版，确保窄屏顺序为 1,2,3...
    use_two_cols = True
    try:
        # Streamlit 没有直接获取客户端宽度的接口，但可以用 JS 注入检测后存到 session_state
        # 简化方案：使用 CSS 让两列在窄屏自动堆叠为单列，保证渲染顺序
        st.markdown("""
        <style>
        @media (max-width: 768px) {
            .bird-card-row { flex-direction: column !important; }
            .bird-card-row > div { width: 100% !important; }
        }
        </style>
        """, unsafe_allow_html=True)
    except Exception:
        pass

    # 使用 1 列垂直流式排版，避免 i%2 在窄屏下出现 1,3,5,7,9 跳序
    # 电脑端用 CSS 模拟两列
    cards_html_parts = []
    for i, bird in enumerate(filtered_birds):
        img_path = get_local_image_path(bird)
        img_html = ""
        if img_path:
            # 使用 file:// 绝对路径
            img_html = f'<img src="file:///{img_path.replace(chr(92), "/")}" style="width:100%;border-radius:8px;" />'
        else:
            img_html = '<div class="placeholder-img" style="font-size:3rem;text-align:center;">🐦</div>'

        card_html = f"""
        <div class="bird-card" style="margin-bottom:14px;padding:14px;border-radius:12px;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.06);">
            <div class="bird-card-row" style="display:flex;gap:12px;align-items:flex-start;">
                <div style="flex:1.5;min-width:0;">
                    <div style="color:#888;font-size:0.85rem;">{bird.get('pinyin', '')}</div>
                    <div style="font-size:1.15rem;font-weight:700;color:#222;">{bird['id']}. {bird['name']}</div>
                    <div style="font-style:italic;color:#666;font-size:0.85rem;">{bird['scientific_name']}</div>
                    <div style="margin-top:6px;">
                        <span class="info-tag" style="background:#f0f4f8;padding:2px 8px;border-radius:10px;font-size:0.78rem;color:#456;margin-right:4px;">{bird['category']}</span>
                        <span class="info-tag" style="background:#f0f4f8;padding:2px 8px;border-radius:10px;font-size:0.78rem;color:#456;margin-right:4px;">{bird['season']}</span>
                        <span class="info-tag" style="background:#f0f4f8;padding:2px 8px;border-radius:10px;font-size:0.78rem;color:#456;">{bird['conservation_level']}</span>
                    </div>
                    <div style="color:#FFB300;font-size:1rem;margin-top:4px;">{bird.get('common_level', '')}</div>
                </div>
                <div style="flex:1;min-width:0;">{img_html}</div>
            </div>
        </div>
        """
        cards_html_parts.append(card_html)

    # 电脑端两列布局
    pc_html = ""
    for i in range(0, len(cards_html_parts), 2):
        left = cards_html_parts[i]
        right = cards_html_parts[i+1] if i+1 < len(cards_html_parts) else '<div></div>'
        pc_html += f"""
        <div style="display:flex;gap:14px;margin-bottom:14px;">
            <div style="flex:1;min-width:0;">{left}</div>
            <div style="flex:1;min-width:0;">{right}</div>
        </div>
        """

    # 注入响应式 CSS
    st.markdown(f"""
    <style>
    .bird-grid-pc {{ display: block; }}
    .bird-grid-mobile {{ display: none; }}
    @media (max-width: 768px) {{
        .bird-grid-pc {{ display: none; }}
        .bird-grid-mobile {{ display: block; }}
    }}
    </style>
    <div class="bird-grid-pc">{pc_html}</div>
    <div class="bird-grid-mobile">{''.join(cards_html_parts)}</div>
    """, unsafe_allow_html=True)

    # 详情按钮（必须用 streamlit widget，放在卡片下方）
    # 电脑端 2 列，手机端 1 列
    if use_two_cols:
        for i, bird in enumerate(filtered_birds):
            cols_btn = st.columns(2)
            with cols_btn[i % 2]:
                if st.button(f"查看详情 · {bird['id']}. {bird['name']}", key=f"btn_{bird['id']}", use_container_width=True):
                    st.session_state['selected_bird'] = bird
                    st.rerun()


def display_detail_page(bird):
    """详情页面"""
    
    # 滚动到顶部
    st.markdown("""
        <script>
            window.parent.scrollTo(0, 0);
            document.body.scrollTop = 0;
            document.documentElement.scrollTop = 0;
        </script>
    """, unsafe_allow_html=True)
    
    # 返回按钮
    if st.button("← 返回列表"):
        st.session_state['selected_bird'] = None
        st.rerun()
    
    st.markdown("---")
    
    # 大图
    img_path = get_local_image_path(bird)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if img_path:
            st.image(img_path, width=550)
        else:
            st.markdown('<div class="detail-img">🐦</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<div style='font-size:2.5rem;font-weight:bold;color:#1B5E20'>{bird['name']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:1.1rem;color:#888'>{bird.get('pinyin', '')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:1.3rem;font-style:italic;color:#666'>{bird['scientific_name']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:1.1rem;color:#666'>{bird['english_name']}</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**目**")
            st.write(bird['category'])
            st.markdown("**科**")
            st.write(bird['family'])
        with col_b:
            st.markdown("**居留类型**")
            st.write(bird['season'])
            st.markdown("**保护级别**")
            st.write(bird['conservation_level'])
        
        st.markdown(f"**常见程度** {bird['common_level']}")
        st.markdown(f"**栖息地** {bird['habitat']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 描述
    st.markdown("### 📝 物种描述")
    st.write(bird['description'])
    
    # 鸣声信息
    st.markdown("### 🎵 鸣声")
    if bird.get('song'):
        st.write(f"*{bird['song']}*")
    
    # 音频
    audio_path = get_local_audio_path(bird)
    if audio_path:
        st.audio(audio_path)
        st.success("已加载本地音频")
    
    st.markdown("---")
    st.caption("数据来源：苏州常见鸟类整理 · 非商用")


def _game_sokoban():
    """推箱子·救小鸟 - 纯 HTML+JS 实现，移动零延迟零闪烁"""
    # 4 关难度递增，每关独有设计理念，地图紧凑、步数合理
    levels = [
        {
            # 第1关 - 入门：1箱直推，3步搞定
            "name": "第1关：初识推箱",
            "intro_bird_ids": [1],
            "map": [
                "#####",
                "# . #",
                "# $ #",
                "# @ #",
                "#####"
            ]
        },
        {
            # 第2关 - 绕墙：1箱需从右侧绕过小墙，7步左右
            "name": "第2关：绕墙救援",
            "intro_bird_ids": [2],
            "map": [
                "#######",
                "#    .#",
                "# ##  #",
                "#     #",
                "#  $  #",
                "#  @  #",
                "#######"
            ]
        },
        {
            # 第3关 - 双箱绕行：两个箱子都需绕墙，约25步（BFS验证可解）
            "name": "第3关：双箱绕行",
            "intro_bird_ids": [3, 4],
            "map": [
                "#########",
                "# .   . #",
                "# # ##  #",
                "#       #",
                "# $   $ #",
                "#   @   #",
                "#########"
            ]
        },
        {
            # 第4关 - 3箱错位墙：3个箱子需协调穿越"## # # #"墙到目标，约33步（BFS验证可解）
            "name": "第4关：3箱错位",
            "intro_bird_ids": [1, 2, 3, 4],
            "map": [
                "#########",
                "# . . . #",
                "# ## # # #",
                "#       #",
                "# $ $ $ #",
                "#   @   #",
                "#########"
            ]
        }
    ]

    if 'sk_level' not in st.session_state:
        st.session_state['sk_level'] = 0
    if 'sk_show_birds' not in st.session_state:
        st.session_state['sk_show_birds'] = False

    level_idx = st.session_state['sk_level']

    if level_idx >= len(levels):
        st.success("🎉 恭喜通关！你成功解救了所有小鸟！")
        st.balloons()
        if st.button("🔄 重新挑战", key="sk_replay"):
            st.session_state['sk_level'] = 0
            st.session_state['sk_show_birds'] = False
            st.rerun()
        return

    import json
    level = levels[level_idx]
    level_map = level['map']
    level_name = level['name']
    bird_ids = level.get('intro_bird_ids', [])
    total_boxes = sum(row.count('$') + row.count('*') for row in level_map)
    max_cols = max(len(r) for r in level_map)
    rows = len(level_map)

    # 动态计算 iframe 高度
    iframe_height = 240 + rows * 60 + 120  # 信息条 + 网格 + 控件 + 提示消息

    st.markdown(f"### 📦 推箱子·救小鸟 · {level_name}")
    st.write("用方向键移动 🧒，把鸟笼 📦 推到鸟巢 🪺，解救被困的小鸟！")

    import streamlit.components.v1 as components

    # 重玩计数器：注入到 HTML 中保证每次重玩时 iframe 内容变化，浏览器必须重新加载
    # 注意：key 必须与 button 的 key 区分开，否则 Streamlit 会报 "cannot be modified after the widget" 错误
    reset_token = st.session_state.get(f'sk_replay_n_{level_idx}', 0)

    game_html = f"""
<!DOCTYPE html>
<html>
<head>
<!-- reset_token={reset_token} -->
<style>
  body {{
    margin: 0;
    padding: 8px;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    background: transparent;
  }}
  #sk-info {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 16px;
    font-weight: bold;
    flex-wrap: wrap;
    gap: 8px;
  }}
  #sk-grid {{
    display: grid;
    gap: 3px;
    background: #bcaaa4;
    padding: 6px;
    border-radius: 8px;
    width: fit-content;
    margin: 0 auto;
  }}
  .sk-cell {{
    width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    border-radius: 6px;
    user-select: none;
  }}
  .sk-wall {{ background: #6d4c41; }}
  .sk-floor {{ background: #f1f8e9; }}
  .sk-target {{ background: #fff59d; }}
  .sk-box {{ background: #ffab91; }}
  .sk-box-on {{ background: #a5d6a7; }}
  .sk-player {{ background: #ffcc80; }}
  #sk-controls {{
    display: grid;
    grid-template-columns: 60px 60px 60px;
    grid-template-rows: 60px 60px;
    gap: 6px;
    margin: 16px auto 0;
    width: fit-content;
  }}
  .sk-btn {{
    background: #43a047;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 28px;
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  }}
  .sk-btn:hover {{ background: #388e3c; }}
  .sk-btn:active {{ background: #2e7d32; transform: translateY(1px); }}
  #sk-msg {{
    color: #2E7D32;
    font-weight: bold;
    margin-top: 12px;
    text-align: center;
    font-size: 18px;
    min-height: 24px;
  }}
</style>
</head>
<body>
<div id="sk-info">
  <span>🎯 第 {level_idx + 1} 关</span>
  <span>🚶 移动：<span id="sk-moves">0</span></span>
  <span>📦 目标：<span id="sk-done">0</span> / {total_boxes}</span>
</div>
<div id="sk-grid"></div>
<div id="sk-controls">
  <div></div>
  <button class="sk-btn" id="btn-up">⬆️</button>
  <div></div>
  <button class="sk-btn" id="btn-left">⬅️</button>
  <button class="sk-btn" id="btn-down">⬇️</button>
  <button class="sk-btn" id="btn-right">➡️</button>
</div>
<div id="sk-msg"></div>

<script>
(function() {{
  const MAP_STR = {json.dumps(level_map)};
  const LEVEL_IDX = {level_idx};
  const TOTAL_BOXES = {total_boxes};

  let walls = new Set();
  let targets = new Set();
  let boxes = new Set();
  let player = null;
  let moves = 0;
  let won = false;

  function posKey(r, c) {{ return r + ',' + c; }}

  for (let r = 0; r < MAP_STR.length; r++) {{
    for (let c = 0; c < MAP_STR[r].length; c++) {{
      const ch = MAP_STR[r][c];
      if (ch === '#') walls.add(posKey(r, c));
      else if (ch === '.') targets.add(posKey(r, c));
      else if (ch === '$') boxes.add(posKey(r, c));
      else if (ch === '@') player = posKey(r, c);
      else if (ch === '*') {{ boxes.add(posKey(r, c)); targets.add(posKey(r, c)); }}
      else if (ch === '+') {{ player = posKey(r, c); targets.add(posKey(r, c)); }}
    }}
  }}

  function render() {{
    const grid = document.getElementById('sk-grid');
    const rows = MAP_STR.length;
    const cols = Math.max(...MAP_STR.map(r => r.length));
    grid.style.gridTemplateColumns = 'repeat(' + cols + ', 56px)';

    let html = '';
    for (let r = 0; r < rows; r++) {{
      for (let c = 0; c < cols; c++) {{
        const k = posKey(r, c);
        let cls = 'sk-floor';
        let emoji = '　';
        if (walls.has(k)) {{ cls = 'sk-wall'; emoji = '🟫'; }}
        else if (player === k) {{ cls = 'sk-player'; emoji = '🧒'; }}
        else if (boxes.has(k)) {{
          if (targets.has(k)) {{ cls = 'sk-box-on'; emoji = '🎁'; }}
          else {{ cls = 'sk-box'; emoji = '📦'; }}
        }}
        else if (targets.has(k)) {{ cls = 'sk-target'; emoji = '🪺'; }}
        html += '<div class="sk-cell ' + cls + '">' + emoji + '</div>';
      }}
    }}
    grid.innerHTML = html;
    document.getElementById('sk-moves').textContent = moves;
    document.getElementById('sk-done').textContent = countDone();
  }}

  function countDone() {{
    let n = 0;
    boxes.forEach(b => {{ if (targets.has(b)) n++; }});
    return n;
  }}

  function move(dr, dc) {{
    if (won) return;
    const [pr, pc] = player.split(',').map(Number);
    const nr = pr + dr, nc = pc + dc;
    const nk = posKey(nr, nc);
    if (walls.has(nk)) return;
    if (boxes.has(nk)) {{
      const bk = posKey(nr + dr, nc + dc);
      if (walls.has(bk) || boxes.has(bk)) return;
      boxes.delete(nk);
      boxes.add(bk);
    }}
    player = nk;
    moves++;
    render();
    if (countDone() === TOTAL_BOXES) {{
      won = true;
      document.getElementById('sk-msg').innerHTML =
        '🎉 通关！用了 ' + moves + ' 步！';
    }}
  }}

  document.getElementById('btn-up').onclick = () => move(-1, 0);
  document.getElementById('btn-down').onclick = () => move(1, 0);
  document.getElementById('btn-left').onclick = () => move(0, -1);
  document.getElementById('btn-right').onclick = () => move(0, 1);

  document.addEventListener('keydown', (e) => {{
    if (won) return;
    if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') {{ e.preventDefault(); move(-1, 0); }}
    else if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') {{ e.preventDefault(); move(1, 0); }}
    else if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') {{ e.preventDefault(); move(0, -1); }}
    else if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') {{ e.preventDefault(); move(0, 1); }}
  }});

  render();
}})();
</script>
</body>
</html>
"""
    # 用 iframe 渲染，动态高度
    components.html(game_html, height=iframe_height, scrolling=False)

    # 玩家自主选择：通关判定由 iframe 内部 JS 完成，玩家点按钮决定下一步
    if not st.session_state.get('sk_show_birds'):
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 重玩本关", key=f"sk_reset_{level_idx}", use_container_width=True):
                st.session_state[f'sk_replay_n_{level_idx}'] = reset_token + 1
                st.rerun()
        with c2:
            if st.button("➡️ 下一关", key=f"sk_next_{level_idx}", type="primary", use_container_width=True):
                st.session_state['sk_show_birds'] = True
                st.rerun()
    else:
        # 彩蛋页面 - 展示本关救出的鸟类
        st.markdown("---")
        st.markdown(f"## 🎉 恭喜通过第 {level_idx + 1} 关！")
        st.markdown(f"### 🐦 成功救出 {len(bird_ids)} 只小鸟！")
        st.balloons()

        cols = st.columns(min(3, len(bird_ids)))
        for i, bid in enumerate(bird_ids):
            bird = next((b for b in BIRDS_DATA if b['id'] == bid), None)
            if not bird:
                continue
            with cols[i % len(cols)]:
                st.markdown('<div class="rescue-card">', unsafe_allow_html=True)
                st.markdown(f"#### {bird['name']}")
                st.markdown(f"*{bird.get('pinyin', '')}*")
                img = get_local_image_path(bird)
                if img:
                    st.image(img, use_container_width=True)
                else:
                    st.markdown('<div style="font-size:5rem;text-align:center">🐦</div>',
                                unsafe_allow_html=True)
                st.caption(f"_{bird['scientific_name']}_")
                st.caption(f"📍 {bird.get('habitat', '')}")
                with st.expander("📖 详细介绍"):
                    st.write(bird['description'])
                    if bird.get('song'):
                        st.info(f"🎵 鸣声：{bird['song']}")
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if level_idx < len(levels) - 1:
                if st.button("➡️ 进入下一关", key=f"sk_advance_{level_idx}", type="primary", use_container_width=True):
                    st.session_state['sk_level'] = level_idx + 1
                    st.session_state['sk_show_birds'] = False
                    st.rerun()
            else:
                st.markdown("## 🌟 你是真正的鸟类守护者！")
                if st.button("🔄 重新挑战全部关卡", key="sk_replay_all", use_container_width=True):
                    st.session_state['sk_level'] = 0
                    st.session_state['sk_show_birds'] = False
                    st.rerun()

    st.caption(f"💡 把 {total_boxes} 个 📦 全部推到 🪺 上即过关 · 鼠标点击按钮或键盘方向键均可控制")


def display_games_page():
    """游戏页面"""
    import random

    st.markdown("## 🕹️ 趣味游戏")
    st.caption("在游戏中认识鸟类 · 边玩边学")

    # 手机端友好的游戏选择：4 个大按钮卡片（电脑端 4 列 / 手机端 2x2）
    if 'home_game' in st.session_state and st.session_state['home_game']:
        # 从首页点进来时直接锁定游戏
        game_key_map = {
            "qimg": "🎨 看图猜鸟",
            "qaudio": "🎵 听音识鸟",
            "qkb": "❓ 知识问答",
            "qbox": "📦 推箱子·救小鸟",
        }
        game = game_key_map.get(st.session_state['home_game'], "🎨 看图猜鸟")
        st.session_state.pop('home_game', None)
        st.session_state['sk_current_game'] = game
    elif 'sk_current_game' not in st.session_state:
        st.session_state['sk_current_game'] = "🎨 看图猜鸟"

    game = st.session_state['sk_current_game']

    # 顶部游戏切换按钮（4 列，电脑端横排 / 手机端 2x2）
    games_list = [
        ("🎨", "看图猜鸟", "qimg"),
        ("🎵", "听音识鸟", "qaudio"),
        ("❓", "知识问答", "qkb"),
        ("📦", "推箱子·救小鸟", "qbox"),
    ]
    nav_cols = st.columns(4)
    for i, (icon, name, key) in enumerate(games_list):
        with nav_cols[i % 4]:
            is_active = (game == f"{icon} {name}")
            bg = "linear-gradient(135deg,#ffb74d,#ff9800)" if is_active else "linear-gradient(135deg,#f5f5f5,#e0e0e0)"
            color = "#fff" if is_active else "#5d4037"
            st.markdown(f"""
            <div style="background:{bg};padding:12px 6px;border-radius:10px;text-align:center;
                        box-shadow:0 2px 6px rgba(0,0,0,0.08);margin-bottom:6px;color:{color};
                        font-weight:600;min-height:50px;display:flex;align-items:center;justify-content:center;">
                <span style="font-size:1.4rem;margin-right:4px;">{icon}</span>{name}
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"切换到{name}", key=f"nav_{key}", use_container_width=True):
                st.session_state['sk_current_game'] = f"{icon} {name}"
                st.rerun()

    st.markdown("---")
    
    if game == "🎨 看图猜鸟":
        st.markdown("### 🎨 看图猜鸟")
        st.write("根据图片猜猜这是什么鸟？")
        
        # 只选有实际图片的鸟（保证一定有图）
        birds_with_img = [b for b in BIRDS_DATA if get_local_image_path(b)]
        
        # 初始化/换题
        if 'qimg_bird' not in st.session_state or st.session_state.get('qimg_new'):
            quiz_bird = random.choice(birds_with_img)
            options = [quiz_bird['name']]
            other_birds = [b for b in birds_with_img if b['id'] != quiz_bird['id']]
            wrong_options = random.sample(other_birds, min(3, len(other_birds)))
            options.extend([b['name'] for b in wrong_options])
            random.shuffle(options)
            st.session_state['qimg_bird'] = quiz_bird
            st.session_state['qimg_options'] = options
            st.session_state['qimg_answered'] = False
            st.session_state['qimg_user'] = None
            st.session_state['qimg_score'] = st.session_state.get('qimg_score', 0)
            st.session_state['qimg_total'] = st.session_state.get('qimg_total', 0)
            st.session_state['qimg_new'] = False
        
        quiz_bird = st.session_state['qimg_bird']
        options = st.session_state['qimg_options']
        answered = st.session_state['qimg_answered']
        user_ans = st.session_state['qimg_user']
        correct = quiz_bird['name']
        
        st.write(f"**得分：{st.session_state['qimg_score']} / {st.session_state['qimg_total']}**")
        
        # 已过滤，quiz_bird 一定有图片
        st.image(get_local_image_path(quiz_bird), width=350)
        
        if not answered:
            # 答题中
            selected = st.radio("你的答案：", options, index=None, key="qimg_radio")
            if selected:
                st.session_state['qimg_answered'] = True
                st.session_state['qimg_user'] = selected
                st.session_state['qimg_total'] += 1
                if selected == correct:
                    st.session_state['qimg_score'] += 1
                st.rerun()
        else:
            # 已答：显示对错 + 下一题
            if user_ans == correct:
                st.success(f"🎉 回答正确！这就是 **{correct}**（{quiz_bird.get('pinyin', '')}）")
            else:
                st.error(f"❌ 回答错误！")
                st.info(f"你的答案：**{user_ans}**　✅ 正确答案：**{correct}**（{quiz_bird.get('pinyin', '')}）")
            
            st.markdown("**📖 鸟种介绍：**")
            st.write(f"*{quiz_bird['scientific_name']}*　{quiz_bird.get('english_name', '')}")
            st.write(quiz_bird['description'])
            
            if st.button("➡️ 下一题", key="qimg_next", use_container_width=True):
                st.session_state['qimg_new'] = True
                st.rerun()
    
    elif game == "🎵 听音识鸟":
        st.markdown("### 🎵 听音识鸟")
        st.write("听音频，猜猜是哪只鸟？")
        
        # 只选有实际音频文件的鸟
        birds_with_audio = [b for b in BIRDS_DATA if get_local_audio_path(b)]
        
        if 'qaud_bird' not in st.session_state or st.session_state.get('qaud_new'):
            quiz_bird = random.choice(birds_with_audio)
            options = [quiz_bird['name']]
            other_birds = [b for b in birds_with_audio if b['id'] != quiz_bird['id']]
            wrong_options = random.sample(other_birds, min(3, len(other_birds)))
            options.extend([b['name'] for b in wrong_options])
            random.shuffle(options)
            st.session_state['qaud_bird'] = quiz_bird
            st.session_state['qaud_options'] = options
            st.session_state['qaud_answered'] = False
            st.session_state['qaud_user'] = None
            st.session_state['qaud_score'] = st.session_state.get('qaud_score', 0)
            st.session_state['qaud_total'] = st.session_state.get('qaud_total', 0)
            st.session_state['qaud_new'] = False
        
        quiz_bird = st.session_state['qaud_bird']
        options = st.session_state['qaud_options']
        answered = st.session_state['qaud_answered']
        user_ans = st.session_state['qaud_user']
        correct = quiz_bird['name']
        
        st.write(f"**得分：{st.session_state['qaud_score']} / {st.session_state['qaud_total']}**")
        
        # 音频（已过滤过，quiz_bird 一定有音频）
        audio_path = get_local_audio_path(quiz_bird)
        st.audio(audio_path)
        
        if not answered:
            selected = st.radio("你的答案：", options, index=None, key="qaud_radio")
            if selected:
                st.session_state['qaud_answered'] = True
                st.session_state['qaud_user'] = selected
                st.session_state['qaud_total'] += 1
                if selected == correct:
                    st.session_state['qaud_score'] += 1
                st.rerun()
        else:
            if user_ans == correct:
                st.success(f"🎉 回答正确！这就是 **{correct}**（{quiz_bird.get('pinyin', '')}）")
            else:
                st.error(f"❌ 回答错误！")
                st.info(f"你的答案：**{user_ans}**　✅ 正确答案：**{correct}**（{quiz_bird.get('pinyin', '')}）")
            
            st.markdown("**📖 鸟种介绍：**")
            st.write(f"*{quiz_bird['scientific_name']}*　{quiz_bird.get('english_name', '')}")
            st.write(quiz_bird['description'])
            if quiz_bird.get('song'):
                st.info(f"🎵 鸣声：{quiz_bird['song']}")
            
            if st.button("➡️ 下一题", key="qaud_next", use_container_width=True):
                st.session_state['qaud_new'] = True
                st.rerun()
    
    elif game == "❓ 知识问答":
        st.markdown("### ❓ 知识问答")
        st.caption("🌟 趣味冷知识 · 那些你可能不知道的鸟类秘密…")

        # 趣味冷知识题库
        TRIVIA_POOL = [
            {
                'q': '哪种鸟的名字里含有数字，但它的“珍珠”项链其实是一簇羽毛？',
                'options': ['珠颈斑鸠', '白头鹎', '麻雀', '灰喜鹊'],
                'a': 0,
                'explain': '珠颈斑鸠颈部黑白相间的斑点看起来像一串珍珠，但这是羽毛不是真的会掉的珠子！繁殖季过后这些羽毛会褪色。'
            },
            {
                'q': '白头鹎的“白头”是怎么来的？',
                'options': ['羽毛天生白色', '年龄越大头越白', '白色枕羽随年龄增长', '会换季变白'],
                'a': 2,
                'explain': '白头鹎小时候头部是橄榄绿色的，随着年龄增长，白色枕羽越来越多，老年个体几乎整头都是白的。所以看到白头特别多的，说明是只老鸟了！'
            },
            {
                'q': '哪种鸟头顶有一把可以“收起来”的羽冠，受惊时会像扇子一样展开？',
                'options': ['戴胜', '八哥', '凤头麦鸡', '灰喜鹊'],
                'a': 0,
                'explain': '戴胜头顶的羽冠平时折叠贴在头上，受到惊扰时会竖起展开，像一把精致的小扇子，因此得名「戴胜」（胜是古代的一种头饰）。'
            },
            {
                'q': '普通翠鸟的蓝色羽毛其实是什么颜色？',
                'options': ['结构色（物理折射）', '黑色素', '食物色素', '水质影响'],
                'a': 0,
                'explain': '翠鸟羽毛的蓝绿色其实是「结构色」——羽毛表面微结构让光线折射出蓝色，跟色素没关系。所以死去的翠鸟标本褪色后会变成灰白色！'
            },
            {
                'q': '哪种苏州常见的鸟腿部几乎是“透明”的，站立时看起来像踩着高跷？',
                'options': ['白鹭', '夜鹭', '苍鹭', '池鹭'],
                'a': 0,
                'explain': '白鹭的腿部油黑，但脚部黄绿色，远看腿部就像透明的一样，配合修长的脖颈，整体就像踩着高跷的芭蕾舞者。'
            },
            {
                'q': '哪种鸟能模仿汽车喇叭、手机铃声等非鸟类声音，掌握50种以上？',
                'options': ['八哥', '乌鸫', '画眉', '鹦鹉'],
                'a': 1,
                'explain': '乌鸫被称为「鸟中口技大师」，能模仿电锯、婴儿哭声、汽车鸣笛、手机铃声等，不仅模仿得像，还能连续变换50多种声音！比八哥还厉害。'
            },
            {
                'q': '哪种鸟飞行时会发出像直升机螺旋桨一样的“噗噗”声？',
                'options': ['珠颈斑鸠', '家鸽', '山斑鸠', '灰斑鸠'],
                'a': 0,
                'explain': '珠颈斑鸠翅膀结构特殊，飞行时翅膀扇动频率产生独特的噗噗声，很远就能听到，是识别它的好方法。'
            },
            {
                'q': '哪种鸟是目前唯一被确认具有自我意识的鸟类，能认出镜中的自己？',
                'options': ['喜鹊', '乌鸦', '鹦鹉', '鸽子'],
                'a': 0,
                'explain': '科学实验证明喜鹊能在镜子中认出自己（会在自己身上找标记而不是攻击镜子里的对手），这是自我意识的标志，连猫狗都做不到！'
            },
            {
                'q': '哪种鸟捕鱼时会先“脚搅水面”，利用鱼的趋光性？',
                'options': ['池鹭', '苍鹭', '白鹭', '翠鸟'],
                'a': 0,
                'explain': '池鹭会用脚轻轻搅动水面，水面波光粼粼会吸引附近小鱼的注意，等鱼游过来看热闹时就一口捕获——简直是鸟类版的钓鱼！'
            },
            {
                'q': '哪种鸟能一口气唱出20多种音调，持续数分钟不重复？',
                'options': ['画眉', '乌鸫', '百灵', '白头鹎'],
                'a': 0,
                'explain': '画眉是鸟类中的「歌唱家」，一场演唱会可以连续唱20多种不同旋律，有时长达数分钟，而且每只画眉都有自己的「原创曲目」。'
            },
            {
                'q': '哪种鸟在城市的路灯下守株待兔，等灯光吸引来的昆虫自投罗网？',
                'options': ['夜鹭', '白鹭', '池鹭', '苍鹭'],
                'a': 0,
                'explain': '夜鹭是夜行性鸟类，白天不太活跃，但晚上会在路灯、霓虹灯下等候，灯光吸引来大量飞虫，夜鹭就坐享其成——典型的借力打力！'
            },
            {
                'q': '哪种鸟记忆力惊人，会把食物藏在上千个不同地点，冬天还能记得80%以上？',
                'options': ['沼泽山雀', '麻雀', '灰喜鹊', '乌鸦'],
                'a': 0,
                'explain': '沼泽山雀（远东山雀）会在秋天分散藏食物于数千个地点，到冬天有80%以上的食物能准确找回，是鸟类中的「记忆冠军」。'
            },
            {
                'q': '哪种鸟的鸟巢入口开在侧面，而且巢穴有隧道式的“玄关”防蛇？',
                'options': ['翠鸟', '戴胜', '啄木鸟', '八哥'],
                'a': 0,
                'explain': '翠鸟在土坡上挖洞筑巢，入口是一个狭窄的圆孔，后面还有一段水平隧道，既方便自己进出，又能防止蛇类直接钻进巢里。'
            },
            {
                'q': '哪种鸟在中国是“留鸟”但在欧洲是“候鸟”？',
                'options': ['灰纹鹟', '乌鸫', '白头鹎', '麻雀'],
                'a': 0,
                'explain': '灰纹鹟在苏州是冬候鸟，但在欧洲它们是留鸟——同一物种在不同地区有不同的迁徙策略，非常有趣。'
            },
            {
                'q': '哪种鸟喜欢在荷花花心里筑巢，利用荷叶遮风挡雨？',
                'options': ['黑水鸡', '白鹭', '池鹭', '小鸊鷉'],
                'a': 0,
                'explain': '黑水鸡会把巢建在荷叶上或芦苇丛中，荷叶的弧度刚好能遮挡雨水，是个天然的「雨伞」——不过大雨时还是会被淋成落汤鸡。'
            },
            {
                'q': '哪种鸟是苏州人最熟悉的“邻居”，一年四季在院子里都能见到？',
                'options': ['白头鹎', '麻雀', '珠颈斑鸠', '灰喜鹊'],
                'a': 0,
                'explain': '白头鹎被苏州人称为「白头翁」，性格活泼不怕人，常在庭院、公园的树冠层跳跃穿梭，是当之无愧的「苏州最亲民小鸟」。'
            },
            {
                'q': '哪种鸟会在春季集群形成壮观的“鸟浪”，几十只同时飞过天际？',
                'options': ['家燕', '白鹭', '麻雀', '灰喜鹊'],
                'a': 2,
                'explain': '麻雀在春季繁殖期后会形成大群，有时几十甚至上百只一起行动，飞过天空时像一道棕色的浪潮，非常壮观。'
            },
            {
                'q': '哪种鸟可以倒退飞行，还能悬停空中？',
                'options': ['雨燕', '家燕', '燕子', '楼燕'],
                'a': 0,
                'explain': '雨燕几乎一生都在空中度过，能倒退飞行、悬停、急转弯，落地反而有困难——有的雨燕甚至睡觉时也在飞！'
            },
            {
                'q': '哪种鸟的鸟蛋颜色能反映出巢穴的健康状况，颜色越深蛋壳越厚？',
                'options': ['乌鸫', '麻雀', '白头鹎', '八哥'],
                'a': 0,
                'explain': '乌鸫的蛋是淡蓝绿色，研究发现生活在污染较轻区域的乌鸫，蛋的颜色更深、蛋壳更厚——蛋的颜色竟然能当环境指标！'
            },
            {
                'q': '哪种鸟的鸟巢用蜘蛛丝当“建筑胶水”，把苔藓、羽毛粘在一起？',
                'options': ['长尾缝叶莺', '白头鹎', '麻雀', '画眉'],
                'a': 0,
                'explain': '长尾缝叶莺会把大叶子缝在一起筑巢，它用喙当针、蜘蛛丝当线，把叶子边缘缝成一个小杯子，再填入柔软的苔藓和羽毛。'
            },
            {
                'q': '哪种鸟在城市里学会了“等红灯”，机动车停车时会到车底下找虫吃？',
                'options': ['乌鸦', '珠颈斑鸠', '麻雀', '灰喜鹊'],
                'a': 0,
                'explain': '城市里的乌鸦非常聪明，会在红灯时飞到车底下找昆虫，绿灯前及时飞走——有些城市的乌鸦甚至学会了把坚果丢到马路上让车压碎。'
            },
            {
                'q': '哪种鸟的雏鸟会“装死”，被捕食者触碰时直接四肢瘫软一动不动？',
                'options': ['珠颈斑鸠', '山麻雀', '麻雀', '白头鹎'],
                'a': 0,
                'explain': '珠颈斑鸠的雏鸟在受到惊扰时会表演「装死」，全身瘫软、心跳减缓，捕食者以为它死了往往就不吃了——这是生存智慧！'
            },
            {
                'q': '哪种苏州常见的鸟，冬季会在雪地上排成“一字阵”觅食？',
                'options': ['麻雀', '白头鹎', '燕雀', '灰喜鹊'],
                'a': 2,
                'explain': '燕雀冬季在苏州比较常见，它们觅食时会排成一字长蛇阵，边走边翻找食物，队伍可以拉得很长，像一条棕色的传送带。'
            },
            {
                'q': '哪种鸟的脚趾可以在水面上快速踩水，奔跑而不沉下去？',
                'options': ['小鸊鷉', '黑水鸡', '白鹭', '池鹭'],
                'a': 1,
                'explain': '黑水鸡的脚趾特别宽大，脚趾间还有瓣膜状结构，能把体重分散到很大的面积上，所以能在荷叶、浮萍上轻盈地奔跑而不沉下去。'
            },
            {
                'q': '哪种鸟有“森林医生”的称号，专门给树治病却从不收诊费？',
                'options': ['啄木鸟', '戴胜', '八哥', '灰喜鹊'],
                'a': 0,
                'explain': '啄木鸟每天敲击树木上千次，能吃掉树皮里的害虫，洞还能给其他鸟做巢，是真正的「森林医生」，而且完全免费义诊！'
            },
        ]

        # 题库缓存
        if 'qkb_pool' not in st.session_state or st.session_state.get('qkb_pool_reset'):
            st.session_state['qkb_pool'] = TRIVIA_POOL[:]
            random.shuffle(st.session_state['qkb_pool'])
            st.session_state['qkb_pool_reset'] = False

        questions = st.session_state['qkb_pool']

        if 'qkb_q' not in st.session_state or st.session_state.get('qkb_new'):
            q = random.choice(questions)
            st.session_state['qkb_q'] = q
            st.session_state['qkb_answered'] = False
            st.session_state['qkb_new'] = False

        q = st.session_state['qkb_q']
        st.markdown(f"**{q['q']}**")

        cols = st.columns(2)
        for i, opt in enumerate(q['options']):
            with cols[i % 2]:
                if st.button(f"  {opt}", key=f"qkb_opt_{i}", use_container_width=True):
                    st.session_state['qkb_answered'] = True
                    st.session_state['qkb_selected'] = i
                    if i == q['a']:
                        st.session_state['qkb_score'] = st.session_state.get('qkb_score', 0) + 1
                        st.success("✅ 回答正确！")
                    else:
                        st.error(f"❌ 回答错误，正确答案是：{q['options'][q['a']]}")

        if st.session_state.get('qkb_answered'):
            st.markdown(f"> 💡 {q['explain']}")
            if st.button("  下一题", key="qkb_next", use_container_width=True):
                st.session_state['qkb_new'] = True
                st.rerun()

            total = st.session_state.get('qkb_score', 0)
            st.info(f"🎯 本局得分：{total} / {len(TRIVIA_POOL)}")

        if st.button("  重新开始", key="qkb_restart", use_container_width=True):
            st.session_state['qkb_pool_reset'] = True
            st.session_state['qkb_score'] = 0
            st.session_state.pop('qkb_q', None)
            st.session_state.pop('qkb_answered', None)
            st.rerun()

    elif game == "📦 推箱子·救小鸟":
        _game_sokoban()


def main():
    # 页面选择：手机端通过首页"开始"按钮跳转，电脑端用侧边栏
    page = st.session_state.get('page') or st.sidebar.radio("页面导航", ["🏠 鸟类图谱", "🕹️ 趣味游戏"])
    # 同步给侧边栏（保证后续 rerun 时一致）
    st.session_state['page'] = page

    if page == "🕹️ 趣味游戏":
        display_games_page()
    else:
        # 鸟类图谱页面
        import random
        # 只从有图的鸟中选今日推荐
        birds_with_img = [b for b in BIRDS_DATA if get_local_image_path(b)]
        today_bird = random.choice(birds_with_img) if birds_with_img else random.choice(BIRDS_DATA)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown("### 🌟 今日鸟种")
            img_path = get_local_image_path(today_bird)
            st.image(img_path, width=280)
            st.markdown(f"**{today_bird['name']}**")
            st.markdown(f"*{today_bird.get('pinyin', '')}*")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown("### 🎯 听音识鸟")
            st.markdown("听音频，猜猜是哪只鸟？")

            # 只从有音频的鸟中选（保证一定可播放）
            birds_with_audio = [b for b in BIRDS_DATA if get_local_audio_path(b) and b['id'] != today_bird['id']]
            if not birds_with_audio:
                birds_with_audio = [b for b in BIRDS_DATA if get_local_audio_path(b)]
            quiz_bird = random.choice(birds_with_audio)
            audio_path = get_local_audio_path(quiz_bird)

            if audio_path:
                st.audio(audio_path)

            with st.expander("🔑 答案"):
                st.markdown(f"**{quiz_bird['name']}** - {quiz_bird.get('pinyin', '')}")
            st.markdown('</div>', unsafe_allow_html=True)

        # 手机端友好的游戏入口：4 个大按钮卡片，电脑端 4 列 / 手机端自动堆叠
        st.markdown("### 🎮 趣味游戏")
        st.caption("边玩边学，认识更多苏州鸟类")
        game_cards = [
            ("🎨", "看图猜鸟", "根据图片猜鸟种", "qimg"),
            ("🎵", "听音识鸟", "听声音认鸟种", "qaudio"),
            ("❓", "知识问答", "趣味鸟类冷知识", "qkb"),
            ("📦", "推箱子·救小鸟", "推箱子通关救鸟", "qbox"),
        ]
        # 电脑端 4 列
        gc_cols = st.columns(4)
        for i, (icon, title, desc, key) in enumerate(game_cards):
            with gc_cols[i % 4]:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#fff8e1,#ffe0b2);
                            padding:16px;border-radius:12px;text-align:center;
                            box-shadow:0 2px 6px rgba(0,0,0,0.08);
                            margin-bottom:8px;min-height:90px;">
                    <div style="font-size:2rem;">{icon}</div>
                    <div style="font-weight:700;color:#5d4037;margin-top:4px;">{title}</div>
                    <div style="font-size:0.78rem;color:#8d6e63;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"开始 · {title}", key=f"home_{key}", use_container_width=True):
                    st.session_state['page'] = "🕹️ 趣味游戏"
                    st.session_state['home_game'] = {
                        "🎨 看图猜鸟": "qimg", "🎵 听音识鸟": "qaudio",
                        "❓ 知识问答": "qkb", "📦 推箱子·救小鸟": "qbox"
                    }[title]
                    st.rerun()
        
        st.markdown('<div class="fact-card">', unsafe_allow_html=True)
        st.markdown("### 📚 趣味知识")
        facts = [
            "🐦 白头鹎会根据地域形成不同的方言，不同地区的白头鹎叫声有差异",
            "🦜 麻雀的寿命可达10年，比很多宠物都长寿",
            "🦆 八哥可以模仿人类说话，经过训练能说简单的词语",
            "🎵 乌鸫的歌声可达100种音调，是鸟类中的歌唱家",
            "🐔 珠颈斑鸠的叫声像咕咕咕，常被误认为是杜鹃",
            "🌿 鸟类的羽毛结构非常精密，帮助它们高效飞翔",
        ]
        fact = random.choice(facts)
        st.markdown(f"> {fact}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        if 'selected_bird' in st.session_state and st.session_state['selected_bird']:
            display_detail_page(st.session_state['selected_bird'])
        else:
            display_card_list()


main()
