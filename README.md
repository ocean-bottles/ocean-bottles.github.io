# Bottle drift on ocean currents

Live map: https://ocean-bottles.github.io

Click anywhere on the ocean to drop 15 bottles and watch them drift for up to five years on real surface currents. Each drop gets a card that tracks how many bottles have washed up, how many are still at sea and how far the farthest has travelled. The "Release 3,000 bottles" button seeds bottles across every ocean, and over five simulated years the ones still at sea gather in the subtropical gyres, the slow whirlpools where floating plastic also collects.

Made for the #30DayMapChallenge 2026, Day 13 (Interactive).

## How it works

The currents come from HYCOM, the Hybrid Coordinate Ocean Model, through Google Earth Engine (`HYCOM/sea_water_velocity`). I took one snapshot a day from September 2019 to August 2024 and averaged the surface current for each calendar month on a 0.25° grid, about 28 km at the equator, between 80°N and 78°S.

Every simulated day a bottle moves with the current where it sits, blended between months as the seasons change. Monthly averages smooth away eddies, so each bottle also takes a small random step every day (an eddy diffusivity of 1,000 m²/s), which is why bottles dropped together drift apart. A bottle that the current pushes against the coast has a small daily chance of washing up there; otherwise it slides along the shore. The bottles ride the water only. Real floating objects are also pushed by the wind, so read the paths as where the sea itself would carry them.

The basemap is NASA's Blue Marble Next Generation with bathymetry. The white flow lines are streamlines of the yearly mean current, drawn brighter and thicker where the water moves faster. Coastlines and country names come from Natural Earth. The map runs on MapLibre GL JS, with everything served from this repository and no API keys.

## Files

- `index.html`: the page and the drift model
- `data/cur_MM.png`: monthly currents, one image per month (red = eastward speed, green = northward speed, 0.015 m/s per step around 128; blue = water mask)
- `data/streams.json`: current flow lines for the background
- `data/basemap_tiles.jpg` and `data/basemap.json`: the Blue Marble tiles packed into one file, with an index of where each tile starts
- `data/coast_country.png` and `data/countries.json`: nearest country for any point, used to name where bottles wash up
- `scripts/`: the Python used to turn the Earth Engine exports into these files, and `scripts/export_hycom.js` for the Earth Engine export

© Elias Omondi, 2026
