from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
VERIFIED = ROOT / 'data' / 'verified_replication_dataset.csv'
RAW = ROOT / 'data' / 'merged_autm.csv'
EVENTS = ROOT / 'data' / 'revision_codes_manual.csv'


def norm(s):
    return (s.astype('string').str.replace(r'\s+', ' ', regex=True).str.strip().str.casefold())


def main():
    v = pd.read_csv(VERIFIED, low_memory=False)
    r = pd.read_csv(RAW, low_memory=False)
    e = pd.read_csv(EVENTS)
    print('VERIFIED SHAPE', v.shape)
    print('RAW SHAPE', r.shape)
    print('VERIFIED COLUMNS')
    print('\n'.join(v.columns))
    print('RAW LICENSE-LIKE COLUMNS')
    print([c for c in r.columns if any(x in c.casefold() for x in ['lic', 'option', 'opt'])])
    print('RAW INSTITUTION-LIKE COLUMNS')
    print([c for c in r.columns if any(x in c.casefold() for x in ['institution', 'university'])])
    print('HARMONIZED UNIQUE', v['institution_standardized'].nunique(dropna=True))
    print('RAW IDS UNIQUE', v['institution_id'].nunique(dropna=True))
    print('EVENTS', len(e), e['direction'].value_counts().to_dict())

    # Are the Appendix-A1 names directly present in the harmonized panel?
    names = set(norm(v['institution_standardized']).dropna())
    e['_norm'] = norm(e['institution'])
    print('EVENT NAME MATCHES', int(e['_norm'].isin(names).sum()), '/', len(e))
    if (~e['_norm'].isin(names)).any():
        print('UNMATCHED EVENT NAMES', e.loc[~e['_norm'].isin(names), 'institution'].tolist())
        # show closest simple candidates by substring tokens
        pool = sorted(v['institution_standardized'].dropna().astype(str).unique())
        for x in e.loc[~e['_norm'].isin(names), 'institution']:
            toks = [t.casefold() for t in x.replace(',', ' ').replace('(', ' ').replace(')', ' ').split() if len(t)>4]
            cand = [p for p in pool if any(t in p.casefold() for t in toks)]
            print(' CANDIDATES', x, cand[:12])

    # Reconstruct observed document sequence from source years in the annual panel.
    d = v[['institution_standardized','year','pci','Source_Year','Is_Carried_Forward']].copy()
    d['year'] = pd.to_numeric(d['year'], errors='coerce')
    d['Source_Year'] = pd.to_numeric(d['Source_Year'], errors='coerce')
    d['pci'] = pd.to_numeric(d['pci'], errors='coerce')
    d = d.dropna(subset=['institution_standardized','Source_Year','pci'])
    # each source year should identify a policy-in-force observation; keep one score per institution/source year
    docs = (d.sort_values(['institution_standardized','Source_Year','year'])
              .drop_duplicates(['institution_standardized','Source_Year'], keep='first')
              .sort_values(['institution_standardized','Source_Year']))
    docs['prev_source_year'] = docs.groupby('institution_standardized')['Source_Year'].shift(1)
    docs['prev_pci'] = docs.groupby('institution_standardized')['pci'].shift(1)
    docs['delta'] = docs['pci'] - docs['prev_pci']
    for thr in [0.02,0.025,0.03,0.04,0.05]:
        rev = docs[docs['delta'].abs() > thr]
        print('DERIVED REVISIONS', thr, 'n=', len(rev), 'inst=', rev['institution_standardized'].nunique(), 'up=', int((rev['delta']>0).sum()), 'down=', int((rev['delta']<0).sum()))

    # Check main events against reconstructed source transitions.
    merged = e.merge(docs, left_on=['_norm','revision_year'], right_on=[norm(docs['institution_standardized']), 'Source_Year'], how='left') if False else None
    for _, row in e.iterrows():
        sub = docs[(norm(docs['institution_standardized']) == row['_norm']) & (docs['Source_Year'] == row['revision_year'])]
        if len(sub):
            z = sub.iloc[0]
            print('EVENTCHECK', row['institution'], int(row['revision_year']), 'derived_prev', z['prev_source_year'], 'derived_delta', round(float(z['delta']), 6), 'pdf_delta', row['delta_pcsi'])
        else:
            print('EVENTCHECK_MISSING', row['institution'], int(row['revision_year']))

    # 2023 licensing audit candidates and medians.
    cols = [c for c in r.columns if any(x in c.casefold() for x in ['lic', 'option', 'opt'])]
    if 'Year' in r.columns:
        y23 = r[pd.to_numeric(r['Year'], errors='coerce') == 2023]
        for c in cols:
            x = pd.to_numeric(y23[c], errors='coerce')
            if x.notna().any():
                print('2023COL', c, 'N', int(x.notna().sum()), 'median', float(x.median()), 'mean', float(x.mean()))

if __name__ == '__main__':
    main()
