# Metal Radio

A tiny installable web player for my favourite hair / glam / 80s metal radio
stations — the same ones I favourited in [cliamp](https://github.com/bjarneo/cliamp).
No native app, no App Store: it's one HTML page you add to your home screen.

## Use it

Open the GitHub Pages URL, then **Share → Add to Home Screen**. It launches
full-screen, keeps playing when the screen locks, and shows play / pause /
next-station on the lock screen and AirPods (Media Session API).

Works the same in a desktop browser — the layout is responsive and the
keyboard media keys are wired up.

## Stations

Defined in the `STATIONS` array near the top of the `<script>` in `index.html`.
Each entry is `{ name, tag, url }` where `url` is a direct stream.

Because the page is served over HTTPS, stream URLs should be HTTPS too —
browsers block plain-HTTP ("mixed content") media. Stations that only offer
HTTP are shown greyed out and won't play on the hosted site (they still work
if you open the app from a plain-HTTP copy on your own network).

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
