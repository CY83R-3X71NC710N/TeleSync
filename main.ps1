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

# Build the path to the 7-Zip executable
$sevenZipPath = "C:\Program Files\7-Zip\7z.exe"

# Build the path to the folder to compress and encrypt
$folderToCompressPath = Join-Path $currentDirectory "sync"

# Build the path to the output file
$outputFilePath = Join-Path $folderPath "sync.7z"

# Compress and encrypt the folder using 7-Zip
& $sevenZipPath a -t7z -m0=lzma2 -mx=9 -mfb=273 -md=256m -ms=on -pMyPassword -mhe=on $outputFilePath $folderToCompressPath

# Check if the output file is larger than 3.9GB and split it if necessary
$maxFileSize = 3.9GB

while ((Get-Item $outputFilePath).Length -gt $maxFileSize) {
    $splitSize = $maxFileSize / 2 # Split the file into two parts
    $outputFileBaseName = [System.IO.Path]::GetFileNameWithoutExtension($outputFilePath)
    $outputFileExtension = [System.IO.Path]::GetExtension($outputFilePath)

    # Split the file using 7-Zip
    & $sevenZipPath a -t7z -m0=lzma2 -mx=9 -mfb=273 -md=256m -ms=on -v$splitSize -pMyPassword -mhe=on "$folderPath\$outputFileBaseName.part" $outputFilePath

    # Delete the original output file
    Remove-Item $outputFilePath

    # Rename the split files to remove the ".001" extension
    $splitFiles = Get-ChildItem "$folderPath\$outputFileBaseName.part.*"
    foreach ($splitFile in $splitFiles) {
        $newFileName = $splitFile.FullName.Replace(".001", "")
        Rename-Item $splitFile.FullName $newFileName
    }

    # Set the output file path to the first part of the split file
    $outputFilePath = "$folderPath\$outputFileBaseName.part"
}

# Remove the ".001" extension from the final part
$finalPartPath = "$folderPath\$outputFileBaseName.part"
Rename-Item "$outputFilePath" -NewName "$finalPartPath$outputFileExtension"
