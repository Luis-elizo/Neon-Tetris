
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    try {
        $doc = $word.Documents.Open("c:\Users\luisa\Universidad\ll ciclo 2026\Estructura de Datos\Neon-Tetris\INFORME_PROYECTO1_EIF207.docx")
        $doc.SaveAs([ref]"c:\Users\luisa\Universidad\ll ciclo 2026\Estructura de Datos\Neon-Tetris\INFORME_PROYECTO1_EIF207.pdf", [ref]17)
        $doc.Close()
        Write-Host "Exportacion exitosa de PDF mediante Word"
    } catch {
        Write-Host "Error al exportar: " $_
    } finally {
        $word.Quit()
    }
    