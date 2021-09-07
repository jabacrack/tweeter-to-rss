import twint

user = "Mikeinelart"

twint_config = twint.Config()
twint_config.Username = user
twint_config.Store_object = True
twint_config.Limit = 60
twint.run.Search(twint_config)
tweets = twint.output.tweets_list

for tweet in tweets:
    a=1