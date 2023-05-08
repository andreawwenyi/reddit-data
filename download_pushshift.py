"""
The following code is modified from https://medium.com/@MaLiN2223/getting-data-from-pushshift-archives-b3bc0e487359
"""
import argparse
import os
from multiprocessing.dummy import Pool as ThreadPool

import tqdm
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

save_folder = "./data_in/"


def trigger_wget(file_type, url, year, month, ext):
    url = url.format(year, month, ext)
    output_file = f"{file_type}_{year}-{month}.{ext}"
    if os.path.exists(output_file):
        print("Skipping", url, "because", output_file, "exists")

    os.system(f"wget -O {save_folder}{output_file} {url}")


def thread_me(worker, jobs):
    pool = ThreadPool(6)
    for r in tqdm.tqdm(pool.imap_unordered(worker, jobs), total=len(jobs)):
        pass  # do nothing
    pool.close()
    pool.join()


def download_month_comments(yearmonth):
    year, month = yearmonth.split("-")
    url = "https://files.pushshift.io/reddit/comments/RC_{0}-{1}.{2}"
    ext = "zst"
    print("Downloading {0} - {1} - {2}".format(year, month, ext))
    trigger_wget("RC", url, year, month, ext)


def get_months_list(start_month, end_month):
    assert start_month < end_month

    month = start_month
    yms = [month]
    while month != end_month:
        next_month = (parse(month + "-01") + relativedelta(months=1)).strftime("%Y-%m")
        yms.append(next_month)
        month = next_month
    return yms


def collect_comments(start_month, end_month):
    thread_me(download_month_comments, get_months_list(start_month, end_month))


#
# def submissions(start_year, end_year):
#     def get_ext(year: int, month: int):
#         if year <= 2010:
#             return "xz"
#         if year <= 2014:
#             return "bz2"
#         if year <= 2016:
#             return "zst"
#         if year == 2017:
#             if month in [7, 11, 12]:
#                 return "xz"
#             else:
#                 return "bz2"
#         if year == 2018:
#             if month < 11:
#                 return "xz"
#             else:
#                 return "zst"
#         return "zst"
#
#     url_v1 = "https://files.pushshift.io/reddit/submissions/RS_{0}-{1}.{2}"
#     url_v2 = "https://files.pushshift.io/reddit/submissions/RS_v2_{0}-{1}.{2}"
#     jobs_input = list()
#     for year in range(start_year, end_year + 1):
#         for month in range(1, 13):
#             url = url_v2 if year <= 2010 else url_v1
#             ext = get_ext(year, month)
#             month = str(month) if month >= 10 else "0" + str(month)
#             print("Downloading {0} - {1} - {2}".format(year, month, ext))
#             trigger_wget("RS", url, year, month, ext)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", dest="t", action="store", required=True)
    parser.add_argument("--start-month", type=int, required=True)
    parser.add_argument("--end-month", type=int, required=True)
    args = parser.parse_args()
    if args.t == "S":
        # submissions(args.start_month, args.end_month)
        pass
    elif args.t == "C":
        collect_comments(args.start_month, args.end_month)
    else:
        print("ERROR", args.t)
