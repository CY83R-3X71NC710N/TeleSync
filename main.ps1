# Define the name of the folder to create
$folderName = "encrypted_zips"

# Get the current working directory
$currentDirectory = Get-Location

# Build the full path to the folder to create
$folderPath = Join-Path $currentDirectory $folderName

# Check if the folder already exists and delete it if it does
if (Test-Path $folderPath) {
    Remove-Item $folderPath -Recurse
}

# Create the folder
New-Item -ItemType Directory -Path $folderPath

# Define the name of the folder to compress and encrypt
$folderToCompressName = "sync"

# Build the path to the folder to compress and encrypt
$folderToCompressPath = Join-Path $currentDirectory $folderToCompressName

# Check if the folder to compress and encrypt exists and create it if it doesn't
if (-not (Test-Path $folderToCompressPath)) {
    New-Item -ItemType Directory -Path $folderToCompressPath
}

# Build the path to the output file
$outputFilePath = Join-Path $folderPath "sync.7z"

# Build the path to the 7-Zip executable
$sevenZipPath = "C:\Program Files\7-Zip\7z.exe"

# Compress and encrypt the folder using 7-Zip
& $sevenZipPath a -t7z -m0=lzma2 -mx=9 -mfb=273 -md=256m -ms=on -pMyPassword -mhe=on $outputFilePath $folderToCompressPath

# Check if the output file is larger than 1.9GB and split it if necessary
$maxFileSize = 1.9GB

if ((Get-Item $outputFilePath).Length -gt $maxFileSize) {
    $splitSize = [Math]::Ceiling((Get-Item $outputFilePath).Length / ($maxFileSize * 1MB))
    $outputFileBaseName = [System.IO.Path]::GetFileNameWithoutExtension($outputFilePath)
    $outputFileExtension = [System.IO.Path]::GetExtension($outputFilePath)

    # Split the file using 7-Zip
    & $sevenZipPath a -t7z -m0=lzma2 -mx=9 -mfb=273 -md=256m -ms=on "-v1g" -pMyPassword -mhe=on "${outputFilePath}.split" "${outputFilePath}"

    # Delete the original file
    Remove-Item $outputFilePath

    # Notify the user about the output file location and size
    Write-Host "The compressed and encrypted file(s) are located in:" $folderPath
    $outputFiles = Get-ChildItem $folderPath -Filter "${outputFileBaseName}*.${outputFileExtension}"
    foreach ($outputFile in $outputFiles) {
        Write-Host $outputFile.Name ("{0:N2} MB" -f ($outputFile.Length / 1MB))
    }
}
elseif ((Get-Item $outputFilePath).Length -le $maxFileSize) {
    # Notify the user about the output file location and size
    Write-Host "The compressed and encrypted file is located in:" $outputFilePath
    $outputFile = Get-Item $outputFilePath
    Write-Host $outputFile.Name ("{0:N2} MB") -f ($outputFile.Length / 1MB)
}
