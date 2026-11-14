from pptx import Presentation
from pptx.util import Inches, Pt
import sys
DOMAIN = sys.argv[1] if len(sys.argv) > 1 else "rentradar.vercel.app"
prs = Presentation(); prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
def add(i, title, lines):
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = title
    tf = s.placeholders[1].text_frame; tf.word_wrap = True
    for j, ln in enumerate(lines):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.text = ln; p.font.size = Pt(20); p.space_after = Pt(10)
add(0, "RentRadar — House Rent Predictor", ["An AI/ML project by Vikranth Reddy", "B.Tech CSE (AI & ML), 2nd Year — Woxsen University", "A model that looks at a house's size, location and amenities and predicts its fair monthly rent"])
add(1, "The Problem", ["House-hunting in a new city means guessing: is this rent fair or a rip-off?", "Listings vary wildly by area, furnishing and distance to the metro — hard to compare by eye", "Can a simple, explainable model turn a house's details into a fair rent estimate?", "RentRadar answers that question with ridge regression anyone can follow"])
add(2, "The Solution — RentRadar", ["Enter 7 details: area, bedrooms, location tier, furnishing, floor, metro distance, building age", "The model returns the predicted monthly rent, plus the per-sq-ft rate and yearly total", "Try a prime 4BHK or a budget 1BHK with one click", "Runs fully in the browser — no backend, no waiting"])
add(3, "Tech Stack", ["Python + scikit-learn: dataset generation and model training", "Ridge regression (alpha = 1.0) on 7 standardised features", "HTML, CSS and vanilla JavaScript for the interactive demo", "GitHub for source control, Vercel for free hosting"])
add(4, "Architecture", ["Dataset: 600 synthetic rental listings built from simple rent logic", "House details -> standardisation -> ridge regression -> monthly rent (floored at Rs 5,000)", "model.json ships with the site; JavaScript applies the same formula", "Training script: train.py; site generator: gen_site.py"])
add(5, "Live Demo", ["Try it: enter the house details and press Predict Rent", "1,200 sq ft mid-city 2BHK, semi-furnished, 3rd floor, 1.5 km from metro, 5 yrs old -> about Rs 40,324/month", "2,200 sq ft prime 4BHK, fully furnished, 12th floor, 0.5 km from metro, 2 yrs old -> about Rs 96,340/month", f"Demo: https://{DOMAIN}"])
add(6, "Results", ["5-fold cross-validation R-squared: 0.909, MAE: Rs 6,320", "Baseline (always guessing the mean rent): MAE Rs 20,291 — about 3.2x worse", "Mean rent in the data: Rs 46,367", "Browser demo matches Python predictions exactly on all test samples, including the Rs 5,000 floor clip"])
add(7, "Future Scope", ["Train on real rental listings from property portals", "Add features: exact locality, amenities, parking, pet-friendly flag", "Add a rent-vs-buy comparison and a fair-price band instead of one number", "Add city-wise models — rents behave differently in Hyderabad vs Mumbai"])
add(8, "Thank You", ["RentRadar — House Rent Predictor", "Vikranth Reddy, B.Tech CSE (AI & ML), Woxsen University", "Source: github.com/HVRGAMING2705/rentradar", "Questions welcome!"])
prs.save("/home/hatch/workspace/goals/daily-ai-ml-project-factory/files/AIML_RentRadar_2026-11-14.pptx")
print("slides:", len(prs.slides._sldIdLst))
