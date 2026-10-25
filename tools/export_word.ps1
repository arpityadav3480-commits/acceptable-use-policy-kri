# Converts a styled HTML file into DOCX and PDF using Microsoft Word.
# Called by build_docs.py. Adds A4 page setup, a table of contents,
# a running header, page numbers, and embeds linked images.
param(
    [Parameter(Mandatory = $true)] [string]$Html,
    [Parameter(Mandatory = $true)] [string]$OutBase,
    [string]$Header = ""
)
$ErrorActionPreference = "Stop"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($Html, $false, $true)
    try { $doc.ActiveWindow.View.Type = 3 } catch {}   # print layout

    # Embed images instead of linking to files on disk
    foreach ($shape in @($doc.InlineShapes)) {
        if ($null -ne $shape.LinkFormat) {
            $shape.LinkFormat.SavePictureWithDocument = $true
            $shape.LinkFormat.BreakLink()
        }
    }
    # Scale every image to 16 cm wide (breaking the link resets it to native size)
    foreach ($shape in @($doc.InlineShapes)) {
        $shape.LockAspectRatio = -1
        $shape.Width = $word.CentimetersToPoints(16)
        $shape.Range.ParagraphFormat.KeepWithNext = -1   # keep figure with its caption
    }

    # Compact table rows: remove the HTML paragraph spacing inside cells
    foreach ($table in @($doc.Tables)) {
        $pf = $table.Range.ParagraphFormat
        $pf.SpaceBeforeAuto = 0
        $pf.SpaceAfterAuto = 0
        $pf.SpaceBefore = 2
        $pf.SpaceAfter = 2
    }

    # A4 page with 2.2 cm margins
    $ps = $doc.PageSetup
    $ps.PageWidth = $word.CentimetersToPoints(21.0)
    $ps.PageHeight = $word.CentimetersToPoints(29.7)
    $ps.TopMargin = $word.CentimetersToPoints(2.2)
    $ps.BottomMargin = $word.CentimetersToPoints(2.2)
    $ps.LeftMargin = $word.CentimetersToPoints(2.2)
    $ps.RightMargin = $word.CentimetersToPoints(2.2)

    # Replace the WORDTOC marker with a real table of contents (main sections only)
    $rng = $doc.Content
    if ($rng.Find.Execute("WORDTOC")) {
        $rng.Text = ""
        $null = $doc.TablesOfContents.Add($rng, $true, 2, 2)
    }

    # Running header and centred page numbers
    foreach ($sec in $doc.Sections) {
        $h = $sec.Headers.Item(1).Range
        $h.Text = $Header
        $h.Font.Name = "Calibri"
        $h.Font.Size = 8
        $h.Font.Color = 8421504
        $h.ParagraphFormat.Alignment = 2
        $null = $sec.Footers.Item(1).PageNumbers.Add(1, $true)
    }
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }

    $doc.SaveAs2("$OutBase.docx", 16)
    $doc.SaveAs2("$OutBase.pdf", 17)
    $doc.Close($false)
    Write-Output "Saved $OutBase.docx and $OutBase.pdf"
}
finally {
    $word.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($word)
}
