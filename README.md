# Airscarf-Standalone-Module

## Usage:
1. Click the Bootmode-Button on your RP2040 Board and connect it to USB
2. Upload "airscarf-v1.uf2" from "dist-folder" to the Boot Connector
3. Connect to new "Airscarf" Network. Use "12345678" as password
4. Go to 192.168.4.1

## Development:
1. Use prebuild binary(see usage)
2. Edit using Thonny editor to change values

## Building distribution:
1. "pip install littlefs-python"
2. Go to build-firmware and run compile.sh

## Building Micropython:
Not required yet, but there is a micropython-build dir for doing exactly that.
