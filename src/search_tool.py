import os
import json
from fastmcp import FastMCP
from google.cloud import discoveryengine
import google.auth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("vertex-search")

# Global client variable
client = None

def initialize_client():
    """Initialize the Discovery Engine Search Service Client."""
    global client
    if client is not None:
        return client

    project_id = os.getenv("PROJECT_ID")
    location = os.getenv("LOCATION")
    data_store_id = os.getenv("DATA_STORE_ID")

    if not all([project_id, location, data_store_id]):
        raise ValueError("Missing required environment variables: PROJECT_ID, LOCATION, DATA_STORE_ID")

    # Handle credentials
    creds_env = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    creds = None
    if creds_env:
        if creds_env.strip().startswith('{'):
            # Treat as JSON string
            creds_dict = json.loads(creds_env)
            creds, _ = google.auth.load_credentials_from_dict(creds_dict)
        else:
            # Treat as file path
            creds, _ = google.auth.load_credentials_from_file(creds_env)

    client = discoveryengine.SearchServiceClient(credentials=creds)
    return client

@mcp.tool()
def search(query: str, limit: int = 5) -> str:
    """
    Perform a search using Vertex AI Search.

    Args:
        query: The search query string
        limit: Maximum number of results to return (default: 5)

    Returns:
        Formatted search results as a string
    """
    try:
        client = initialize_client()

        project_id = os.getenv("PROJECT_ID")
        location = os.getenv("LOCATION")
        data_store_id = os.getenv("DATA_STORE_ID")

        # Construct the serving config resource path
        serving_config = client.serving_config_path(
            project=project_id,
            location=location,
            data_store=data_store_id,
            serving_config="default_search",
        )

        # Perform the search
        request = discoveryengine.SearchRequest(
            serving_config=serving_config,
            query=query,
            page_size=limit,
        )

        response = client.search(request)

        # Process and format results
        results = []
        for result in response.results:
            document = result.document
            title = document.struct_data.get("title", "No title")
            snippet = document.struct_data.get("snippet", document.struct_data.get("summary", "No snippet"))
            link = document.struct_data.get("link", "No link")

            results.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n")

        if not results:
            return "No search results found."

        return "\n---\n".join(results)

    except Exception as e:
        return f"Error performing search: {str(e)}"

if __name__ == "__main__":
    mcp.run()