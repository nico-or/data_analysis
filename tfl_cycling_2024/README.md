# Transport for London Cycling Data

Exploratory Data Analysis of the Transport for London (TfL) Cycling trip data.

## Overview

The main goal is to apply the knowledge aquired during the [Google Data Analytics Professional Certificate](https://www.coursera.org/professional-certificates/google-data-analytics) course, while keeping it simple enough to fit in the plaintext format of a github repository.

I will analyze a single year worth of data, to limit the scope of the analysis while I test the format of publication.

I will work with the 2024 year data since is the most recent complete year as the time of writting.

I will be working mainly with:

| Tool                                   | Use                                |
| -------------------------------------- | ---------------------------------- |
| [DuckDB](https://duckdb.org/)          | Parse, clean and query the dataset |
| [Mermaid](https://mermaid.js.org/)     | General purpouse diagrams          |
| [Seaborn](https://seaborn.pydata.org/) | Complex plots                      |

## Data Descripton

The data source is the [Transport for London (TfL) Open Data](https://tfl.gov.uk/info-for/open-data-users/our-open-data), in particular, their [cycling section](https://cycling.data.tfl.gov.uk/).

The data is published aggregating 2 weeks of data per CSV file (2 per month, 24 in a year).

### Schema

Every record in the dataset has the following fields:

| Field                | Data Type  | Role      | Description                                          |
| -------------------- | ---------- | --------- | ---------------------------------------------------- |
| Number               | UINT       | PK        | Record ID                                            |
| Start date           | DATETIME   | Attribute | Start of trip timestamp                              |
| Start station number | VARCHAR(6) | FK        | Start station ID                                     |
| Start station        | STRING     | Attribute | Name of start station                                |
| End date             | DATETIME   | Attribute | End of trip timestamp                                |
| End station number   | VARCHAR(6) | FK        | End station ID                                       |
| End station          | STRING     | Attribute | Name of end station                                  |
| Bike number          | UINT       | FK        | Bike ID                                              |
| Bike model           | STRING     | Attribute | Type of bike                                         |
| Total duration       | STRING     | Attribute | Human-readable representation of Total duration (ms) |
| Total duration (ms)  | UINT       | Attribute | Bike trip lenght in miliseconds                      |

Some observations:

- The Station Number fields is encoded as a 6-character long 0 padded integer (123 becomes '00123'), so we will use a fixed length VARCHAR to store it instead of an UINT.
- The Bike model could be stored as an ENUM, but we will use a STRING to keep things simple.

### Download

Opening the [TfL cycling repositorty](https://cycling.data.tfl.gov.uk/) and executing the following script on the browser console will return an array with the desired 24 elements. After that, one could use many methods to actually download the CSV files.

```js
links = $$("a");
links.filter((e) => e.innerText.includes("2024.csv"));
```

To save disk space we compress eeach individual file using gzip.

```sh
ls data/*.csv | parallel -j 6 gzip -k {}
```

This reduces the dataset size from 1.4Gb to 300Mb.
