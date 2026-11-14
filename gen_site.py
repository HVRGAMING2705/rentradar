import json
m = json.load(open("model.json"))
features, mean, std = m["features"], m["mean"], m["std"]
coef, icpt = m["coef"], m["intercept"]
mt = m["metrics"]
r2, mae, rmse, base_mae, mean_rent = mt["cv_r2"], mt["cv_mae"], mt["cv_rmse"], mt["baseline_mae"], mt["mean_rent"]
DOMAIN = "rentradar.vercel.app"
JS_MODEL = f"""const MEAN = {json.dumps(mean)};
const STD = {json.dumps(std)};
const COEF = {json.dumps(coef)};
const INTERCEPT = {icpt};
function rentPred(vals){{
  let z = INTERCEPT;
  for (let i = 0; i < 7; i++) z += COEF[i] * (vals[i] - MEAN[i]) / STD[i];
  return Math.max(z, 5000);
}}"""
index = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RentRadar — House Rent Predictor | AI/ML Project</title>
<meta name="description" content="RentRadar predicts the monthly rent of a house from its area, bedrooms, location, furnishing, floor, metro distance and building age, using a ridge regression model trained on 600 synthetic rental listings. Try it live in your browser.">
<link rel="canonical" href="https://{DOMAIN}/">
<meta property="og:title" content="RentRadar — House Rent Predictor">
<meta property="og:description" content="Enter a house's details and instantly see its predicted monthly rent, with a real trained ML model running in your browser.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://{DOMAIN}/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="RentRadar — House Rent Predictor">
<meta name="twitter:description" content="Ridge regression rent predictor for houses. Try the live demo in your browser.">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"RentRadar","applicationCategory":"EducationalApplication","description":"House rent predictor using ridge regression.","url":"https://{DOMAIN}/"}}</script>
<style>
body{{font-family:Arial,Helvetica,sans-serif;color:#000;background:#fff;max-width:720px;margin:0 auto;padding:24px;line-height:1.5}}
h1{{font-size:2em}} label{{display:block;margin:12px 0 4px;font-weight:bold}}
input,select{{width:100%;padding:10px;font-size:16px;border:1px solid #000;border-radius:4px;box-sizing:border-box}}
button{{margin-top:16px;margin-right:8px;padding:12px 24px;font-size:17px;background:#000;color:#fff;border:none;border-radius:4px;cursor:pointer}}
#result{{margin-top:24px;padding:20px;border:2px solid #000;border-radius:8px;display:none}}
#result b{{font-size:1.6em}}
.note{{color:#333;font-size:.95em}} code{{background:#f2f2f2;padding:2px 5px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:0 20px}}
</style>
</head>
<body>
<h1>&#127968; RentRadar — House Rent Predictor</h1>
<p class="note">A 2nd-year B.Tech AI/ML project by Vikranth Reddy. A ridge regression model trained on 600 synthetic rental listings predicts a house&apos;s monthly rent from its area, bedrooms, location tier, furnishing, floor, distance to the nearest metro station and building age. 5-fold CV: <b>R&sup2; = {r2:.3f}</b>, <b>MAE = &#8377;{mae:,.0f}</b> vs a mean-guess baseline MAE of &#8377;{base_mae:,.0f} (mean rent &#8377;{mean_rent:,.0f}).</p>
<div class="grid">
<label>Area (sq ft)<input type="number" step="1" id="f0" value="1200"></label>
<label>Bedrooms<input type="number" step="1" min="1" max="4" id="f1" value="2"></label>
<label>Location tier<select id="f2"><option value="1">1 — Suburb</option><option value="2" selected>2 — Mid-city</option><option value="3">3 — Prime</option></select></label>
<label>Furnishing<select id="f3"><option value="0">Unfurnished</option><option value="1" selected>Semi-furnished</option><option value="2">Fully furnished</option></select></label>
<label>Floor<input type="number" step="1" min="0" max="20" id="f4" value="3"></label>
<label>Distance to metro (km)<input type="number" step="0.1" min="0.2" max="8" id="f5" value="1.5"></label>
<label>Building age (years)<input type="number" step="1" min="0" max="25" id="f6" value="5"></label>
</div>
<button onclick="predict()">Predict Rent</button>
<button onclick="tryPrime()">Try prime 4BHK</button>
<button onclick="tryBudget()">Try budget 1BHK</button>
<div id="result"></div>
<p class="note">How it works: your seven numbers are standardised (subtract the training mean, divide by the standard deviation), multiplied by the model&apos;s learned weights, and summed with a bias to give the monthly rent in rupees; predictions are floored at &#8377;5,000. The exact same weights run in this page and in the Python training script (<code>train.py</code>), so the browser result matches the trained model.</p>
<p class="note">Try it: a 1,200 sq ft mid-city 2BHK, semi-furnished, 3rd floor, 1.5 km from the metro, 5 years old &rarr; about &#8377;40,324/month. A 2,200 sq ft prime 4BHK, fully furnished, 12th floor, 0.5 km from the metro, 2 years old &rarr; about &#8377;96,340/month. A 600 sq ft suburb 1BHK, unfurnished, 20 years old, 6 km from the metro &rarr; the &#8377;5,000 floor.</p>
<p class="note">Honest note: this model was trained on synthetic listings generated from simple rent logic, so it is a classroom demo — real rents also depend on the exact locality, demand, amenities and negotiation, which seven numbers can&apos;t capture.</p>
<p><a href="https://github.com/HVRGAMING2705/rentradar">View source on GitHub</a></p>
<script>
{JS_MODEL}
function show(){{
  const vals = [];
  for (let i = 0; i < 7; i++) vals.push(parseFloat(document.getElementById("f" + i).value) || 0);
  const rent = rentPred(vals);
  const el = document.getElementById("result");
  el.style.display = "block";
  const perSqft = (rent / vals[0]).toFixed(0);
  const verdict = rent >= 80000 ? "&#128308; PREMIUM — prime location or large luxury home" : rent >= 35000 ? "&#128993; MID-RANGE — typical city rent" : "&#128994; BUDGET — affordable, smaller or outer-area home";
  el.innerHTML = "<b>&#8377;" + rent.toLocaleString("en-IN", {{maximumFractionDigits: 0}}) + " / month</b><br>" + verdict +
    "<br><span class=note>About &#8377;" + perSqft + " per sq ft &middot; yearly &#8377;" + Math.round(rent * 12).toLocaleString("en-IN") + ".</span>";
}}
function predict(){{ show(); }}
function tryPrime(){{ const v = [2200, 4, 3, 2, 12, 0.5, 2]; for (let i = 0; i < 7; i++) document.getElementById("f" + i).value = v[i]; show(); }}
function tryBudget(){{ const v = [600, 1, 1, 0, 1, 6, 20]; for (let i = 0; i < 7; i++) document.getElementById("f" + i).value = v[i]; show(); }}
</script>
</body>
</html>
"""
open("index.html", "w").write(index)
vercel = {
 "headers": [{"headers": [
   {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"},
   {"key": "X-Content-Type-Options", "value": "nosniff"},
   {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
   {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
   {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
   {"key": "Cross-Origin-Opener-Policy", "value": "same-origin"},
   {"key": "Access-Control-Allow-Origin", "value": f"https://{DOMAIN}"},
   {"key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; base-uri 'self'; frame-ancestors 'self'"}],
  "source": "/(.*)"}]}
open("vercel.json", "w").write(json.dumps(vercel, indent=1))
open("404.html", "w").write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Page Not Found — RentRadar</title><style>body{{font-family:Arial,sans-serif;color:#000;max-width:640px;margin:60px auto;padding:24px}}</style></head><body><h1>404 — Page not found</h1><p>This page does not exist on RentRadar.</p><p><a href="https://{DOMAIN}/">Back to RentRadar</a></p></body></html>""")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
open("sitemap.xml", "w").write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://{DOMAIN}/</loc></url></urlset>
""")
open("README.md", "w").write(f"""# RentRadar — House Rent Predictor

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

Ridge regression (alpha=1.0) on standardized features — area, bedrooms, location tier, furnishing, floor, distance to metro, building age — trained on 600 synthetic rental listings (seed 42).

- 5-fold CV R&sup2;: {r2:.3f}, MAE: &#8377;{mae:,.0f} (mean-guess baseline MAE: &#8377;{base_mae:,.0f}); mean rent &#8377;{mean_rent:,.0f}
- Live demo: https://{DOMAIN} (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.

Note: classroom demo on synthetic listings — real rents also depend on exact locality, demand, amenities and negotiation.
""")
samples = json.load(open("parity_samples.json"))
parity = JS_MODEL + "\n" + "\n".join(
    f"console.log(JSON.stringify({{row: {json.dumps(s['row'])}, js: rentPred({json.dumps(s['row'])}), py: {s['pred']}}}));"
    for s in samples)
open("parity.js", "w").write(parity)
print("site files written, R2", r2)
