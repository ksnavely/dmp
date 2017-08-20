"""
dmp

Sorting and measures on deer harvest data from the NY DEC 2016
harvest summary.
"""
import pandas as pd
pd.set_option('expand_frame_repr', False)


DMP_FILE = "dmp.csv"
TOTAL_TAKEN_FILE = "total_taken.csv"
TOO_FAR_REGIONS = ["1", "2", "8", "9"] 
EXCLUSIONS = [
    "4T", # just tidal flats
    "7H", # no public land
    "6G" # very far away
]


def read_csv(filename):
  """
  read_csv

  Read a space delimited 'csv' file with Pandas
  """
  df = pd.read_csv(filename, delimiter='\s+')
  df = df.set_index("wmu")
  df.index.name = "wmu"
  return df


def filter_stats(df, include_pp_req=True):
  """
  Removing undesired data from our deer management permit
  dataset.
  """
  # remove non resident data
  del df["nres_1"]
  del df["nres_2"]

  # filter out PP_REQ areas
  if not include_pp_req:
      df = df[df["res_1"] != "PP_REQ"]

  # These regions are quite the drive from eastern NY
  for num in TOO_FAR_REGIONS:
      df = df[~df.index.str.startswith(num)]

  # These regions have been excluded for commented reasons
  for reg in EXCLUSIONS:
      df = df[~df.index.str.startswith(reg)]

  # filter out NA res_1 probability  
  df = df[~df["res_1"].isnull()]

  # filter out no dmps
  df = df[df["dmp_target"] != "0"]

  # filter out land-owner only stuff
  df = df[df["res_1"] != "LO/DV"]

  return df


def apply_sorting_indexes(df):
    def row_sort_indexes(row):
        # DMP target -- set max to 50 DMP/sq mile
        target_dmps = row["dmp_target"]
        target_dmps = 50 * float(row["area"]) if target_dmps == "max" else float(target_dmps)

        # DMP Success Average
        success_avg = float(row["success_avg"])

        # Total deer taken per square mile
        total_sq_mile = float(row["total_sq_mile"])

        # Create a 'sort factor' which we can manipulate to find
        # desireable deer areas
        s1 = total_sq_mile * success_avg * target_dmps

        dmps_sq_mile = row["dmp_per_sq_mile"]
        dmps_sq_mile = 50 if row["dmp_target"] == "max" else float(dmps_sq_mile)
        
        return pd.Series([s1, dmps_sq_mile], index=["s1", "dmps_sq_mile"])

    df = pd.concat([df, df.apply(row_sort_indexes, axis=1)], axis=1, join="inner")
    df["s1"] = df["s1"] / df["s1"].max()

    df = df.sort_values(["s1"], ascending=False)
    print("\n\n**** Sorted by s1: (deer taken / sq mile) * (dmp success avg) * (num target dmps)")
    print(df[:10])

    df = df.sort_values(["total_sq_mile"], ascending=False)
    print("\n\n**** Sorted by deer taken / sq mile")
    print(df[:10])

    df = df.sort_values(["dmps_sq_mile"], ascending=False)
    print("\n\n**** Sorted by dmps per square mile (5 if max total dmps)")
    print(df[:10])

    return df


def process_data():
    dmp_df = read_csv(DMP_FILE)
    taken_df = read_csv(TOTAL_TAKEN_FILE)

    if not dmp_df.index.equals(taken_df.index):
        raise Exception("Mismatched indexes!")

    df = pd.concat([dmp_df, taken_df], axis=1, join="inner")

    df = filter_stats(df)
    df = apply_sorting_indexes(df)

    return df

if __name__ == "__main__":
    df = process_data()
