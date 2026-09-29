from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
D = pd.read_csv(ROOT/'data/processed/province_opportunity_scorecard.csv').sort_values('rank')
BLUE='#1f77b4'; GREY='#666666'; BG='#f7f9fc'
fig = plt.figure(figsize=(14,8), facecolor='white')
fig.suptitle('Zambia Higher-Education Market Intelligence — Executive View', fontsize=18, fontweight='bold', y=.97)

# KPI cards
cards = [
    ('Top opportunity', D.iloc[0].province, f"{D.iloc[0].opportunity_score:.1f}/100"),
    ('Largest market', D.loc[D.population_2022.idxmax(),'province'], f"{D.population_2022.max()/1e6:.2f}m people"),
    ('Strongest employment base', D.loc[D.employment_to_population_2023_pct.idxmax(),'province'], f"{D.employment_to_population_2023_pct.max():.1f}%"),
    ('Fastest 2010–22 growth', D.loc[D.growth_2010_2022_pct.idxmax(),'province'], f"{D.growth_2010_2022_pct.max():.1f}%"),
]
for i,(title, main, sub) in enumerate(cards):
    ax = fig.add_axes([.05+i*.235,.76,.21,.12])
    ax.set_facecolor(BG)
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(.04,.75,title,fontsize=10,color=GREY,transform=ax.transAxes)
    ax.text(.04,.40,main,fontsize=16,fontweight='bold',color=BLUE,transform=ax.transAxes)
    ax.text(.04,.10,sub,fontsize=10,color=GREY,transform=ax.transAxes)

# Rank chart
ax1 = fig.add_axes([.07,.12,.41,.56])
p=D.sort_values('opportunity_score')
ax1.barh(p.province,p.opportunity_score,color=BLUE)
ax1.set_title('Provincial opportunity score',loc='left',fontweight='bold')
ax1.set_xlabel('Score (0–100)'); ax1.set_xlim(0,100); ax1.grid(axis='x',alpha=.2)
for y,v in enumerate(p.opportunity_score): ax1.text(v+1,y,f'{v:.1f}',va='center',fontsize=8)

# Matrix
ax2 = fig.add_axes([.57,.12,.38,.56])
for _,r in D.iterrows():
    marker='o' if r.line_of_rail_competition=='High' else 's'
    ax2.scatter(r.population_2022/1e6,r.opportunity_score,s=90,color=BLUE,marker=marker,alpha=.85)
    ax2.annotate(r.province,(r.population_2022/1e6,r.opportunity_score),xytext=(5,4),textcoords='offset points',fontsize=8)
ax2.set_title('Market size vs opportunity',loc='left',fontweight='bold')
ax2.set_xlabel('Population (millions)'); ax2.set_ylabel('Opportunity score'); ax2.grid(alpha=.2)
fig.text(.76,.065,'○ line-of-rail high competition   □ lower competition context',ha='center',fontsize=8,color=GREY)
fig.text(.5,.02,'Decision-support model built from ZamStats, HEA and public Cavendish fee data. Scores are transparent analyst assumptions, not enrolment forecasts.',ha='center',fontsize=9,color=GREY)

out=ROOT/'visualizations/10_executive_dashboard.png'
plt.savefig(out,dpi=180,bbox_inches='tight'); plt.close()
print(out)
