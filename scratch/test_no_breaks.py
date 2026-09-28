import os
import subprocess
import pypdf
import docx

doc = docx.Document('INFORME_PROYECTO1_EIF207.docx')
for idx in [40, 34, 27, 20]:
    p = doc.paragraphs[idx]
    p._p.getparent().remove(p._p)

out_docx = r'c:\Users\luisa\Universidad\ll ciclo 2026\Estructura de Datos\Neon-Tetris\scratch\test_no_breaks.docx'
out_pdf = r'c:\Users\luisa\Universidad\ll ciclo 2026\Estructura de Datos\Neon-Tetris\scratch\test_no_breaks.pdf'
doc.save(out_docx)

ps_script = f'''
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {{
    $doc = $word.Documents.Open("{out_docx}")
    $doc.SaveAs([ref]"{out_pdf}", [ref]17)
    $doc.Close()
}} finally {{
    $word.Quit()
}}
'''
open('scratch/export_test.ps1', 'w', encoding='utf-8').write(ps_script)
subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', 'scratch/export_test.ps1'])

r = pypdf.PdfReader(out_pdf)
print('Total pages without extra breaks:', len(r.pages))
for idx, page in enumerate(r.pages):
    txt = page.extract_text().strip()
    print(f'=== PAGE {idx+1} (len: {len(txt)}) ===')
    first_line = txt.split('\n')[0] if txt else ''
    last_line = txt.split('\n')[-1] if txt else ''
    print(f"  First: {first_line[:90]}")
    print(f"  Last:  {last_line[:90]}")
