import requests
import re
import matplotlib.pyplot as plt

years = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

bans2014 = {}
bans2015 = {}
bans2016 = {}
bans2017 = {}
bans2018 = {}
bans2019 = {}
bans2020 = {}
bans2021 = {}

bans = {
    2014: bans2014,
    2015: bans2015,
    2016: bans2016,
    2017: bans2017,
    2018: bans2018,
    2019: bans2019,
    2020: bans2020,
    2021: bans2021,
}

def getLogURL(year, month, day):
    URL = 'https://overrustlelogs.net/Destinygg%20chatlog/'
    URL += months[month - 1]
    URL += '%20'
    URL += str(year)
    URL += '/'
    URL += str(year)
    URL += '-'
    URL += str(month).zfill(2)
    URL += '-'
    URL += str(day).zfill(2)
    URL += '.txt'
    return URL

banRE = '\[[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} UTC\] Ban: \w+ banned'

for year in years:

    daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0:
        daysInMonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for monthIndex in range(len(months)):
        for day in range(1, daysInMonth[monthIndex] + 1):
            print(str(year) + ': ' + months[monthIndex] + ', ' + str(day))

            URL = getLogURL(year, monthIndex + 1, day)
            r = requests.get(URL)

            if (r.status_code != 200):
                print('Failure')
            else:
                lines = r.text.splitlines()
                for line in lines:
                    matches = re.findall(banRE, line)
                    # A real ban message should only be matched once
                    if (len(matches) == 1):
                        for ban in matches:
                            print(ban)
                            username = ban[len('[1234-56-78 04:20:69 UTC] Ban: '):][:-len(' banned')]
                            if username in bans[year]:
                                bans[year][username] += 1
                            else:
                                bans[year][username] = 1

topBans2014 = {}
topBans2015 = {}
topBans2016 = {}
topBans2017 = {}
topBans2018 = {}
topBans2019 = {}
topBans2020 = {}
topBans2021 = {}

topBans = {
    2014: topBans2014,
    2015: topBans2015,
    2016: topBans2016,
    2017: topBans2017,
    2018: topBans2018,
    2019: topBans2019,
    2020: topBans2020,
    2021: topBans2021
}

totalBans = {}

for year in years:
    #https://stackoverflow.com/questions/7197315/5-maximum-values-in-a-python-dictionary
    topBans[year] = sorted(bans[year], key=bans[year].get, reverse=True)[:10]

    plt.style.use('ggplot')
    plt.figure(figsize=(16,9))
    plt.rcParams.update({'font.size': 22})
    plt.subplots_adjust(left=0.3)
    plt.title('DGG bans in ' + str(year))
    plt.xlabel('Usernames')
    plt.ylabel('Bans')
    plt.barh(topBans[year], list(map(bans[year].get, topBans[year])))
    plt.savefig('dggBans' + str(year) + '.png')

    for username in bans[year]:
        if username in totalBans:
            totalBans[username] += bans[year][username]
        else:
            totalBans[username] = bans[year][username]

topTotalBans = sorted(totalBans, key=totalBans.get, reverse=True)[:10]

plt.style.use('ggplot')
plt.figure(figsize=(16,9))
plt.rcParams.update({'font.size': 22})
plt.subplots_adjust(left=0.3)
plt.title('Total DGG bans')
plt.xlabel('Usernames')
plt.ylabel('Bans')
plt.barh(topTotalBans, list(map(totalBans.get, topTotalBans)))
plt.savefig('dggBansTotal.png')