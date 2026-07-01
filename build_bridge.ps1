$python = "C:\Users\hurben\.espressif\python_env\idf5.3_py3.11_env\Scripts\python.exe"
$esptool = "C:\Espressif\frameworks\esp-idf-v5.3.1\components\esptool_py\esptool\esptool.py"
$build_dir = "d:\PROJECTS\Antigravity\Erebor\tusb_serial_device\build"

Write-Host "Flashing USB Bridge to ESP32-P4 (Forcing Revision Check)..."

# Using --force to bypass "chip revision in range [v0.1 - v0.99] (this chip is revision v1.0)" error
& $python $esptool -p COM4 -b 460800 --before default_reset --after hard_reset --chip esp32p4 write_flash --force --flash_mode dio --flash_size 2MB --flash_freq 80m 0x2000 "$build_dir\bootloader\bootloader.bin" 0x8000 "$build_dir\partition_table\partition-table.bin" 0x10000 "$build_dir\tusb_serial_device.bin"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Bridge Flashed Successfully!" -ForegroundColor Green
}
else {
    Write-Host "Bridge Flashing Failed." -ForegroundColor Red
}

Read-Host "Press Enter to exit..."
