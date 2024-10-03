# Define invalid characters in Windows filenames
$invalidChars = [System.IO.Path]::GetInvalidFileNameChars()

# Function to replace invalid characters with an underscore (_)
function Rename-InvalidFiles {
    param ($path)
    
    # Get all files and directories in the specified path
    Get-ChildItem -Path $path -Recurse | ForEach-Object {
        $oldName = $_.FullName
        $newName = $_.FullName

        # Replace invalid characters in filenames
        $newName = -replace "[$($invalidChars -join '')]", "_"

        # If the new name is different, rename the file or directory
        if ($oldName -ne $newName) {
            Rename-Item -Path $oldName -NewName $newName
            Write-Host "Renamed: $oldName to $newName"
        }
    }
}

# Run the function on the current directory
Rename-InvalidFiles -path "D:\LLLM Data\linux_data"
