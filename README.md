Scraper for Shanghai Futures Exchange price/volume data from their Daily Express section, which covers:

| code      | product |
| ----------- | ----------- |
| cu_f  |  copper |
| al_f  |  aluminium |
| zn_f  |  zinc |
| pb_f  |  lead|
|au_f  |  gold|
|ag_f  |  silver|
|rb_f   | steel rebar|
|wr_f  |  steel wire rod|
|hc_f  |  hot rolled coils|
|fu_f  |  fuel oil|
|bu_f  |  bitumen|
|ru_f   | natural rubber|
|ni_f   | nickel|
|sn_f  |  tin|
|sc_f  |  crude oil|
|sp_f  |  woodpulp|
|ss_f  |  stainless steel|
|nr_f  |  TSR 20 |
|lu_f  |  LSFO |
|bc_f  |  bare copper|
|ec_f  |  SCFIS(Europe) |
|ao_f  |  aluminium oxide|
|br_f  |  synthetic rubber|
|ad_f   | cast aluminium alloy|
|op_f  |  offset paper|

See `sample data.csv`.

Inspired by [je-suis-tm](https://github.com/je-suis-tm/web-scraping) who showed us a clever .dat file trick but unfortunately stopped maintaining his scraper, so I built my own.



## Usage
pip install -r requirements.txt <br />

set `start_date` and `end_date` and run `shfe.py`
