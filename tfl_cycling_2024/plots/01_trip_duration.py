import duckdb
import seaborn as sns
import matplotlib.pyplot as plt

conn = duckdb.connect('trips.duckdb',config={
    'access_mode': 'READ_ONLY'
    })

query = """
SELECT
    station_start_id,
    station_end_id,
    (duration_ms/(1000*60)) AS duration_minutes
FROM trips_raw;
"""

data = conn.execute(query).df()
conn.close()

# Trip duration histogram
plt.figure()
sns.histplot(
    data, x='duration_minutes',
    stat='count', log_scale=True
)
plt.savefig('plots/1_duration_hist_total.png')

# Trip duration histogram < 120 minutes
TIME_LIMIT = 120 # 2 hours

plt.figure()
sns.histplot(
    data[data['duration_minutes'] < TIME_LIMIT],
    x='duration_minutes',
    stat='count',
    binwidth=2,
)
plt.savefig('plots/1_duration_hist_120_min.png')

# Trip duration histogram < 5 minutes
TIME_LIMIT = 5 # 5 minutes

plt.figure()
sns.histplot(
    data[data['duration_minutes'] < TIME_LIMIT],
    x='duration_minutes',
    stat='count',
    binwidth=0.2,
)
plt.savefig('plots/1_duration_hist_5_min_raw.png')

# Trip duration histogram < 1 minute
TIME_LIMIT = 5 # 5 minutes

plt.figure()
sns.histplot(
    data[
        (data['duration_minutes'] <= TIME_LIMIT) &
        (data['station_start_id'] != data['station_end_id'])
    ],
    x='duration_minutes',
    stat='count',
    binwidth=0.2,
)
plt.savefig('plots/1_duration_hist_5_min_clean.png')