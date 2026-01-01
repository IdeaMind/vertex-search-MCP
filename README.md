# Vertex AI Search MCP Tool

A Model Context Protocol (MCP) server for interacting with Google Cloud Vertex AI Search. This tool enables AI agents and MCP-compatible clients (like Claude Desktop) to perform searches on Vertex AI data stores, integrating seamlessly with your Google Cloud projects for intelligent search capabilities.

## Prerequisites

- **Python Version:** Python 3.8 or higher.
- **Google Cloud Project:** 
  - A Google Cloud project with Vertex AI Search (formerly Discovery Engine) enabled.
  - Enable the Discovery Engine API in your project.
  - Create a Vertex AI Search data store and note its ID.
- **Authentication:**
  - A service account key file with permissions to access the Discovery Engine Search API (roles like `roles/discoveryengine.viewer` or custom roles with `discoveryengine.search`).
  - Alternatively, if running on Google Cloud infrastructure (e.g., Cloud Run, Compute Engine), default application credentials can be used.
- **Tools:** 
  - `uv` (recommended for dependency management and running scripts) or `pip` for installation.
  - Access to Google Cloud Console for setup.

## Configuration

This tool relies on environment variables for Google Cloud authentication and Vertex AI Search specifics. Create a `.env` file in the project root by copying `.env.example` and filling in your values.

### Environment Variables

- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your service account key JSON file (e.g., `/path/to/service-account-key.json`). Required for authentication unless using default credentials.
- `PROJECT_ID`: Your Google Cloud project ID (e.g., `my-project-123`).
- `LOCATION`: The location of your Vertex AI Search data store (e.g., `global` or `us-central1`).
- `DATA_STORE_ID`: The ID of your Vertex AI Search data store (e.g., `default_data_store`).

Example `.env` file (copy from `.env.example`):

```
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
PROJECT_ID=your-google-cloud-project-id
LOCATION=global
DATA_STORE_ID=your-vertex-ai-search-data-store-id
```

Load the `.env` file automatically when running the tool (handled by `python-dotenv`).

## Installation & Usage

### Development

1. Clone or navigate to the project directory.
2. Copy `.env.example` to `.env` and configure your environment variables.
3. Install dependencies:
   - Using `uv` (recommended): `uv sync`
   - Using `pip`: `pip install -e .` (editable install for development).
4. Run the MCP server locally:
   - Using `uv`: `uv run src/search_tool.py`
   - Using `python`: `python src/search_tool.py`

The server will start and expose the `search` tool, which can be used by MCP clients to query your Vertex AI Search data store.

### Deployment via UVX

UVX allows running Python projects without a full installation, ideal for quick deployments or testing.

- **From Local Source Directory:** Navigate to the project root and run:
  ```
  uvx --from . src/search_tool.py
  ```
  This executes the script using the local `pyproject.toml` dependencies without installing the project globally.

- **If Published to PyPI (Hypothetical):** Once the package is published, run:
  ```
  uvx vertex-search-mcp-tool
  ```
  Ensure your `.env` file is loaded or pass environment variables directly (e.g., `GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json uvx --from . src/search_tool.py`).

UVX will handle dependency resolution via `pyproject.toml` and start the MCP server.

### Claude Desktop Config

To integrate this tool with Claude Desktop, add it to your `claude_desktop_config.json` file (typically in `~/.claude/` or your app data directory). Here's a sample configuration snippet:

```json
{
  "mcpServers": {
    "vertex-search": {
      "command": "uvx",
      "args": ["--from", "/path/to/your/project", "src/search_tool.py"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/service-account-key.json",
        "PROJECT_ID": "your-google-cloud-project-id",
        "LOCATION": "global",
        "DATA_STORE_ID": "your-vertex-ai-search-data-store-id"
      },
      "cwd": "/path/to/your/project"
    }
  }
}
```

- Replace `/path/to/your/project` with the absolute path to the project directory.
- Update the `env` section with your actual values (avoid hardcoding sensitive paths; consider using a secure method like environment variables or secrets management).
- Restart Claude Desktop after updating the config. The `search` tool will then be available for use in conversations.

## Troubleshooting

- **Authentication Errors (e.g., "Permission Denied" or "Invalid Credentials"):**
  - Verify `GOOGLE_APPLICATION_CREDENTIALS` points to a valid service account key.
  - Ensure the service account has the necessary IAM roles (e.g., `roles/discoveryengine.viewer`).
  - If using default auth, confirm the environment (e.g., GCP VM) has the correct metadata.
  - Test auth with `gcloud auth application-default login` or `gcloud auth activate-service-account`.

- **Missing Environment Variables:**
  - Check that `PROJECT_ID`, `LOCATION`, and `DATA_STORE_ID` are set in `.env` or exported.
  - The tool will raise a `ValueError` if any are missing—review the error message for specifics.
  - Ensure `.env` is in the project root and loaded (the script uses `load_dotenv()`).

- **No Search Results:**
  - Confirm the `DATA_STORE_ID` matches an existing, populated data store in Vertex AI Search.
  - Verify the data store location matches `LOCATION`.
  - Test the data store directly in the Google Cloud Console to ensure queries return results.
  - Check query syntax; the `search` tool expects a simple string query.

- **Dependency Issues:**
  - Run `uv sync` or `pip install -r requirements.txt` (generated from `pyproject.toml`).
  - If using UVX, ensure `uv` is up-to-date: `pip install -U uv`.

- **MCP Server Not Starting:**
  - Check for Python version compatibility (3.8+).
  - Review console output for import errors (e.g., missing `google-cloud-discoveryengine`).
  - Ensure no port conflicts if the server binds to a specific port.

For further issues, consult the [Google Cloud Vertex AI Search documentation](https://cloud.google.com/generative-ai-app-builder/docs) or the [FastMCP documentation](https://github.com/jlowin/fastmcp).