# RentRadar — House Rent Predictor

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

Ridge regression (alpha=1.0) on standardized features — area, bedrooms, location tier, furnishing, floor, distance to metro, building age — trained on 600 synthetic rental listings (seed 42).

- 5-fold CV R&sup2;: 0.909, MAE: &#8377;6,320 (mean-guess baseline MAE: &#8377;20,291); mean rent &#8377;46,367
- Live demo: https://rentradar.vercel.app (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.

Note: classroom demo on synthetic listings — real rents also depend on exact locality, demand, amenities and negotiation.
