
import requests
import pandas as pd
import numpy as np
import re
import datetime as dt
import os
import timeit

# it's possible to parse the .dat file with SHFE data as json like this:

# def etl_json(response):
#     inside = response.json()["o_curinstrument"]
#     df = pd.json_normalize(inside)
#     df = df[["PRODUCTID", "DELIVERYMONTH", "CLOSEPRICE", "VOLUME", "OPENINTEREST"]]
#     ...cleaning, processing, etc...
#     return df

# but I found it takes at least 50% longer than regex:



# SHFE uses yyyymmdd
def format_date(date) -> str:
    date = date.strftime('%Y-%m-%d').replace('-','')
    return date



def request(date):

    session=requests.Session()
    response = session.get(
        url=f"https://www.shfe.com.cn/data/tradedata/future/dailydata/kx{date}.dat",
        headers= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",

        "Connection": "keep-alive"}
    )
    return response



def etl_regex(response, date):

    content = response.content.decode('utf_8-sig')

    if len(content) >= 100:
        tail = content[-100:]
    else:
        tail = content[:]

    matches = re.findall(r'"(?i:report_date)"\s*:\s*"([^"]*)"', tail)
    if not matches:
        raise Exception("report date not found")

    report_date = matches[0]
    # print(f"report date = {report_date}")
    assert int(report_date) == int(date), "SHFE futures report date does not match desired (url) date. Check report date to see why it's different from url / menus."
    # the only string type
    product_id=re.findall(r'"PRODUCTID"\s*:\s*"([^"]*)"', content)

    # all other types are floats
    delivery_month=re.findall(r'"(?i:DELIVERYMONTH)"\s*:\s*"([^"]*)"', content)
    close_price=re.findall(r'"(?i:CLOSEPRICE)"\s*:\s*(\d*)', content)
    volume=re.findall(r'"(?i:VOLUME)"\s*:\s*(\d*)', content)
    open_interest=re.findall(r'"(?i:OPENINTEREST)"\s*:\s*(\d*)', content)


    df = pd.DataFrame({
        "product_id": pd.Series(product_id, dtype='str'),
        "transaction_date": pd.Series([date for _ in range(len(product_id))], dtype= 'str'),  # fill whole column with the same date
        "delivery_month": pd.Series(delivery_month, dtype='str'),
        "close_price": pd.Series(close_price, dtype='str'),
        "volume": pd.Series(volume, dtype='str'),
        "open_interest": pd.Series(open_interest, dtype='str')
        })


    df = df.replace(r'^\s*$', np.nan, regex=True)
    df = df[df["delivery_month"] != "小计"]
    df = df.dropna()

    df = df.astype({
        "delivery_month": int,
        "close_price": float,
        "volume": float,
        "open_interest": float})

    return df


def main():

    db = pd.DataFrame()

    start_date = pd.to_datetime("2026-01-29")
    end_date = pd.to_datetime("2026-01-29")


    n_days = (end_date - start_date).days + 1

    date = start_date
    timer_start = timeit.default_timer()


    for i in range(0, n_days):

        current_date=format_date(date)

        print(f"requested date = {current_date}", end="")

        response=request(current_date)

        if response.status_code == 200:
            try:
                df = etl_regex(response, current_date)
                db = pd.concat([db, df], ignore_index=True)
                print(f" -> {response.status_code} -> successfully parsed ({i+1}/{n_days})")
            except:
                print(f" -> {response.status_code} -> shfe returned empty list ({i+1}/{n_days})")

        elif response.status_code == 404:
            print(f" -> {response.status_code} -> no trades found (weekend or trading holiday) ({i+1}/{n_days})")

        date += dt.timedelta(days=1)  # go to next day regardless of status code

    # print(timeit.timeit(lambda: etl_json(response), number=1000))
    # print(timeit.timeit(lambda: etl_regex(response, date), number=1000))

    timer_end = timeit.default_timer()
    print(f"Extracted {db.shape[0]} rows in {timer_end - timer_start:.2f} seconds")

    # robust file save noodle
    filename = f"shfe-{format_date(start_date)}-{format_date(end_date)}-{n_days}days"
    try:
        db.to_csv(f"{filename}.csv")
    except:
        i=1
        while i<100:
            try:
                db.to_csv(f"{filename}({i}).csv")
                break
            except:
                i+=1
    print(f"Saved as {filename}.csv")




if __name__ == "__main__":
    main()
