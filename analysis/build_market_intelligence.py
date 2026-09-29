from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
PROC = ROOT / 'data' / 'processed'
VIS = ROOT / 'visualizations'
PROC.mkdir(parents=True, exist_ok=True)
VIS.mkdir(parents=True, exist_ok=True)

BLUE = '#1f77b4'  # standard Matplotlib/Python blue
DARK = '#222222'
LIGHT = '#e8eef7'


def minmax(s):
    s = pd.to_numeric(s)
    lo, hi = s.min(), s.max()
    if hi == lo:
        return pd.Series(np.ones(len(s)), index=s.index)
    return (s - lo) / (hi - lo)


def savefig(name):
    plt.tight_layout()
    plt.savefig(VIS / name, dpi=180, bbox_inches='tight')
    plt.close()


df = pd.read_csv(RAW / 'province_indicators.csv')
weights = pd.read_csv(RAW / 'model_weights.csv').set_index('metric')['weight'].to_dict()

df['growth_2010_2022_pct'] = (df['population_2022'] / df['population_2010'] - 1) * 100
# HEA's 2023 report says >80% of private universities/university colleges are concentrated
# along the Lusaka/Copperbelt/Central line of rail. This is therefore an ordinal whitespace proxy,
# not a count of competitors by province.
df['competitive_whitespace_raw'] = np.where(df['line_of_rail_competition'].eq('High'), 0.20, 1.00)

df['market_size_score'] = minmax(df['population_2022'])
df['growth_score'] = minmax(df['growth_2010_2022_pct'])
df['employment_score'] = minmax(df['employment_to_population_2023_pct'])
df['affordability_headroom_score'] = 1 - minmax(df['poverty_gap_2022_pct'])
df['whitespace_score'] = df['competitive_whitespace_raw']

df['opportunity_score'] = 100 * (
    df['market_size_score'] * weights['Market size'] +
    df['growth_score'] * weights['Population growth'] +
    df['employment_score'] * weights['Employment base'] +
    df['affordability_headroom_score'] * weights['Affordability headroom'] +
    df['whitespace_score'] * weights['Competitive whitespace']
)

df['opportunity_score'] = df['opportunity_score'].round(1)
df['rank'] = df['opportunity_score'].rank(method='min', ascending=False).astype(int)
df['decision_segment'] = pd.cut(
    df['opportunity_score'], bins=[-np.inf, 45, 60, np.inf],
    labels=['Develop / distance-led', 'Selective growth', 'Priority market']
)

df.sort_values('rank').to_csv(PROC / 'province_opportunity_scorecard.csv', index=False)

# Executive summary metrics
summary = pd.DataFrame([
    ['Highest opportunity score', df.loc[df['opportunity_score'].idxmax(), 'province'], df['opportunity_score'].max()],
    ['Largest population', df.loc[df['population_2022'].idxmax(), 'province'], int(df['population_2022'].max())],
    ['Highest employment-to-population ratio', df.loc[df['employment_to_population_2023_pct'].idxmax(), 'province'], df['employment_to_population_2023_pct'].max()],
    ['Lowest poverty gap', df.loc[df['poverty_gap_2022_pct'].idxmin(), 'province'], df['poverty_gap_2022_pct'].min()],
    ['Fastest population growth 2010-2022', df.loc[df['growth_2010_2022_pct'].idxmax(), 'province'], df['growth_2010_2022_pct'].max()],
], columns=['metric','province','value'])
summary.to_csv(PROC / 'executive_metrics.csv', index=False)

# 1 Population
p = df.sort_values('population_2022')
plt.figure(figsize=(9,5.5))
plt.barh(p['province'], p['population_2022']/1e6, color=BLUE)
plt.xlabel('Population (millions)')
plt.title('Zambia 2022 Population by Province')
plt.grid(axis='x', alpha=.2)
savefig('01_population_by_province.png')

# 2 Growth
p = df.sort_values('growth_2010_2022_pct')
plt.figure(figsize=(9,5.5))
plt.barh(p['province'], p['growth_2010_2022_pct'], color=BLUE)
plt.xlabel('Population growth, 2010–2022 (%)')
plt.title('Provincial Market Growth')
plt.grid(axis='x', alpha=.2)
savefig('02_population_growth.png')

# 3 Employment base
p = df.sort_values('employment_to_population_2023_pct')
plt.figure(figsize=(9,5.5))
plt.barh(p['province'], p['employment_to_population_2023_pct'], color=BLUE)
plt.axvline(34.3, color=DARK, linestyle='--', linewidth=1.2, label='National 2023: 34.3%')
plt.xlabel('Employment-to-population ratio (%)')
plt.title('Working-Adult Market Proxy: Employment Base')
plt.legend(frameon=False)
plt.grid(axis='x', alpha=.2)
savefig('03_employment_base.png')

# 4 Affordability pressure
p = df.sort_values('poverty_gap_2022_pct', ascending=False)
plt.figure(figsize=(9,5.5))
plt.barh(p['province'], p['poverty_gap_2022_pct'], color=BLUE)
plt.xlabel('Poverty gap ratio (%)')
plt.title('Affordability Pressure Proxy by Province')
plt.figtext(.5, -.02, 'Lower poverty-gap values imply more affordability headroom; this is not household disposable income.', ha='center', fontsize=9)
plt.grid(axis='x', alpha=.2)
savefig('04_affordability_pressure.png')

# 5 Opportunity rank
p = df.sort_values('opportunity_score')
plt.figure(figsize=(9,5.8))
plt.barh(p['province'], p['opportunity_score'], color=BLUE)
plt.xlabel('Opportunity score (0–100)')
plt.title('Higher-Education Market Opportunity Score')
plt.xlim(0,100)
plt.grid(axis='x', alpha=.2)
for i, v in enumerate(p['opportunity_score']):
    plt.text(v+1, i, f'{v:.1f}', va='center', fontsize=9)
savefig('05_opportunity_ranking.png')

# 6 Market matrix
plt.figure(figsize=(9,6))
for _, r in df.iterrows():
    marker = 'o' if r['line_of_rail_competition']=='High' else 's'
    plt.scatter(r['population_2022']/1e6, r['opportunity_score'], s=70, marker=marker, color=BLUE, alpha=.85)
    plt.annotate(r['province'], (r['population_2022']/1e6, r['opportunity_score']), xytext=(5,4), textcoords='offset points', fontsize=8)
plt.xlabel('Population 2022 (millions)')
plt.ylabel('Opportunity score')
plt.title('Market Size vs Opportunity')
plt.grid(alpha=.2)
plt.figtext(.5, -.02, 'Circle = HEA line-of-rail high-competition context; square = lower competition context.', ha='center', fontsize=9)
savefig('06_market_matrix.png')

# 7 National industry profile from public microdata metadata; sample distribution, not survey-weighted population estimate
ind = pd.read_csv(RAW / 'zambia_2023_industry_profile.csv').sort_values('sample_share_pct').tail(12)
plt.figure(figsize=(10,6))
plt.barh(ind['industry'], ind['sample_share_pct'], color=BLUE)
plt.xlabel('Share of valid employed records in public LFS metadata (%)')
plt.title('Zambia Labour-Market Structure — 2023 LFS Public Metadata')
plt.grid(axis='x', alpha=.2)
savefig('07_industry_profile.png')

# 8 Programme price bands
prog = pd.read_csv(RAW / 'cavendish_2026_programmes.csv')
prog['representative_local_fee_zmw'] = prog[['day_zmw','evening_zmw','weekend_zmw','distance_zmw']].bfill(axis=1).iloc[:,0]
p = prog.sort_values('representative_local_fee_zmw')
plt.figure(figsize=(10,6.8))
plt.barh(p['code'], p['representative_local_fee_zmw'], color=BLUE)
plt.xlabel('Published local fee amount (ZMW)')
plt.title('Cavendish University Zambia — 2026 Published Programme Fee Bands')
plt.figtext(.5, -.02, 'Uses the first available local fee field from the published schedule; chart does not assume annual billing frequency.', ha='center', fontsize=8.5)
plt.grid(axis='x', alpha=.2)
savefig('08_cavendish_fee_bands.png')

# 9 Component score decomposition for top provinces
cols = ['market_size_score','growth_score','employment_score','affordability_headroom_score','whitespace_score']
labels = ['Market size','Growth','Employment','Affordability','Whitespace']
top = df.nlargest(6,'opportunity_score').sort_values('opportunity_score')
weighted = np.column_stack([
    top['market_size_score']*weights['Market size']*100,
    top['growth_score']*weights['Population growth']*100,
    top['employment_score']*weights['Employment base']*100,
    top['affordability_headroom_score']*weights['Affordability headroom']*100,
    top['whitespace_score']*weights['Competitive whitespace']*100,
])
plt.figure(figsize=(10,6))
left = np.zeros(len(top))
for j, lab in enumerate(labels):
    plt.barh(top['province'], weighted[:,j], left=left, label=lab)
    left += weighted[:,j]
plt.xlabel('Weighted score contribution')
plt.title('What Drives the Opportunity Score?')
plt.legend(ncol=3, frameon=False, fontsize=8)
plt.grid(axis='x', alpha=.15)
savefig('09_score_decomposition.png')

# Write a compact decision table
out = df[['rank','province','opportunity_score','decision_segment','population_2022','growth_2010_2022_pct','employment_to_population_2023_pct','poverty_gap_2022_pct','line_of_rail_competition']].sort_values('rank')
out.to_csv(PROC / 'management_decision_table.csv', index=False)

print(out.to_string(index=False))
