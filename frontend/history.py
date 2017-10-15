"""
CoinMarketCap USD Price History

Print the CoinMarketCap USD price history for a particular cryptocurrency in CSV format.
"""
import sys
import re
from urllib.request import urlopen


def download_data(currency, start_year, end_year):
    """
    Download HTML price history for the specified cryptocurrency and time range from CoinMarketCap.
    """

    start_date = start_year + '0101'
    end_date = end_year + '1231'
    url = 'https://coinmarketcap.com/' + currency + \
        '/historical-data/' + '?start=' + start_date + '&end=' + end_date

    try:
        page = urlopen(url, timeout=10)
        if page.getcode() != 200:
            raise Exception('Failed to load page')
        html = page.read()
        page.close()

    except Exception as e:
        print('Error fetching price data from ' + url)
        print('Did you use a valid CoinMarketCap currency?\nIt should be entered exactly as displayed on CoinMarketCap.com (case-insensitive), with dashes in place of spaces.')

        if hasattr(e, 'message'):
            print("Error message: " + e.message)
        else:
            print(e)
        sys.exit(1)

    return html


def extract_data(html):
    """
    Extract the price history from the HTML.

    The CoinMarketCap historical data page has just one HTML table.  This table contains the data we want.
    It's got one header row with the column names.

    We need to derive the "average" price for the provided data.
    """

    head = re.search(r'<thead>(.*)</thead>', html.decode('utf-8'), re.DOTALL).group(1)
    header = re.findall(r'<th .*>([\w ]+)</th>', string=head)
    header.append('Average (High + Low / 2)')

    body = re.search(r'<tbody>(.*)</tbody>', html.decode('utf-8'), re.DOTALL).group(1)
    raw_rows = re.findall(
        r"<tr[^>]*>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*</tr>",
        string=body)

    # strip commas
    rows = []
    for row in raw_rows:
        table = str.maketrans(dict.fromkeys('b'))
        row = [field.translate(str.maketrans(table)) for field in row]
        rows.append(row)

    # calculate averages
    def append_average(row):
        high = float(row[header.index('High')])
        low = float(row[header.index('Low')])
        average = (high + low) / 2
        row.append('{:.2f}'.format(average))
        return row
    rows = [append_average(row) for row in rows]

    return header, rows
