import os
import requests
from typing import Dict
import arxiv
import pypandoc
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urljoin, urlparse
import shutil

AR5IV_BASE_URL: str = "https://ar5iv.labs.arxiv.org/html/"


def fetch_ar5iv_html(arxiv_id: str) -> str:
    url: str = f"{AR5IV_BASE_URL}{arxiv_id}"
    response: requests.Response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove all images and tables
    for element in soup.find_all(["img", "table"]):
        element.decompose()

    return str(soup)


def generate_epub(html_content: str, output_path: str) -> None:
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all math elements
    math_elements = soup.find_all("math")

    for math in math_elements:
        # Find the LaTeX annotation
        latex = math.find("annotation", {"encoding": "application/x-tex"})
        if latex:
            # Remove all mathml stuff and replace with normal latex
            # webtex will then convert these into embedded inline images
            new_script = soup.new_tag("script", type="math/tex")
            new_script.string = latex.string.strip()
            math.replace_with(new_script)
        else:
            # If no LaTeX found, remove the math element
            math.decompose()

    # Convert to EPUB using Pandoc
    pypandoc.convert_text(
        str(soup),
        to="epub",
        format="html",
        outputfile=output_path,
        extra_args=[
            "--webtex",
        ],
    )


def get_arxiv_metadata(arxiv_id: str) -> Dict[str, str]:
    client = arxiv.Client()
    search = arxiv.Search(id_list=[arxiv_id])
    paper: arxiv.Result = next(client.results(search))
    return {
        "title": paper.title,
        "authors": paper.authors[0].name.split()[-1] if paper.authors else "",
        "year": str(paper.published.year),
    }


def get_output_filename(arxiv_id: str) -> str:
    metadata: Dict[str, str] = get_arxiv_metadata(arxiv_id)
    filename: str = f"{metadata['authors']} {metadata['year']} - {metadata['title']}"
    filename = "".join(
        c for c in filename if c.isalnum() or c in (" ", "-", "_")
    ).rstrip()
    return filename


def extract_arxiv_id(input_str: str) -> str:
    cleaned = input_str.strip().rstrip("/")
    if "arxiv.org" in cleaned:
        return cleaned.split("/")[-1]
    return cleaned


def process_arxiv_id(
    input_id: str, output_folder: str = ".", custom_filename: str = None
) -> None:
    arxiv_id = extract_arxiv_id(input_id)
    print(f"Processing ID: {arxiv_id}...")

    if custom_filename:
        filename = custom_filename
    else:
        filename = arxiv_id

    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
        epub_output_path: str = os.path.join(output_folder, f"{filename}.epub")
        if not os.path.exists(epub_output_path):
            html_content: str = fetch_ar5iv_html(arxiv_id)
            generate_epub(html_content=html_content, output_path=epub_output_path)
            print(f"Generated EPUB: {epub_output_path}")
        else:
            print(f"Skipping EPUB generation - file already exists: {epub_output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a single arXiv ID to EPUB.")
    parser.add_argument("arxiv_id", help="arXiv ID to process")
    parser.add_argument(
        "-o",
        "--output",
        default=".",
        help="Output folder for EPUB file (optional, default: current directory)",
    )
    parser.add_argument(
        "-f",
        "--filename",
        help="Output filename for EPUB file (optional, default: arxiv ID)",
    )
    args = parser.parse_args()

    process_arxiv_id(args.arxiv_id, args.output, args.filename)
    print("Finished processing.")
