from pathlib import Path
import urllib.request
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
VERIFIED = ROOT / 'data' / 'verified_replication_dataset.csv'
RAW = ROOT / 'data' / 'merged_autm.csv'
EVENTS = ROOT / 'data' / 'revision_codes_manual.csv'
P1_COMMIT = '25a9472b34334825b6d6c6a334f5b88eb00695b5'
P1_URL = (
    'https://raw.githubusercontent.com/krish533/Tech-transfer-1/'
    f'{P1_COMMIT}/P1_replication_package/data/derived/'
    'policy_level_indices_institution_year.csv'
)


def norm(s):
    return (s.astype('string')
            .str.replace(r'\s+', ' ', regex=True)
            .str.strip()
            .str.casefold())


def summarize_candidate(r, col, events):
    if col not in r.columns:
        return
    vals = r[col]
    n_unique = vals.nunique(dropna=True)
    n_nonmissing = vals.notna().sum()
    keys = set(norm(vals).dropna())
    event_norm = norm(events['institution'])
    print('INSTITUTION CANDIDATE', col, 'unique=', n_unique,
          'nonmissing=', int(n_nonmissing),
          'event matches=', int(event_norm.isin(keys).sum()), '/', len(events))
    # Check uniqueness after harmonization.
    tmp = pd.DataFrame({
        'inst': vals.astype('string'),
        'year': pd.to_numeric(r['Year'], errors='coerce')
    }).dropna()
    dup = int(tmp.duplicated(['inst', 'year']).sum())
    print('  duplicated institution-year rows=', dup)


def build_observed_docs(p1):
    x = p1.copy()
    x['Year'] = pd.to_numeric(x['Year'], errors='coerce')
    x['Mean_Tone_Score'] = pd.to_numeric(x['Mean_Tone_Score'], errors='coerce')
    x['Is_Carried_Forward'] = pd.to_numeric(x['Is_Carried_Forward'], errors='coerce')
    obs = x[x['Is_Carried_Forward'].eq(0)].copy()
    obs = (obs.dropna(subset=['Institution', 'Year', 'Mean_Tone_Score'])
              .sort_values(['Institution', 'Year'])
              .drop_duplicates(['Institution', 'Year'], keep='last'))
    obs['prev_year'] = obs.groupby('Institution')['Year'].shift(1)
    obs['prev_pcsi'] = obs.groupby('Institution')['Mean_Tone_Score'].shift(1)
    obs['delta'] = obs['Mean_Tone_Score'] - obs['prev_pcsi']
    return obs


def main():
    v = pd.read_csv(VERIFIED, low_memory=False)
    r = pd.read_csv(RAW, low_memory=False)
    e = pd.read_csv(EVENTS)
    print('VERIFIED SHAPE', v.shape)
    print('RAW SHAPE', r.shape)
    print('RAW IDS UNIQUE', r['[ID]'].nunique(dropna=True) if '[ID]' in r else 'NA')
    print('EVENTS', len(e), e['direction'].value_counts().to_dict())

    # Identify the 149-institution AUTM harmonization separately from the P1 match key.
    inst_cols = [c for c in ['Institution', 'Institution_std', 'Institution_pci',
                              'Institution_std_lower'] if c in r.columns]
    for c in inst_cols:
        summarize_candidate(r, c, e)

    print('VERIFIED institution_standardized unique=',
          v['institution_standardized'].nunique(dropna=True),
          'nonmissing=', int(v['institution_standardized'].notna().sum()))

    # Show how AUTM harmonized names map to P1 names, including UMB.
    if 'Institution_std' in r.columns and 'Institution_pci' in r.columns:
        cross = (r[['Institution_std', 'Institution_pci']]
                 .dropna(how='all').drop_duplicates())
        print('CROSSWALK PAIRS', len(cross))
        md = cross[
            norm(cross['Institution_std']).str.contains('maryland', na=False) |
            norm(cross['Institution_pci']).str.contains('maryland', na=False)
        ]
        print('MARYLAND CROSSWALK')
        print(md.to_string(index=False))

    # Download the pinned full P1 policy-in-force panel, then recover directly observed docs.
    p1_path = ROOT / 'data' / '_p1_for_sept25_diagnostics.csv'
    urllib.request.urlretrieve(P1_URL, p1_path)
    p1 = pd.read_csv(p1_path, low_memory=False)
    obs = build_observed_docs(p1)
    print('P1 FULL PANEL', len(p1), 'institutions', p1['Institution'].nunique())
    print('P1 DIRECT OBSERVED', len(obs), 'institutions', obs['Institution'].nunique())

    # Link full P1 document histories to AUTM using the dedicated P1 name key.
    p1_link_names = set(norm(r['Institution_pci']).dropna()) if 'Institution_pci' in r else set()
    obs['_norm'] = norm(obs['Institution'])
    linked = obs[obs['_norm'].isin(p1_link_names)].copy()
    print('P1 DIRECT OBSERVED AT AUTM-LINKED INSTITUTIONS', len(linked),
          'institutions', linked['Institution'].nunique())
    for thr in [0.02, 0.025, 0.03, 0.04, 0.05]:
        rev = linked[linked['delta'].abs() > thr]
        print('FULL-P1 LINKED REVISIONS', thr,
              'n=', len(rev), 'inst=', rev['Institution'].nunique(),
              'up=', int((rev['delta'] > 0).sum()),
              'down=', int((rev['delta'] < 0).sum()))

    # Compare main events to P1 document transitions, allowing explicit aliasing where needed.
    alias = {
        'university of maryland, baltimore (umb)': 'university of maryland baltimore',
    }
    e['_norm'] = norm(e['institution']).replace(alias)
    p1_norm = norm(obs['Institution'])
    matched = 0
    for _, row in e.iterrows():
        sub = obs[(p1_norm == row['_norm']) & (obs['Year'] == row['revision_year'])]
        if len(sub):
            z = sub.iloc[0]
            matched += 1
            print('EVENTCHECK', row['institution'], int(row['revision_year']),
                  'p1_name=', z['Institution'],
                  'derived_prev=', z['prev_year'],
                  'derived_delta=', round(float(z['delta']), 6),
                  'pdf_delta=', row['delta_pcsi'])
        else:
            print('EVENTCHECK_MISSING', row['institution'], int(row['revision_year']))
    print('MAIN EVENT TRANSITIONS MATCHED IN FULL P1', matched, '/', len(e))

    # FY2023 licensing audit: the manuscript replaces the changed total field by Lic Iss + Opt Iss.
    y23 = r[pd.to_numeric(r['Year'], errors='coerce') == 2023].copy()
    for c in ['Tot Lic/Opt Exe', 'Lic Iss', 'Opt Iss']:
        if c in y23:
            x = pd.to_numeric(y23[c], errors='coerce')
            print('2023 LICENSE AUDIT', c, 'N=', int(x.notna().sum()),
                  'median=', float(x.median()), 'mean=', float(x.mean()))
    if {'Lic Iss', 'Opt Iss'}.issubset(y23.columns):
        comp = (pd.to_numeric(y23['Lic Iss'], errors='coerce') +
                pd.to_numeric(y23['Opt Iss'], errors='coerce'))
        print('2023 LICENSE AUDIT component_sum N=', int(comp.notna().sum()),
              'median=', float(comp.median()), 'mean=', float(comp.mean()))

    # Remove downloaded diagnostic copy; workflow should not mutate tracked data.
    if p1_path.exists():
        p1_path.unlink()


if __name__ == '__main__':
    main()
