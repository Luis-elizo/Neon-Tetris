
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    try {
        $doc = $word.Documents.Open("c:\Users\luisa\Universidad\ll ciclo 2026\Estructura de Datos\Neon-Tetris\scratch\test_6_pages.docx")
        $doc.SaveAs([ref]"c:\Users\luisa\Universidad\ll ciclo 2026\Estructura de Datos\Neon-Tetris\scratch\test_6_pages.pdf", [ref]17)
        $doc.Close()
    } finally {
        $word.Quit()
    }
    