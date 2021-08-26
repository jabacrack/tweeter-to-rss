import twint
from feedgen.feed import FeedGenerator
from flask import Flask, Response
from markupsafe import escape

app = Flask(__name__)


def generate_content(text, pictures, source_link):
    pictures = [f'<img src={x}/>' for x in pictures]
    pictures = "<br/>".join(pictures)
    source = f'<a href={source_link} target="_blank">source</a>'
    content = f'{text}<br/>{pictures}<br/>{source}'
    return content


def generate_rss(user, amount):
    twint_config = twint.Config()
    twint_config.Username = user
    twint_config.Store_object = True

    if amount != 'all':
        twint_config.Limit = amount

    twint.run.Search(twint_config)
    tweets = twint.output.tweets_list

    fg = FeedGenerator()
    fg.title(user)
    fg.link(href=f'https://twitter.com/{user}', rel='alternate')
    fg.description(f'Tweets feed for {user}')
    for tweet in tweets:
        content = generate_content(tweet.tweet, tweet.photos, tweet.link)

        entry = fg.add_entry()
        entry.guid(guid=tweet.link, permalink=True)
        entry.title(tweet.name)
        entry.author({'name': tweet.name, 'email': 'noname@example.com'})
        entry.content(content)
    return fg.rss_str(pretty=True)


@app.route("/<name>/amount/<amount>")
def index(name, amount):
    xml = generate_rss(escape(name), escape(amount))
    return Response(xml, mimetype='text/xml')


# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=8080, debug=True)
#     # rss = generate_rss("Mikeinelart", 20)

