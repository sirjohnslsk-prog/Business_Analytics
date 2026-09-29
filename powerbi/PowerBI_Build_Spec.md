# Power BI Build Specification

This repository does not include a fabricated `.pbix` binary. Instead it provides the exact model design and measures required to reproduce the management dashboard in Power BI.

## Model tables
- `Province Market` — one row per province.
- `Programme Fee` — one row per Cavendish programme.
- `Model Weights` — analyst-controlled score weights.
- Future production facts: `Enquiry`, `Application`, `Registration`, `Campaign Spend`, `Fee Collection`.

## Recommended pages
1. Executive Market Overview
2. Recruitment Territory Analysis
3. Affordability & Working-Adult Market
4. Competition / Whitespace
5. Programme & Fee Portfolio
6. Campaign Scenario
7. Data Quality & Source Lineage

## Interaction requirements
- Province slicer.
- Decision-segment slicer.
- Tooltip showing raw source metrics behind each score.
- Drill-through from executive rank to province detail.
- Prominent disclaimer that the score is not an enrolment forecast.

## Suggested visual standards
- Use standard restrained business colours.
- Keep one primary blue series for comparisons.
- Use neutral grey for benchmarks and annotations.
- Avoid gauges where a labelled KPI card or bar provides clearer comparison.
