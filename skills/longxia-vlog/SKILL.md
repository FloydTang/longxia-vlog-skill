# 🦞 龙虾简单 Vlog Skill（longxia-vlog）

## 场景

学员参加龙虾线下课 → 在对话框发照片/视频素材给龙虾 → 龙虾问几个问题 → AI 自动生成完整定制视频 → 飞书发成片

**核心原则**：
- ❌ 不用固定模板
- ✅ **动态生成 index.html**：每个人的素材、文案、分镜都不一样
- ✅ 片头/片尾统一露出品牌：**半斤九两 · AI未来派 | 🦞AI升级之旅**
- ✅ 自动化流程：素材 → 文案 → TTS → 分镜 → HTML → 渲染 → 出片

---

## 环境要求

### 必备

```bash
# HyperFrames CLI（必须先安装）
npm install -g hyperframes@latest --ignore-scripts

# 验证
npx hyperframes --version        # ≥ 0.6.40
ffmpeg -version                  # 需 FFmpeg
google-chrome --version          # 需 Chrome（用于渲染）
```

### 初始化项目

```bash
mkdir -p ~/lobster-vlog/assets
cd ~/lobster-vlog
npx hyperframes init  # 生成 hyperframes.json
```

> 每个学员 = 一个独立项目目录，每个项目和别人的素材、文案、渲染结果互不干扰。

---

## 完整流程（Step by Step）

### Step 1：收素材

学员在对话框直接发照片/视频。龙虾下载到 `assets/`：

```bash
# 命名：按顺序 photo-1.jpg, photo-2.jpg, ...
# 视频：clip-1.mp4
# assets/ 下放的是这个学员的专属素材
```

### Step 2：问 5 个问题，生成文案

依次问学员（语气轻松自然，像聊天）：

1. **你叫什么名字？从哪里来？**
2. **这是第几次来？之前来过吗？**
3. **这次龙虾课最大的收获是什么？**
4. **学完你最想先用在哪？**
5. **对自己说一句什么？**

拿到回答 → 生成文案 JSON。**文案必须包含品牌露出**：

```json
{
  "scenes": [
    {
      "type": "opening",
      "narration": "开场配音",
      "caption": "主标题"
    },
    {
      "type": "photo",
      "narration": "书场评弹的配音",
      "caption": "古镇书场",
      "sub_caption": "琵琶声里，时光慢了下来"
    },
    {
      "type": "video",
      "narration": "旗袍试穿配音",
      "caption": "试了件旗袍",
      "sub_caption": "差点认不出自己"
    },
    {
      "type": "ending",
      "narration": "收尾配音，必须包含品牌信息",
      "branding": "AI未来派 | 🦞AI升级之旅",
      "cta": "半斤九两 · AI让外贸更简单"
    }
  ]
}
```

**文案风格指南**（已验证效果好的）：
- 一句话主文案 + 一句金句
- 金句要有记忆点：*"慢不是懒，是充电"*、*"谁说搞AI的不能有江南柔情"*
- 结尾固定：**AI未来派 | 🦞AI升级之旅**（可追加个性化文案）
- 片尾可加：**半斤九两 · AI让外贸更简单**

### Step 3：生成 TTS 配音

一段一段分别生成，方便计算分镜时长：

```bash
SKILL_DIR="/workspace/projects/workspace/skills/coze-voice-gen"
cd "$SKILL_DIR"

# 推荐声音：zh_female_jitangnv_saturn_bigtts（温暖激励女声）
# 语速：speech-rate 5（比默认快5%，更自然）

for i in {0..5}; do
  # 逐段生成
  npx ts-node scripts/tts.ts \
    --speaker zh_female_jitangnv_saturn_bigtts \
    --speech-rate 5 \
    --text "第${i}段配音文案"
done

# 下载到 assets/
curl -o ~/lobster-vlog/assets/voice-0.mp3 <URL>
```

### Step 4：获取/生成 BGM

```bash
# 方案A：用 Python 生成古风 BGM（免版权，时长可控）
python3 /workspace/projects/workspace/skills/longxia-vlog/scripts/generate-bgm.py ~/lobster-vlog/assets/

# 方案B：搜索免费 BGM
# 推荐 Pixabay Music / StockTune，CC0 授权
```

### Step 5：测量音频 → 计算分镜时间

```bash
cd ~/lobster-vlog

echo "=== 配音时长 ==="
TOTAL=0
starts=()
durs=()

for f in assets/voice-*.mp3; do
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  starts+=($TOTAL)
  durs+=($dur)
  printf "  %s: %.2fs (start=%.2f)\n" "$(basename $f)" "$dur" "$TOTAL"
  TOTAL=$(echo "$TOTAL + $dur" | bc)
done

echo ""
echo "视频总时长: ${TOTAL}s"

echo "=== BGM 时长 ==="
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/bgm.mp3
```

### Step 6：动态生成 index.html

这是核心步骤。基于学员的素材、文案、配音时长，**用代码动态拼装完整的 index.html**。

**必须处理的细节**：
1. 每段配音一个 `<audio>` 标签，`data-start` 累加计算
2. BGM 在 track 0，配音在 track 1
3. 照片场景在 track ≥ 2 递增
4. `<video>` 元素（如果有）必须放在根级，**不能嵌套**在 `data-start` 的 div 里
5. 字幕位置用 `bottom: 360-400px`（画面中间偏下），不要贴底
6. 开场/结尾要带科技感特效（网格、光晕环、扫描线），体现"AI"品牌调性

**生成脚本参考**（用 Python 或直接写 HTML）：

```python
# 伪代码：动态生成 index.html
scenes_html = ""
for i, scene in enumerate(scenes_data):
    start = scene['start']
    dur = scene['duration']
    if scene['type'] == 'opening':
        scenes_html += render_opening(start, dur, scene)
    elif scene['type'] == 'photo':
        scenes_html += render_photo_scene(i, start, dur, scene)
    elif scene['type'] == 'video':
        scenes_html += render_video_clip(i, start, dur, scene)
    elif scene['type'] == 'ending':
        scenes_html += render_ending(start, dur, scene)

# 组装完整 HTML
html = f"""
<!doctype html>
<html>...
  <div id="root" data-start="0" data-duration="{total_dur}" data-width="720" data-height="1280">
    <audio data-start="0" data-duration="{total_dur}" data-track-index="0" src="assets/bgm.mp3" loop></audio>
    {"".join(voice_tags)}
    {scenes_html}
  </div>
  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused: true }});
    {animations_js}
    window.__timelines["main"] = tl;
  </script>
</html>
"""
```

### Step 7：校验

```bash
npx hyperframes validate
```

**目标：0 error**（对比度警告可以忽略）。

### Step 8：渲染

```bash
# 预览用 10fps
npx hyperframes render --fps 10

# 最终版可以用 24fps（更流畅但渲染更慢）
```

### Step 9：飞书发给学员

渲染完成后，通过飞书直接把 MP4 文件发给学员。

---

## 品牌元素清单

每期视频必须包含以下品牌信息（固定位置、固定文案）：

| 位置 | 内容 | 必需 |
|------|------|------|
| 开场龙虾图标 | 🦞 | ✅ |
| 开场字幕 | 半斤九两 · AI未来派 | ✅ |
| 结尾大标题 | AI未来派 | ✅ |
| 结尾副标题 | 🦞 AI升级之旅 | ✅ |
| 片尾 CTA | 半斤九两 · AI让外贸更简单 | ✅ |
| 水印 | 🦞 LONGSHA AI | ✅（每张素材右上角） |

---

## 科技感特效（已验证可复用）

开场/结尾的 CSS/GSAP 特效可以直接复用：

```css
/* 网格背景 */
.grid-overlay {
  background-image:
    linear-gradient(rgba(56, 189, 248, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(56, 189, 248, 0.06) 1px, transparent 1px);
  background-size: 60px 60px;
}

/* 发光圆环 */
.glow-ring {
  width: 500px; height: 500px;
  border-radius: 50%;
  border: 1px solid rgba(56, 189, 248, 0.15);
}

/* 扫描线 */
.scan-line {
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.3), transparent);
}

/* 渐变色标题 */
.glow-text {
  background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

GSAP 动画（开场示例）：

```js
tl.from(".grid-overlay", { opacity: 0, duration: 0.8 }, 0);
tl.from(".glow-ring", { scale: 0.3, opacity: 0, duration: 0.8 }, 0);
tl.to(".glow-ring", { rotation: 180, duration: 3.0, ease: "none" }, 0);
tl.set(".scan-line", { top: "0%" });
tl.to(".scan-line", { top: "100%", duration: 1.5 }, 0);
tl.from(".icon", { opacity: 0, scale: 0.3, duration: 0.5 }, 0.4);
tl.from(".main-title", { opacity: 0, y: 30, duration: 0.7 }, 0.9);
```

---

## 已验证的技术要点（避坑指南）

### video 元素
- ❌ 不要放在 `data-track-index` 的 clip 容器里
- ✅ 放在 root 层，自身带 `data-start` 和 `data-duration`
- ✅ 加 `muted playsinline`

### 音频
- ✅ 每段配音独立生成（不用整段录），方便反推分镜
- ❌ 配音时间点不能有重叠（哪怕 0.0000003s 都不行）
- ✅ BGM 用 `loop` 属性，短于视频会自动续播

### 字幕位置
- ❌ 不要用 `bottom: 40-80px`（贴底难看）
- ✅ 用 `bottom: 360-400px`（中间偏下）

### 渲染速度
- `--fps 10`：3 分钟渲染（预览用）
- 目标：最终版用 24fps 更流畅

---

## CHANGELOG

- 2026-05-25: v1 创建，基于南浔漫步 demo 验证，去模板化，强调动态生成
