# 1_paper_crawler.py
# 2_paper_screen.py
# 3_download_pdf.py
# 4_inf_extract.py
# 5_script_make.py

echo "1. Start crawling papers..."
python3 paper_crawler.py ../../data/paper_daily.db
echo "2. Start screening papers..."
python3 paper_screen.py ../../data/paper_daily.db
echo "3. Start downloading pdfs..."
python3 download_pdf.py ../../data/paper_daily.db ../../data/paper/
echo "4. Start extracting information..."
python3 inf_extract.py ../../data/paper_daily.db ../../data/summary/
echo "5. Start making scripts..."
python3 script_make.py ../../data/summary/