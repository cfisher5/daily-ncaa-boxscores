from scraper import scrape_box_scores, get_links

year = input('Please enter the year in this format: xxxx\n')
month = input('Please enter the month in this format: x\n')
day = input('Please enter the day in this format: x\n')

# Or if you want to run this as a daily script to get previous night's boxscores:
# yesterday = date.today() - timedelta(1)
# yesterdaytuple = yesterday.timetuple()
# year = yesterdaytuple[0]
# month = yesterdaytuple[1]
# day = yesterdaytuple[2]

links = get_links(year, month, day)
scrape_box_scores(links, year, month, day)