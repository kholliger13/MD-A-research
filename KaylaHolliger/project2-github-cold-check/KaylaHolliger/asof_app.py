"""Run: .venv/bin/python -m streamlit run asof_app.py"""
from datetime import date
from io import StringIO
import re
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd
import streamlit as st

SERIES = {
    'BAA': "Moody's Baa corporate bond yield",
    'FEDFUNDS': 'Federal funds rate',
    'DGS10': '10-year Treasury yield',
    'MORTGAGE30US': '30-year mortgage rate',
}


def parse_csv(content, series, vintage=None):
    frame = pd.read_csv(StringIO(content), na_values=['.'], dtype=str)
    expected_value = series if vintage is None else f"{series}_{vintage:%Y%m%d}"
    returned_vintage = None
    valid_value_column = len(frame.columns) == 2 and frame.columns[1] == expected_value
    if vintage is not None and len(frame.columns) == 2:
        match = re.fullmatch(re.escape(series) + r'_(\d{8})', frame.columns[1])
        if match:
            returned_vintage = pd.to_datetime(match.group(1), format='%Y%m%d').date()
            valid_value_column = returned_vintage <= vintage
    if (len(frame.columns) != 2 or frame.columns[0] not in ('DATE', 'observation_date')
            or not valid_value_column):
        raise ValueError('The download is not the requested FRED series/vintage CSV.')
    frame.columns = ['Date', 'Value']
    frame['Date'] = pd.to_datetime(frame['Date'], errors='raise')
    frame['Value'] = pd.to_numeric(frame['Value'], errors='raise')
    if frame['Date'].isna().any() or frame['Date'].duplicated().any():
        raise ValueError('The download contains missing or duplicate dates.')
    if frame['Value'].isin([float('inf'), float('-inf')]).any():
        raise ValueError('The download contains infinite values.')
    frame = frame.set_index('Date').sort_index()
    frame.attrs['returned_vintage'] = returned_vintage
    return frame


@st.cache_data(show_spinner=False, max_entries=256)
def download_today(series, downloaded_on):
    """One public FRED CSV request; the date key renews the cache daily."""
    url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?' + urlencode({'id': series})
    with urlopen(url, timeout=40) as response:
        content = response.read().decode('utf-8-sig')
    return parse_csv(content, series)


@st.cache_data(show_spinner=False, max_entries=256)
def download_asof(series, vintage, downloaded_on):
    """One public ALFRED CSV request for the selected historical vintage."""
    url = 'https://alfred.stlouisfed.org/graph/alfredgraph.csv?' + urlencode(
        {'id': series, 'vintage_date': vintage.isoformat()})
    with urlopen(url, timeout=40) as response:
        content = response.read().decode('utf-8-sig')
    frame = parse_csv(content, series, vintage)
    return frame.loc[frame.index <= pd.Timestamp(vintage)]


def comparison(series, current, historical):
    current = current['Value'].dropna()
    historical = historical['Value'].dropna()
    last_then = historical.index[-1] if not historical.empty else None
    common = current.index.intersection(historical.index)
    return {
        'Series': f'https://fred.stlouisfed.org/series/{series}',
        'Last measured date · as known then': last_then,
        'Value · as known then': historical.iloc[-1] if last_then is not None else None,
        'Last measured date · today': current.index[-1] if not current.empty else None,
        'Value · today': current.iloc[-1] if not current.empty else None,
        'Newer values today': int((current.index > last_then).sum()) if last_then is not None else None,
        'Revised values on shared dates': int((current.loc[common] != historical.loc[common]).sum()),
    }


def main():
    st.set_page_config(page_title='Interest Rates · As Known', layout='wide')
    today = date.today()
    st.title('Interest Rates · As Known')
    st.caption(f'Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today ({today:%B %d, %Y}); built with AI help, a learning demonstration, not investment advice.')
    selected = st.sidebar.multiselect('Series', list(SERIES), default=list(SERIES),
                                      format_func=lambda s: f'{s} — {SERIES[s]}')
    extra = st.sidebar.text_input('Add another FRED series ID', value='PAYEMS', placeholder='PAYEMS', key='extra_id').strip().upper()
    if extra:
        if re.fullmatch(r'[A-Z0-9_.-]+', extra):
            if extra not in selected:
                selected.append(extra)
        else:
            st.sidebar.error('Enter a FRED series ID, such as PAYEMS.')
    start = st.sidebar.date_input('Start date', date(2020, 1, 1), max_value=today)
    vintage = st.sidebar.date_input('As known on', today, max_value=today, key='asof_date')
    rows = []
    for series in selected:
        st.subheader(f'{series} · {SERIES.get(series, series)}')
        try:
            with st.spinner(f'Downloading {series}…'):
                current = download_today(series, today)
                historical = download_asof(series, vintage, today)
            displayed = current.loc[current.index >= pd.Timestamp(start)]
            if displayed['Value'].notna().any():
                st.line_chart(displayed, x_label='Date measured', y_label='Value')
            else:
                st.info('No nonmissing values on or after the start date.')
            row = comparison(series, current, historical)
            last_then = row['Last measured date · as known then']
            st.caption(f"Last measured date in the data known on {vintage:%Y-%m-%d}: "
                       + (f'{last_then:%Y-%m-%d}' if last_then is not None else 'no available value'))
            returned_vintage = historical.attrs.get('returned_vintage')
            if returned_vintage and returned_vintage != vintage:
                st.caption(f'ALFRED returned a snapshot labeled {returned_vintage:%Y-%m-%d} for the requested {vintage:%Y-%m-%d} cutoff.')
            rows.append(row)
        except Exception as exc:
            st.error(f'{series}: could not load this series. Check the ID or try again. {exc}')
            rows.append({'Series': f'https://fred.stlouisfed.org/series/{series}'})
    if rows:
        st.subheader('Then and today')
        st.dataframe(pd.DataFrame(rows), hide_index=True, width='stretch', column_config={
            'Series': st.column_config.LinkColumn('Series', display_text=r'https://fred\.stlouisfed\.org/series/(.*)'),
            'Last measured date · as known then': st.column_config.DateColumn(format='YYYY-MM-DD'),
            'Last measured date · today': st.column_config.DateColumn(format='YYYY-MM-DD'),
            'Newer values today': st.column_config.NumberColumn(format='%d'),
            'Revised values on shared dates': st.column_config.NumberColumn(format='%d'),
        })
        st.caption('Counts use nonmissing observations across the full downloaded history. Revisions compare values only where both downloads have a value on the same measured date. Without a historical value, the newer-value count is unavailable. Observation dates label measured periods; they are not publication timestamps.')
    else:
        st.info('Select a series or enter another FRED series ID.')


if __name__ == '__main__':
    main()
