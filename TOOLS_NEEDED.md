# External Tools Required

This document lists document formats that require external tools/libraries to function.

## Container Formats

| Format | Tool Needed | Install Command |
|--------|-------------|-----------------|
| rar | unrar | `apt install unrar` |
| sevenzip | 7z | `apt install p7zip-full` |

## Ebook Formats

| Format | Python Library | Install Command |
|--------|-----------------|-----------------|
| epub | ebooklib | `pip install ebooklib` |
| mobi | python-mobi | `pip install python-mobi` |
| azw | kindleunpack | `pip install kindleunpack` |

## CAD Formats

| Format | Python Library | Install Command |
|--------|-----------------|-----------------|
| dxf | ezdxf | `pip install ezdxf` |
| dwg | ezdxf (ODA needed) | `pip install ezdxf` |
| step | pythonocc | `pip install pythonocc` |
| iges | pythonocc | `pip install pythonocc` |
| blend | Blender Python API | Requires Blender installed |
| fbx | fbx-sdk | Requires FBX SDK |

## Office Formats

| Format | Python Library | Install Command |
|--------|-----------------|-----------------|
| pptx | python-pptx | `pip install python-pptx` |
| odt | odfpy | `pip install odfpy` |
| latex | latex | `apt install texlive-latex-base` |
| rtf | - | Built-in (python) |
| asciidoc | asciidoc | `pip install asciidoc` |

## Media Formats

| Format | Tool Needed | Install Command |
|--------|-------------|-----------------|
| video | ffmpeg | `apt install ffmpeg` |
| audio | ffmpeg | `apt install ffmpeg` |
| heic | libheif | `apt install libheif-tools` |
| raw | dcraw/libraw | `apt install libraw-dev` |

## Status: Working Without External Tools

These formats work out of the box:
- csv, json, yaml, xml (data)
- ini, toml, env (config)
- zip, tar (container)
- obj, stl, scad, gltf (basic CAD)
- epub (planned)
- rtf (planned)
