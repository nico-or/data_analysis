import duckdb
import seaborn as sns
import matplotlib.pyplot as plt

conn = duckdb.connect('trips.duckdb',config={
    'access_mode': 'READ_ONLY'
    })

query = """
SELECT
    (station_start_id == station_end_id) AS round_trip,
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
)
plt.savefig('plots/1_duration_hist_120_min.png')

# Trip duration histogram < 5 minutes
TIME_LIMIT = 5 # 5 minutes

plt.figure()
sns.histplot(
    data[data['duration_minutes'] < TIME_LIMIT],
    x='duration_minutes',
    stat='count',
)
plt.savefig('plots/1_duration_hist_5_min_raw.png')

# Trip duration histogram < 1 minute
TIME_LIMIT = 5 # 5 minutes

plt.figure()
sns.histplot(
    data[
        (data['duration_minutes'] <= TIME_LIMIT) &
        (data['round_trip'] == False)
    ],
    x='duration_minutes',
    stat='count',
)
plt.savefig('plots/1_duration_hist_5_min_clean.png')

# Trip duration histogram same start end
plt.figure()
sns.histplot(
    data[data['round_trip'] == True],
    x='duration_minutes',
    stat='count',
    log_scale=True
)
plt.savefig('plots/1_duration_hist_round_trip.png')

# Trip duration histogram
plt.figure()
sns.histplot(
    data,
    x='duration_minutes',
    hue='round_trip',
    stat='count',
    log_scale=True
)
plt.savefig('plots/1_duration_hist_round_trip_both.png')

# Trip duration histogram
plt.figure()
sns.histplot(
    data[data['round_trip'] == True],
    x='duration_minutes',
    stat='count',
    log_scale=True
)
plt.savefig('plots/1_duration_hist_round_trip_clean.png')