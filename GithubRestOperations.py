import base64
import json
import requests
import riskgpt_interaction as ai

class GitHubPullRequestOpeartions:
    def __init__(self, owner, repo, token, pull_request_number):
        self.owner = owner
        self.repo = repo
        self.token = token
        self.pull_request_number = pull_request_number
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'token {self.token}'
        }

    def get_changed_file_details(self):
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/pulls/{self.pull_request_number}/files'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()

    def get_file_content(self, content_url):
        response = requests.get(content_url, headers=self.headers)
        response.raise_for_status()  # Raise an error for bad status codes
        content = response.json()['content']
        return base64.b64decode(content).decode('utf-8')

    def post_comment_on_pull_request(self, ai_generated_comment):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues/{self.pull_request_number}/comments"
        payload = json.dumps({"body": ai_generated_comment})
        response = requests.post(url, headers=self.headers, data=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        print('Comment posted successfully')

if __name__ == "__main__":
    with open("config.json", 'r') as file:
        conf= json.load(file)
    owner = conf["github"]["owner"]
    repo = conf["github"]["repo"]
    token = conf["github"]["token"]
    pull_request_number = conf["github"]["pull_request_number"]

    github_pr = GitHubPullRequestOpeartions(owner, repo, token, pull_request_number)

    changed_files = github_pr.get_changed_file_details()
    aiGeneratedComment = ""
    for file in changed_files:
        file_path = file['filename']
        file_extension = file_path.split('.')[-1]
        conf["file_path"] = file_path
        conf["file_extension"] = file_extension
        # print(file_path)
        # print(f'File: {file_path} Extension: {file_extension}')
        content = github_pr.get_file_content(file['contents_url'])
        # print(content)
        # call the AI model to generate comment
        aiGeneratedComment += ai.callAiModel(conf,content)
        # aiGeneratedComment += "" # Append the AI generated comment for each file
        print(aiGeneratedComment)
    # Once the AI generated comment is ready, post it on the pull request
    github_pr.post_comment_on_pull_request(aiGeneratedComment)