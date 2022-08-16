from helium import *
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# publicAddress = '0xc7f9f7acc3941cc0da9956410d0023fb936a6a09'
# publicAddress = '0xdac17f958d2ee523a2206206994597c13d831ec7'
publicAddress = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'

url = f'https://debank.com/profile/{publicAddress}'
browser = start_firefox(url, headless=False)
wait_until(lambda: browser.find_element(By.CLASS_NAME, "db-table-body"), timeout_secs=20)

soup = BeautifulSoup(browser.page_source, 'html.parser')
tableRows = soup.select('div.db-table-body .db-table-row')

tokensData = []
for row in tableRows:
    cells = row.select('div.db-table-cell')
    tokenName = cells[0].select('div:first-child > div:last-child')[0].text
    tokensData.append({
        "value": cells[-1].text,
        "token": tokenName
    })
browser.quit()
# print(tokensData)

url = f'https://coindix.com/?name={tokensData[0]["token"]}&kind=single&chain=ethereum'
browser = start_firefox(url, headless=False)
wait_until(lambda: browser.find_element(By.ID, "xdefivaults"), timeout_secs=20)

soup = BeautifulSoup(browser.page_source, 'html.parser')
tableRows = soup.select('#xdefivaults > tr:nth-child(-n+3)')

results = []
for row in tableRows:
    tds = row.select('td')

    result = {"tokens": [], "rewards": []}
    tokenElements = tds[1].select('div:first-child > div > div')
    for tokenElement in tokenElements:
        if tokenElement.text != "":
            result["tokens"].append(tokenElement.text)

    result["protocol"] = tds[2].select('div:first-child > div')[0].text
    result["network"] = tds[2].select('div:first-child > div')[1].text
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

    linkDiv = tds[10].select('div:first-child')[0]
    result["link"] = linkDiv["onclick"][11:-2]

    results.append(result)
    # print(row.prettify())
    # print('\n')

browser.quit()
print(results)
