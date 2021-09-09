import twint
from twint import tweet as tw
from feedgen.feed import FeedGenerator
from flask import Flask, Response
from markupsafe import escape
from urllib.parse import urlparse, urljoin
from datetime import datetime, timezone

app = Flask(__name__)
image_exts = (".jpg", ".jpeg", ".png", ".gif")


def is_youtube(url):
    parts = urlparse(url)
    netloc = parts.netloc.removeprefix("www.")
    # return url.startswith(("youtu.be", "youtube.com"))
    return netloc.startswith("youtu.be")


def is_image(url):
    return url.endswith(image_exts)


def embed_url(url, title):
    return f'<a href="{url}"  target="_blank">{title}</a>'


def embed_picture(url):
    return f'<img src="{url}" />'


def embed_youtube(url):
    parts = urlparse(url)
    #parts = parts.path.split("/")
    #code = parts[1]
    video_url = f"https://www.youtube.com/embed{parts.path}"
    player = f'<iframe width="480" height="270" src="{video_url}" title="YouTube video player" ' \
           f'frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; ' \
           f'picture-in-picture" allowfullscreen></iframe> '
    return f'{embed_url(url, url)}<br/>{player}'


def generate_content(text, pictures, urls, source_link):
    pictures = [embed_picture(x) for x in pictures]
    unknown_urls = []
    for url in urls:

        if is_image(url):
            pictures.append(embed_picture(url))
        elif is_youtube(url):
            pictures.append(embed_youtube(url))
        else:
            unknown_urls.append(embed_url(url, url))
    pictures.extend(unknown_urls)
    pictures = "<br/>".join(pictures)
    source = embed_url(source_link, "source")
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
    tweets.sort(key=lambda x: datetime.strptime(x.datetime, tw.Tweet_formats['datetime']))
    for tweet in tweets:
        content = generate_content(tweet.tweet, tweet.photos, tweet.urls, tweet.link)
        pub_date = datetime.strptime(tweet.datetime, tw.Tweet_formats['datetime'])
        zone = datetime.now(timezone.utc).astimezone().tzinfo
        pub_date_with_zone = datetime.combine(pub_date.date(), pub_date.time(), zone)

        entry = fg.add_entry()
        entry.pubDate(pub_date_with_zone)
        entry.guid(guid=tweet.link, permalink=True)
        entry.title(tweet.name)
        entry.author({'name': tweet.name, 'email': 'noname@example.com'})
        entry.content(content)
    return fg.rss_str(pretty=True)


@app.route("/<name>/amount/<amount>")
def index(name, amount):
    xml = generate_rss(escape(name), escape(amount))
    return Response(xml, mimetype='text/xml')


if __name__ == "__main__":
    rss = generate_rss("Mikeinelart", 20)
