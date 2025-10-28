---
name: ffmpeg
description: Guide for using FFmpeg - a comprehensive multimedia framework for video/audio encoding, conversion, streaming, and filtering. Use when processing media files, converting formats, extracting audio, creating streams, applying filters, or optimizing video/audio quality.
license: LGPL/GPL
version: 1.0.0
---

# FFmpeg Skill

FFmpeg is a comprehensive open-source multimedia framework that handles video, audio, and other multimedia files and streams. It provides command-line tools and libraries for recording, converting, and streaming audio and video.

## When to Use This Skill

Use this skill when:
- Converting media files between formats (MP4, MKV, WebM, AVI, etc.)
- Encoding/decoding video with different codecs (H.264, H.265, VP9, AV1)
- Processing audio files (AAC, MP3, FLAC, Opus)
- Live streaming to platforms (Twitch, YouTube, RTMP servers)
- Creating HLS/DASH adaptive streams
- Extracting audio from video files
- Applying video/audio filters (scale, crop, denoise, volume)
- Screen recording and capture
- Optimizing video quality and file size
- Batch processing media files
- Analyzing media file properties

## Core Components

### Command-Line Tools

**ffmpeg**: Primary tool for transcoding, conversion, and streaming
**ffprobe**: Media analysis and inspection tool
**ffplay**: Minimalist multimedia player for testing

### Libraries

- **libavcodec**: Encoding/decoding codecs
- **libavformat**: Container formats and I/O
- **libavfilter**: Audio/video filtering framework
- **libavutil**: Utility functions
- **libswscale**: Video scaling and color conversion
- **libswresample**: Audio resampling and mixing

## Common Video Codecs

### Modern Codecs

**H.264 (libx264)**: Most widely supported, excellent compression/quality balance
- Best for: Universal compatibility, streaming, web video
- Quality range: CRF 17-28 (lower = better quality)

**H.265/HEVC (libx265)**: 25-50% better compression than H.264
- Best for: 4K video, file size reduction
- Slower encoding, limited browser support

**VP9**: Royalty-free, WebM format
- Best for: YouTube, open-source projects
- Good quality/compression, Chrome/Firefox support

**AV1 (libaom-av1, libsvtav1)**: Next-generation codec, best compression
- Best for: Future-proofing, ultimate quality/size ratio
- Very slow encoding (improving with SVT-AV1)

### Legacy Codecs
- MPEG-4 (Xvid/DivX)
- MPEG-2
- VP8

## Common Audio Codecs

**AAC**: Industry standard, excellent quality
**MP3**: Universal compatibility, good quality
**Opus**: Best quality at low bitrates, ideal for voice/streaming
**FLAC**: Lossless compression, archival quality
**Vorbis**: Open-source, good quality
**AC-3/DTS**: Surround sound formats

## Container Formats

**MP4**: Universal compatibility, streaming-friendly
**MKV (Matroska)**: Feature-rich, supports multiple tracks/subtitles
**WebM**: Web-optimized (VP8/VP9 + Vorbis/Opus)
**AVI**: Legacy format, broad compatibility
**MOV**: Apple QuickTime format
**TS**: Transport stream for broadcasting
**FLV**: Flash video (legacy streaming)

## Basic Operations

### Format Conversion

Simple format conversion without re-encoding:
```bash
ffmpeg -i input.mkv -c copy output.mp4
```

Convert with specific codecs:
```bash
ffmpeg -i input.avi -c:v libx264 -c:a aac output.mp4
```

### Quality-Based Encoding (CRF)

Constant Rate Factor - best for quality-focused encoding:

```bash
# H.264 encoding (CRF 23 = default, 17-28 recommended range)
ffmpeg -i input.mkv -c:v libx264 -preset slow -crf 22 -c:a copy output.mp4

# H.265 encoding (higher compression)
ffmpeg -i input.mkv -c:v libx265 -preset medium -crf 24 -c:a copy output.mp4

# VP9 encoding (WebM)
ffmpeg -i input.mkv -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus output.webm
```

**CRF Scale:**
- 0 = Lossless (huge file size)
- 17-18 = Visually lossless
- 20-23 = High quality (recommended)
- 24-28 = Medium quality
- 30+ = Low quality
- 51 = Worst quality

**Presets** (speed vs compression):
- ultrafast, superfast, veryfast, faster, fast
- medium (default)
- slow, slower, veryslow (better compression)
- placebo (not recommended - minimal gains)

### Bitrate-Based Encoding (Two-Pass)

For targeting specific file sizes:

```bash
# Pass 1 (analysis)
ffmpeg -y -i input.mkv -c:v libx264 -b:v 2600k -pass 1 -an -f null /dev/null

# Pass 2 (encoding)
ffmpeg -i input.mkv -c:v libx264 -b:v 2600k -pass 2 -c:a aac -b:a 128k output.mp4
```

### Audio Extraction

Extract audio without re-encoding:
```bash
ffmpeg -i video.mp4 -vn -c:a copy audio.m4a
```

Extract and convert to MP3:
```bash
ffmpeg -i video.mp4 -vn -q:a 0 audio.mp3
```

Extract with specific bitrate:
```bash
ffmpeg -i video.mp4 -vn -c:a libmp3lame -b:a 192k audio.mp3
```

### Video Scaling/Resizing

Scale to specific dimensions:
```bash
ffmpeg -i input.mp4 -vf scale=1280:720 output.mp4
```

Scale maintaining aspect ratio:
```bash
# Width 1280, height auto-calculated
ffmpeg -i input.mp4 -vf scale=1280:-1 output.mp4

# Height 720, width auto-calculated
ffmpeg -i input.mp4 -vf scale=-1:720 output.mp4
```

Scale to half resolution:
```bash
ffmpeg -i input.mp4 -vf scale=iw/2:ih/2 output.mp4
```

### Trimming/Cutting Video

Cut without re-encoding (fast but less precise):
```bash
ffmpeg -i input.mp4 -ss 00:01:30 -to 00:03:00 -c copy output.mp4
```

Cut with re-encoding (precise):
```bash
ffmpeg -i input.mp4 -ss 00:01:30 -t 00:01:30 -c:v libx264 -c:a aac output.mp4
```

Parameters:
- `-ss`: Start time (HH:MM:SS or seconds)
- `-to`: End time
- `-t`: Duration (instead of end time)

### Concatenation

**Method 1: Concat demuxer (same codec/format)**

Create `concat.txt`:
```
file 'input1.mp4'
file 'input2.mp4'
file 'input3.mp4'
```

Run:
```bash
ffmpeg -f concat -safe 0 -i concat.txt -c copy output.mp4
```

**Method 2: Concat filter (different formats)**
```bash
ffmpeg -i input1.mp4 -i input2.mp4 -i input3.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" output.mp4
```

## Advanced Filtering

### Video Filters

**Multiple filters (chain with comma):**
```bash
ffmpeg -i input.mp4 -vf "scale=1280:720,hqdn3d" output.mp4
```

**Denoise:**
```bash
ffmpeg -i input.mp4 -vf hqdn3d output.mp4
```

**Deinterlace:**
```bash
ffmpeg -i input.mp4 -vf yadif output.mp4
```

**Crop:**
```bash
# Crop to 1280x720 from top-left (0,0)
ffmpeg -i input.mp4 -vf "crop=1280:720:0:0" output.mp4

# Auto-detect and remove black borders
ffmpeg -i input.mp4 -vf "cropdetect" output.mp4
```

**Rotate:**
```bash
# Rotate 90 degrees clockwise
ffmpeg -i input.mp4 -vf "transpose=1" output.mp4

# Rotate 180 degrees
ffmpeg -i input.mp4 -vf "transpose=1,transpose=1" output.mp4
```

**Watermark/Logo:**
```bash
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "overlay=10:10" output.mp4
```

**Speed adjustment:**
```bash
# 2x speed
ffmpeg -i input.mp4 -vf "setpts=0.5*PTS" -af "atempo=2.0" output.mp4

# 0.5x speed (slow motion)
ffmpeg -i input.mp4 -vf "setpts=2.0*PTS" -af "atempo=0.5" output.mp4
```

### Audio Filters

**Volume adjustment:**
```bash
# Increase volume by 10dB
ffmpeg -i input.mp4 -af "volume=10dB" output.mp4

# Set to 50% volume
ffmpeg -i input.mp4 -af "volume=0.5" output.mp4
```

**Normalize audio:**
```bash
ffmpeg -i input.mp4 -af loudnorm output.mp4
```

**Crossfade between audio:**
```bash
ffmpeg -i audio1.mp3 -i audio2.mp3 \
  -filter_complex "[0][1]acrossfade=d=5" output.mp3
```

**Mix multiple audio tracks:**
```bash
ffmpeg -i input1.mp3 -i input2.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=longest" output.mp3
```

## Streaming

### RTMP Streaming (Twitch/YouTube)

**Basic stream:**
```bash
ffmpeg -re -i input.mp4 -c:v libx264 -preset veryfast \
  -maxrate 3000k -bufsize 6000k -pix_fmt yuv420p -g 50 \
  -c:a aac -b:a 128k -ar 44100 \
  -f flv rtmp://live.twitch.tv/app/YOUR_STREAM_KEY
```

**Screen capture + stream (Linux):**
```bash
ffmpeg -f x11grab -s 1920x1080 -framerate 30 -i :0.0 \
  -f pulse -ac 2 -i default \
  -c:v libx264 -preset veryfast -tune zerolatency \
  -maxrate 2500k -bufsize 5000k -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ar 44100 \
  -f flv rtmp://live.twitch.tv/app/YOUR_STREAM_KEY
```

**Screen capture (Windows DirectShow):**
```bash
ffmpeg -f dshow -i video="screen-capture-recorder":audio="Stereo Mix" \
  -c:v libx264 -preset ultrafast -tune zerolatency \
  -maxrate 750k -bufsize 3000k \
  -f flv rtmp://live.twitch.tv/app/YOUR_STREAM_KEY
```

**Important streaming parameters:**
- `-re`: Read input at native frame rate (real-time)
- `-tune zerolatency`: Optimize for low latency
- `-g 50`: Keyframe every 50 frames (2 seconds @ 25fps)
- `-maxrate`: Maximum bitrate
- `-bufsize`: Rate control buffer (typically 2x maxrate)

### HLS Streaming

Generate adaptive HLS stream:
```bash
ffmpeg -i input.mp4 \
  -c:v libx264 -preset fast -crf 22 -g 48 -sc_threshold 0 \
  -c:a aac -b:a 128k \
  -f hls -hls_time 6 -hls_playlist_type vod \
  -hls_segment_filename "segment_%03d.ts" \
  playlist.m3u8
```

**Multi-bitrate HLS:**
```bash
ffmpeg -i input.mp4 \
  -map 0:v -map 0:a -map 0:v -map 0:a \
  -c:v libx264 -crf 22 -c:a aac -b:a 128k \
  -b:v:0 2000k -s:v:0 1280x720 -b:v:1 5000k -s:v:1 1920x1080 \
  -var_stream_map "v:0,a:0 v:1,a:1" \
  -master_pl_name master.m3u8 \
  -f hls -hls_time 6 -hls_list_size 0 \
  stream_%v/index.m3u8
```

### UDP/RTP Streaming

**UDP stream:**
```bash
ffmpeg -re -i input.mp4 -c copy -f mpegts udp://192.168.1.100:1234
```

**RTP audio stream:**
```bash
ffmpeg -re -i audio.mp3 -c:a libopus -f rtp rtp://192.168.1.100:5004
```

## Hardware Acceleration

### NVIDIA NVENC

```bash
# H.264 with NVENC
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc -preset fast -crf 22 output.mp4

# H.265 with NVENC
ffmpeg -hwaccel cuda -i input.mp4 -c:v hevc_nvenc -preset fast -crf 24 output.mp4
```

### Intel QuickSync (QSV)

```bash
ffmpeg -hwaccel qsv -c:v h264_qsv -i input.mp4 \
  -c:v h264_qsv -preset fast -global_quality 22 output.mp4
```

### AMD VCE

```bash
ffmpeg -hwaccel auto -i input.mp4 \
  -c:v h264_amf -quality balanced -rc cqp -qp 22 output.mp4
```

## Media Analysis

### Inspect media file

```bash
# Detailed information
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# Human-readable format
ffprobe input.mp4

# Get duration
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 input.mp4

# Get resolution
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height \
  -of csv=s=x:p=0 input.mp4

# Get bitrate
ffprobe -v error -show_entries format=bit_rate \
  -of default=noprint_wrappers=1:nokey=1 input.mp4
```

## Batch Processing

### Bash loop for batch conversion

```bash
# Convert all MKV files to MP4
for file in *.mkv; do
  ffmpeg -i "$file" -c:v libx264 -crf 22 -c:a aac "${file%.mkv}.mp4"
done

# Resize all videos to 720p
for file in *.mp4; do
  ffmpeg -i "$file" -vf scale=-1:720 "720p_${file}"
done
```

### Parallel processing with GNU Parallel

```bash
# Install: sudo apt-get install parallel

# Process multiple files in parallel
ls *.mkv | parallel ffmpeg -i {} -c:v libx264 -crf 22 -c:a aac {.}.mp4
```

## Common Patterns

### Create GIF from video

```bash
# High quality GIF
ffmpeg -i input.mp4 -vf "fps=15,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif

# Simple GIF
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1" output.gif
```

### Extract frames as images

```bash
# Extract all frames
ffmpeg -i input.mp4 frame_%04d.png

# Extract 1 frame per second
ffmpeg -i input.mp4 -vf fps=1 frame_%04d.png

# Extract single frame at 5 seconds
ffmpeg -ss 00:00:05 -i input.mp4 -frames:v 1 frame.png
```

### Create video from images

```bash
# From numbered images
ffmpeg -framerate 30 -i frame_%04d.png -c:v libx264 -crf 22 -pix_fmt yuv420p output.mp4

# From pattern
ffmpeg -framerate 24 -pattern_type glob -i '*.png' -c:v libx264 output.mp4
```

### Add subtitles

```bash
# Burn subtitles into video
ffmpeg -i video.mp4 -vf subtitles=subtitles.srt output.mp4

# Embed subtitle track (soft subtitles)
ffmpeg -i video.mp4 -i subtitles.srt -c copy -c:s mov_text output.mp4
```

### Remove audio

```bash
ffmpeg -i input.mp4 -an -c:v copy output.mp4
```

### Replace audio

```bash
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
```

### Create thumbnail

```bash
# Single thumbnail at 5 seconds
ffmpeg -i input.mp4 -ss 00:00:05 -vframes 1 -vf scale=320:-1 thumb.jpg

# Multiple thumbnails (one per minute)
ffmpeg -i input.mp4 -vf fps=1/60,scale=320:-1 thumb_%03d.jpg
```

## Performance Optimization

### Speed vs Quality Trade-offs

**Fast encoding (real-time processing):**
```bash
ffmpeg -i input.mp4 -c:v libx264 -preset ultrafast -crf 23 output.mp4
```

**Balanced (default):**
```bash
ffmpeg -i input.mp4 -c:v libx264 -preset medium -crf 22 output.mp4
```

**High quality (archival):**
```bash
ffmpeg -i input.mp4 -c:v libx264 -preset veryslow -crf 18 output.mp4
```

### Multi-threading

FFmpeg automatically uses multiple CPU cores. Override with:
```bash
ffmpeg -threads 8 -i input.mp4 -c:v libx264 output.mp4
```

## Best Practices

1. **Use CRF for quality-focused encoding** - Better than bitrate for most use cases
2. **Two-pass for size targets** - When file size is critical
3. **Copy streams when possible** - Use `-c copy` to avoid re-encoding
4. **Choose appropriate presets** - Balance speed vs compression
5. **Match output to source** - Don't upscale or use higher quality than source
6. **Test short clips first** - Verify settings before batch processing
7. **Hardware acceleration** - Use GPU encoding for faster processing
8. **Audio matters** - Don't neglect audio codec/bitrate choices
9. **Use filters efficiently** - Chain multiple filters with commas
10. **Verify output** - Always check quality after encoding

## Common Parameters Reference

### Video Parameters
- `-c:v` or `-vcodec`: Video codec
- `-b:v`: Video bitrate (e.g., `2M`, `2500k`)
- `-crf`: Constant Rate Factor (0-51)
- `-preset`: Encoding speed/quality (ultrafast to veryslow)
- `-tune`: Encoding optimization (film, animation, zerolatency)
- `-pix_fmt`: Pixel format (yuv420p for compatibility)
- `-r`: Frame rate (e.g., `30`, `60`)
- `-g`: GOP size (keyframe interval)

### Audio Parameters
- `-c:a` or `-acodec`: Audio codec
- `-b:a`: Audio bitrate (e.g., `128k`, `192k`)
- `-ar`: Audio sample rate (e.g., `44100`, `48000`)
- `-ac`: Audio channels (1=mono, 2=stereo)
- `-q:a`: Audio quality for VBR (0=best for MP3)

### General Parameters
- `-i`: Input file
- `-y`: Overwrite output without asking
- `-n`: Never overwrite output
- `-t`: Duration to encode
- `-ss`: Start time offset
- `-to`: End time
- `-vf`: Video filters
- `-af`: Audio filters
- `-map`: Stream selection
- `-metadata`: Set metadata
- `-f`: Force format

## Troubleshooting

### "Unknown encoder" errors
Install codec libraries:
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg libx264-dev libx265-dev libvpx-dev

# Check available encoders
ffmpeg -encoders
```

### Output compatibility issues
Use safe defaults for maximum compatibility:
```bash
ffmpeg -i input.mkv -c:v libx264 -profile:v high -level 4.0 \
  -pix_fmt yuv420p -c:a aac -b:a 128k output.mp4
```

### Performance issues
- Use hardware acceleration (`-hwaccel`)
- Choose faster presets (`-preset fast`)
- Reduce resolution with scale filter
- Use multiple threads explicitly

### Quality issues
- Lower CRF value (18-22 for high quality)
- Use slower preset (`-preset slow`)
- Use two-pass encoding for better bitrate distribution
- Match or exceed source bitrate

## Resources

- Official Documentation: https://ffmpeg.org/documentation.html
- FFmpeg Wiki: https://trac.ffmpeg.org/
- Codec Guides: https://trac.ffmpeg.org/wiki/Encode
- Filter Documentation: https://ffmpeg.org/ffmpeg-filters.html
- GitHub Repository: https://github.com/ffmpeg/ffmpeg
- Community Examples: https://trac.ffmpeg.org/wiki/

## Implementation Checklist

When using FFmpeg:

- [ ] Verify FFmpeg installation (`ffmpeg -version`)
- [ ] Check available codecs for your use case
- [ ] Test encoding settings on short clip first
- [ ] Choose appropriate codec for target platform
- [ ] Set quality level (CRF or bitrate)
- [ ] Configure audio codec and bitrate
- [ ] Apply necessary filters (scale, crop, etc.)
- [ ] Consider hardware acceleration if available
- [ ] Verify output quality and file size
- [ ] Test output compatibility on target devices
- [ ] Document settings for reproducibility
- [ ] Create batch scripts for repetitive tasks
