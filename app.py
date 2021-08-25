import twint
from feedgen.feed import FeedGenerator
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


def generate_rss(user, amount):
    twint_config = twint.Config()
    twint_config.Username = user
    twint_config.Store_object = True

    if amount != 'all':
        twint_config.Limit = amount

    twint.run.Search(twint_config)
    tweets = twint.output.tweets_list

    fg = FeedGenerator()
    fg.id(f'https://twitter.com/{user}')
    fg.title(user)
    fg.link(href=f'https://twitter.com/{user}', rel='alternate')
    fg.description(f'Tweets feed for {user}')
    for tweet in tweets:
        pictures = [f'<img src={x}/>' for x in tweet.photos]
        pictures = "\n".join(pictures)
        # videos = [f'<a href={x} target="_blank"/>' for x in tweet.video]
        # videos = "\n".join(videos)
        source = f'<a href={tweet.link} target="_blank">source</a>'
        content = f'{tweet.tweet}\n{pictures}\n{source}'

        entry = fg.add_entry()
        entry.id(tweet.id_str)
        entry.title(tweet.name)
        entry.author({'name': tweet.name, 'email': 'noname@example.com'})
        entry.content(content)
    return fg.rss_str(pretty=True)


@app.route("/<name>/amount/<amount>")
def index(name, amount):
    return generate_rss(escape(name), escape(amount))


# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=8080, debug=True)
#     # rss = generate_rss("Mikeinelart", 20)

