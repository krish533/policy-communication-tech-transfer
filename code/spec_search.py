"""Diagnostic search for the exact research-size tercile construction in the Sept. 25 draft."""
import numpy as np
import pandas as pd
import revision_event_study as re


def rank_tercile(s):
    out = pd.Series(pd.NA, index=s.index, dtype='Int64')
    ok = s.notna()
    if ok.sum():
        r = s[ok].rank(method='average', pct=True)
        out.loc[ok] = np.minimum(np.ceil(r * 3).astype(int) - 1, 2)
    return out


def fixed_inst(panel, values):
    p = panel.copy()
    t = rank_tercile(values)
    mapping = dict(zip(values.index, t))
    p['size_tercile'] = p['institution'].map(mapping).astype('Int64')
    return p


def stack_variant(stacks, mode):
    s = stacks.copy()
    if mode == 'stack_pre_mean':
        v = (s[s.event_time.between(-4, -1)]
             .groupby(['stack','institution'])['research_exp'].mean())
    elif mode == 'stack_pre_median':
        v = (s[s.event_time.between(-4, -1)]
             .groupby(['stack','institution'])['research_exp'].median())
    elif mode == 'stack_full_mean':
        v = s.groupby(['stack','institution'])['research_exp'].mean()
    elif mode == 'stack_m1':
        v = (s[s.event_time.eq(-1)].set_index(['stack','institution'])['research_exp'])
    elif mode == 'stack_t0':
        v = (s[s.event_time.eq(0)].set_index(['stack','institution'])['research_exp'])
    else:
        raise ValueError(mode)
    cat_parts = []
    for stack_id, z in v.groupby(level=0):
        zz = z.droplevel(0)
        tt = rank_tercile(zz)
        tmp = pd.DataFrame({'stack': stack_id, 'institution': tt.index, 'new_size': tt.values})
        cat_parts.append(tmp)
    cats = pd.concat(cat_parts, ignore_index=True)
    s = s.drop(columns=['size_tercile']).merge(cats, on=['stack','institution'], how='left')
    s = s.rename(columns={'new_size':'size_tercile'})
    return s


def report(label, stacks):
    r = re.fit_outcome(stacks, 'ln_licenses')
    print('VARIANT', label,
          'gap', round(r['gap'],6), 'se', round(r['gap_se'],6),
          'pre_p', round(r['pre_p'],6),
          'up', round(r['up'],6), 'down', round(r['down'],6), 'N', r['n'])
    print('  PATH', [(z['event_time'], round(z['gap'],4)) for z in r['path']])


def main():
    raw = pd.read_csv(re.RAW, low_memory=False)
    base = re.make_panel(raw)
    universe = re.revision_universe(raw)
    events = re.load_main_events()

    report('inst_mean_rank_current', re.make_stacks(base, universe, events))

    # Institution-level fixed variants.
    grp = base.groupby('institution', observed=True)['research_exp']
    variants = {
        'inst_median': grp.median(),
        'inst_first': grp.first(),
        'inst_1991_2000_mean': base[base.year.between(1991,2000)].groupby('institution')['research_exp'].mean(),
        'inst_1991_2005_mean': base[base.year.between(1991,2005)].groupby('institution')['research_exp'].mean(),
        'inst_2000_2010_mean': base[base.year.between(2000,2010)].groupby('institution')['research_exp'].mean(),
    }
    for label, vals in variants.items():
        p = fixed_inst(base, vals)
        report(label, re.make_stacks(p, universe, events))

    # Time-varying annual terciles.
    p = base.copy()
    p['size_tercile'] = p.groupby('year', group_keys=False)['research_exp'].apply(rank_tercile).astype('Int64')
    report('calendar_year_rank', re.make_stacks(p, universe, events))

    # Global observation-level expenditure cutpoints (time varying category).
    p = base.copy()
    cuts = p['research_exp'].quantile([1/3, 2/3]).to_numpy()
    p['size_tercile'] = np.select(
        [p.research_exp <= cuts[0], p.research_exp <= cuts[1]], [0,1], default=2)
    report('global_observation_cutpoints', re.make_stacks(p, universe, events))

    # Stack-specific categories based on values known around each event.
    base_stacks = re.make_stacks(base, universe, events)
    for mode in ['stack_pre_mean','stack_pre_median','stack_full_mean','stack_m1','stack_t0']:
        report(mode, stack_variant(base_stacks, mode))

if __name__ == '__main__':
    main()
