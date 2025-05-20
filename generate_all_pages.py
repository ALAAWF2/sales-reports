
import os
import datetime

# === توليد صفحة كل مدير ===
def generate_manager_index(manager_name, files, folder_path):
    list_items = ""
    for f in sorted(files):
        if f.lower().endswith(('.pdf', '.xlsx')):
            file_path = os.path.join(folder_path, f)
            size_kb = os.path.getsize(file_path) // 1024
            modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %I:%M %p")
            file_type = "PDF" if f.lower().endswith(".pdf") else "Excel"
            list_items += f"""
            <li>
              <div>
                <strong>{f}</strong><br>
                <span>📅 {modified_time} | 🗂️ {file_type} | 💾 {size_kb} KB</span>
              </div>
              <a href="./{f}" download class="download">تحميل</a>
            </li>
            """

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>تقارير {manager_name}</title>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Cairo', sans-serif;
      background: #f7f7f7;
      padding: 40px;
      max-width: 900px;
      margin: auto;
    }}
    h1 {{
      text-align: center;
      color: #ff6600;
      margin-bottom: 30px;
    }}
    .back {{
      display: block;
      margin: 10px auto 30px;
      text-align: center;
      text-decoration: none;
      color: #555;
      font-weight: bold;
      border: 1px solid #ccc;
      padding: 8px 16px;
      border-radius: 8px;
      width: fit-content;
    }}
    ul {{
      list-style: none;
      padding: 0;
    }}
    li {{
      background: white;
      margin: 15px 0;
      padding: 15px;
      border-radius: 10px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .download {{
      background: #ff6600;
      color: white;
      padding: 8px 16px;
      border-radius: 8px;
      text-decoration: none;
    }}
    .download:hover {{
      background: #e65c00;
    }}
  </style>
</head>
<body>
  <h1>تقارير {manager_name}</h1>
  <a class="back" href="../../index.html">⬅ العودة للرئيسية</a>
  <ul>
    {list_items if list_items else "<p style='text-align:center'>لا توجد تقارير حالياً</p>"}
  </ul>
</body>
</html>"""

# === توليد الصفحة الرئيسية ===
def generate_main_index(manager_folders):
    links_html = ""
    for manager in sorted(manager_folders):
        safe_path = manager.replace(" ", "%20")
        links_html += f'    <a class="btn" href="reports/{safe_path}/index.html">{manager}</a>\n'

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>OrangeBed&Bath - Sales Reports</title>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Cairo', sans-serif;
      background: #f4f7fa;
      margin: 0;
      padding: 0;
    }}
    header {{
      background: #ff6600;
      padding: 20px;
      text-align: center;
      color: white;
      font-size: 24px;
      font-weight: bold;
    }}
    .container {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      padding: 40px;
      gap: 20px;
    }}
    .btn {{
      background: white;
      padding: 15px 30px;
      border-radius: 12px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      text-decoration: none;
      color: black;
      font-weight: 500;
      transition: 0.2s;
    }}
    .btn:hover {{
      background: #eee;
    }}
  </style>
</head>
<body>
  <header>OrangeBed&Bath - Sales Reports</header>
  <div class="container">
{links_html}  </div>
</body>
</html>"""

# === التنفيذ الرئيسي ===
def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    reports_path = os.path.join(base_path, "reports")

    if not os.path.exists(reports_path):
        print("❌ لم يتم العثور على مجلد reports في نفس مسار السكربت.")
        return

    manager_folders = []
    for manager in os.listdir(reports_path):
        folder = os.path.join(reports_path, manager)
        if os.path.isdir(folder):
            manager_folders.append(manager)
            files = os.listdir(folder)
            html = generate_manager_index(manager, files, folder)
            with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)
            print(f"✅ تم توليد صفحة {manager}")

    # توليد الصفحة الرئيسية
    index_html = generate_main_index(manager_folders)
    with open(os.path.join(base_path, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("✅ تم توليد الصفحة الرئيسية index.html")

if __name__ == "__main__":
    main()
