from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from html.parser import HTMLParser

from castle.research_sources import trusted_sources


class TextExtractor(HTMLParser):

    def __init__(self):

        super().__init__()

        self.parts = []
        self.ignore = False

    def handle_starttag(self, tag, attrs):

        if tag in ("script", "style", "noscript"):

            self.ignore = True

    def handle_endtag(self, tag):

        if tag in ("script", "style", "noscript"):

            self.ignore = False

    def handle_data(self, data):

        if not self.ignore:

            text = data.strip()

            if text:

                self.parts.append(text)

    def get_text(self):

        return " ".join(self.parts)


def is_trusted_source(source_url):

    for source in trusted_sources.values():

        if source["url"] == source_url:

            return True

    return False


def get_source_type(source_url):

    for source in trusted_sources.values():

        if source["url"] == source_url:

            if "llms.txt" in source_url:

                return "DOCUMENTATION_INDEX"

            return "WEBPAGE"

    return "UNKNOWN"


def fetch_source(source_url):

    if not is_trusted_source(source_url):

        return {
            "status": "BLOCKED",
            "content": "",
            "message": "Source is not in the trusted source library."
        }

    source_type = get_source_type(source_url)

    try:

        request = Request(
            source_url,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urlopen(request, timeout=15) as response:

            content = response.read().decode(
                "utf-8",
                errors="ignore"
            )

        if source_type == "WEBPAGE":

            parser = TextExtractor()

            parser.feed(content)

            content = parser.get_text()

        return {
            "status": "SUCCESS",
            "content": content,
            "message": "Trusted source retrieved successfully.",
            "source_type": source_type
        }

    except HTTPError as error:

        if error.code == 429:

            return {
                "status": "RATE_LIMITED",
                "content": "",
                "message": "The trusted source is temporarily rate limiting Castle.",
                "source_type": source_type
            }

        return {
            "status": "HTTP_ERROR",
            "content": "",
            "message": f"HTTP error {error.code}: {error.reason}",
            "source_type": source_type
        }

    except URLError as error:

        return {
            "status": "CONNECTION_ERROR",
            "content": "",
            "message": f"Connection error: {error.reason}",
            "source_type": source_type
        }

    except Exception as error:

        return {
            "status": "ERROR",
            "content": "",
            "message": str(error),
            "source_type": source_type
        }
def search_documentation(content, query, limit=5):

    if not content:

        return []

    query_words = [
        word.lower()
        for word in query.split()
        if word.strip()
    ]

    if not query_words:

        return []

    results = []

    for line in content.splitlines():

        line = line.strip()

        if not line:

            continue

        line_lower = line.lower()

        score = 0

        for word in query_words:

            if word in line_lower:

                score += 1

        if score > 0:

            results.append({
                "score": score,
                "entry": line
            })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:limit]

def run_research(question, source_name, source_url):

    result = {
        "question": question,
        "source": source_name,
        "url": source_url,
        "source_type": get_source_type(source_url),
        "status": "READY"
    }

    return result