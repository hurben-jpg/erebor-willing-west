$env:IDF_PATH = 'C:\Espressif\frameworks\esp-idf-v5.3.1'
$env:OPENOCD_SCRIPTS = 'C:\Users\hurben\.espressif\tools\openocd-esp32\v0.12.0-esp32-20240318\openocd-esp32\share\openocd\scripts'
$env:IDF_CCACHE_ENABLE = '1'
$env:ESP_ROM_ELF_DIR = 'C:\Users\hurben\.espressif\tools\esp-rom-elfs\20240305\'
$env:IDF_PYTHON_ENV_PATH = 'C:\Users\hurben\.espressif\python_env\idf5.3_py3.11_env'
$env:ESP_IDF_VERSION = '5.3'
$idf_tools_path = 'C:\Users\hurben\.espressif\tools\xtensa-esp-elf-gdb\14.2_20240403\xtensa-esp-elf-gdb\bin;C:\Users\hurben\.espressif\tools\riscv32-esp-elf-gdb\14.2_20240403\riscv32-esp-elf-gdb\bin;C:\Users\hurben\.espressif\tools\xtensa-esp-elf\esp-13.2.0_20240530\xtensa-esp-elf\bin;C:\Users\hurben\.espressif\tools\riscv32-esp-elf\esp-13.2.0_20240530\riscv32-esp-elf\bin;C:\Users\hurben\.espressif\tools\esp32ulp-elf\2.38_20240113\esp32ulp-elf\bin;C:\Users\hurben\.espressif\tools\cmake\3.24.0\bin;C:\Users\hurben\.espressif\tools\openocd-esp32\v0.12.0-esp32-20240318\openocd-esp32\bin;C:\Users\hurben\.espressif\tools\ninja\1.11.1\;C:\Users\hurben\.espressif\tools\idf-exe\1.0.3\;C:\Users\hurben\.espressif\tools\ccache\4.8\ccache-4.8-windows-x86_64;C:\Users\hurben\.espressif\tools\dfu-util\0.11\dfu-util-0.11-win64;C:\Users\hurben\.espressif\python_env\idf5.3_py3.11_env\Scripts;C:\Espressif\frameworks\esp-idf-v5.3.1\tools;'
$env:PATH = $idf_tools_path + $env:PATH

Set-Location 'd:\PROJECTS\Antigravity\Erebor\ESP32-P4-WIFI6-Touch-LCD-XC-Demo\ESP-IDF\06_displaypanel_3.4inch'

Write-Host "Building project..."
idf.py build

Write-Host "Regenerating binary with correct chip revision..."
& "C:\Users\hurben\.espressif\python_env\idf5.3_py3.11_env\Scripts\python.exe" "C:/Espressif/frameworks/esp-idf-v5.3.1/components/esptool_py/esptool/esptool.py" --chip esp32p4 elf2image --min-rev-full 100 --flash_mode dio --flash_freq 80m --flash_size 2MB -o "build\test_esp_lcd_jd9365_fixed.bin" "build\test_esp_lcd_jd9365.elf"

Write-Host "Flashing to COM4..."
& "C:\Users\hurben\.espressif\python_env\idf5.3_py3.11_env\Scripts\python.exe" "C:/Espressif/frameworks/esp-idf-v5.3.1/components/esptool_py/esptool/esptool.py" --chip esp32p4 -p COM4 -b 460800 --before=default_reset --after=hard_reset write_flash --flash_mode dio --flash_freq 80m --flash_size 2MB 0x10000 "build\test_esp_lcd_jd9365_fixed.bin"
