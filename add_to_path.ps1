# Add the Python Scripts directory to the current session's PATH
$scriptDir = "C:\Users\casey\AppData\Roaming\Python\Python310\Scripts"
if ($env:PATH -notlike "*$scriptDir*") {
    $env:PATH += ";$scriptDir"
    Write-Output "Added $scriptDir to PATH for the current session."
}
else {
    Write-Output "$scriptDir is already in PATH."
}
