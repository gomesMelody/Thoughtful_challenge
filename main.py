import time
import pandas as pd
from datetime import datetime

from scripts.seleniumClass import SeleniumConn

def search_latimes(search_phrase, period=1):
    """
    This function searches for news from Los Angeles Times website
    and downloads the news from the given period.

    Parameters
    ----------
    search_phrase : str
        The phrase to search for on the website
    period : int, optional
        The number of months to retrieve the news for, by default 1

    Returns
    -------
    None
    """
    # create an instance of the SeleniumConn class
    conn = SeleniumConn()

    # connect to the website and search for the given phrase
    conn.connect("https://www.latimes.com/")
    conn.search_for_phrase(search_phrase)

    # get the current month
    today = datetime.today()
    month = today.month

    # get the news for the given period
    news = []
    for i in range(period):
        if period <= 1:
            news.extend(conn.iterate_news_by_month(month,2024))
        else:
            news.extend(conn.iterate_news_by_month(month,2024))
            month -= 1

    # create a DataFrame from the news list
    news_df = pd.DataFrame(news)

    # add two columns to the DataFrame
    # the first column is the count of the search phrase
    # in the title and description
    news_df['count'] = (news_df['title'].str.count(search_phrase)+news_df['description'].str.count(search_phrase))

    # the second column is a boolean indicating if the description
    # contains monetary values
    news_df['has_money'] = (news_df['description'].str.contains(r'\$') 
                            | news_df['description'].str.contains(r'\USD') 
                            | news_df['description'].str.contains(r'\dollars') 
                            | news_df['tittle'].str.contains(r'\$') 
                            | news_df['tittle'].str.contains(r'\USD') 
                            | news_df['tittle'].str.contains(r'\dollars'))

    # save the DataFrame to an Excel file
    news_df.to_excel(f"output/results_{today.strftime('%Y-%m-%d')}_{search_phrase}_{period}_{datetime.now().timestamp()}.xlsx")

    # close the Selenium connection
    conn.close()

if __name__ == "__main__":
    search_latimes("covid", 2)