# Metal Radio

A retro synthwave web player for hair / glam / 80s metal radio stations from
around the world — commercial-free and underground-leaning where possible.
No native app, no App Store: it's one HTML page you add to your home screen.

## Use it

Open the GitHub Pages URL, then **Share → Add to Home Screen**. It launches
full-screen, keeps playing when the screen locks, and shows play / pause /
next-station plus live track info on the lock screen and AirPods (Media
Session API).

Works the same in a desktop browser — the layout is responsive and the
keyboard media keys are wired up.

## Now playing metadata

There's no backend, so the player reads live artist/title/album straight from
each stream host's own public now-playing API in the browser:

- **laut.fm** stations → `api.laut.fm/station/<id>/current_song` (includes album + cover)
- **RadioKing** stations → `api.radioking.io/widget/radio/<slug>/track/current` (includes cover)
- **Zeno.fm** stations → live-pushed via `api.zeno.fm/mounts/metadata/subscribe/<mount>` (SSE)
- **cdnstream1.com**-hosted stations → `yp.cdnstream1.com/metadata/<mount>/current.json` (raw ID3 frames — title/artist/album/art), when the metadata ID happens to match the stream's own mount name (not guaranteed, but free to try)
- anything else → a best-effort Icecast `status-json.xsl` probe on the stream's origin, matched to the exact mount being played (a host can multiplex several stations behind one status page)

When a station doesn't expose any of these (or CORS blocks it), the panel
shows a plain **"No live track info for this station"** note instead of
guessing — that's an honest limitation of some platforms (Live365, StreamMonkey/
RockAntenne, Audalaxy/radiobob, the DAS/cdnstream1 stations whose metadata ID
doesn't match their stream mount, several old-school Shoutcast/Centova hosts),
not a bug, and it's roughly a third of the current station list.

When we do get an artist/title, album/cover art fills in from the provider if
it supplies one, else a quick [iTunes Search API](https://performance-partners.apple.com/search-api)
lookup — used for the album line, the blurred backdrop, and the lock-screen
artwork.

## Stations

Defined in the `STATIONS` array near the top of the `<script>` in `index.html`.
Each entry is `{ name, tag, country, url }` where `url` is a direct stream.

Because the page is served over HTTPS, stream URLs should be HTTPS too —
browsers block plain-HTTP ("mixed content") media. Stations that only offer
HTTP are shown greyed out and won't play on the hosted site (they still work
if you open the app from a plain-HTTP copy on your own network).

The `<audio>` element deliberately has no `crossorigin` attribute — most of
these indie/underground streams don't send CORS headers on the actual audio
bytes, and adding `crossorigin` would make the browser refuse to play them
(this app doesn't touch raw audio samples, so it doesn't need CORS media).

## Icons

`icons/icon.svg` (bolt glyph, transparent background) is the source for the
"any"-purpose icons (`icon-192.png`, `icon-512.png`, `apple-touch-icon.png`,
`favicon-32.png`), regenerated with `rsvg-convert -w <size> -h <size>
--background-color=none icons/icon.svg -o <out>.png`. `icon-512-maskable.png`
is a separate asset from `icon-maskable.svg` (bolt **with** the dark
rounded-square backing) — Android's adaptive-icon mask needs an opaque
maskable source or it shows the wallpaper through oddly-shaped cutouts; the
transparent glyph is only for icons nothing else is going to crop.

### Sync from cliamp

```sh
scripts/sync-favorites.py            # reads ~/.config/cliamp/radio_favorites.toml
git commit -am "sync stations" && git push
```

## Develop locally

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

Service worker + Add-to-Home-Screen need a secure context: `localhost` counts,
or use the deployed HTTPS URL.

## Deploy

Static hosting only. On GitHub Pages: Settings → Pages → deploy from `main` /
root. Any push updates the app; bump `CACHE` in `sw.js` when the shell changes
so clients pick it up.
