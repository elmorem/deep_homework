from ..config.config import Config


def get_retriever(retriever: str):
    """
    Gets the retriever
    Args:
        retriever (str): retriever name

    Returns:
        retriever: Retriever class

    """
    match retriever:
        case "google":
            from homework_researcher.retrievers.google.google import GoogleSearch
            return GoogleSearch
        case "searx":
            from homework_researcher.retrievers.searx.searx import SearxSearch
            return SearxSearch
        case "searchapi":
            from homework_researcher.retrievers.searchapi.searchapi import SearchApiSearch
            return SearchApiSearch
        case "serpapi":
            from homework_researcher.retrievers.serpapi.serpapi import SerpApiSearch
            return SerpApiSearch
        case "serper":
            from homework_researcher.retrievers.serper.serper import SerperSearch
            return SerperSearch
        case "duckduckgo":
            from homework_researcher.retrievers.duckduckgo.duckduckgo import Duckduckgo
            return Duckduckgo
        case "bing":
            from homework_researcher.retrievers.bing.bing import BingSearch
            return BingSearch
        case "arxiv":
            from homework_researcher.retrievers.arxiv.arxiv import ArxivSearch
            return ArxivSearch
        case "tavily":
            from homework_researcher.retrievers.tavily.tavily_search import TavilySearch
            return TavilySearch
        case "exa":
            from homework_researcher.retrievers.exa.exa import ExaSearch
            return ExaSearch
        case "semantic_scholar":
            from homework_researcher.retrievers.semantic_scholar.semantic_scholar import SemanticScholarSearch
            return SemanticScholarSearch
        case "pubmed_central":
            from homework_researcher.retrievers.pubmed_central.pubmed_central import PubMedCentralSearch
            return PubMedCentralSearch
        case "custom":
            from homework_researcher.retrievers.custom.custom import CustomRetriever
            return CustomRetriever
        case _:
            return None


def get_retrievers(headers: dict[str, str], cfg: Config):
    """
    Determine which retriever(s) to use based on headers, config, or default.

    Args:
        headers (dict): The headers dictionary
        cfg (Config): The configuration object

    Returns:
        list: A list of retriever classes to be used for searching.
    """
    # Check headers first for multiple retrievers
    if headers.get("retrievers"):
        retrievers = headers.get("retrievers").split(",")
    # If not found, check headers for a single retriever
    elif headers.get("retriever"):
        retrievers = [headers.get("retriever")]
    # If not in headers, check config for multiple retrievers
    elif cfg.retrievers:
        retrievers = cfg.retrievers
    # If not found, check config for a single retriever
    elif cfg.retriever:
        retrievers = [cfg.retriever]
    # If still not set, use default retriever
    else:
        retrievers = [get_default_retriever().__name__]

    # Convert retriever names to actual retriever classes
    # Use get_default_retriever() as a fallback for any invalid retriever names
    return [get_retriever(r) or get_default_retriever() for r in retrievers]


def get_default_retriever():
    from homework_researcher.retrievers.tavily.tavily_search import TavilySearch
    return TavilySearch
