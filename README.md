# dmp

This python script performs simple sorting and prioritizing on wildlife management unit (WMU) data in NY. 
The data is from 2016 and for the 2017 deer season. I used it to help me select units in
which to apply for deer management permits -- antlerless only bonus tags.

## Dependencies
```
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

[Pandas](https://pypi.python.org/pypi/pandas/0.20.3): "Powerful data structures for data analysis, time series, and statistics"

## Data
Two data files are used to generate tables of NY deer unit statistics.

### dmp.csv:
```
wmu  area    dmp_target  dmp_per_sq_mile  success_avg  res_1   res_2   nres_1  nres_2
1C   903.3   max         NA               12.8        HIGH    HIGH    HIGH    HIGH
3A   694.3   0           0.0              NA           NONE    NONE    NONE    NONE
3C   316.1   2000       6.3              13.9        MED     NONE    NONE    NONE
...
```

This file contains dmp-specific information.
 - wmu: wildlife management unit
 - area: total land area of the WMU in square miles
 - dmp_target: the target number of distributed dmp tags. 'max' indicates that the NY DEC will distribute as many as possible.
 - dmp_per_sq_mile: the dmp density for the WMU
 - success_avg: success average of dmp tags
 - res_1: first-choice resident tag selection chance
 - res_2: second-choice resident tag selection chance
 - nres_1: first-choice non-resident tag selection chance
 - nres_2: second-choice non-resident tag selection chance

Source data was hand transfered from the NY DEC website. A few vim macros normalized the dataset for analysis.
  - [DMP Availability and Probability of Selection](http://www.dec.ny.gov/outdoor/30409.html)

From the website, per NY DEC 2017:
```
Statewide Total: 625,300 excluding units without DMP targets.

High = more than 2/3 of applicants receive a DMP.
Medium = between 1/3 & 2/3 receive a DMP.
Low = less than 1/3 of applicants will receive a DMP.
PP Req = only applicants with preference points have a chance of receiving a DMP. May require 1, 2, or 3 preference points to be selected.
LO/DV = only qualifying landowners (greater than 50 acres) and veterans with disabilities will receive a DMP.
None = No DMPs are available.
NA = DEC is not authorized to issue DMPs in these units.
Notes:

    WMU 1C is bowhunting-only from October - December. A special permit is Required during the January Firearms Season.
    WMUs 3S, 4J, and 8C are bowhunting-only during all deer seasons.
    Antlerless-only Bonus DMPs are available in WMUs 1C, 3S, 4J, and 8C for hunters who fill a DMP in these units.
    Preference points increase the chances of selection but do not guarantee issuance. Preference points are won and lost on the 1st DMP selection. If preference points are required on the 2nd permit, only applicants who were denied a 1st permit are eligible.
    Qualifying landowners and veterans with disabilities will receive their 1st choice DMP in all open WMUs.
```

### total_taken.csv

```
wmu  bucks_taken  buck_sq_mile  total_deer  total_sq_mile
1C   1321         1.5           3207        3.6
3A   652          0.9           774         1.1
3C   692          2.2           1020        3.2
...
```

The total taken statistics file provides information about deer harvest in general (for 2016).
 - wmu: wildlife management unit
 - bucks_taken: the number of antlered deer harvested in the WMU
 - bucks_sq_mile: the antelered take density for the WMU
 - total_deer: The combined antlered/antlerless take count for the WMU
 - total_sq_mile: The combined take density for the WMU

Source data was hand transfered from the NY DEC website. A few vim macros normalized the dataset for analysis.
 - [Deer and Bear Harvests](http://www.dec.ny.gov/outdoor/42232.html)

From the 2016 harvest summary:

```
The values presented here are calculated estimates.
The precision of the statewide take estimate is within 1-2 percent.
```

## Usage

To be honest I mostly did some rough hacking via ipython :)

I've put together something a little more traditional too:

```
python -m dmp.py
```

As set up, dmp will return sorted tables of three measures:
  - an arbitrary-unit value 's1': (deer taken / sq mile) * (dmp success avg) * (num target dmps)
 
  - total combined take density.
  - dmps per square mile (5 if max total dmps)
    - the max dmps throw a wrench into the match, but 5 is a fair, perhaps conservative value

```
 python -m dmp


**** Sorted by s1: (deer taken / sq mile) * (dmp success avg) * (num target dmps)
       area dmp_target  dmp_per_sq_mile  success_avg res_1   res_2  bucks_taken  buck_sq_mile  total_deer  total_sq_mile        s1  dmps_sq_mile
wmu                                                                                                                                             
3M    749.2      35900             47.9         10.9  HIGH    HIGH         2880           3.8        6781            9.1  1.000000          47.9
7J    838.9      31300             37.3         11.0  HIGH    HIGH         2385           2.8        6164            7.3  0.705826          37.3
...

**** Sorted by deer taken / sq mile
       area dmp_target  dmp_per_sq_mile  success_avg   res_1   res_2  bucks_taken  buck_sq_mile  total_deer  total_sq_mile        s1  dmps_sq_mile
wmu                                                                                                                                               
3M    749.2      35900             47.9         10.9    HIGH    HIGH         2880           3.8        6781            9.1  1.000000          47.9
4C    164.8       1400              8.5         23.2     MED    NONE          725           4.4        1331            8.1  0.073882           8.5
...

**** Sorted by dmps per square mile (5 if max total dmps)
      area dmp_target  dmp_per_sq_mile  success_avg res_1 res_2  bucks_taken  buck_sq_mile  total_deer  total_sq_mile        s1  dmps_sq_mile
wmu                                                                                                                                          
4J   148.9        max              NaN          9.3  HIGH  HIGH          223           1.5         495            3.3  0.064165          50.0
3S   430.8        max              NaN          9.8  HIGH  HIGH          562           1.3        1259            2.9  0.171912          50.0
...
```
