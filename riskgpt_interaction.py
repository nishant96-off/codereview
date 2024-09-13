import requests
import json

# Set up the headers with the Bearer token
def initializeRequestDetails(conf,content):
    with open("prompt.txt", 'r') as file:
        prompt= file.read()
    headers = {
        'Authorization': f'Bearer {conf["riskgpt"]["token"]}',
        'Content-Type': 'application/json'  # Ensure this matches the expected content type
    }

    # Define the payload (replace with actual data required by the API)
    payload = {
        'content': prompt.replace('##CodeContent##', content).replace('##FileExtension##', conf["file_extension"]),  # Example field, replace with actual fields
        'mode': 'General',               # Example field, replace with actual fields
        'thread_id':conf["riskgpt"]["thread_id"] # Example field, replace with actual fields
    }
    return headers, payload

def getAiResponse(conf, headers, payload):
    try:
        response = requests.post(conf["riskgpt"]["api_url"], headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        # Print the response JSON data
        return response.json()[1]["content"]
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print("*********************************")
        print(f'Response content: {response.text}')  # Print the response content for more details
    except requests.exceptions.RequestException as err:
        print(f'Request error occurred: {err}')
    
def callAiModel(conf,content):
    headers, payload = initializeRequestDetails(conf,content)
    aiGeneratedComment = "\n\n**" +conf["file_path"] + "**\n"
    aiGeneratedComment += getAiResponse(conf, headers, payload)
    
    return aiGeneratedComment