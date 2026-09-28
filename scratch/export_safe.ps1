$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open("c:\Users\luisa\Universidad\ll ciclo 2026\Estructura de Datos\Neon-Tetris\INFORME_PROYECTO1_EIF207.docx", $false, $true)
    $doc.SaveAs([ref]"c:\Users\luisa\Universidad\ll ciclo 2026\Estructura de Datos\Neon-Tetris\scratch\user_current.pdf", [ref]17)
    $doc.Close()
    Write-Host "Exportacion exitosa"
} catch {
    Write-Host "Error: " $_
} finally {
    $word.Quit()
}
