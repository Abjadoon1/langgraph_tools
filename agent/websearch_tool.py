from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()
tavily_key = os.getenv("TAVILY_API_KEY")


client = TavilyClient(api_key=tavily_key)


def search_web(query, max_results=3):
    response = client.search(query=query, max_results=max_results)

    results = []

    for result in response.get("results", []):
        content = result.get("content", "")

        results.append(
            {
                "title": result.get("title", "unknown"),
                "url": result.get("url", "unknown"),
                "summary": content[:500],
            }
        )

    return results


print(search_web("what is circle"))
