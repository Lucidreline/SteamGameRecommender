from bs4 import BeautifulSoup
import csv
import requests
from collections import Counter

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}
cookies = {'birthtime': '568022401'}

class Game:
    def __init__(self, _storeLink, _intrested):
        self.intrested = True if int(_intrested) == 1 else False


        page = requests.get(_storeLink, headers=headers, cookies=cookies) #opens the link to the user's Steam game
        soup = BeautifulSoup(page.content, "lxml") # parses it so that we can extract what we need
        
        try:
            self.name = soup.find('div', class_='apphub_AppName').text.strip()
        except:
            print('Game coudnt be found')
            exit() # If I cant even find the game then I most likely cant find any data

        self.description = soup.find('div', class_='game_description_snippet').text.strip()
        self.tags = soup.find('div', class_='glance_tags popular_tags').text.strip().replace('\t', '').split('\r\n')
    
        if len(self.tags) > 0:
            self.tags[len(self.tags) - 1] = self.tags[len(self.tags) - 1][:-1] #removes the plus sign from the back of the last element

        reviewBlock = soup.find_all('div', class_='user_reviews_summary_row')
        if len(reviewBlock) == 2:
            # Game has both Recent and All reviews
            try:
                self.recentReviewStatus = reviewBlock[0].find('span', class_='game_review_summary').text.strip()
                self.recentReviewCount = int(reviewBlock[0].find('span', class_='responsive_hidden').text.strip()[1:][:-1].replace(',', '')) #gets review count and removes surrounding parenthesis
            except AttributeError: 
                self.recentReviewStatus = 'None'
                self.recentReviewCount = 0
                
            try:
                self.allReviewStatus = reviewBlock[1].find('span', class_='game_review_summary').text.strip()
                self.allReviewCount = int(reviewBlock[1].find('span', class_='responsive_hidden').text.strip()[1:][:-1].replace(',', '')) #gets review count and removes surrounding parenthesis
            except: 
                self.allReviewStatus = 'None'
                self.allReviewCount = 0
        else:
            # game only has 'All reviews' but not 'Recent Reviews'
            self.recentReviewStatus = 'None'
            self.recentReviewCount = 0
            try:
                self.allReviewStatus = reviewBlock[0].find('span', class_='game_review_summary').text.strip()
                self.allReviewCount = int(reviewBlock[0].find('span', class_='responsive_hidden').text.strip()[1:][:-1].replace(',', '')) #gets review count and removes surrounding parenthesis
            except: 
                self.allReviewStatus = 'None'
                self.allReviewCount = 0
        

        devRows = soup.find_all('div', class_='dev_row')
        self.developers = [element.text.strip() for element in devRows[0].find_all('a')]
        self.publishers = [element.text.strip() for element in devRows[1].find_all('a')]

        try:
            self.ratings = soup.find('p', class_='descriptorText').text.strip().split('\r\n')
        except AttributeError:
            self.ratings = []

        

    def printVals(self):
        print('\n\nName:', self.name)
        print('\nIntrested: Yes' if self.intrested else '\nIntrested: No')
        print('\nDescription:', self.description)
        print('\nRecent Reviews:', self.recentReviewStatus, self.recentReviewCount, '\nAll Reviews:', self.allReviewStatus, self.allReviewCount)
        print('\nTags:', self.tags)
        print('\nRatings:', self.ratings)
        print('\nDevelopers:', self.developers)
        print('\nPublishers:', self.publishers)


def PrepData():
    # Name, Description, 
    print('prep')

def CombineListsToDict(_listOfLists):
    combinedLists = []

    for list in _listOfLists:
        combinedLists.extend(list)
    
    mostCommonElements = dict(Counter(combinedLists).most_common())
    
    counter = 0
    flippedInOrderDict = {}
    for element in mostCommonElements:
        flippedInOrderDict[counter] = element
        counter = counter + 1
    return flippedInOrderDict







  
    
        