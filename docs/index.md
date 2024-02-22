---
toc: false
---

<style>

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  margin: 4rem 0 8rem;
  text-wrap: balance;
  text-align: center;
}

.hero h1 {
  margin: 2rem 0;
  max-width: none;
  font-size: 14vw;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(30deg, var(--theme-foreground), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero h2 {
  margin: 0;
  max-width: 34em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
}

</style>

<div class="hero">
  <h1>Sea Surface Temperature Anomalies</h1>
</div>

---

# Quick Guide to Plotting

Unfortunately, due to complex nature of the data ingestion, we cannot take advantage of Oberservable Framework's dynamic data loaders.

Instead, we must run the `ssta.json.py` data loader before running or building our notebook.

To accomplish this:

1. Ensure you have Python and [Poetry](https://python-poetry.org/) installed.

2. Run `poetry install` in the root of the project directory.

In `ssta.json.py`, you'll find a block of code:

```python
# You may configure these values yourself ###########
#
# Set the region of interest
LONGITUDE_MIN = -91.837959
LONGITUDE_MAX = -81.837959
LATITUDE_MIN = 13.837959
LATITUDE_MAX = 18.837959
#
# Set the start and end dates (use YYYY-MM-DD format)
START_DATE = "2023-11-21"
END_DATE = "2023-11-26"
#
#####################################################
```

Replace each value with your own.

Once saved, you may now run:

```sh
poetry run python docs/ssta.json.py
```

in the root of the project directory.

> Note: Depending on how large your region of interest or your time range is, this may take some time.

Once complete, you can now run or build this notebook as you would any Observable Framework notebook.
