from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from html.parser import HTMLParser
from pathlib import Path
from datetime import datetime
import json
import re

from castle.research_sources import trusted_sources


CACHE_DIR = Path("castle") / "research_cache"


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "does",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "what",
    "why",
    "with",
}


RESEARCH_CONCEPTS = {
    "privacy": {
        "privacy",
        "private",
        "privacy-preserving",
        "confidential",
        "confidentiality",
    },

    "disclosure": {
        "disclosure",
        "disclose",
        "disclosing",
        "selective",
    },

    "protection": {
        "protect",
        "protection",
        "protected",
        "security",
        "secure",
    },

    "identity": {
        "identity",
        "identities",
        "credential",
        "credentials",
    },

    "verification": {
        "verify",
        "verification",
        "verified",
        "prove",
        "proof",
        "proofs",
    },

    "smart_contracts": {
        "smart",
        "contract",
        "contracts",
        "compact",
    },
}


def normalise_text(text):

    text = text.lower()

    text = text.replace(
        "privacy-preserving",
        "privacy preserving"
    )

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def tokenise(text):

    normalised = normalise_text(text)

    return [
        word
        for word in normalised.split()
        if word and word not in STOP_WORDS
    ]


def word_variants(word):

    variants = {
        word
    }

    if word.endswith("ies") and len(word) > 4:

        variants.add(
            word[:-3] + "y"
        )

    if word.endswith("ing") and len(word) > 5:

        variants.add(
            word[:-3]
        )

    if word.endswith("ed") and len(word) > 4:

        variants.add(
            word[:-2]
        )

    if word.endswith("s") and len(word) > 3:

        variants.add(
            word[:-1]
        )

    return variants


def get_concepts_for_word(word):

    concepts = []

    for concept, words in RESEARCH_CONCEPTS.items():

        if word in words:

            concepts.append(
                concept
            )

    return concepts


class TextExtractor(HTMLParser):

    def __init__(self):

        super().__init__()

        self.parts = []
        self.ignore = False

    def handle_starttag(self, tag, attrs):

        if tag in (
            "script",
            "style",
            "noscript"
        ):

            self.ignore = True

    def handle_endtag(self, tag):

        if tag in (
            "script",
            "style",
            "noscript"
        ):

            self.ignore = False

    def handle_data(self, data):

        if not self.ignore:

            text = data.strip()

            if text:

                self.parts.append(text)

    def get_text(self):

        return " ".join(
            self.parts
        )


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
            "message": (
                "Source is not in the trusted source library."
            )
        }

    source_type = get_source_type(
        source_url
    )

    try:

        request = Request(
            source_url,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urlopen(
            request,
            timeout=15
        ) as response:

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
            "message": (
                "Trusted source retrieved successfully."
            ),
            "source_type": source_type
        }

    except HTTPError as error:

        if error.code == 429:

            return {
                "status": "RATE_LIMITED",
                "content": "",
                "message": (
                    "The trusted source is temporarily "
                    "rate limiting Castle."
                ),
                "source_type": source_type
            }

        return {
            "status": "HTTP_ERROR",
            "content": "",
            "message": (
                f"HTTP error {error.code}: {error.reason}"
            ),
            "source_type": source_type
        }

    except URLError as error:

        return {
            "status": "CONNECTION_ERROR",
            "content": "",
            "message": (
                f"Connection error: {error.reason}"
            ),
            "source_type": source_type
        }

    except Exception as error:

        return {
            "status": "ERROR",
            "content": "",
            "message": str(error),
            "source_type": source_type
        }


def create_cache_metadata(
    cache_file,
    source_url=None
):

    metadata_file = cache_file.with_suffix(
        cache_file.suffix + ".json"
    )

    if source_url is None:

        source_url = (
            "https://docs.midnight.network"
        )

    metadata = {
        "source": source_url,
        "source_type": get_source_type(
            source_url
        ),
        "cache_file": str(cache_file),
        "size_bytes": cache_file.stat().st_size,
        "updated_at": datetime.fromtimestamp(
            cache_file.stat().st_mtime
        ).astimezone().isoformat()
    }

    metadata_file.write_text(
        json.dumps(
            metadata,
            indent=4
        ),
        encoding="utf-8"
    )

    return metadata


def cache_source(
    source_url,
    cache_name
):

    if not is_trusted_source(source_url):

        return {
            "status": "BLOCKED",
            "message": (
                "Source is not in the trusted source library."
            ),
            "cache_file": ""
        }

    result = fetch_source(
        source_url
    )

    if result["status"] != "SUCCESS":

        return {
            "status": result["status"],
            "message": result["message"],
            "cache_file": ""
        }

    CACHE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    cache_file = CACHE_DIR / cache_name

    cache_file.write_text(
        result["content"],
        encoding="utf-8"
    )

    metadata_file = cache_file.with_suffix(
        cache_file.suffix + ".json"
    )

    metadata = {
        "source": source_url,
        "source_type": result["source_type"],
        "cache_file": str(cache_file),
        "size_bytes": cache_file.stat().st_size,
        "updated_at": datetime.now().astimezone().isoformat()
    }

    metadata_file.write_text(
        json.dumps(
            metadata,
            indent=4
        ),
        encoding="utf-8"
    )

    return {
        "status": "CACHED",
        "message": (
            "Trusted documentation saved "
            "to Castle's local cache."
        ),
        "cache_file": str(cache_file),
        "source": source_url,
        "source_type": result["source_type"],
        "metadata_file": str(metadata_file)
    }


def load_cached_source(cache_name):

    cache_file = CACHE_DIR / cache_name

    if not cache_file.exists():

        return {
            "status": "NOT_FOUND",
            "content": "",
            "message": (
                "No cached documentation found."
            )
        }

    content = cache_file.read_text(
        encoding="utf-8"
    )

    return {
        "status": "SUCCESS",
        "content": content,
        "message": (
            "Cached documentation loaded successfully."
        ),
        "cache_file": str(cache_file)
    }


def get_cache_metadata(cache_name):

    cache_file = CACHE_DIR / cache_name

    metadata_file = cache_file.with_suffix(
        cache_file.suffix + ".json"
    )

    if not cache_file.exists():

        return {
            "status": "NOT_FOUND",
            "message": (
                "No cached documentation found."
            ),
            "metadata": {}
        }

    if not metadata_file.exists():

        try:

            metadata = create_cache_metadata(
                cache_file
            )

            return {
                "status": "REPAIRED",
                "message": (
                    "Cache metadata was missing and "
                    "has been rebuilt from the local cache."
                ),
                "metadata": metadata
            }

        except Exception as error:

            return {
                "status": "METADATA_ERROR",
                "message": str(error),
                "metadata": {}
            }

    try:

        metadata = json.loads(
            metadata_file.read_text(
                encoding="utf-8"
            )
        )

        return {
            "status": "SUCCESS",
            "message": (
                "Cache metadata loaded successfully."
            ),
            "metadata": metadata
        }

    except Exception as error:

        return {
            "status": "METADATA_ERROR",
            "message": str(error),
            "metadata": {}
        }


def search_documentation(
    content,
    query,
    limit=5
):

    if not content:

        return []

    query_tokens = tokenise(
        query
    )

    if not query_tokens:

        return []

    query_concepts = set()

    for query_word in query_tokens:

        for concept in get_concepts_for_word(
            query_word
        ):

            query_concepts.add(
                concept
            )

    results = []

    for line_number, line in enumerate(
        content.splitlines(),
        start=1
    ):

        line = line.strip()

        if not line:

            continue

        line_tokens = tokenise(
            line
        )

        if not line_tokens:

            continue

        line_normalised = normalise_text(
            line
        )

        score = 0
        matched_words = []
        matched_concepts = []

        for query_word in query_tokens:

            variants = word_variants(
                query_word
            )

            matched = False

            for variant in variants:

                if variant in line_tokens:

                    matched = True
                    break

            if matched:

                score += 1

                matched_words.append(
                    query_word
                )

        line_concepts = set()

        for line_word in line_tokens:

            for concept in get_concepts_for_word(
                line_word
            ):

                line_concepts.add(
                    concept
                )

        shared_concepts = (
            query_concepts
            & line_concepts
        )

        if shared_concepts:

            score += (
                len(shared_concepts)
                * 1
            )

            matched_concepts = sorted(
                shared_concepts
            )

        query_phrase = normalise_text(
            query
        )

        if (
            query_phrase
            and query_phrase in line_normalised
        ):

            score += 4

        if len(query_tokens) > 1:

            matched_count = len(
                set(matched_words)
            )

            if matched_count == len(
                set(query_tokens)
            ):

                score += 3

        if score > 0:

            results.append(
                {
                    "line_number": line_number,
                    "score": score,
                    "entry": line,
                    "matched_words": matched_words,
                    "matched_concepts": matched_concepts
                }
            )

    results.sort(
        key=lambda item: (
            item["score"],
            len(item["matched_words"]),
            len(item["matched_concepts"])
        ),
        reverse=True
    )

    return results[:limit]


def attach_evidence_provenance(
    search_results,
    source_name,
    source_url,
    cache_file
):

    enriched_results = []

    for number, item in enumerate(
        search_results,
        start=1
    ):

        enriched_item = dict(item)

        enriched_item["evidence_id"] = (
            f"E{number:03d}"
        )

        enriched_item["source"] = (
            source_name
        )

        enriched_item["source_url"] = (
            source_url
        )

        enriched_item["cache_file"] = (
            cache_file
        )

        enriched_item["provenance"] = {
            "evidence_id": (
                f"E{number:03d}"
            ),
            "source": source_name,
            "source_url": source_url,
            "cache_file": cache_file,
            "cache_line": item.get(
                "line_number"
            )
        }

        enriched_results.append(
            enriched_item
        )

    return enriched_results


def build_research_result(
    question,
    source_name,
    source_url,
    search_results,
    cache_file=None
):

    if cache_file is None:

        cache_file = str(
            CACHE_DIR / "midnight_docs.txt"
        )

    enriched_results = attach_evidence_provenance(
        search_results,
        source_name,
        source_url,
        cache_file
    )

    result = {
        "question": question,
        "source": source_name,
        "url": source_url,
        "trusted": is_trusted_source(
            source_url
        ),
        "status": "READY",
        "cache_file": cache_file,
        "results": enriched_results
    }

    return result


def run_research(
    question,
    source_name,
    source_url
):

    result = {
        "question": question,
        "source": source_name,
        "url": source_url,
        "source_type": get_source_type(
            source_url
        ),
        "status": "READY"
    }

    return result