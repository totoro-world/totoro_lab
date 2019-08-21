import webbrowser

chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))  
webbrowser.get('chrome').open('https://wallstreetcn.com/')