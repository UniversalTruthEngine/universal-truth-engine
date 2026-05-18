# UTE Map Prototype v1

This folder contains the first visual topology prototype for the Universal Truth Engine.

## Files

- `index.html` — map page
- `style.css` — visual styling
- `graph.js` — D3 force-directed graph logic
- `data/truth-map-v1.json` — graph data for the first 14 Core Truths

## Visual Encoding

- Node size = dependency centrality
- Node colour = confidence level
- Edge thickness = dependency weight
- Layout = force-directed relationship map

## Hosting

This prototype is designed for GitHub Pages.

In GitHub:

1. Go to repository Settings.
2. Open Pages.
3. Set source to deploy from branch.
4. Choose branch: `main`.
5. Choose folder: `/docs`.
6. Save.

GitHub will then publish the map as a public webpage.
