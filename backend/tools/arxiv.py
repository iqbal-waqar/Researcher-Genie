import requests
import xml.etree.ElementTree as ET
from langchain_core.tools import tool

def search_arxiv_papers(topic: str, max_results: int = 5) -> dict:
    query = topic.lower().replace(" ", "+").replace("(", "").replace(")", "").replace('"', "")
    
    url = (
        "http://export.arxiv.org/api/query"
        f"?search_query=all:{query}"
        f"&max_results={max_results}"
        "&sortBy=submittedDate"
        "&sortOrder=descending"
    )
    
    resp = requests.get(url)
    if not resp.ok:
        raise ValueError(f"Bad response from arXiv API: {resp.status_code}")
    
    return parse_arxiv_xml(resp.text)
def parse_arxiv_xml(xml_content: str) -> dict:
    entries = []
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    root = ET.fromstring(xml_content)
    
    for entry in root.findall("atom:entry", ns):
        authors = [author.findtext("atom:name", namespaces=ns) for author in entry.findall("atom:author", ns)]
        
        pdf_link = None
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("type") == "application/pdf":
                pdf_link = link.attrib.get("href")
                break

        entries.append({
            "title": entry.findtext("atom:title", namespaces=ns),
            "summary": entry.findtext("atom:summary", namespaces=ns).strip(),
            "authors": authors,
            "pdf": pdf_link
        })

    return {"entries": entries}


@tool
def arxiv_search(topic: str) -> str:
    """Search for recently uploaded arXiv papers

    Args:
        topic: The topic to search for papers about

    Returns:
        Formatted string with paper information including titles, authors, summaries, etc.
    """
    try:
        topic_lower = topic.lower()
        if any(phrase in topic_lower for phrase in ["interested in paper", "paper 1", "paper 2", "paper 3", "paper 4", "paper 5", "1st paper", "2nd paper", "3rd paper", "4th paper", "5th paper", "first paper", "second paper", "third paper", "fourth paper", "fifth paper"]):
            return "ERROR: This appears to be a paper selection request. Please use read_pdf tool instead of arxiv_search for analyzing specific papers."

        papers = search_arxiv_papers(topic)

        if len(papers['entries']) == 0:
            return f"📚 No recent papers found for topic: {topic}\n\nTry a different search term or let me know if you'd like to explore a related topic."

        formatted_papers = f"# 📚 **Recent Papers on {topic.title()}**\n\n"
        formatted_papers += f"Found **{len(papers['entries'])} papers** from arXiv:\n\n"

        for i, paper in enumerate(papers['entries'], 1):
            title = paper['title'].strip().replace('\n', ' ').replace('  ', ' ')

            authors = paper['authors'][:3]
            author_text = ', '.join(authors)
            if len(paper['authors']) > 3:
                author_text += f" and {len(paper['authors']) - 3} others"

            summary = paper['summary'].strip().replace('\n', ' ').replace('  ', ' ')
            if len(summary) > 300:
                summary = summary[:300] + "..."

            formatted_papers += f"## **Paper {i}: {title}**\n\n"
            formatted_papers += f"👥 **Authors:** {author_text}\n\n"
            formatted_papers += f"📄 **Summary:** {summary}\n\n"
            formatted_papers += f"🔗 **PDF:** [Download Paper]({paper['pdf']})\n\n"
            formatted_papers += "---\n\n"

        formatted_papers += "## 🎯 **Next Step**\n\n"
        formatted_papers += "**Which paper are you interested in?** You can say:\n"
        formatted_papers += "- \"I am interested in paper 1\"\n"
        formatted_papers += "- \"I am interested in paper 2\"\n"
        formatted_papers += "- \"I am interested in paper 3\"\n"
        formatted_papers += "- \"I am interested in paper 4\"\n"
        formatted_papers += "- \"I am interested in paper 5\"\n\n"

        return formatted_papers

    except Exception as e:
        return f"❌ Error searching for papers on {topic}: {str(e)}\n\nPlease try a different search term."
