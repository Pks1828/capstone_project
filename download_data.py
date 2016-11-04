# http://real-chart.finance.yahoo.com/table.csv?s=ZEEL.NS&d=9&e=25&f=2016&g=d&a=6&b=1&c=2002&ignore=.csv
import os
import urllib
import time

# http://real-chart.finance.yahoo.com/table.csv?s=RL
def get_url(ticker, start_date = None, end_date = None):
    base_url = "http://real-chart.finance.yahoo.com/table.csv?s="
    return base_url+ticker



def download_file(url, filepath):
    '''
    Downloads the file from the given url
    Args:
        filepath: The Absolute or Relative path of file including filename and extension
        url: The url from which we need to download the data

    Returns:

    '''
    urllib.urlretrieve (url.replace("\\","/"), filepath)


def one_time_download(folder_path, index_name, index_file):
    dir_path = folder_path+index_name+"/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    f = open(index_file,"r")
    failed = []
    for line in f:
        ticker = line.split("\t")[0]
        if "&" in ticker:
            print ticker
        url = get_url(ticker)
        try:
            download_file(url, dir_path+ticker.replace("&","N")+".csv")
            print ("File Downloaded for : "+ticker+"; for index: "+index_name)
            time.sleep(1)
        except Exception as e:
            failed.append(ticker)
            print ("Error downloading ticker: "+ticker+" for index: "+index_name+": "+str(e))
    # Re Trying for Failed Ones
    if len(failed) > 0:
        # Wait for one minute
        time.sleep(60)
        for ticker in failed:
            url = get_url(ticker)
            try:
                download_file(url, dir_path+ticker.replace("&","N")+".csv")
                print ("File Downloaded for : "+ticker+"; for index: "+index_name)
                time.sleep(5)
            except Exception as e:
                print ("Error downloading ticker: "+ticker+" for index: "+index_name+": "+str(e))


one_time_download("stock_data/","SNP500","Indexes/SNP500.tsv")
one_time_download("stock_data/","FTSE100","Indexes/FTSE100.tsv")
one_time_download("stock_data/","NIFTY50","Indexes/NIFTY50.tsv")