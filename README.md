# Cold Path

Snowstorm safety app for Buffalo / Western NY: local risk, a readiness checklist, a trusted circle of family,
neighbors and verified helpers, and a Gemini-powered storm assistant.

> Prototype status: weather, radar, outages, shelters and users are **simulated** (a replay of a blizzard).
> The National Weather Service card is the only live data, and it only works when the page is served normally.

## Project layout
```
index.html            page structure
css/styles.css        all styling (themes, animations, layout)
js/app.js             all app logic (loaded as an ES module)
public/               copied to the site root as-is: manifest.webmanifest, sw.js, icons/
vite.config.js        dev server settings
server/               optional Python backend (Gemini proxy + SMS stub)
```

## Run the front end (Vite)
Needs Node 18+ (newer Vite versions want Node 20+; npm will warn you).
```bash
npm install -D vite     # first time only: installs the latest Vite that works with your Node
npm run dev             # http://localhost:5173 with instant reload on save
npm run build           # production files in dist/
npm run preview         # serve the built dist/ locally
npm run api             # second terminal: Gemini backend on :8000 (see below)
```
If you used an earlier version of this project with live-server, delete `node_modules` and `package-lock.json` first.

## Turn on Gemini (optional)
```bash
cd server
python3 -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export GEMINI_API_KEY=your_key                           # Windows PowerShell: $env:GEMINI_API_KEY="your_key"
uvicorn chat_proxy:app --port 8000 --reload
```
In the app, open the chat (**Ask Gemini**) > **Connect Gemini** > Backend URL `http://localhost:8000/chat` > Save.
Never put an API key in `app.js`. Before launch, restrict `allow_origins` in `chat_proxy.py` to your real site.
The backend has not been tested against the live Gemini API yet, so check the model name first.

## Where to change things
- Simulated storm: `SCN`, `SC`, and the `I()` / `cen()` model in `js/app.js`.
- Places (towns, shelters, hospitals, police): the `TW`, `SH` and `PL` arrays in `js/app.js`.
- Gemini rules: the `SYS` prompt in `js/app.js`.
- Colors and themes: the `:root` variables at the top of `css/styles.css`.

## Not built yet (needs more than front-end code)
Real ID and background checks, SMS delivery, real model accuracy results, and partnerships (Erie County, 211, Red Cross).
