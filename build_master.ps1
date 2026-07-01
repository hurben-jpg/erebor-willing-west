$env:IDF_PATH = 'C:\Espressif\frameworks\esp-idf-master'
$env:OPENOCD_SCRIPTS = 'C:\Users\hurben\.espressif\tools\openocd-esp32\v0.12.0-esp32-20250707\openocd-esp32\share\openocd\scripts'
$env:IDF_CCACHE_ENABLE = '1'
$env:ESP_ROM_ELF_DIR = 'C:\Users\hurben\.espressif\tools\esp-rom-elfs\20241011\'
$env:IDF_PYTHON_ENV_PATH = 'C:\Users\hurben\.espressif\python_env\idf6.1_py3.11_env'
$idf_tools_path = 'C:\Users\hurben\.espressif\tools\riscv32-esp-elf-gdb\16.3_20250913\riscv32-esp-elf-gdb\bin;C:\Users\hurben\.espressif\tools\riscv32-esp-elf\esp-15.2.0_20250929\riscv32-esp-elf\bin;C:\Users\hurben\.espressif\tools\cmake\4.0.3\bin;C:\Users\hurben\.espressif\tools\openocd-esp32\v0.12.0-esp32-20250707\openocd-esp32\bin;C:\Users\hurben\.espressif\tools\ninja\1.12.1\;C:\Users\hurben\.espressif\tools\idf-exe\1.0.3\;C:\Users\hurben\.espressif\tools\ccache\4.12.1\ccache-4.12.1-windows-x86_64;C:\Users\hurben\.espressif\python_env\idf6.1_py3.11_env\Scripts;C:\Espressif\frameworks\esp-idf-master\tools;'
$env:PATH = $idf_tools_path + $env:PATH

Set-Location 'd:\PROJECTS\Antigravity\Erebor\ESP32-P4-WIFI6-Touch-LCD-XC-Demo\ESP-IDF\02_HelloWorld'

Write-Host "Building Hello World with ESP-IDF Master Branch (v6.1-dev)..."
idf.py build

if (Test-Path "build\HelloWorld.elf") {
    Write-Host "Build successful! Flashing to device..."
    idf.py -p COM4 flash monitor
}
else {
    Write-Host "Build failed - trying set-target first..."
    idf.py set-target esp32p4
    idf.py build
    
    if (Test-Path "build\HelloWorld.elf") {
        Write-Host "Build successful after set-target! Flashing..."
        idf.py -p COM4 flash monitor
    }
    else {
        Write-Host "Build failed"
    }
}
