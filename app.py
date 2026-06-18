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

    # 响应式布局：电脑端 2 列（用 st.columns），手机端用 CSS 让 columns 堆叠为 1 列
    # 保证渲染顺序永远是 1,2,3,4,5...（不会出现 1,3,5,7,9）
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            flex: 0 0 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
            width: 100% !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # 把所有鸟按 2 个一组划分（电脑端 2 列，手机端 CSS 堆叠为 1 列）
    # 关键：每只鸟的内部使用 st.columns(2) 排文字和图片 → 窄屏时被 CSS 强制堆叠
    for i in range(0, len(filtered_birds), 2):
        left_bird = filtered_birds[i]
        right_bird = filtered_birds[i + 1] if i + 1 < len(filtered_birds) else None
        cols = st.columns(2)
        for col, bird in zip(cols, [left_bird, right_bird]):
            if bird is None:
                continue
            with col:
                _render_bird_card(bird)


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
    # CSS 网格模板需要的列数和行数
    map_cols = max_cols
    map_rows = rows

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
    align-items: flex;
    justify-content: center;
    font-size: 32px;
    user-select: none;
    /* 关键：去掉圆角让格子连成整体 */
    border-radius: 0;
  }}
  #sk-grid {{
    display: grid;
    grid-template-columns: repeat({map_cols}, 56px);
    grid-template-rows: repeat({map_rows}, 56px);
    gap: 1px;
    background: #4e342e;            /* 缝隙颜色 = 墙体深色，让地图连成一片 */
    padding: 3px;
    border-radius: 10px;
    width: fit-content;
    margin: 12px auto 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
  }}
  .sk-wall {{ background: #6d4c41; }}
  .sk-floor {{ background: #f1f8e9; }}
  .sk-target {{ background: #fff59d; }}
  .sk-box {{ background: #ffab91; }}
  .sk-box-on {{ background: #66bb6a; }}      /* 箱子在目标上时用深绿，对比更强 */
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
  /* 响应式：窄屏（手机）自动缩小 - 保持 1px 缝隙让地图连贯 */
  @media (max-width: 420px) {{
    body {{ padding: 4px; }}
    #sk-info {{ font-size: 13px; }}
    #sk-grid {{
      grid-template-columns: repeat({map_cols}, 30px);
      grid-template-rows: repeat({map_rows}, 30px);
      gap: 1px;
      padding: 2px;
      border-radius: 6px;
    }}
    .sk-cell {{ width: 30px; height: 30px; font-size: 18px; }}
    #sk-controls {{
      grid-template-columns: 48px 48px 48px;
      grid-template-rows: 48px 48px;
      gap: 4px;
      margin: 10px auto 0;
    }}
    .sk-btn {{ font-size: 22px; border-radius: 6px; }}
    #sk-msg {{ font-size: 15px; margin-top: 8px; }}
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


def _render_bird_card(bird):
    """渲染单只鸟的卡片（streamlit 原生组件，无 HTML）"""
    with st.container(border=True):
        col_text, col_img = st.columns([1.5, 1])
        with col_text:
            st.caption(bird.get('pinyin', ''))
            st.markdown(f"**{bird['id']}. {bird['name']}**")
            st.caption(bird['scientific_name'])
            # 标签
            tag_html = (
                f"`{bird['category']}` `{bird['season']}` `{bird['conservation_level']}`"
            )
            st.markdown(tag_html)
            st.markdown(f"<span style='color:#FFB300'>{bird.get('common_level', '')}</span>", unsafe_allow_html=True)
        with col_img:
            img_path = get_local_image_path(bird)
            if img_path:
                st.image(img_path, use_container_width=True)
            else:
                st.markdown("<div style='text-align:center;font-size:3rem'>🐦</div>", unsafe_allow_html=True)
        if st.button(f"查看详情 · {bird['name']}", key=f"btn_{bird['id']}", use_container_width=True):
            st.session_state['selected_bird'] = bird
            st.rerun()


def display_games_page():
    """游戏页面 - 独立页面，电脑端 + 手机端均可用（左上角 « 进入）"""
    import random

    st.markdown("## 🕹️ 趣味游戏")
    st.caption("在游戏中认识鸟类 · 边玩边学")

    # 顶部游戏切换（4 列，电脑端横排 / 手机端 2x2）
    games_list = [
        ("🎨", "看图猜鸟", "qimg"),
        ("🎵", "听音识鸟", "qaudio"),
        ("❓", "知识问答", "qkb"),
        ("📦", "推箱子·救小鸟", "qbox"),
    ]
    if 'sk_current_game' not in st.session_state:
        st.session_state['sk_current_game'] = "🎨 看图猜鸟"
    game = st.session_state['sk_current_game']

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

    # 路由到对应游戏
    if game == "🎨 看图猜鸟":
        display_qimg_inline()
    elif game == "🎵 听音识鸟":
        display_qaudio_inline()
    elif game == "❓ 知识问答":
        display_qkb_inline()
    elif game == "📦 推箱子·救小鸟":
        display_qbox_inline()


def display_qimg_inline():
    """看图猜鸟 - 可在 expander 中内联调用"""
    import random
    st.markdown("**根据图片猜猜这是什么鸟？**")

    birds_with_img = [b for b in BIRDS_DATA if get_local_image_path(b)]
    if not birds_with_img:
        st.warning("暂无可用图片")
        return

    if 'qimg_bird' not in st.session_state or st.session_state.get('qimg_new'):
        quiz_bird = random.choice(birds_with_img)
        options = [quiz_bird['name']]
        other_birds = [b for b in birds_with_img if b['id'] != quiz_bird['id']]
        options.extend([b['name'] for b in random.sample(other_birds, min(3, len(other_birds)))])
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

    st.caption(f"得分：{st.session_state['qimg_score']} / {st.session_state['qimg_total']}")
    st.image(get_local_image_path(quiz_bird), width=300)

    if not answered:
        selected = st.radio("你的答案：", options, index=None, key="qimg_radio")
        if selected:
            st.session_state['qimg_answered'] = True
            st.session_state['qimg_user'] = selected
            st.session_state['qimg_total'] += 1
            if selected == correct:
                st.session_state['qimg_score'] += 1
            st.rerun()
    else:
        if user_ans == correct:
            st.success(f"🎉 正确！这就是 **{correct}**（{quiz_bird.get('pinyin', '')}）")
        else:
            st.error(f"❌ 错误！你的答案：**{user_ans}**　✅ 正确：**{correct}**")
        with st.expander("📖 鸟种介绍", expanded=True):
            st.write(f"*{quiz_bird['scientific_name']}*　{quiz_bird.get('english_name', '')}")
            st.write(quiz_bird['description'])
        if st.button("➡️ 下一题", key="qimg_next", use_container_width=True):
            st.session_state['qimg_new'] = True
            st.rerun()
    if st.button("🔄 重新开始", key="qimg_restart", use_container_width=True):
        for k in ['qimg_bird','qimg_options','qimg_answered','qimg_user','qimg_score','qimg_total','qimg_new']:
            st.session_state.pop(k, None)
        st.rerun()


def display_qaudio_inline():
    """听音识鸟 - 可在 expander 中内联调用"""
    import random
    st.markdown("**听音频，猜猜是哪只鸟？**")

    birds_with_audio = [b for b in BIRDS_DATA if get_local_audio_path(b)]
    if not birds_with_audio:
        st.warning("暂无可用音频")
        return

    if 'qaud_bird' not in st.session_state or st.session_state.get('qaud_new'):
        quiz_bird = random.choice(birds_with_audio)
        options = [quiz_bird['name']]
        other_birds = [b for b in birds_with_audio if b['id'] != quiz_bird['id']]
        options.extend([b['name'] for b in random.sample(other_birds, min(3, len(other_birds)))])
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

    st.caption(f"得分：{st.session_state['qaud_score']} / {st.session_state['qaud_total']}")
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
            st.success(f"🎉 正确！这就是 **{correct}**（{quiz_bird.get('pinyin', '')}）")
        else:
            st.error(f"❌ 错误！你的答案：**{user_ans}**　✅ 正确：**{correct}**")
        with st.expander("📖 鸟种介绍", expanded=True):
            st.write(f"*{quiz_bird['scientific_name']}*　{quiz_bird.get('english_name', '')}")
            st.write(quiz_bird['description'])
            if quiz_bird.get('song'):
                st.info(f"🎵 鸣声：{quiz_bird['song']}")
        if st.button("➡️ 下一题", key="qaud_next", use_container_width=True):
            st.session_state['qaud_new'] = True
            st.rerun()
    if st.button("🔄 重新开始", key="qaud_restart", use_container_width=True):
        for k in ['qaud_bird','qaud_options','qaud_answered','qaud_user','qaud_score','qaud_total','qaud_new']:
            st.session_state.pop(k, None)
        st.rerun()


def display_qkb_inline():
    """知识问答 - 可在 expander 中内联调用"""
    import random
    st.markdown("**🌟 趣味冷知识 · 那些你可能不知道的鸟类秘密…**")

    TRIVIA_POOL = [
        {'q': '哪种鸟的名字里含有数字，但它的"珍珠"项链其实是一簇羽毛？', 'options': ['珠颈斑鸠', '白头鹎', '麻雀', '灰喜鹊'], 'a': 0,
         'explain': '珠颈斑鸠颈部黑白相间的斑点看起来像一串珍珠，但这是羽毛不是真的会掉的珠子！繁殖季过后这些羽毛会褪色。'},
        {'q': '白头鹎的"白头"是怎么来的？', 'options': ['羽毛天生白色', '年龄越大头越白', '白色枕羽随年龄增长', '会换季变白'], 'a': 2,
         'explain': '白头鹎小时候头部是橄榄绿色的，随着年龄增长，白色枕羽越来越多，老年个体几乎整头都是白的。'},
        {'q': '哪种鸟头顶有一把可以"收起来"的羽冠，受惊时会像扇子一样展开？', 'options': ['戴胜', '八哥', '凤头麦鸡', '灰喜鹊'], 'a': 0,
         'explain': '戴胜头顶的羽冠平时折叠贴在头上，受到惊扰时会竖起展开，像一把精致的小扇子，因此得名「戴胜」。'},
        {'q': '普通翠鸟的蓝色羽毛其实是什么颜色？', 'options': ['结构色（物理折射）', '黑色素', '食物色素', '水质影响'], 'a': 0,
         'explain': '翠鸟羽毛的蓝绿色其实是「结构色」——羽毛表面微结构让光线折射出蓝色，跟色素没关系。死后的翠鸟标本会褪成灰白色。'},
        {'q': '哪种苏州常见的鸟腿部几乎是"透明"的，站立时看起来像踩着高跷？', 'options': ['白鹭', '夜鹭', '苍鹭', '池鹭'], 'a': 0,
         'explain': '白鹭的腿部油黑，但脚部黄绿色，远看腿部就像透明的一样，配合修长的脖颈，整体就像踩着高跷的芭蕾舞者。'},
        {'q': '哪种鸟能模仿汽车喇叭、手机铃声等非鸟类声音，掌握50种以上？', 'options': ['八哥', '乌鸫', '画眉', '鹦鹉'], 'a': 1,
         'explain': '乌鸫被称为「鸟中口技大师」，能模仿电锯、婴儿哭声、汽车鸣笛、手机铃声等，比八哥还厉害。'},
        {'q': '哪种鸟飞行时会发出像直升机螺旋桨一样的"噗噗"声？', 'options': ['珠颈斑鸠', '家鸽', '山斑鸠', '灰斑鸠'], 'a': 0,
         'explain': '珠颈斑鸠翅膀结构特殊，飞行时翅膀扇动频率产生独特的噗噗声，很远就能听到。'},
        {'q': '哪种鸟是目前唯一被确认具有自我意识的鸟类，能认出镜中的自己？', 'options': ['喜鹊', '乌鸦', '鹦鹉', '鸽子'], 'a': 0,
         'explain': '科学实验证明喜鹊能在镜子中认出自己（会在自己身上找标记而不是攻击镜子里的对手），连猫狗都做不到！'},
        {'q': '哪种鸟捕鱼时会先"脚搅水面"，利用鱼的趋光性？', 'options': ['池鹭', '苍鹭', '白鹭', '翠鸟'], 'a': 0,
         'explain': '池鹭会用脚轻轻搅动水面，水面波光粼粼会吸引附近小鱼的注意，等鱼游过来就一口捕获。'},
        {'q': '哪种鸟记忆力惊人，会把食物藏在上千个不同地点，冬天还能记得80%以上？', 'options': ['沼泽山雀', '麻雀', '灰喜鹊', '乌鸦'], 'a': 0,
         'explain': '沼泽山雀会在秋天分散藏食物于数千个地点，到冬天有80%以上能准确找回，是鸟类中的「记忆冠军」。'},
        {'q': '哪种鸟的鸟巢入口开在侧面，而且巢穴有隧道式的"玄关"防蛇？', 'options': ['翠鸟', '戴胜', '啄木鸟', '八哥'], 'a': 0,
         'explain': '翠鸟在土坡上挖洞筑巢，入口是一个狭窄的圆孔，后面还有一段水平隧道，既方便自己进出，又能防止蛇类直接钻进巢里。'},
        {'q': '哪种鸟喜欢在荷花花心里筑巢，利用荷叶遮风挡雨？', 'options': ['黑水鸡', '白鹭', '池鹭', '小鸊鷉'], 'a': 0,
         'explain': '黑水鸡会把巢建在荷叶上或芦苇丛中，荷叶的弧度刚好能遮挡雨水，是个天然的「雨伞」。'},
        {'q': '哪种鸟是苏州人最熟悉的"邻居"，一年四季在院子里都能见到？', 'options': ['白头鹎', '麻雀', '珠颈斑鸠', '灰喜鹊'], 'a': 0,
         'explain': '白头鹎被苏州人称为「白头翁」，性格活泼不怕人，是当之无愧的「苏州最亲民小鸟」。'},
        {'q': '哪种鸟的脚趾可以在水面上快速踩水，奔跑而不沉下去？', 'options': ['小鸊鷉', '黑水鸡', '白鹭', '池鹭'], 'a': 1,
         'explain': '黑水鸡的脚趾特别宽大，脚趾间还有瓣膜状结构，能把体重分散到很大的面积上，能在荷叶、浮萍上轻盈奔跑。'},
        {'q': '哪种鸟有"森林医生"的称号，专门给树治病却从不收诊费？', 'options': ['啄木鸟', '戴胜', '八哥', '灰喜鹊'], 'a': 0,
         'explain': '啄木鸟每天敲击树木上千次，能吃掉树皮里的害虫，洞还能给其他鸟做巢，是真正的「森林医生」。'},
    ]

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
        for k in ['qkb_q','qkb_answered','qkb_selected','qkb_new']:
            st.session_state.pop(k, None)
        st.rerun()


def display_qbox_inline():
    """推箱子 - 可在 expander 中内联调用"""
    _game_sokoban()


def main():
    # 页面选择：侧边栏（手机端点左上角 « 展开）
    page = st.sidebar.radio("页面导航", ["🏠 鸟类图谱", "🕹️ 趣味游戏"])

    if page == "🕹️ 趣味游戏":
        display_games_page()
        return

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

    # 手机端固定浮动提示：sidebar 折叠前就在屏幕左上角显示"游戏"入口
    st.markdown("""
    <style>
    .mobile-game-hint {
        display: none;
    }
    @media (max-width: 768px) {
        .mobile-game-hint {
            display: flex;
            align-items: center;
            gap: 4px;
            position: fixed;
            top: 14px;
            left: 68px;
            z-index: 9999;
            background: linear-gradient(135deg, #fff3e0, #ffe0b2);
            color: #5d4037;
            padding: 6px 12px;
            border-radius: 18px;
            font-size: 13px;
            font-weight: 700;
            box-shadow: 0 2px 6px rgba(0,0,0,0.18);
            pointer-events: none;
        }
    }
    </style>
    <div class="mobile-game-hint">
        <span style="font-size:1.15rem;">🎮</span>
        <span>点 <span style="color:#ff6f00;font-size:1.1rem;">«</span> 进游戏</span>
    </div>
    """, unsafe_allow_html=True)

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
