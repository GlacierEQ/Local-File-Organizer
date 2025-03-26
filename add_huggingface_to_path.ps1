# Adds the Python Scripts directory to the current session’s PATH
$hfScripts = "C:\Users\casey\AppData\Roaming\Python\Python310\Scripts"
if ($env:PATH -notlike "*$hfScripts*") {
    $env:PATH += ";$hfScripts"
    Write-Output "Added $hfScripts to PATH for the current session."
}
else {
    Write-Output "$hfScripts is already in PATH."
}
