# GreenFleet IQ — Geotab Vibe Coding Contest 2026

## 🚀 Deploy to GitHub Pages

### Step 1: Push to GitHub
```bash
git add greenfleet-iq.html
git commit -m "Add GreenFleet IQ - EV & Carbon optimizer"
git push origin main
```

### Step 2: Enable GitHub Pages
- Go to your repo → Settings → Pages
- Source: Deploy from branch → `main` / `root`
- Wait 2-3 minutes

### Step 3: Install in MyGeotab
1. MyGeotab → click your profile icon (top-right) → **Administration > System Settings > Add-Ins**
2. Enable **"Allow unverified Add-Ins"** → Yes
3. Paste the JSON below (replace `YOUR_GITHUB_USERNAME` and `YOUR_REPO`)
4. Save → Hard refresh (`Ctrl+Shift+R`)

---

## 📋 MyGeotab Config JSON

```json
{
  "name": "GreenFleet IQ",
  "supportEmail": "https://github.com/pokoboe/fleetflea",
  "version": "1.0.0",
  "items": [{
    "url": "https://pokoboe.github.io/fleetflea/greenfleet-iq.html",
    "path": "ActivityLink",
    "menuName": {
      "en": "🌿 GreenFleet IQ"
    }
  }]
}
```

---

## 🌿 What GreenFleet IQ Does

### Tab 1: Carbon Overview
- Total CO₂ emitted by fleet (last 30 days)
- Fuel consumption estimate
- Top CO₂ emitters bar chart
- Drive vs Idle fuel breakdown donut chart
- EV readiness ring indicator

### Tab 2: Idle Analyzer
- Ranks all vehicles by idle hours
- Shows wasted fuel (litres) and preventable CO₂ (kg) per vehicle
- Critical / High / Normal idle status badges
- Fleet-wide idle waste summary

### Tab 3: EV Readiness Score (0-100)
EV Score algorithm:
- **+40 pts**: Avg daily distance ≤ 200km (EV range covers it)
- **+30 pts**: High idle % (EVs don't waste energy idling)
- **+20 pts**: Frequent short trips (EV optimal use case)
- **+10 pts**: Base score

Recommendations:
- Which vehicles to switch NOW
- Potential annual CO₂ savings
- Fuel cost reduction estimate

### Tab 4: AI Insights (Geotab Ace)
- 5 pre-built green fleet questions
- Free-form natural language query box
- Full 3-step Ace API integration (create-chat → send-prompt → poll)
- Displays AI reasoning + data table

---

## ⚙️ Technical Notes

- **Data source**: `Trip` API (last 30 days, up to 50,000 trips)
- **No backend needed**: Pure Add-In, hosted on GitHub Pages
- **CO₂ constants used**:
  - 2.31 kg CO₂ per litre gasoline
  - 0.10 L/km average fuel consumption
  - 0.8 L/hour idling fuel burn
- **Ace**: Requires admin to enable in Administration > Beta Features
- **Charts**: Chart.js 4.4.1 from CDN (no build step)

---

## 🏆 Contest Categories Targeted

| Category | How |
|----------|-----|
| 🌿 **Green Award** ($2,500) | Direct focus on CO₂ reduction + EV transition |
| 🥇 **Vibe Master** ($10,000) | Polished UI, real Geotab data, actionable insights |
| 🥈 **Innovator** ($5,000) | Ace AI integration + novel EV scoring algorithm |
