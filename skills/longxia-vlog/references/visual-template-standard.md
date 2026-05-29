# 视觉模板标准

## 核心判断

龙虾 Vlog 不应该每条视频重新发散视觉。正确做法是固定 2-3 套模板包，让龙虾只在模板包内替换素材、文案、字幕和节奏。

当前默认模板是 `course-memory`。它已经固定为：

- 片头：真实场景照片全屏底图 + 半透明品牌卡片。
- 正文：真实素材全屏 + 中下部半透明字幕卡。
- 片尾：真实场景照片全屏底图 + 品牌 CTA 卡片。
- 水印：左上角小水印，正文出现，片头片尾不重复抢视觉。
- 底部：细进度线，保留平台 UI 安全区。

## 模板包

| 模板包 | 适合场景 | 气质 | 禁忌 |
| --- | --- | --- | --- |
| `course-memory` | 线下课、活动纪念、飞书交付 | 温暖、真实、干净 | 过度赛博、蓝紫网格、假科技隧道 |
| `trade-owner-growth` | 外贸老板学习成长、团队培训 | 稳重、行动感、轻科技 | 炫技特效盖过人物和行动 |
| `social-starter` | 小红书、朋友圈、TikTok 作业 | 轻快、清晰、有发布感 | 字幕太多、品牌太硬、节奏太慢 |

## 设计 token

| 项目 | 标准 |
| --- | --- |
| 背景 | 优先使用真实场景照片，文字由 HTML 渲染 |
| 主标题 | 48-64px，最多两行 |
| 副标题 | 24-34px，最多两行 |
| 正文字体 | 系统黑体或项目统一字体，不混用花字 |
| 主色 | 深墨色、白色、半斤九两品牌强调色 |
| 强调色 | 只用于标题、线条或 CTA，不铺满画面 |
| 水印 | 小尺寸、低透明度、固定角落 |
| 安全区 | 底部保留 180-220px，避免平台 UI 遮挡 |

## 片头 / 片尾素材原则

优先级：

1. 课程场地、活动现场、学员素材中的真实照片。
2. 本 Skill 固定备用图：`template/opening-bg.jpeg`、`template/ending-bg.jpeg`。
3. 无字、无 logo、无二维码的生成背景。

不要再默认使用蓝紫科技隧道、抽象网格、随机方块或带“AI生成”水印的图片。片头片尾的作用是建立品牌和真实场景，不是展示模型会画图。

## 图片生成原则

背景图不要生成文字、logo、二维码或品牌字样。图片模型生成文字不稳定，所有可读信息都放在 HTML 层。

只有在没有真实照片时，才使用下面的提示词。

开头背景提示词：

```text
vertical 9:16 clean cinematic real-photo-like background for an AI learning vlog,
warm classroom or course venue atmosphere,
soft depth, realistic light, space in center for title overlay,
no text, no watermark, no logo, no QR code, no UI, no fake characters,
premium but not sci-fi tunnel, no blue-purple grid, suitable for Chinese business training video
```

结尾背景提示词：

```text
vertical 9:16 calm premium real-photo-like venue background for AI business training,
soft evening light, garden or classroom exterior, warm accent, center safe area,
no text, no watermark, no logo, no QR code, no UI,
designed for HTML title overlay and call to action
```

## 片头结构

1. 0.0-0.5s：背景淡入。
2. 0.3-1.2s：半透明品牌卡片入场。
3. 0.6-2.6s：主标题、副标题和课程标识出现。
4. 2.8-3.5s：切入第一张真实素材。

## 片尾结构

1. 真实场景照片或主体素材回收。
2. 一句总结，不超过 18 个字。
3. 固定 CTA。
4. 结束前 0.5 秒不再出现新文字。

## 固定模板文件

- `template/template-pack.json`
- `template/course-memory.css`
- `template/course-memory-brand-scenes.html`
- `template/opening-bg.jpeg`
- `template/ending-bg.jpeg`
