# Hush

Offline-first PWA for mindfulness and sleep with ad-free ambient soundscapes. Mix rain, ocean, thunder, and nature sounds without interruption or phone radiation.

## Why This Exists

YouTube and apps have ads that disrupt relaxation. This PWA solves that by:
- **No ads**: Ever. Period.
- **Fully offline**: Works in airplane mode (no phone radiation while sleeping)
- **Custom mixing**: Combine multiple sounds to create your perfect soundscape
- **Free forever**: No subscriptions, no tracking

## Features

### Core
- **Curated scenes**: Rain, ocean, forest, thunderstorm, campfire, streams
- **Audio mixer**: Combine multiple sounds with individual volume control
- **Sleep timer**: Auto-stop after 30/60/90 minutes with fade out
- **Offline-first**: All sounds cached locally, works without internet
- **Background audio**: Continues playing with screen off
- **Dark mode**: Essential for sleep apps

### Advanced
- **Custom mixes**: Save and share favourite combinations
- **Scene library**: Downloadable sound packs (rain, nature, weather)
- **Breathing guides**: Visual breathing exercises for meditation
- **Gentle alarms**: Wake to nature sounds instead of harsh beeps
- **Statistics**: Track usage patterns and sleep duration

## Architecture

```
┌─────────────────────────────┐
│   PWA (HTML/CSS/JS)         │
│   - Audio player            │
│   - Scene browser           │
│   - Volume mixer            │
│   - Timer controls          │
└──────────┬──────────────────┘
           │
    Service Worker
    (Offline-first)
           │
   ┌───────┴────────┐
   │                │
Cache API      IndexedDB
(audio files)  (metadata, mixes)
```

## Technology Stack

- **Frontend**: Vanilla JS or lightweight React
- **Audio**: Web Audio API + HTML5 Audio elements
- **Storage**: Cache API for audio files, IndexedDB for metadata
- **PWA**: Service Worker with Workbox
- **Build**: Vite for fast development
- **Hosting**: Cloudflare Pages or Netlify (free tier)

## Sound Sources

### BBC Sound Effects (Primary)
- [BBC Rewind Sound Effects Library](https://sound-effects.bbcrewind.co.uk/search)
- 33,000+ high-quality recordings
- Free for personal use (with attribution)
- Categories: Nature, weather, ambience, transport

### Additional Sources
- **Freesound.org**: CC-licensed community sounds
- **Archive.org**: Public domain nature recordings
- **Synthetic**: Generate brown/white/pink noise using Web Audio API
- **Custom**: User-uploaded recordings (future feature)

## Curated Scenes

### Weather
- **Gentle Rain**: Light rain on leaves
- **Heavy Rain**: Downpour with distant thunder
- **Thunderstorm**: Rain, thunder, wind combination
- **Rain on Tent**: Intimate camping ambience

### Nature
- **Ocean Waves**: Beach with gentle surf
- **Forest**: Birds, wind through trees, rustling leaves
- **Stream**: Babbling brook, flowing water
- **Campfire**: Crackling fire, occasional pops

### Ambience
- **Night Sounds**: Crickets, distant owls, gentle breeze
- **Mountain Stream**: Water over rocks, birds
- **Coastal Evening**: Waves, seagulls, gentle wind
- **Winter Forest**: Wind, occasional bird calls

## User Experience

### First Visit
1. Browse curated scenes
2. Select "Ocean Waves"
3. PWA downloads audio files (with progress indicator)
4. Play immediately once cached
5. Install prompt: "Add to Home Screen for offline use"

### Sleep Mode Flow
1. Choose scene or create custom mix
2. Adjust individual track volumes
3. Set timer (30 mins, 1 hour, 2 hours, continuous)
4. Enable fade out (last 5 minutes)
5. Press play, put phone face-down
6. Enable airplane mode (optional)
7. Audio continues with screen off
8. Automatically stops after timer

### Offline Usage
- All previously used sounds available offline
- Download additional scenes when connected
- Storage manager shows cached sounds and sizes
- Remove unused sounds to free space

## Technical Implementation

### Service Worker Strategy
```javascript
// Cache audio files aggressively
const CACHE_NAME = 'sleep-sounds-v1';
const AUDIO_CACHE = 'audio-files-v1';

self.addEventListener('fetch', (event) => {
  if (event.request.url.endsWith('.mp3')) {
    event.respondWith(
      caches.match(event.request)
        .then(response => response || fetch(event.request))
    );
  }
});
```

### Audio Mixer
```javascript
class SoundMixer {
  constructor() {
    this.tracks = new Map();
    this.fadeInterval = null;
  }

  addTrack(name, url, volume = 0.7) {
    const audio = new Audio(url);
    audio.loop = true;
    audio.volume = volume;
    this.tracks.set(name, audio);
  }

  async play() {
    const promises = Array.from(this.tracks.values())
      .map(audio => audio.play());
    await Promise.all(promises);
  }

  fadeOut(durationMs = 5000) {
    const steps = 50;
    const interval = durationMs / steps;
    let step = 0;

    this.fadeInterval = setInterval(() => {
      step++;
      const factor = 1 - (step / steps);

      this.tracks.forEach(audio => {
        audio.volume = audio.volume * factor;
      });

      if (step >= steps) {
        this.stop();
      }
    }, interval);
  }

  stop() {
    clearInterval(this.fadeInterval);
    this.tracks.forEach(audio => {
      audio.pause();
      audio.currentTime = 0;
    });
  }
}
```

### Storage Management
```javascript
// Estimate storage usage
async function getStorageInfo() {
  if ('storage' in navigator && 'estimate' in navigator.storage) {
    const estimate = await navigator.storage.estimate();
    return {
      usage: estimate.usage,
      quota: estimate.quota,
      percentUsed: (estimate.usage / estimate.quota) * 100
    };
  }
}

// Cache sound with progress
async function cacheSound(name, url, onProgress) {
  const response = await fetch(url);
  const reader = response.body.getReader();
  const contentLength = +response.headers.get('Content-Length');

  let receivedLength = 0;
  const chunks = [];

  while (true) {
    const {done, value} = await reader.read();
    if (done) break;

    chunks.push(value);
    receivedLength += value.length;
    onProgress(receivedLength / contentLength);
  }

  const blob = new Blob(chunks);
  const cache = await caches.open('audio-files-v1');
  await cache.put(url, new Response(blob));
}
```

## File Size Management

**Typical Sizes**:
- Single ambient loop: 2-5 MB (MP3, 5-10 minutes looped)
- Complete scene (3-4 tracks): 10-15 MB
- 10 scenes: ~100-150 MB total

**Strategy**:
- Only cache sounds user has played
- Show storage usage in settings
- Let user remove unused scenes
- Compress audio appropriately (128-192 kbps MP3)

## PWA Manifest

```json
{
  "name": "Hush",
  "short_name": "Hush",
  "description": "Ad-free ambient sounds for sleep and meditation",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0a0e27",
  "theme_color": "#1e3a8a",
  "orientation": "portrait",
  "categories": ["health", "lifestyle"],
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

## Development

### Prerequisites
- Node.js 18+
- Modern browser with PWA support

### Setup
```bash
git clone https://github.com/deanturpin/hush.git
cd hush
npm install
npm run dev
```

### Build
```bash
npm run build    # Production build
npm run preview  # Test production build locally
```

### Deploy
```bash
# Cloudflare Pages or Netlify
# Connect GitHub repo, auto-deploy on push to main
```

## Roadmap

### Phase 1: MVP (Week 1)
- [ ] PWA setup with manifest and service worker
- [ ] 5 curated scenes from BBC Sound Effects
- [ ] Basic audio player (play/pause/stop)
- [ ] Volume control per track
- [ ] Offline caching
- [ ] Dark mode

### Phase 2: Core Features (Week 2)
- [ ] Sleep timer with fade out
- [ ] Custom mix creation
- [ ] Save/load favourite mixes
- [ ] Storage management UI
- [ ] Install prompt
- [ ] Background audio handling

### Phase 3: Polish (Week 3)
- [ ] 15+ scenes across categories
- [ ] Breathing exercise visualisations
- [ ] Usage statistics
- [ ] Scene download manager
- [ ] iOS/Android testing and fixes
- [ ] Performance optimisation

### Phase 4: Advanced (Future)
- [ ] Binaural beats option
- [ ] Guided meditation audio
- [ ] Gentle alarm feature
- [ ] Community-shared mixes
- [ ] User-uploaded sounds
- [ ] Widget for quick access

## Licensing

### Code
MIT Licence - use freely

### Audio
- **BBC Sound Effects**: RemArc Licence (personal use with attribution)
- **Other sources**: CC0, CC-BY, or public domain
- **Attribution**: Displayed in app settings and about page

## Privacy

- **No tracking**: Zero analytics or telemetry
- **No accounts**: No sign-up required
- **Local storage only**: All data stays on device
- **No ads**: Ever

## Browser Support

- **Chrome/Edge**: Full support
- **Firefox**: Full support
- **Safari (iOS/macOS)**: Full support with minor PWA limitations
- **Samsung Internet**: Full support

## Contributing

Contributions welcome! Areas of interest:
- Additional curated sound scenes
- UI/UX improvements
- Performance optimisation
- Bug fixes

## Acknowledgements

- [BBC Sound Effects](https://sound-effects.bbcrewind.co.uk/) - Extensive high-quality audio library
- [Freesound.org](https://freesound.org/) - Community sound effects
- [Workbox](https://developers.google.com/web/tools/workbox) - Service worker utilities

## References

- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Cache API](https://developer.mozilla.org/en-US/docs/Web/API/Cache)
- [PWA Best Practices](https://web.dev/progressive-web-apps/)
