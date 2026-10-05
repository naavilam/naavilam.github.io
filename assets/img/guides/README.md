# Software guide illustrations

Literature Alerts now uses five actual source excerpts, copied from the local project on 2026-10-05. **No `lital01.png`–`lital05.png` files are required.** The excerpts and original line references are in `_data/literature-examples.json`, rendered through `_includes/source-excerpt.html`. Update that data file when the upstream configuration changes.

GitHub Version Control now uses six native HTML terminal illustrations. **No `gitvc01.png`–`gitvc06.png` files are required.** Their fictional session is stored in `_data/release-examples.json` and rendered by `_includes/release-terminal.html`. Minor and major release examples show conceptual state transitions, explicitly labeled as such.

Save your PNG screenshots in the folders below. The pages show a styled placeholder until each file exists; on the next Jekyll build the actual image appears automatically. No post editing is required. All image URLs use `relative_url` for deployment under a base path.

Use readable screenshots, ideally 1400–1800 px wide. Crop unnecessary browser chrome, keep text legible, and omit credentials and webhook URLs. PNG filenames are case-sensitive. Figures link to their full-size image.

| Folder | Filename | Capture |
| --- | --- | --- |
| `molecular-symmetry/` | `molsym01.png` | Molecule selector and XYZ coordinate panel |
| `molecular-symmetry/` | `molsym02.png` | Interactive 3D molecular view |
| `molecular-symmetry/` | `molsym03.png` | Representation, palette and display controls |
| `molecular-symmetry/` | `molsym04.png` | Symmetry analysis selection panel |
| `molecular-symmetry/` | `molsym05.png` | TeX result and PDF export actions |
| `molecular-symmetry/` | `molsym06.png` | Custom XYZ pasted into the editable coordinate field |
| `quantum-battleship/` | `qubat01.png` | AWS backend carousel and game configuration |
| `quantum-battleship/` | `qubat02.png` | Player name and experiment consent dialog |
| `quantum-battleship/` | `qubat03.png` | Player board, opponent board and coordinate attack field |
| `quantum-battleship/` | `qubat04.png` | End-of-game overlay showing the battle outcome |
| `quantum-battleship/` | `qubat05.png` | Analytics page with hardware, shots and charts |
| `zotero-plugin/` | `zoter01.png` | GitHub release assets with the XPI plugin package |
| `zotero-plugin/` | `zoter02.png` | Zotero plugin manager installing the downloaded XPI |
| `zotero-plugin/` | `zoter03.png` | Mirror root and log directory configuration |
| `zotero-plugin/` | `zoter04.png` | Collection context menu with the sanitize action |
| `zotero-plugin/` | `zoter05.png` | Zotero collection hierarchy beside the mirrored filesystem tree |

The reusable component is `_includes/software-figure.html`; the scoped styling is `assets/css/software-guides.css`. To add a figure, include the component with `folder`, `file`, `alt`, and `caption`. Use English alternative text and captions.

Content was checked against public repository source on 2026-10-05. Capture the actual deployed interface for each figure; its labels can differ from the English guide.
