# Turn off console output
$null = [Console]::OpenStandardOutput().Flush()
$null = [Console]::SetOut([IO.TextWriter]::Null)

# Generate a random wait time between 0 to 17 minutes
$random = New-Object Random
$waitTime = $random.Next(0, 5 * 60 * 1000)

# Wait for the random amount of time
#Start-Sleep -Milliseconds $waitTime
#Start-Sleep -Milliseconds 60000

# Loop until the last line of the Python script output is "bye"
while ($true) {
    # Start a new terminal and execute the Python script
    Start-Process -FilePath "python3" -ArgumentList "C:\Users\hyang\Desktop\meow\lit_clock.py" -WindowStyle Hidden -Wait

    # Get the last line of the Python script output
    $lastLine = Get-Content -Path "C:\Users\hyang\Desktop\meow\output.txt" | Select-Object -Last 1

    # Check if the last line is "bye"
    if ($lastLine -eq "bye") {
        # Wait for 1 second
        Start-Sleep -Seconds 1
        break
    }
}