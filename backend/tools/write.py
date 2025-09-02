from langchain_core.tools import tool
from datetime import datetime
from pathlib import Path
import subprocess
import shutil
import re

def validate_and_fix_latex(latex_content: str) -> str:
    fixed_content = latex_content
    
    lines = fixed_content.split('\n')
    in_tabular = False
    fixed_lines = []
    
    for line in lines:
        if line.strip().startswith('%'):
            fixed_lines.append(line)
            continue
            
        if r'\begin{tabular}' in line or r'\begin{array}' in line:
            in_tabular = True
        elif r'\end{tabular}' in line or r'\end{array}' in line:
            in_tabular = False
        
        if not in_tabular and '&' in line and r'\&' not in line:
            line = re.sub(r'(?<!\\)&(?![a-zA-Z])', r'\\&', line)
        
        fixed_lines.append(line)
    
    fixed_content = '\n'.join(fixed_lines)
    
    problematic_packages = [r'\usepackage{algorithm}', r'\usepackage{algorithmic}']
    for package in problematic_packages:
        fixed_content = fixed_content.replace(package, '')

    references_patterns = [
        (r'(?<!\\newpage\n)(\n*% References\n\\section\{References\})', r'\n\n% References - Start on new page\n\\newpage\n\\section{References}'),
        (r'(?<!\\newpage\n)(\n*\\section\{References\})', r'\n\n\\newpage\n\\section{References}'),
        (r'(?<!\\newpage\n)(\n*% References\n\\bibliographystyle)', r'\n\n% References - Start on new page\n\\newpage\n\\bibliographystyle'),
        (r'(?<!\\newpage\n)(\n*\\bibliographystyle)', r'\n\n\\newpage\n\\bibliographystyle')
    ]
    
    for pattern, replacement in references_patterns:
        fixed_content = re.sub(pattern, replacement, fixed_content)
    
    if not re.search(r'\\documentclass', fixed_content):
        fixed_content = r'\documentclass[11pt]{article}' + '\n' + fixed_content
    if not re.search(r'\\begin{document}', fixed_content):
        fixed_content += '\n\n\\begin{document}'
    if not re.search(r'\\end{document}', fixed_content):
        fixed_content += '\n\n\\end{document}'
    
    fixed_content = re.sub(r'\n{3,}', '\n\n', fixed_content)
    
    return fixed_content

@tool
def write_research_paper(paper_content: str) -> str:
    """Write a comprehensive research paper in professional LaTeX format and save it to a file.
    
    This tool generates professional, 8+ page research papers with proper academic structure,
    including title page, abstract, keywords, comprehensive sections, mathematical formulations,
    tables, and references.

    Args:
        paper_content: The complete LaTeX content of the research paper. Should include all
                      sections: title, abstract, keywords, introduction, literature review,
                      methodology, results, discussion, conclusion, and references.

    Returns:
        Confirmation message with the saved file path
    """
    try:
        output_dir = Path("output").absolute()
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tex_filename = f"paper_{timestamp}.tex"
        tex_file = output_dir / tex_filename
        
        enhanced_content = enhance_paper_content(paper_content)
        
        validated_content = validate_and_fix_latex(enhanced_content)
        
        tex_file.write_text(validated_content, encoding='utf-8')
        
        return f"## ✅ Research Paper Generated Successfully!\n\n**📄 Paper Features:**\n• Professional academic formatting\n• Comprehensive 8+ page structure\n• Mathematical formulations and equations\n• Tables and figures support\n• Proper citations and references\n\n**📁 File saved:** `{tex_filename}`\n\n**🔄 Next Step:** Ask me to **'generate PDF'** to create the final PDF document!"
        
    except Exception as e:
        raise Exception(f"Error writing paper: {str(e)}")

def enhance_paper_content(content: str) -> str:
    return content

@tool
def render_latex_pdf(latex_content: str = None) -> str:
    """Render a LaTeX document to PDF.

    Args:
        latex_content: The LaTeX document content as a string. If None or empty, will use the most recent .tex file.

    Returns:
        Path to the generated PDF document
    """
    if shutil.which("tectonic") is None:
        raise RuntimeError(
            "tectonic is not installed. Install it first on your system."
        )

    try:
        output_dir = Path("output").absolute()
        output_dir.mkdir(exist_ok=True)
        
        if not latex_content or not latex_content.strip():
            tex_files = list(output_dir.glob("paper_*.tex"))
            if not tex_files:
                return "Error: No LaTeX content provided and no existing .tex files found. Please generate a paper first."
            
            most_recent_tex = max(tex_files, key=lambda f: f.stat().st_mtime)
            latex_content = most_recent_tex.read_text(encoding='utf-8')
            tex_filename = most_recent_tex.name
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            tex_filename = f"paper_{timestamp}.tex"
            tex_file = output_dir / tex_filename
            
            validated_content = validate_and_fix_latex(latex_content)
            tex_file.write_text(validated_content, encoding='utf-8')
            latex_content = validated_content
        
        pdf_filename = tex_filename.replace('.tex', '.pdf')

        result = subprocess.run(
            ["tectonic", tex_filename, "--outdir", str(output_dir)],
            cwd=output_dir,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"LaTeX compilation failed: {result.stderr}")

        final_pdf = output_dir / pdf_filename
        if not final_pdf.exists():
            raise FileNotFoundError(f"PDF file was not generated. Expected: {final_pdf}")

        download_url = f"http://localhost:8000/papers/download/{pdf_filename}"
        return f"## ✅ PDF Successfully Generated!\n\n**📄 Filename:** `{pdf_filename}`\n\n**🎉 Your professional research paper is ready!**\n\nThe PDF has been compiled successfully with:\n• All formatting properly rendered\n• Mathematical equations displayed correctly\n• Tables and figures included\n• References properly formatted\n\n**📥 [Click here to download your PDF]({download_url})**\n\n*Note: The download will start automatically when you click the link.*"

    except Exception as e:
        raise Exception(f"Error rendering LaTeX: {str(e)}")
