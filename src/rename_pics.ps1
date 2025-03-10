# Set the folder path where the .jpg files are located
$folderPath = Read-Host -Prompt "Enter the folder path"

# Get all .jpg files in the folder
$jpgFiles = Get-ChildItem -Path $folderPath -Filter *.jpg

# Loop through each .jpg file
foreach ($file in $jpgFiles) {
    # Get the Modified date
    $modifiedDate = $file.LastWriteTime

    # Format the Modified date as yyyyMMdd
    $dateFormatted = $modifiedDate.ToString("yyyyMMdd")

    # Construct the new file name
    $newFileName = "{0}_{1}{2}" -f $dateFormatted, "_cactus", $file.Extension

    # Construct the full paths for the old and new file names
    $oldFilePath = Join-Path -Path $folderPath -ChildPath $file.Name
    $newFilePath = Join-Path -Path $folderPath -ChildPath $newFileName

    # Rename the file
    Rename-Item -Path $oldFilePath -NewName $newFileName
}