#!/usr/bin/env python3
"""
龙虾 Vlog BGM 生成器
用五声音阶生成古风/中国风背景音乐
输出：35 秒 WAV + MP3
"""

import struct, math, wave, os, subprocess

SAMPLE_RATE = 44100
DURATION = 35
VOLUME = 0.12

NOTES = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63,
    'G4': 392.00, 'A4': 440.00,
    'C5': 523.25, 'D5': 587.33, 'E5': 659.25,
    'G5': 783.99, 'A5': 880.00,
    'C3': 130.81, 'D3': 146.83, 'E3': 164.81,
    'G3': 196.00, 'A3': 220.00,
}

# 江南风格旋律（五声音阶）
MELODY = [
    ('E4', 1.5), ('G4', 1.0), ('A4', 1.5), ('G4', 1.0),
    ('E4', 1.5), ('C5', 1.0), ('A4', 1.5), ('G4', 1.0),
    ('A4', 1.5), ('G4', 1.0), ('E4', 1.5), ('D4', 1.0),
    ('C4', 1.0), ('E4', 1.0), ('G4', 1.5), ('A4', 1.0),
    ('E4', 1.5), ('G4', 1.0), ('C5', 1.5), ('A4', 1.0),
    ('G4', 1.5), ('E4', 1.0), ('D4', 1.0), ('C4', 1.0),
    ('A4', 1.5), ('G4', 1.0), ('E4', 1.5), ('C5', 1.0),
    ('A4', 1.0), ('G4', 1.0), ('E4', 1.0), ('D4', 1.0),
]

def generate_bgm(output_dir):
    total_samples = int(SAMPLE_RATE * DURATION)
    buffer = [0.0] * total_samples

    # 主旋律
    t_pos = 0
    while t_pos < DURATION:
        for note_name, note_len in MELODY:
            if t_pos >= DURATION:
                break
            freq = NOTES[note_name]
            start_sample = int(t_pos * SAMPLE_RATE)
            end_sample = int((t_pos + note_len) * SAMPLE_RATE)
            for t in range(start_sample, min(end_sample, total_samples)):
                rel = (t - start_sample) / SAMPLE_RATE
                dur = (end_sample - start_sample) / SAMPLE_RATE
                env = math.exp(-rel / (dur * 0.3))
                val = math.sin(2 * math.pi * freq * rel) * env * VOLUME
                val += math.sin(2 * math.pi * freq * 2 * rel) * env * VOLUME * 0.25
                val += math.sin(2 * math.pi * freq * 3 * rel) * env * VOLUME * 0.1
                buffer[t] += val
            t_pos += note_len

    # 低音 drone
    for t in range(total_samples):
        rel = t / SAMPLE_RATE
        drone1 = math.sin(2 * math.pi * 130.81 * rel) * VOLUME * 0.3
        drone2 = math.sin(2 * math.pi * 196.00 * rel) * VOLUME * 0.2
        tremolo = 0.8 + 0.2 * math.sin(2 * math.pi * 2.0 * rel)
        buffer[t] += (drone1 + drone2) * tremolo

    # 装饰音
    for t in range(total_samples):
        rel = t / SAMPLE_RATE
        if int(rel * 2) % 4 == 0:
            if t % int(SAMPLE_RATE / 8) < int(SAMPLE_RATE / 16):
                buffer[t] += math.sin(2 * math.pi * 880.0 * rel) * VOLUME * 0.15

    # 归一化 + 淡入淡出
    max_val = max(abs(v) for v in buffer)
    if max_val > 0:
        buffer = [v / max_val * 0.35 for v in buffer]

    fade_in = int(SAMPLE_RATE * 0.5)
    for i in range(fade_in):
        buffer[i] *= i / fade_in
    fade_out = int(SAMPLE_RATE * 2)
    for i in range(fade_out):
        buffer[total_samples - fade_out + i] *= (fade_out - i) / fade_out

    # 写 WAV
    wav_path = os.path.join(output_dir, 'bgm.wav')
    with wave.open(wav_path, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        for v in buffer:
            wav.writeframes(struct.pack('<h', int(v * 32767)))

    # 转 MP3
    mp3_path = os.path.join(output_dir, 'bgm.mp3')
    subprocess.run([
        'ffmpeg', '-i', wav_path,
        '-codec:a', 'libmp3lame', '-b:a', '128k',
        mp3_path, '-y'
    ], capture_output=True)

    print(f'✅ BGM 生成成功: {mp3_path}')
    print(f'   时长: {DURATION}s | 大小: {os.path.getsize(mp3_path)/1024:.0f}KB')

if __name__ == '__main__':
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    generate_bgm(target)
