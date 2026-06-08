# Realtor.com Photos Extractor

A small Python script that downloads full-resolution photos from a saved [realtor.com](https://www.realtor.com) listing page.

Realtor.com serves compressed images in the browser. This tool reads the listing data embedded in a saved HTML file and downloads the original high-resolution versions (up to 2048×1536) to a folder on your machine.

## Requirements

- Python 3.9 or newer (Homebrew installs a suitable Python automatically)
- No third-party packages — uses only the standard library

## Usage

### 1. Install the script

Install via [Homebrew](https://brew.sh):

```bash
brew tap lstarrett/utilities
brew install realtor-photo-extractor
```

This installs the `realtor-photo-extractor` command on your PATH.

### 2. Save the listing page

1. Open a listing on [realtor.com](https://www.realtor.com) in your browser.
2. Wait for the page to finish loading (including the photo gallery).
3. Right-click on the page and choose **Save Page As…** (or **Save As…**).
4. Save the file as **Web Page, Complete** (or **HTML only** — both work). Note where you saved it (saving the page to a dedicated directory named for the property is recommended, so that photos can be extracted to the same place)

### 3. Run the script

Pass the saved HTML file as the argument:

```bash
realtor-photo-extractor path/to/listing.html
```

By default, photos are saved to a `photos/` folder in the current directory.

Optionally, use `-o` to choose where photos should go:

```bash
realtor-photo-extractor path/to/listing.html -o ~/Pictures/my-listing
```

### 4. Check the results

The script prints progress as each photo downloads. When it finishes, open the output folder — photos are named `001.jpg`, `002.jpg`, and so on.

## Options


| Flag             | Description                                               |
| ---------------- | --------------------------------------------------------- |
| `-o`, `--output` | Output directory (default: `photos/`)                     |
| `--thumb`        | Download thumbnail URLs instead of full-resolution images |


## Example

```bash
realtor-photo-extractor ~/Downloads/123-Main-St.html -o ~/Pictures/123-main-st
```

## License

MIT — see [LICENSE](LICENSE).