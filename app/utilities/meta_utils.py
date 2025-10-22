import os
import httpx
from typing import Optional
from app.core.config import settings
import requests
# META_ACCESS_TOKEN = settings.Access_Token  # Long-lived token


META_ACCESS_TOKEN="EAGZBCgfHQpesBPYwxB75jgrmuxa1zgzQMMxIcuVjZCjmywLC3h5FcbcKtzZCVfiqDT7YnZCkpxsI5ltU98Ivp2nQyPLSjtferMq3TUnVByAfnOaazVIwqUSfW9SYBZCRTBxCvqVlnZA47c736mowBrp2eGNumZCA1YsqjBqXg63tf0v7DULggGN1gjZAGwuXOTUi4uzjXA2s0QKzOTnAEOiwO5RzS7t7k3zJ"
GRAPH_URL = "https://graph.facebook.com/v23.0"


import requests
import re
from googlesearch import search

import re
from googleapiclient.discovery import build

# Replace with your actual keys
# API_KEY = "AIzaSyBlw5PZeC-0HakqnMphXj761yju4xhAFFs"  # Your Google API key
API_KEY = "AIzaSyBlw5PZeC-0HakqnMphXj761yju4xhAFFs"

SEARCH_ENGINE_ID = "268d69758392d4ba1" 
def google_search(query, api_key, cse_id, **kwargs):
    """Perform a Google Custom Search."""
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
    return res.get("items", [])

def extract_facebook_pages(company_name):
    """
    Extract only main Facebook page links for the given company.
    """
    query = f"site:facebook.com {company_name}"
    results = google_search(query, API_KEY, SEARCH_ENGINE_ID)

    page_links = []
    for item in results:
        link = item.get("link", "")
        # Match only main page URLs (skip posts, photos, etc.)
        # if re.match(r"^https://www\.facebook\.com/[^/]+/?$", link):
        #     page_links.append(link)
        if re.match(r"^https://www\.facebook\.com/[A-Za-z0-9.\-]+/?$", link):
            page_links.append(link)

    return page_links


