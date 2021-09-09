import twint
from datetime import datetime
from twint import tweet as tw


user = "SomeOnes_Tweet"

twint_config = twint.Config()
twint_config.Username = user
twint_config.Store_object = True
twint_config.Limit = 60
twint.run.Search(twint_config)
tweets = twint.output.tweets_list
tweets.sort(key=lambda x: datetime.strptime(x.datetime, tw.Tweet_formats['datetime']))

a=1
# for tweet in tweets:
#     a=1