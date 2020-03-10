import pandas as pd
import matplotlib.pyplot as plt

data_url = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/'
            'csse_covid_19_data/csse_covid_19_time_series/')

confirmed_url = data_url + 'time_series_19-covid-Confirmed.csv'
deaths_url = data_url + 'time_series_19-covid-Deaths.csv'
recovered_url = data_url + 'time_series_19-covid-Recovered.csv'


class TimeSeriesData(pd.DataFrame):
    @classmethod
    def from_csv_url(cls, url):
        return cls(pd.read_csv(url, error_bad_lines=False))

    @property
    def countries(self):
        return sorted(set(self['Country/Region']))

    @property
    def num_countries(self):
        return len(countries)

    @property
    def dates(self):
        return pd.to_datetime(self.columns[4:])

    def by_country(self, country):
        data = self[self['Country/Region']==country]
        return pd.Series(data[data.columns[4:]].sum(),
                         index=self.dates)


confirmed = TimeSeriesData.from_csv_url(confirmed_url)
deaths = TimeSeriesData.from_csv_url(deaths_url)
recovered = TimeSeriesData.from_csv_url(recovered_url)

def plot_country(country, log=True):
    for df, color, label in [(confirmed, 'k', 'Confirmed'),
                             (deaths, 'r', 'Deaths'),
                             (recovered, 'g', 'Recovered')]:
        ax = df.by_country(country).plot(
            linewidth=2,
            marker='o',
            color=color,
            label=label
        )
    if log:
        ax.set_yscale('log')

    plt.title('COVID-19 cases in {}'.format(country))
    plt.legend()

def dash_data_by_country(country):
    data = []
    for df, color, label in [(confirmed, 'k', 'Confirmed'),
                             (deaths, 'r', 'Deaths'),
                             (recovered, 'g', 'Recovered')]:
        series = df.by_country(country)
        data.append(
            {'x': series.index.to_pydatetime(),
             'y': list(series.values),
             'name': label}
        )
    return data
