# BGM 选择标准

## 结论

BGM 不能只靠脚本生成。课程交付和公开发布优先使用授权曲库；`generate-bgm.py` 只作为无网、无曲库、课堂演示时的兜底。

## 优先级

1. 已购买或已授权的半斤九两曲库。
2. 免费可商用曲库，并保存来源、授权和下载日期。
3. `scripts/generate-bgm.py` 生成兜底音乐。

## 风格映射

| 模板包 | 推荐 mood | 节奏 | 说明 |
| --- | --- | --- | --- |
| `course-memory` | warm-memory | 70-90 BPM | 温暖、纪念、不要煽情 |
| `trade-owner-growth` | clean-training | 85-100 BPM | 稳定、行动感、适合培训 |
| `social-starter` | upbeat-social | 100-120 BPM | 更轻快，适合社媒发布 |
| 江南/旅行类素材 | jiangnan-lite | 70-85 BPM | 只在素材确实匹配时使用 |

## 音量

- TTS 必须清楚。
- BGM 峰值不要抢人声，建议最终混音比旁白低 12-18dB。
- 片头可以略高，进入正文后必须降低。
- 片尾 CTA 前不要突然大音量。

## 禁忌

- 不使用平台版权不明的热门歌曲。
- 不使用过强鼓点盖过旁白。
- 不把 Python 合成音乐当作正式默认交付。
- 不让每位学员都用完全相同且辨识度太高的旋律。

## 兜底脚本

```bash
python3 skills/longxia-vlog/scripts/generate-bgm.py assets --mood warm-memory --duration 60
```

可选 mood：

- `warm-memory`
- `clean-training`
- `upbeat-social`
- `jiangnan-lite`
