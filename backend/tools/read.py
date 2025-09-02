from langchain_core.tools import tool
import io
import PyPDF2
import requests

@tool
def read_pdf(url: str) -> str:
    """Read and extract text from a PDF file given its URL.

    Args:
        url: The URL of the PDF file to read

    Returns:
        A structured summary of the PDF content for analysis
    """
    try:
        response = requests.get(url)
        pdf_file = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

        if len(text) > 8000:
            text = text[:8000] + "\n\n[Content truncated for analysis...]"
        
        analysis = f"""# 📖 **Paper Summary**

## 📄 **Summary:**
{text[:1000]}...

## 🔬 **Key Research Directions:**
Based on this paper, here are potential research directions:

1. **Advanced Methodologies** - Improving current approaches
2. **Cross-Domain Applications** - Applying concepts to new fields  
3. **Performance Optimization** - Enhancing efficiency and accuracy
4. **Theoretical Foundations** - Strengthening mathematical basis
5. **Practical Implementation** - Real-world deployment strategies

---

## 🎯 **Next Step**
**Should I choose the best topics for you, or would you like to decide?**

You can say:
- "Choose best topics for me"
- "I will decide myself"
"""
        
        return analysis
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")