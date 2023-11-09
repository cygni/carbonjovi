import json
import re

def contains_url(string):
    # Regular expression to match URLs
    url_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^()\s<>]+|\(([^()\s<>]+|(\([^()\s<>]+\)))*\))+(?:\(([^()\s<>]+|(\([^()\s<>]+\)))*\)|[^`!()\[\]{};:'\".,<>?«»“”‘’]))"

    # Check if the string contains any URLs
    return bool(re.search(url_pattern, string))

def format_response(response):
    # Example usage
    test_string = "This is a sample text with a URL: 1"
    print(contains_url(test_string))  # Output: True


    delim = "\n"
    sources = delim.join("* " + item for item in response['sources'])

    if contains_url(response['answer']):
        print('Contains URL')
        return response['answer']
    else:
        print('NO URL')
        answer = f"""{response['answer']}

Sources:
{sources}
"""
        return answer



response_dict = {
  'answer': "Yes, there are Kubernetes patterns that can be considered for green software. One such pattern is the 'Right-sizing' pattern, which involves optimizing the resource allocation of Kubernetes pods to ensure that they are using the minimum amount of resources necessary. This helps to reduce energy consumption and minimize the carbon footprint of the software. Another pattern is the 'Auto-scaling' pattern, which allows Kubernetes to automatically adjust the number of pods based on the workload. This ensures that resources are efficiently utilized and prevents over-provisioning, which can lead to unnecessary energy consumption. These patterns, along with other best practices for efficient resource management, can contribute to the development of greener and more sustainable software systems.",
  'sources': [
    "https://greensoftware.foundation/articles/london-meetup-recap-building-a-green-tech-culture",
    "https://cts.cygni.se/speakers",
    "https://greensoftware.foundation/articles/green-software-advocate-series-an-interview-with-pindy-bhullar"
  ]
}

print(format_response(response_dict))

