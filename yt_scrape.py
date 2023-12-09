from youtube_search import YoutubeSearch
import subprocess
#import webbrowser

# Define the search term
search_term = "Yoga downward dog"

# Search for the term on YouTube
results = YoutubeSearch(search_term, max_results=2).to_dict()

brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" 

# Print the URLs of the first 5 videos
for video in results:
    url = 'https://www.youtube.com' + video['url_suffix']
    #webbrowser.open('https://www.youtube.com' + video['url_suffix'])
    subprocess.Popen([brave_path, '--incognito', url])