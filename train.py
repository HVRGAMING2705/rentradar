import json
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_predict, KFold
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

rng = np.random.default_rng(42)
N = 600  # synthetic house-rental listings

area = rng.uniform(400, 2500, N)                       # sq ft
bedrooms = rng.integers(1, 5, N).astype(float)         # 1-4 BHK
location_tier = rng.integers(1, 4, N).astype(float)    # 1 suburb, 2 mid-city, 3 prime
furnishing = rng.integers(0, 3, N).astype(float)       # 0 unfurnished, 1 semi, 2 fully
floor = rng.integers(0, 21, N).astype(float)           # floor number
metro_dist = rng.uniform(0.2, 8.0, N)                 # km to nearest metro station
building_age = rng.uniform(0, 25, N)                  # years

X_raw = np.column_stack([area, bedrooms, location_tier, furnishing, floor, metro_dist, building_age])
FEATURES = ["area_sqft", "bedrooms", "location_tier", "furnishing",
            "floor", "distance_to_metro_km", "building_age_years"]

# Generative rent: per-sq-ft rate depends on location tier, plus premiums for
# bedrooms/furnishing/floor, minus metro distance and building age.
rate_per_sqft = np.where(location_tier == 1, 18.0,
                 np.where(location_tier == 2, 28.0, 45.0))
rent = (area * rate_per_sqft
        + bedrooms * 1500
        + furnishing * 2500
        + floor * 150
        - metro_dist * 800
        - building_age * 120
        + rng.normal(0, 2500, N))
rent = np.clip(rent, 5000, None)
y = rent

mean = X_raw.mean(axis=0)
std = X_raw.std(axis=0)
X = (X_raw - mean) / std

model = Ridge(alpha=1.0).fit(X, y)
kf = KFold(5, shuffle=True, random_state=42)
pred_cv = cross_val_predict(Ridge(alpha=1.0), X, y, cv=kf)
r2 = float(r2_score(y, pred_cv))
mae = float(mean_absolute_error(y, pred_cv))
rmse = float(np.sqrt(mean_squared_error(y, pred_cv)))
base_mae = float(mean_absolute_error(y, np.full(N, y.mean())))
print(f"n={N} mean_rent={y.mean():.0f} median_rent={np.median(y):.0f}")
print(f"CV R2={r2:.3f} MAE={mae:.0f} RMSE={rmse:.0f} baseline_MAE={base_mae:.0f}")

mj = {"features": FEATURES, "mean": mean.tolist(), "std": std.tolist(),
      "coef": model.coef_.tolist(), "intercept": float(model.intercept_),
      "metrics": {"cv_r2": r2, "cv_mae": mae, "cv_rmse": rmse,
                  "baseline_mae": base_mae, "mean_rent": float(y.mean()), "n": N}}
with open("model.json", "w") as f:
    json.dump(mj, f, indent=1)

def py_pred(row):
    xs = (np.array(row) - mean) / std
    return float(max(model.predict([xs])[0], 5000))

samples = [
    [1200, 2, 2, 1, 3, 1.5, 5],     # mid-city 2BHK, semi-furnished
    [2200, 4, 3, 2, 12, 0.5, 2],    # prime 4BHK, fully furnished, near metro
    [600, 1, 1, 0, 1, 6.0, 20],     # suburb 1BHK, unfurnished, old, far from metro
    [1500, 3, 3, 2, 8, 1.0, 1],     # prime 3BHK, fully furnished, new
    [900, 2, 1, 1, 0, 0.3, 15],     # suburb 2BHK, ground floor, near metro
]
for s in samples:
    print(s, "->", round(py_pred(s), 2), "Rs/month")
with open("parity_samples.json", "w") as f:
    json.dump([{"row": s, "pred": py_pred(s)} for s in samples], f, indent=1)
