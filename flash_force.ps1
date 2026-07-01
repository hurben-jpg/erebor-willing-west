$env:IDF_PYTHON_ENV_PATH = 'C:\Users\hurben\.espressif\python_env\idf5.3_py3.11_env'
$esptool = "C:/Espressif/frameworks/esp-idf-v5.3.1/components/esptool_py/esptool/esptool.py"
$python = "C:\Users\hurben\.espressif\python_env\idf5.3_py3.11_env\Scripts\python.exe"

cd 'd:\PROJECTS\Antigravity\Erebor\ESP32-P4-WIFI6-Touch-LCD-XC-Demo\ESP-IDF\06_displaypanel_3.4inch\build'

& $python $esptool --chip esp32p4 -p COM4 -b 460800 --before=default_reset --after=hard_reset write_flash --force --flash_mode dio --flash_freq 80m --flash_size 2MB 0x2000 bootloader/bootloader.bin 0x10000 test_esp_lcd_jd9365.bin 0x8000 partition_table/partition-table.bin
