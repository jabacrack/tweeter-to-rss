import twint
from feedgen.feed import FeedGenerator
from flask import Flask, Response
from markupsafe import escape
from urllib.parse import urlparse

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
    parts = url.split("/")
    code = parts[1]
    return f'<iframe width="480" height="270" src="https://www.youtube.com/embed/{code}" title="YouTube video player" ' \
           f'frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; ' \
           f'picture-in-picture" allowfullscreen></iframe> '


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
    for tweet in tweets:
        content = generate_content(tweet.tweet, tweet.photos, tweet.urls, tweet.link)

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


if __name__ == "__main__":
    rss = generate_rss("Mikeinelart", 20)
