# Longxia Vlog Skill

龙虾 Vlog 内容生产 Skill，用于 OpenClaw / 扣子龙虾 / HyperFrames 工作流。

当前稳定版：`v1.2.0`。

这个 Skill 的定位不是“完全去模板化剪辑器”，而是：

> 审美模板化，内容动态化。

也就是说，片头、片尾、字体、字幕层级、水印、BGM 选择规则和验收标准要固定；学员素材、采访回答、故事线、分镜顺序和旁白内容再由龙虾动态生成。

## 适用场景

- 龙虾线下课学员纪念 Vlog。
- 内容营销课 / 社媒营销课的第一条短视频体验。
- 外贸老板或团队成员把活动素材整理成一条可发布的竖屏短视频。
- 课程交付后的品牌传播素材，不作为复杂真实素材剪辑系统。

不适合：

- 大量真实视频素材的精剪项目。
- 长视频生产系统。
- 需要专业调色、复杂转场、真人口播合成的项目。

## 核心流程

```text
收素材
-> 问 5 个问题
-> 生成脚本 JSON
-> 生成/接收分段 TTS
-> 选择 BGM
-> 选择视觉模板包
-> 动态生成 index.html
-> HyperFrames 渲染
-> 质量检查
-> 飞书交付 / 课程作业回收
```

## Skill 结构

```text
skills/longxia-vlog/
├── SKILL.md
├── references/
│   ├── bgm-selection-standard.md
│   ├── production-quality-checklist.md
│   ├── scene-matching-checklist.md
│   └── visual-template-standard.md
├── scripts/
│   ├── generate-bgm.py
│   └── render-vlog.sh
└── template/
    ├── template-pack.json
    ├── course-memory.css
    ├── course-memory-brand-scenes.html
    ├── opening-bg.jpeg
    ├── ending-bg.jpeg
    └── gsap.min.js
```

## 环境要求

- HyperFrames CLI >= 0.6.40；本仓库渲染脚本默认锁定 `hyperframes@0.6.46`
- FFmpeg / ffprobe
- Chrome 或可被 HyperFrames 调用的 Chromium
- Python 3.9+
- 可选：扣子龙虾 TTS 或其他可返回 `voice-0.mp3`、`voice-1.mp3` 的 TTS 服务

## 当前升级重点

1. 把“去模板化”修正为“半模板化生产”。
2. 片头片尾改成“实景照片 + HTML 品牌卡片”的固定模板，文字不要烘焙进图片。
3. BGM 以授权曲库优先，Python 生成器只做离线兜底。
4. TTS 依赖明确为外部接口或已生成音频，不再假设本仓库自带扣子 TTS 脚本。
5. 补齐素材识别、画面匹配、字幕安全区、音量和最终出片质检规则。

## 明天课堂可用边界

- 可用：学员上传 3-7 个素材 + 5 个回答，生成 35-75 秒竖屏 Vlog。
- 可用：扣子龙虾生成 TTS 后，本 Skill 负责分镜、排版、BGM、渲染和质检。
- 可用：没有合适片头片尾素材时，使用 `template/opening-bg.jpeg` 和 `template/ending-bg.jpeg` 的固定实景备用图。
- 暂不承诺：自动生成高质量 TTS、专业精剪、大量视频素材混剪、自动发布到社媒。
- 不建议：用系统 TTS 或 Python 兜底 BGM 作为正式用户交付版本。

## 课程化路径

工具工作间定位：`精选外部Skill / 品牌内容产出工具 / 内容营销支线 P1 候选`

推荐同步链路：

```text
工具工作间
-> 半斤九两工具库 / 精选外部Skill
-> 课程工作间 / 内容制作入门课
-> 半斤九两课程库
-> 飞书知识库同步 + 作战台同步
```

作战台只展示课程化后的任务入口、描述词、学习链接和作业提交，不直接展示本仓库原始过程文档。

## License

MIT

---

<!-- jiuliang-about-start -->

## 关于半斤九两 / About EVEN BETTER

半斤九两科技（EVEN BETTER）专注“外贸 + AI”的真实落地。我们希望帮助外贸企业把产品、客户、渠道和团队流程，沉淀成客户看得懂、渠道跑得动、团队留得下的系统。

我们主要提供：

- 外贸 AI 落地方法：围绕 Build / Traffic / Team，判断企业该先建资产、放流量，还是建系统。
- 企业表达与内容增长：把产品、案例、FAQ、老板经验和信任证据，整理成海外客户看得懂的内容资产。
- 主动开发流程：从客户画像、线索搜索、客户背调到开发信和跟进复盘，跑出可复用闭环。
- 团队 AI 工作流：把经验写进 AGENTS.md、SOP、模板库、检查清单和可复用 Skill。

更多内容可以查看我们整理的 [《外贸人 Codex 蓝皮书》](https://github.com/FloydTang/waimaoren-codex-bluebook)。

### 找到我们

- 官网：[tang92.com](https://tang92.com)
- 公众号：半斤九两
- GitHub：[@FloydTang](https://github.com/FloydTang)

扫码关注公众号，领取后续模板、案例和更新；也可以通过公众号后台留言联系九两。

<p>
  <img src="https://raw.githubusercontent.com/FloydTang/waimaoren-codex-bluebook/main/assets/wechat-qr.png" alt="半斤九两公众号二维码" width="180">
</p>

<!-- jiuliang-about-end -->
