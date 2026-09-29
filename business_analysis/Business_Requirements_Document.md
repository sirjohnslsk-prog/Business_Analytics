# Business Requirements Document (BRD)

## 1. Purpose
Create a Zambia-specific market-intelligence system that helps university management prioritise recruitment territories and evaluate growth strategies using external evidence before committing marketing or physical-expansion resources.

## 2. Business problem
Recruitment budgets are finite, Zambia's provinces differ materially in market size, growth, labour-market participation, affordability pressure and higher-education competition, and decisions made from isolated spreadsheets can lead to inconsistent priorities.

## 3. Objectives
- Establish one governed provincial market scorecard.
- Identify priority, selective-growth and distance-led markets.
- Provide transparent drivers behind each score.
- Enable recruitment scenario analysis in Excel.
- Provide a reusable data structure that can later absorb internal enquiry/application/registration data.

## 4. In scope
- Zambia's 10 provinces.
- ZamStats population, labour-market and poverty indicators.
- HEA competition context.
- Public Cavendish programme and fee information.
- Python, SQL, Excel and visual reporting outputs.

## 5. Out of scope
- Individual student records.
- Confidential university financial data.
- Claims about actual Cavendish conversion rates, profitability or student demand.
- Automated decisions about admissions or individual students.

## 6. Primary business users
- Vice Chancellor / Executive Management
- Registrar / Admissions
- Marketing and Recruitment
- Finance
- Academic leadership / programme owners
- ICT / Data team

## 7. Functional requirements
| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Compare all provinces on a consistent scorecard | Must |
| FR-02 | Show source metrics behind each score | Must |
| FR-03 | Allow opportunity-model weights to be changed | Should |
| FR-04 | Provide management-ready visuals | Must |
| FR-05 | Allow recruitment funnel scenarios in Excel | Must |
| FR-06 | Preserve source URLs and reference years | Must |
| FR-07 | Support future loading of internal enrolment data | Should |
| FR-08 | Distinguish source facts from analyst assumptions | Must |

## 8. Non-functional requirements
- Reproducible calculations.
- No personally identifiable student data.
- Clear metric definitions.
- Traceable source lineage.
- Outputs readable by non-technical executives.
- Assumptions editable rather than hard-coded into conclusions.

## 9. Success criteria
The prototype is successful when a manager can answer: (1) which provinces deserve immediate attention, (2) why they rank that way, (3) what assumptions drive the result, and (4) what a sample recruitment campaign could produce under changed conversion assumptions.
