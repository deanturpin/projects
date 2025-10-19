# Shazam to Tidal

Live audio recognition web app that identifies playing music and creates Tidal playlists.

## Features

- **Live Audio Recognition**: Uses your device microphone to identify songs in real-time
- **Automatic Playlist Creation**: Builds Tidal playlists from identified tracks
- **Cross-Platform**: Works on laptop and Android via web browser
- **No Manual Entry**: Just listen and let it work out what's playing

## How It Works

1. Open the web app on your device
2. Grant microphone access
3. Start listening to music (club, radio, DJ mix, etc.)
4. The app identifies tracks and adds them to your Tidal playlist
5. Access your playlist via deep links that open in the Tidal app

## Tech Stack

- Web Audio API for microphone access
- Audio fingerprinting service (ACRCloud/AudD) for song identification
- Tidal API for playlist management
- Static web app (deployable to GitHub Pages/Vercel/Netlify)

## Roadmap

### Phase 1: Core Functionality
- [ ] Set up web app with microphone access
- [ ] Integrate audio fingerprinting API
- [ ] Basic song identification display
- [ ] Tidal deep link generation

### Phase 2: Playlist Integration
- [ ] Tidal API authentication
- [ ] Automatic playlist creation/updates
- [ ] Track deduplication
- [ ] Real-time UI updates

### Phase 3: Enhanced Features
- [ ] Mix stream analysis (upload/stream DJ mixes)
- [ ] Batch processing of audio files
- [ ] Export playlist as various formats
- [ ] History and statistics

## Getting Started

Coming soon...

## Contributing

This is a personal project but suggestions and contributions are welcome!

## Licence

MIT
