import duckdb
import seaborn as sns
import matplotlib.pyplot as plt

conn = duckdb.connect('trips.duckdb',config={
    'access_mode': 'READ_ONLY'
    })

query = """
SELECT
bike_id,
COUNT(*) as use_count
FROM trips
GROUP BY bike_id
ORDER BY use_count DESC;
"""
df_bike_uses = conn.execute(query).df()

query = """
SELECT
MIN(date_start) AS first_use_date
FROM trips
GROUP BY bike_id;
"""
df_bike_first_date = conn.execute(query).df()

query = """
SELECT
COUNT(*) as use_count,
MIN(date_start) AS first_use_date
FROM trips
GROUP BY bike_id;
"""
df_bike_corr_1 = conn.execute(query).df()

conn.close()

# Bike use count histogram
plt.figure()
sns.histplot(
    df_bike_uses,
    x='use_count',
    stat='count',
)
plt.savefig('plots/2_bike_use_count.png')

# First trip date histogram
plt.figure()
sns.ecdfplot(
    df_bike_first_date,
    x='first_use_date',
)
plt.savefig('plots/2_bike_first_use_date.png')

# Correlation between use count and first use date
plt.figure()
g = sns.JointGrid(
    data=df_bike_corr_1,
    x='first_use_date',
    y='use_count')
g.plot(sns.scatterplot,sns.histplot, alpha=0.1),
plt.savefig('plots/2_bike_corr_1.png')
