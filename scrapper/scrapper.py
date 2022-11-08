from helium import *
from bs4 import BeautifulSoup

# publicAddress = '0xc7f9f7acc3941cc0da9956410d0023fb936a6a09'
# publicAddress = '0xdac17f958d2ee523a2206206994597c13d831ec7'
# publicAddress = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'


def getScrappedData(publicAddress):
    url = f'https://debank.com/profile/{publicAddress}'
    browser = start_firefox(headless=True)
    go_to(url)
    wait_until(S(".HeaderInfo_changeInfo__3exlY").exists, timeout_secs=1800)

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    assetsAmountElement = soup.select_one('.HeaderInfo_totalAssetInner__1mOQs')
    assetsAmountElement.select_one('.HeaderInfo_changeInfo__3exlY').decompose()

    if assetsAmountElement.text == '$0':
        kill_browser()
        return 'no-assets'

    wait_until(S(".db-table-body").exists, timeout_secs=1800)
    tableRows = soup.select('div.db-table-body .db-table-row')

    tokensData = []
    for row in tableRows:
        cells = row.select('div.db-table-cell')
        tokenName = cells[0].select('div:first-child > div:last-child')[0].text
        tokensData.append({
            "value": cells[-1].text,
            "token": tokenName
        })
    # print(tokensData)

    # url = f'https://coindix.com/?name={tokensData[0]["token"]}&kind=single&chain=ethereum'
    url = f'https://nanoly.com/ethereum-kind:single-name:{tokensData[0]["token"]}'
    go_to(url)
    wait_until(S("#xdefivaults > tr:first-child").exists, timeout_secs=1800)

    soup = BeautifulSoup(browser.page_source, 'html.parser')

    tableRows = soup.select('#xdefivaults > tr:nth-child(-n+3)')
    if len(tableRows) == 0:
        tableRows = soup.select('#xdefivaults > tr:nth-child(-n+2)')
        if len(tableRows) == 0:
            tableRows = soup.select('#xdefivaults > tr:nth-child(1)')
            if len(tableRows) == 0:
                kill_browser()
                return 'no-assets'

    results = []
    for row in tableRows:
        tds = row.select('td')

        result = {"tokens": [], "rewards": []}
        tokenElements = tds[1].select('a:first-child > div > div')
        for tokenElement in tokenElements:
            if tokenElement.text != "":
                result["tokens"].append(tokenElement.text)

        result["protocol"] = tds[2].select('a > div')[0].text
        result["network"] = tds[2].select('a > div')[1].text
        result["base"] = tds[3].text
        result["reward"] = tds[4].text

        rewardElements = tds[6].select('.reward')
        for rewardElement in rewardElements:
            result["rewards"].append(rewardElement.text)

        result["APY"] = tds[7].text
        result["TVL"] = tds[9].text

        tvl_value = float(result["TVL"][1:].replace(',', ''))
        if tvl_value > 1000000:
            result["risk"] = "low"
        elif tvl_value > 500000:
            result["risk"] = "medium"
        else:
            result["risk"] = "high"

        result["link"] = tds[10].select('a')[0]["href"]

        results.append(result)
        # print(row.prettify())
        # print('\n')

    kill_browser()
    return results


# print(getScrappedData(publicAddress))
