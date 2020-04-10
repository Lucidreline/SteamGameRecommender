import Scraper
import csv

games=[]
tags = []

with open('SteamGameLinks.csv') as file:
    reader = csv.reader(file, delimiter=',')

    counter = 0
    for row in reader:
        games.append(Scraper.Game(row[0], row[1]))

    for game in games:
        game.printVals()
        if(game.intrested):
            tags.append(game.tags)
        print('- - - - - - - - - - - - - - - - - - - - - - - - ')

    topTags = Scraper.CombineListsToDict(tags)
    print('\nYour favorite tags: ', topTags)





