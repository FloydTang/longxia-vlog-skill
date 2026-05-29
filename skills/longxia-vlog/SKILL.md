---
name: longxia-vlog
description: Create Longxia branded 9:16 course, event, and learning-memory vlogs with fixed visual templates, real-material scene matching, TTS/BGM rules, HyperFrames rendering, and quality checks. Use when a user wants 龙虾 to turn photos/videos and five short answers into a polished branded vlog for 半斤九两 courses or social content.
---

# 龙虾 Vlog 内容生产 Skill

## 任务定位

帮助学员把线下课、活动、外贸展会、团队学习或日常素材，整理成一条 9:16 竖屏短视频。

核心原则：

- **审美模板化**：片头、片尾、字体、字幕、安全区、水印、BGM 规则和 CTA 固定。
- **内容动态化**：素材、故事线、分镜顺序、旁白、字幕和节奏按每个学员生成。
- **TTS 可复用**：优先使用扣子龙虾或已验证 TTS 服务生成分段音频。
- **BGM 不硬生成**：授权曲库优先，脚本生成只作为离线兜底。
- **先可发布，再追求炫技**：稳定、清楚、好交付优先于复杂特效。

当前可直接使用的稳定模板包是 `course-memory`。它固定：

- 实景照片片头 / 片尾底图。
- 半透明品牌卡片。
- 正文真实素材全屏 + 中下部字幕卡。
- 左上角低干扰水印。
- 底部进度线和平台安全区。

## 推荐视频规格

| 项目 | 标准 |
| --- | --- |
| 比例 | 9:16 |
| 分辨率 | 720x1280 或 1080x1920 |
| 时长 | 35-75 秒 |
| 帧率 | 预览 10fps，最终 24fps |
| 输出 | MP4 / AAC |
| 字幕 | 画面中下部，避开底部平台 UI |
| 文案 | 一句叙事 + 一句记忆点，少长句 |

## 项目目录约定

每个学员一个独立目录：

```text
~/lobster-vlog/<student-id>/
├── answers.json
├── script.json
├── timings.json
├── index.html
├── assets/
│   ├── photo-1.jpg
│   ├── photo-2.jpg
│   ├── clip-1.mp4
│   ├── opening-bg.jpeg
│   ├── ending-bg.jpeg
│   ├── voice-0.mp3
│   ├── voice-1.mp3
│   └── bgm.mp3
└── renders/
```

## Step 1：收素材并做清点

龙虾收到素材后，先整理到 `assets/`，再输出素材清点：

```json
{
  "assets": [
    {
      "file": "photo-1.jpg",
      "type": "photo",
      "content_guess": "课堂合影",
      "usable": true,
      "risk": ""
    },
    {
      "file": "clip-1.mp4",
      "type": "video",
      "content_guess": "现场片段",
      "usable": true,
      "risk": "横屏，需裁切"
    }
  ]
}
```

素材判断优先级：

1. 人物表情清楚。
2. 事件信息明确。
3. 画面不糊、不黑、不严重遮挡。
4. 能与学员回答形成关系。
5. 不含隐私、付款、后台、客户敏感信息。

## Step 2：问 5 个问题

语气自然，像课程助教，不要像表单：

1. 你叫什么？这次从哪里来？
2. 这是你第几次参加龙虾相关活动？
3. 这次最有收获的一点是什么？
4. 回去后你最想先用 AI 做哪件事？
5. 如果给这次自己留一句话，你想说什么？

如果素材明显不够，追加一个问题：

> 这条视频更想偏“纪念感”“成长感”还是“发朋友圈/小红书更好看”？

## Step 3：选择视觉模板包

不要每次重新发散视觉风格。先选模板包，再生成文案和分镜。

| 模板包 | 用途 | 视觉关键词 | 默认 BGM |
| --- | --- | --- | --- |
| `course-memory` | 线下课纪念 Vlog | 真实、温暖、干净、轻品牌 | warm-memory |
| `trade-owner-growth` | 外贸老板成长记录 | 稳重、行动感、轻科技 | clean-training |
| `social-starter` | 社媒内容入门作业 | 更轻快、更短、更适合发布 | upbeat-social |

模板包详细规则见 `references/visual-template-standard.md`。

`course-memory` 的固定版式文件：

- `template/template-pack.json`：模板 token、品牌文案和默认时长。
- `template/course-memory.css`：正式 CSS 版式。
- `template/course-memory-brand-scenes.html`：片头和片尾 HTML 结构片段。
- `template/opening-bg.jpeg` / `template/ending-bg.jpeg`：没有现场照片时的备用实景底图。

## Step 4：生成脚本 JSON

脚本必须结构化，方便后续生成 HTML 和验收。

```json
{
  "template_pack": "course-memory",
  "student": {
    "name": "学员名",
    "origin": "城市或公司"
  },
  "video": {
    "ratio": "9:16",
    "target_duration": 50,
    "tone": "温暖、有行动感、不煽情"
  },
  "scenes": [
    {
      "id": "s0",
      "type": "opening",
      "asset": "assets/opening-bg.jpeg",
      "narration": "今天，我们把一次学习，剪成一条属于你的 AI 升级记录。",
      "caption": "龙虾 AI 升级之旅",
      "sub_caption": "半斤九两 · AI 让外贸更简单",
      "duration_hint": 4
    },
    {
      "id": "s1",
      "type": "photo",
      "asset": "assets/photo-1.jpg",
      "narration": "从现场的一张合影开始，这一天不是听完就算，而是准备回去开干。",
      "caption": "把学习变成行动",
      "sub_caption": "先做第一件能落地的事",
      "duration_hint": 7
    },
    {
      "id": "s2",
      "type": "ending",
      "asset": "assets/ending-bg.jpeg",
      "narration": "下一次，就让龙虾陪你把内容、客户和生意一步步做出来。",
      "caption": "AI 未来派",
      "sub_caption": "龙虾 AI 升级之旅",
      "cta": "半斤九两 · AI 让外贸更简单",
      "duration_hint": 5
    }
  ]
}
```

文案规则：

- 每段旁白 8-24 个汉字为主，避免长句。
- 字幕不要逐字铺满，主字幕只保留结论。
- 品牌露出固定放在开头、片尾、水印和 CTA，不要每段都打广告。
- 不要把学员塑造成虚假成功案例，只写真实体验和下一步行动。

## Step 5：生成或接收 TTS

本仓库不内置扣子 TTS 脚本。TTS 来源有两种：

1. 扣子龙虾 / 扣子平台生成分段语音，下载成 `assets/voice-0.mp3`、`voice-1.mp3`。
2. 其他已授权 TTS 服务生成同名分段音频。

不要用 macOS `say` 或类似系统音作为正式交付声音；它只能做本地流程占位。

建议声音：

- 女声：温暖、清楚、轻微激励感。
- 男声：沉稳、不要播音腔太重。
- 语速：比默认快 3%-8%，避免拖沓。

硬规则：

- 每个 scene 一段独立音频。
- 音频之间不能重叠。
- 旁白总时长决定分镜时长，不要先写死分镜。

## Step 6：选择 BGM

BGM 选择优先级：

1. 已授权曲库中选择合适音乐。
2. 免费可商用曲库，保存来源和授权说明。
3. 使用 `scripts/generate-bgm.py` 生成离线兜底音乐。

```bash
python3 skills/longxia-vlog/scripts/generate-bgm.py \
  ~/lobster-vlog/<student-id>/assets \
  --mood warm-memory \
  --duration 60
```

兜底脚本生成的是“可用底乐”，不是默认最佳音乐。课程交付建议优先用曲库。

BGM 标准见 `references/bgm-selection-standard.md`。

## Step 7：测量音频并生成 timings.json

```bash
cd ~/lobster-vlog/<student-id>

python3 - <<'PY'
import glob
import json
import subprocess

total = 0.0
voices = []

for file in sorted(glob.glob("assets/voice-*.mp3")):
    duration = float(subprocess.check_output([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        file,
    ]))
    voices.append({"file": file, "start": round(total, 3), "duration": round(duration, 3)})
    total += duration

with open("timings.json", "w", encoding="utf-8") as f:
    json.dump({"voices": voices, "total_duration": round(total, 3)}, f, ensure_ascii=False, indent=2)
PY
```

生成 HTML 前必须核对：

- `voice-*` 数量与非静音 scene 数量一致。
- 起始时间单调递增。
- 总时长与目标时长差距不超过 10 秒；超过就重写文案或调整素材段落。

## Step 8：动态生成 index.html

动态部分：

- 素材文件。
- 每段 scene 的 start / duration。
- 字幕内容。
- 轻微 pan / zoom / crop 参数。

固定部分：

- 模板包 CSS token。
- 片头、片尾结构。
- 字幕安全区。
- 水印位置。
- CTA 文案。

HyperFrames 关键规则：

1. BGM 放 `data-track-index="0"`。
2. 分段配音放 `data-track-index="1"`。
3. 照片和字幕放 track 2 及以后。
4. `<video>` 元素放在 root 下，自身带 `data-start` 和 `data-duration`，不要嵌套在 clip div 里。
5. 字幕不要贴底，720x1280 时主字幕建议 `bottom: 280px` 到 `360px`。
6. 图片背景不要带 AI 生成水印、乱码文字或不可控品牌字样；所有文字用 HTML 渲染。

片头 / 片尾生成规则：

1. 优先从学员素材或课程场地素材中选一张真实照片作为 `assets/opening-bg.jpeg` 和 `assets/ending-bg.jpeg`。
2. 如果没有合适照片，再复制 `template/opening-bg.jpeg` 和 `template/ending-bg.jpeg` 到 `assets/`。
3. 片头/片尾文字必须放在 HTML 卡片里，不写进图片。
4. 片头/片尾使用 `template/course-memory.css` 的 `.lx-brand-*` 样式，不重新发散风格。

## Step 9：校验和渲染

```bash
# 预览
bash skills/longxia-vlog/scripts/render-vlog.sh ~/lobster-vlog/<student-id> --preview

# 最终版
bash skills/longxia-vlog/scripts/render-vlog.sh ~/lobster-vlog/<student-id> --final
```

最终版默认 24fps。预览版默认 10fps。

## Step 10：质量检查

出片前必须过一遍：

- 开头 3 秒看得出主题。
- 主体素材不少于 3 个有效画面。
- 字幕没有压到底部平台 UI 区。
- 人脸和主要物体没有被标题遮挡。
- BGM 音量明显低于 TTS。
- 片尾有 CTA，但不盖过学员故事。
- 没有明显 AI 水印、乱码、错别字、画面黑屏。

完整清单见 `references/production-quality-checklist.md`。

## 品牌露出规则

| 位置 | 内容 | 规则 |
| --- | --- | --- |
| 开场 | 半斤九两 · 龙虾 AI 升级之旅 | 3-4 秒，不要堆字 |
| 水印 | 半斤九两 / 龙虾 | 右上角或左上角，小而稳定 |
| 片尾 | AI 未来派 · 半斤九两 / AI 让外贸更简单 | 4-6 秒 |
| 交付文案 | 这是你的第一条龙虾 Vlog | 飞书发送时附一句说明 |

## 开头和结尾背景规则

优先使用真实场景照片。不要再默认生成蓝紫科技隧道、抽象方块、随机 AI 背景。

仅当没有真实照片时，才生成“无字背景”，文字由 HTML 负责。

开头背景：

```text
vertical 9:16 clean cinematic background for an AI learning vlog,
warm classroom and subtle technology atmosphere,
soft depth, realistic light, space in center for title overlay,
no text, no watermark, no logo, no QR code, no UI, no fake characters,
premium but not sci-fi tunnel, suitable for Chinese business training video
```

结尾背景：

```text
vertical 9:16 calm premium outro background for AI business training,
subtle light trail, clean dark surface, warm accent, center safe area,
no text, no watermark, no logo, no QR code, no UI,
designed for HTML title overlay and call to action
```

## 失败边界

- 素材太少、太糊或全是无关截图时，不承诺自动出高质量视频。
- 未授权音乐不能直接用于公开发布。
- 扣子 TTS、HyperFrames、FFmpeg、Chrome 任一不可用时，需要换本地环境或改成交付脚本稿。
- 这个 Skill 不是专业剪辑师，不处理复杂叙事、长视频和大量素材精剪。
- 如果没有真实素材，不把模板背景硬包装成学员成果。

## CHANGELOG

- 2026-05-29: v1.2 固定 `course-memory` 正式版式；片头片尾改为实景背景 + HTML 品牌卡；明确系统 TTS 只作占位。
- 2026-05-26: v1.1 升级为半模板化视频生产 Skill；补视觉模板、BGM、TTS、素材匹配和质检边界。
- 2026-05-25: v1 创建，基于南浔漫步 demo 验证，强调动态生成。
