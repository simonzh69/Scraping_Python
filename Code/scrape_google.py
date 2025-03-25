import requests
from bs4 import BeautifulSoup
import sqlite3
import sys

def get_google_search_results(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    return response.text

def parse_search_results(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for div in soup.find_all("div", class_="g"):
        title = div.find("h3").text
        link = div.find("a")["href"]
        snippet = div.find("span", class_="st").text
        results.append({"title": title, "link": link, "snippet": snippet})
    return results

def store_in_database(query, results):
    conn = sqlite3.connect("google_search_results.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS google_results
        (id INTEGER PRIMARY KEY,
         query TEXT,
         title TEXT,
         link TEXT,
         snippet TEXT,
         timestamp TEXT DEFAULT CURRENT_TIMESTAMP)
    """)
    for result in results:
        cursor.execute("INSERT INTO google_results (query, title, link, snippet) VALUES (?, ?, ?, ?)", 
                       (query, result["title"], result["link"], result["snippet"]))
    conn.commit()
    conn.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <search_query>")
        return
    query = sys.argv[1]
    html = get_google_search_results(query)
    results = parse_search_results(html)
    store_in_database(query, results)
    print("Scraping completed successfully.")

if __name__ == "__main__":
    main()