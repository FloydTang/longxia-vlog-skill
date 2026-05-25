# 🦞 Longxia Vlog Skill

**龙虾 Vlog 生成 Skill** — 用于 [OpenClaw](https://github.com/openclaw/openclaw) 的 AI Agent 技能包。

学员参加龙虾线下课 → 在对话框发照片/视频素材给龙虾 → AI 自动询问 → 生成个性化 Vlog → 飞书发成片。

## 核心流程

```
收素材 → 问5个问题 → 生成文案 → TTS配音 → BGM生成 → 动态HTML → HyperFrames渲染 → 出片
```

## Skill 结构

```
skills/longxia-vlog/
├── SKILL.md              # 完整流程文档
├── template/
│   ├── opening-bg.jpeg   # 开场背景图
│   ├── ending-bg.jpeg    # 结尾背景图
│   └── gsap.min.js       # GSAP 动画库 (用于科技感特效)
└── scripts/
    ├── generate-bgm.py   # 古风 BGM 生成器 (五声音阶)
    └── render-vlog.sh    # 一键渲染脚本
```

## 环境要求

- [HyperFrames CLI](https://github.com/OpenHyperFrames/cli) ≥ 0.6.40
- FFmpeg (用于音频转码)
- Google Chrome (用于渲染)
- Python 3 (用于 BGM 生成)

## 品牌露出

每期视频固定包含品牌信息：
- 开场：🦞 + 半斤九两 · AI未来派
- 结尾：AI未来派 | 🦞AI升级之旅
- CTA：半斤九两 · AI让外贸更简单
- 水印：🦞 LONGSHA AI

## License

MIT
