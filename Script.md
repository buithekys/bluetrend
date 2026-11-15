# BlueTrend — 2-Minute Pitch Script & Q&A

## 1. 2-Minute English Pitch Script (~270 words)

> "Hello judges. We are presenting **BlueTrend** — a Web GIS decision-support system for monitoring Southeast Asia’s seagrass ecosystems.
>
> **Why seagrass?** Seagrass meadows are critical Blue Carbon sinks and coastal nurseries, yet they are disappearing rapidly due to ocean warming and land-based sediment runoff. Conservation managers need to know *where* to act first.
>
> **Our Solution:** BlueTrend integrates **21,221 seagrass polygons** from UNEP-WCMC with **14 verified HydroBASINS watersheds** and four **NASA Earth Observation datasets**: MODIS-Aqua Sea Surface Temperature (`SST`), Water Turbidity (`Kd490`), `GPM IMERG` Precipitation, and `AIRS CO₂`.
>
> **How it works:** Instead of relying on black-box guesses, we use the non-parametric **Mann-Kendall test** and **Sen’s Slope** over 22 years of NASA data (**2003–2024**). Our pipeline proves a statistically significant warming trend across Southeast Asia (`p = 1e-06`), alongside rising atmospheric CO₂.
>
> On our interactive map, we sample real NASA `SST`, `Kd490`, and rainfall values at the top 350 largest seagrass meadows to classify them into **High, Medium, and Low Risk**.
>
> **Actionable Impact:** When a user selects a region—like the *Mekong & Gulf of Thailand*, *Gulf of Tonkin*, or *Strait of Malacca*—BlueTrend dynamically updates the risk breakdown, forecasts 3-year trends, and generates **context-aware conservation suggestions**, plus a one-click **CSV risk report** for Marine Protected Area managers.
>
> BlueTrend turns 22 years of NASA satellite data into clear, immediate action to protect Southeast Asia’s Blue Carbon. Thank you!"

---

## 2. Anticipated Q&A

1. **Q: Why did you use Mann-Kendall and Sen’s Slope instead of standard linear regression or Deep Learning?**
   - **A:** Climate and ocean data have strong seasonality and extreme events like El Niño. **Mann-Kendall** and **Sen’s Slope** are non-parametric, meaning they are robust against outliers and don’t assume normal distribution—making them the gold standard in Earth science.

2. **Q: Why are many seagrass meadows labeled "Not reported" for Family/Genus?**
   - **A:** Those polygons in the global UNEP-WCMC dataset were mapped via satellite remote sensing without ground-truth species surveys. Our risk model does not depend on species names; it relies on spatial coordinates and NASA environmental stressors (`SST`, `Kd490`, `GPM`).

3. **Q: Why does the map popup show `SST (2018–2024)` while the trend chart shows `2003–2024`?**
   - **A:** We use the **22-year (2003–2024)** time series to prove long-term regional warming, while using the **most recent 7-year spatial grid (2018–2024)** to reflect *current* thermal and turbidity stress at each meadow without diluting it with cooler decades.

4. **Q: What is your next step after the Hackathon?**
   - **A:** Integrating higher-resolution Sentinel-2/Landsat imagery for local estuaries and adding field-survey validation with local MPA managers.
