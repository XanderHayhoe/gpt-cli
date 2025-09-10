"""
gpt-cli summarize <url> [--model <model>]
Summarize the content of a web page at <url> using the specified OpenAI model.

"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from gpt_cli.llm import get_command

class GptCliParseURL():
    def __init__(self, url: str):
        self.url = url
        self.driver = webdriver.Chrome()
        
    def __str__(self):
        return self.url

    def set_url(self, url: str):
        self.url = url
    
    def get_page_content(self) -> str:
        self.driver.get(self.url)
        paragraphs = self.driver.find_elements(By.TAG_NAME, "p")
        content = "\n".join([p.text for p in paragraphs])
        return content
    def close(self):
        self.driver.quit()
    
    def summarize(self, model: str) -> str:
 
        page_content = self.get_page_content()
        request = f"Summarize the following content:\n\n{page_content}"
        response = get_command(request, model=model)
        return response["command"]
def summarize_page(url: str, model: str):
    parser = GptCliParseURL(url)
    summary = parser.summarize(model)
    parser.close()
    return summary
