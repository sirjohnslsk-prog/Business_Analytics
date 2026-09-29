# User Acceptance Test Cases

| Test | User action | Expected result |
|---|---|---|
| UAT-01 | Open processed scorecard | Exactly 10 provinces with unique ranks |
| UAT-02 | Compare Lusaka metrics with raw source table | Population, employment and poverty values reconcile |
| UAT-03 | Change target province in Excel | Context metrics update to selected province |
| UAT-04 | Double campaign budget with other assumptions unchanged | Estimated leads/applications/registrations double |
| UAT-05 | Increase lead-to-application conversion | Registrations rise without changing budget |
| UAT-06 | Set conversion to zero | Model does not return divide-by-zero error |
| UAT-07 | Re-run Python analysis | Processed CSVs and PNGs regenerate successfully |
| UAT-08 | Review README limitation section | No claim that opportunity score is actual enrolment forecast |
