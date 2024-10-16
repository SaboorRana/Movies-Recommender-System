$sourceFile = "similarity.pkl"
$chunkSize = 90MB  # First chunk is 90MB, remaining will be the second part
$destinationPath = "similarity_part_"

$stream = [System.IO.File]::OpenRead($sourceFile)
$buffer = New-Object byte[] $chunkSize
$index = 0

while (($readBytes = $stream.Read($buffer, 0, $chunkSize)) -gt 0) {
    $partFile = "{0}{1}.pkl" -f $destinationPath, $index
    $writeStream = [System.IO.File]::Create($partFile)
    $writeStream.Write($buffer, 0, $readBytes)
    $writeStream.Close()
    $index++
}

$stream.Close()
