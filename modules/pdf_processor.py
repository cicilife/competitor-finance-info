import os
import re
import logging
import pdfplumber
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self, pdf_dir: str = "data/raw/pdf"):
        self.pdf_dir = pdf_dir

    def extract_text(self, pdf_path: str, max_pages: int = 50) -> str:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for i, page in enumerate(pdf.pages):
                    if i >= max_pages:
                        break
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
                return text.strip()
        except Exception as e:
            logger.error(f"Failed to extract text from {pdf_path}: {str(e)[:50]}")
            return ""

    def extract_tables(self, pdf_path: str, max_pages: int = 20) -> List[List[List[str]]]:
        tables = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    if i >= max_pages:
                        break
                    page_tables = page.extract_tables()
                    for table in page_tables:
                        if table and len(table) > 1:
                            tables.append(table)
            return tables
        except Exception as e:
            logger.error(f"Failed to extract tables from {pdf_path}: {str(e)[:50]}")
            return []

    def parse_financial_data(self, text: str) -> Dict:
        data = {}
        
        patterns = {
            "revenue": [
                (r"营收[\s\S]*?([\d,.]+)\s*(亿元|亿|万元|万|美元|USD)", "CNY"),
                (r"收入[\s\S]*?([\d,.]+)\s*(亿元|亿|万元|万|美元|USD)", "CNY"),
                (r"Revenue[\s\S]*?([\d,.]+)\s*(billion|million|thousand)", "USD"),
                (r"营业收入[\s\S]*?([\d,.]+)\s*(亿元|亿|万元|万)", "CNY")
            ],
            "profit": [
                (r"净利润[\s\S]*?([\d,.]+)\s*(亿元|亿|万元|万)", "CNY"),
                (r"纯利润[\s\S]*?([\d,.]+)\s*(亿元|亿|万元|万)", "CNY"),
                (r"Net Profit[\s\S]*?([\d,.]+)\s*(billion|million)", "USD"),
                (r"归属于母公司[\s\S]*?([\d,.]+)\s*(亿元|亿|万元|万)", "CNY")
            ],
            "gross_margin": [
                (r"毛利率[\s\S]*?([\d.]+)%", "%"),
                (r"Gross Margin[\s\S]*?([\d.]+)%", "%"),
                (r"毛利[\s\S]*?([\d.]+)%", "%")
            ],
            "net_margin": [
                (r"净利率[\s\S]*?([\d.]+)%", "%"),
                (r"Net Margin[\s\S]*?([\d.]+)%", "%"),
                (r"净利润率[\s\S]*?([\d.]+)%", "%")
            ]
        }
        
        for key, pattern_list in patterns.items():
            for pattern, unit in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    value = match.group(1).replace(",", "").replace(".", "")
                    try:
                        data[key] = {"value": float(value), "unit": unit}
                        break
                    except ValueError:
                        continue
        
        year_match = re.search(r"(20\d{2})", text)
        if year_match:
            data["year"] = year_match.group(1)
        
        quarter_match = re.search(r"(Q[1-4]|第[一二三四]季度)", text)
        if quarter_match:
            data["quarter"] = quarter_match.group(1)
        
        return data

    def summarize_pdf(self, pdf_path: str) -> Dict:
        text = self.extract_text(pdf_path)
        if not text:
            return {"error": "Failed to extract text"}
        
        summary = {
            "file_path": pdf_path,
            "filename": os.path.basename(pdf_path),
            "text_length": len(text),
            "financial_data": self.parse_financial_data(text),
            "tables_found": len(self.extract_tables(pdf_path))
        }
        
        return summary

    def process_pdf_directory(self, brand_name: str) -> List[Dict]:
        brand_dir = os.path.join(self.pdf_dir, brand_name)
        results = []
        
        if not os.path.exists(brand_dir):
            return results
        
        for filename in os.listdir(brand_dir):
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(brand_dir, filename)
                logger.info(f"Processing PDF: {pdf_path}")
                summary = self.summarize_pdf(pdf_path)
                results.append(summary)
        
        return results

    def save_summary(self, summary: Dict, output_path: str):
        import json
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)