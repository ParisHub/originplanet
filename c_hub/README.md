# OriginPlanet C Hub

This folder contains a tiny C helper executable used by `originplanet.hta` for local compute demo integration.

## Build

### Linux/macOS (for validation)
```bash
gcc -std=c11 -Wall -Wextra -pedantic -O2 -o originplanet_c_hub originplanet_c_hub.c
```

### Windows (MSVC)
```bat
cl /nologo /W4 /O2 originplanet_c_hub.c /Fe:originplanet_c_hub.exe
```

### Windows (MinGW)
```bat
gcc -std=c11 -Wall -Wextra -O2 -o originplanet_c_hub.exe originplanet_c_hub.c
```

## Run
```bash
./originplanet_c_hub --eval 2+3
```
Expected output:
```text
5
```

## Notes for HTA integration
- The HTA expects `originplanet_c_hub.exe` to be located next to `originplanet.hta`.
- The current parser intentionally supports only a strict `integer+integer` expression shape for the first milestone.
