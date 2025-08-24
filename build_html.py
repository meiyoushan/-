#!/usr/bin/env python3
import re, os, shutil, zipfile
from docx import Document
from jinja2 import Template

# 0. 环境变量
GITHUB_REPO = os.getenv('GITHUB_REPOSITORY', 'meiyoushan/quiz')   # 形如 user/repo
SRC_DOCX    = '三练习.docx'
DIST_DIR    = 'dist'

# 1. 清理旧产物
shutil.rmtree(DIST_DIR, ignore_errors=True)
os.makedirs(DIST_DIR, exist_ok=True)

# 2. 读取 docx
doc  = Document(SRC_DOCX)
text = '\n'.join(p.text for p in doc.paragraphs)

# 3. 正则提取题目
pattern = re.compile(
    r'(\d+)\.【.*?】(.+?)(?=A\.(.+?)B\.(.+?)C\.(.+?)D\.(.+?)(?:E\.(.+?))?)(?=\d+\.|$)',
    re.S)
questions = []
for num, stem, *opts_raw in pattern.findall(text):
    opts = [f"{letter}.{opt.strip()}" for letter, opt in zip('ABCDE', opts_raw) if opt and opt.strip()]
    questions.append({'q': int(num), 'stem': stem.strip(), 'opts': opts})

# 4. 生成 html
tpl = Template(open('templates/question.tpl').read())
for q in questions:
    html = tpl.render(q=q['q'], stem=q['stem'], opts=q['opts'], github={'repository':GITHUB_REPO})
    open(f'{DIST_DIR}/q{q["q"]}.html', 'w', encoding='utf-8').write(html)

# 5. 复制图片（Docx 中 media 解压到 dist）
with zipfile.ZipFile(SRC_DOCX) as z:
    for name in z.namelist():
        if name.startswith('word/media/'):
            img_name = os.path.basename(name)
            q_num = int(re.search(r'image(\d+)\.', img_name).group(1))
            z.extract(name, DIST_DIR)
            shutil.move(f'{DIST_DIR}/{name}', f'{DIST_DIR}/image{q_num}.png')

print('✅ 已生成', len(questions), '道题')
