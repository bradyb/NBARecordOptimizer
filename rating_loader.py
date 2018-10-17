import pandas as pd
import requests
import os

import nba_site_constants

def ScrapeURL(base_url, parameters):
    response = requests.get(baseURL, params=parameters, headers=user_agent_headers)
    response.raise_for_status()
    headers = response.json()['resultSets'][0]['headers']
    stats = response.json()['resultSets'][0]['rowSet']
    stats_df = pd.DataFrame(stats, columns=headers)
    stats_df['Season'] = parameters['Season']
    # stats_df.drop(['CFID', 'CFPARAMS'], axis=1, inplace=True)
    return stats_df



def main():
 	print 'hello beautiful'

if __name__ == "__main__":
    main()