$python = "C:\Users\hurben\.espressif\python_env\idf5.3_py3.11_env\Scripts\python.exe"
$esptool = "C:\Espressif\frameworks\esp-idf-v5.3.1\components\esptool_py\esptool\esptool.py"
$build_dir = "d:\PROJECTS\Antigravity\Erebor\esp-hosted\esp_hosted_fg\esp\esp_driver\network_adapter\build"

Write-Host "Flashing ESP32-C6 Firmware via P4 Bridge..."
Write-Host "Ensure P4 is running the bridge app (tusb_serial_device) and C6 is in bootloader mode."

& $python $esptool -p COM4 -b 115200 --before default_reset --after hard_reset --chip esp32c6 write_flash --flash_mode dio --flash_size 4MB --flash_freq 80m 0x0 "$build_dir\bootloader\bootloader.bin" 0x8000 "$build_dir\partition_table\partition-table.bin" 0xd000 "$build_dir\ota_data_initial.bin" 0x10000 "$build_dir\network_adapter.bin"

if ($LASTEXITCODE -eq 0) {
    Write-Host "C6 Firmware Flashed Successfully!" -ForegroundColor Green
}
else {
    Write-Host "Flashing Failed. Please check connections and boot mode." -ForegroundColor Red
}

Read-Host "Press Enter to exit..."
