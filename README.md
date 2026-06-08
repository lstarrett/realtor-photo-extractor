# Realtor.com Photos Extractor

A small Python script that downloads full-resolution photos from a saved [realtor.com](https://www.realtor.com) listing page.

Realtor.com serves compressed images in the browser. This tool reads the listing data embedded in a saved HTML file and downloads the original high-resolution versions (up to 2048×1536) to a folder on your machine.

## Requirements

- Python 3.9 or newer
- No third-party packages — uses only the standard library

## Usage

### 1. Save the listing page

1. Open a listing on [realtor.com](https://www.realtor.com) in your browser.
2. Wait for the page to finish loading (including the photo gallery).
3. Right-click on the page and choose **Save Page As…** (or **Save As…**).
4. Save the file as **Web Page, Complete** (or **HTML only** — both work). Note where you saved it.

### 2. Run the script

From this directory, pass the saved HTML file as the argument:

```bash
python3 extract_realtor_photos.py path/to/listing.html
```

By default, photos are saved to `photos/<filename>/` (e.g. `photos/listing/` if you saved as `listing.html`).

### 3. Choose an output directory (optional)

Use `-o` to specify where photos should go:

```bash
python3 extract_realtor_photos.py path/to/listing.html -o ~/Pictures/my-listing
```

### 4. Check the results

The script prints progress as each photo downloads. When it finishes, open the output folder — photos are named `001.jpg`, `002.jpg`, and so on.

## Options


| Flag             | Description                                               |
| ---------------- | --------------------------------------------------------- |
| `-o`, `--output` | Output directory (default: `photos/<html-stem>/`)         |
| `--thumb`        | Download thumbnail URLs instead of full-resolution images |


## Example

```bash
python3 extract_realtor_photos.py ~/Downloads/123-Main-St.html -o ~/Pictures/123-main-st
```

## License

MIT — see [LICENSE](LICENSE).