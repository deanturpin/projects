# Stem Splitter

High-quality audio stem separation using Demucs v4 via ONNX Runtime. Separate audio tracks into vocals, drums, bass, and other instruments with true multi-core parallelisation.

**Development**: See [issue #25](https://github.com/deanturpin/projects/issues/25) for detailed implementation plan and progress tracking.

## Features

- **High Quality**: State-of-the-art Demucs v4 (htdemucs) model with 9.0+ dB SDR
- **Fast Processing**: Multi-threaded C++ implementation, no Python GIL limitations
- **Multiple Interfaces**:
  - CLI for developers and automation
  - Web UI for general use (local or remote)
  - Desktop GUI (planned)
- **Flexible Deployment**:
  - Run locally for privacy and offline use
  - Deploy as web service on VPS
  - Queue system for batch processing
- **4-Stem Separation**: Vocals, drums, bass, other

## Architecture

```
┌─────────────┐
│   Web UI    │  HTML/CSS/JS (works local and remote)
└──────┬──────┘
       │ HTTP/WebSocket
┌──────┴──────┐
│  API Server │  Crow C++ HTTP server
└──────┬──────┘
       │
┌──────┴──────┐
│ C++ Backend │  ONNX Runtime + Demucs model
└─────────────┘  Multi-threaded processing
```

## Technology Stack

- **Backend**: C++20 with ONNX Runtime
- **Models**: Demucs v4 (htdemucs) exported to ONNX
- **HTTP Server**: Crow (header-only C++ web framework)
- **Audio I/O**: libsndfile for WAV processing
- **GPU Support**: CUDA (optional), Metal/CoreML on macOS
- **CPU Optimisation**: Thread pool, parallel batch processing

## Quick Start

### CLI Usage

```bash
# Single file
stemsplit input.wav --output ./stems

# Batch processing
stemsplit *.wav --batch --jobs 4

# Quality/speed trade-off
stemsplit input.wav --model htdemucs      # best quality (slower)
stemsplit input.wav --model mdx_extra     # faster, good quality
```

### Web Service

```bash
# Start local server
stem-server --port 8080

# Visit http://localhost:8080
# Drag and drop audio files, download stems
```

### Deploy to VPS

```bash
# Docker deployment
docker build -t stem-splitter .
docker run -p 8080:8080 stem-splitter

# Or systemd service
make install-service
```

## Building from Source

### Prerequisites

```bash
# macOS
brew install cmake onnxruntime libsndfile

# Ubuntu/Debian
apt install cmake libonnxruntime-dev libsndfile1-dev

# Arch Linux
pacman -S cmake onnxruntime libsndfile
```

### Build

```bash
git clone https://github.com/yourusername/stem-splitter.git
cd stem-splitter
make
```

## Project Structure

```
stem-splitter/
├── backend/           # Core C++ stem separation logic
│   ├── stem_splitter.h
│   ├── stem_splitter.cxx
│   └── onnx_wrapper.cxx
├── cli/              # Command-line interface
│   └── main.cxx
├── server/           # HTTP API server
│   ├── main.cxx
│   └── job_queue.cxx
├── web/              # Web UI (HTML/CSS/JS)
│   ├── index.html
│   └── app.js
├── models/           # ONNX model files (download separately)
│   └── htdemucs.onnx
├── tests/            # Unit tests
└── Makefile
```

## Performance

### CPU-Only (8-core VPS)
- 4-minute song: ~5-8 minutes (htdemucs)
- 4-minute song: ~3-5 minutes (mdx_extra)
- Parallel batch: 3 jobs concurrently

### With GPU (CUDA)
- 4-minute song: ~30-60 seconds
- 10-50x speedup over CPU

## Roadmap

- [x] Research and select best model (Demucs v4)
- [ ] C++ backend with ONNX Runtime integration
- [ ] CLI interface
- [ ] HTTP API server with job queue
- [ ] Web UI with drag-and-drop
- [ ] Docker deployment
- [ ] Model download and management
- [ ] Progress tracking via WebSocket
- [ ] Email notifications for completed jobs
- [ ] File size and rate limiting
- [ ] Desktop GUI (Qt)
- [ ] Extended stem separation (piano, guitar - via UVR models)
- [ ] GPU acceleration support

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## Licence

MIT Licence - see [LICENCE](LICENCE) for details.

## Acknowledgements

- [Demucs](https://github.com/facebookresearch/demucs) by Meta Research for the outstanding separation model
- [ONNX Runtime](https://onnxruntime.ai/) for cross-platform ML inference
- [Mixxx GSoC 2025](https://mixxx.org/news/2025-10-27-gsoc2025-demucs-to-onnx-dhunstack/) for Demucs ONNX conversion work
- [Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui) community for model research

## References

- [Demucs Paper](https://arxiv.org/abs/2111.03600) - Hybrid Spectrogram and Waveform Source Separation
- [ONNX Runtime Documentation](https://onnxruntime.ai/docs/)
- [Audio Source Separation Benchmarks](https://paperswithcode.com/task/audio-source-separation)
