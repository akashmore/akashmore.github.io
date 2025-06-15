# Akash More Website

This repository contains static files for the personal website.

## Running link tests

A simple test script checks that all local links and resources referenced by the HTML files exist within the repository. Ensure you have `beautifulsoup4` installed and run:

```bash
python tests/test_links.py
```

The script parses every `.html` file and reports missing local paths if any are found.
