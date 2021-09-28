import tweepy
import pandas
import csv
import re #regular expression
import nltk
from nltk.corpus import stopwords
##nltk.download('stopwords')# Download stopwords
import textblob
from textblob import TextBlob
import sys



consumer_key = '1QRIUdf4Sx4xdMDc46nQ6vYZ3'
consumer_secret = '5tEVf8mm8dUjYftXiae9QERBDFiKXrVSWkjRm2jpfBNy0NRm1Q'
access_token = '1191719379186192384-Gn0pBMspYGX2BCQxqyZACjNtAQ67YL'
access_secret = 'WuVwxRsXdw9gtTK1OTWK7McCtAC7l8Y0BSfYEUhcYEWv0'
access_token_secret=access_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True )


non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
##print(x.translate(non_bmp_map))



def cleaning(tweet):
    ##Handle Emoticons and Emojis
    #HappyEmoticons
    emoticons_happy = set([
        ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
        ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
        '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
        'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
        '<3'
        ])
    
    #Sad Emoticons
    emoticons_sad = set([
        ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
        ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
        ':c', ':{', '>:\\', ';('
        ])
    
    ##Emoji patterns
    #combine sad and happy emoticons
    emoticons = emoticons_happy.union(emoticons_sad)
    
    emoji_pattern = re.compile("["
             u"\U0001F600-\U0001F64F"  # emoticons
             u"\U0001F300-\U0001F5FF"  # symbols & pictographs
             u"\U0001F680-\U0001F6FF"  # transport & map symbols
             u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
             u"\U00002702-\U000027B0"
             u"\U000024C2-\U0001F251"
             "]+", flags=re.UNICODE)

##    extract_link
##    regex = r' https?://[^\s<>"]+|www\.[^\s<>"]+ '
##    match = re.search(regex, tweet.full_text)
##    if match:
##        print("links: ", match)

    #replace consecutive non-ASCII characters with a space
    tweet1 = re.sub(r'[^\x00-\x7F]+|,Ä¶',' ', tweet)
##    print("a1             ",tweet1)

    #remove emojis from tweet
    tweet2 = emoji_pattern.sub(r'', tweet1)   
##    print("a2             ",tweet2)

    #utility function to clean tweet text by removing links, special characters using simple regex statements. 
    tweet3=re.sub("(@[A-Za-z0-9_]+)|([^0-9A-Za-z_ \t]) |(\w+:\/\/\S+)", " ", tweet2) 
##    print("a3             ",tweet3)

    #removing numbers
    tweet4= re.sub(" (\d+) | (\d+)(.)(\d+) ", ' ',tweet3) # number alone
    tweet5= re.sub("(\d+)", ' ',tweet4) # number attached
##    print("a4             ",tweet5)

    # removing some charachters 
####    tweet6= re.sub(".", ' ',tweet4) # !!!! remove all
    tweet6= re.sub("[\";:\|,~!=\-+#$%&*\(\)?\.\/]+", ' ',tweet5)
##    print("a5             ",tweet6)
   
    # Create a sublist of lower case words for each tweet
    words_in_tweet = tweet6.lower().split()
##    print("a5    ",words_in_tweet)

    stop_words = set(stopwords.words('english'))
    tweet_cleaned=''
    for word in words_in_tweet:
        if word not in stop_words:
            tweet_cleaned +=' '+ word       
##    print("a6    ",tweets_cleaned)

    return tweet_cleaned



KEYWORDS_ent=['entrepreneur']
LANG='en'
loc_list=['London']
print(loc_list)
KEYWORDS_mng=['manager']



##csvFile_Loc = open('list_ent_ld.csv', 'w',newline='')
##csvWriter = csv.writer(csvFile_Loc,delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
##csvWriter.writerow(["user_screen_name",
##                    "user_name",
##                    "user_id",
##                    "tweet",
##                    "location_profile",
##                    "profile_description"])
##

##csvFile_Loc = open('list_mng_ld.csv', 'w',newline='')
##csvWriter = csv.writer(csvFile_Loc,delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
##csvWriter.writerow(["user_screen_name",
##                    "user_name",
##                    "user_id",
##                    "tweet",
##                    "location_profile",
##                    "profile_description"])



search_term = "* -filter:retweets"
##search_term = "'#entrepreneur' OR business owner'' OR 'founded' OR 'founder'  -filter:retweets"

tweets = tweepy.Cursor(api.search,
                       q=search_term,
                       result_type="recent",
                       lang='en',
                       tweet_mode="extended",
                       geocode="51.507351,-0.127758,20km"
                       ).items()


# Collecting target tweets
n_total=0
n_ent=0
n_mng=0

for tweet in tweets:
    n_total +=1
##    print(tweet.full_text.translate(non_bmp_map))
##    print(tweet.user.screen_name.translate(non_bmp_map))

    in_loc=0
    for loc in loc_list:
        if loc.lower() in tweet.user.location.lower():
            in_loc +=1
    if  in_loc>0:
#        print(tweet.user.location.translate(non_bmp_map))
#        print(tweet)
#        print(tweet.metadata)


        words_in_description=cleaning(tweet.user.description)


        is_ent=0
#        print(tweet.user.description.translate(non_bmp_map))
#        print(words_in_description)
        for key in KEYWORDS_ent:
            if key in words_in_description:
#            if (' ' + key + ' ') in (' ' + tweet.user.description + ' ')
                is_ent = 1
#                print("ent")


        is_mng= 0        
        for key_not in   KEYWORDS_mng:
            if key_not in words_in_description:
                is_mng = 1
#                print("mng")


    
        if (is_ent == 1) and (is_mng == 0):
            n_ent +=1
            print("ent")
            csvFile_Loc = open('list_ent_ld.csv', 'a',encoding="utf-8",newline='')
            csvWriter = csv.writer(csvFile_Loc, delimiter=';' , quoting=csv.QUOTE_MINIMAL)
            csvWriter.writerow([tweet.user.screen_name.translate(non_bmp_map),
                               tweet.user.name.translate(non_bmp_map),
                               tweet.user.id,
                               tweet,
                               tweet.user.location.translate(non_bmp_map),
                               tweet.user.description])

        if (is_ent == 0) and (is_mng == 1):
            n_mng +=1
            print("mng")
            csvFile_Loc = open('list_mng_ld.csv', 'a',encoding="utf-8",newline='')
            csvWriter = csv.writer(csvFile_Loc, delimiter=';' , quoting=csv.QUOTE_MINIMAL)
            csvWriter.writerow([tweet.user.screen_name.translate(non_bmp_map),
                               tweet.user.name.translate(non_bmp_map),
                               tweet.user.id,
                               tweet,
                               tweet.user.location.translate(non_bmp_map),
                               tweet.user.description])
            
# end of "for" loop















