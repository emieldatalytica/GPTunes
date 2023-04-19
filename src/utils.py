def extract_json_from_response(response: str) -> str:
    """Extract the json from the response.

    Args:
        response (str): The response from the assistant.

    Returns:
        str: The extracted json.
    """
    start = response.find("```") + 3
    end = response.find("```", start)
    return response[start:end]
