import os
import unittest
from bs4 import BeautifulSoup
from urllib.parse import urlparse

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

class TestHtmlLinks(unittest.TestCase):
    def setUp(self):
        self.html_files = []
        for root, dirs, files in os.walk(REPO_ROOT):
            for f in files:
                if f.endswith('.html'):
                    self.html_files.append(os.path.join(root, f))

    def _is_local(self, link):
        if not link or link.startswith('#'):
            return False
        parsed = urlparse(link)
        return parsed.scheme == ''

    def test_links_exist(self):
        missing = []
        for html_file in self.html_files:
            with open(html_file, 'r', encoding='utf-8') as fh:
                soup = BeautifulSoup(fh, 'html.parser')
            attrs = [(tag.get('href'), html_file) for tag in soup.find_all(href=True)]
            attrs += [(tag.get('src'), html_file) for tag in soup.find_all(src=True)]
            for path, source in attrs:
                if not self._is_local(path):
                    continue
                # strip query and fragment
                cleaned = path.split('#')[0].split('?')[0]
                if cleaned.startswith('/'):
                    target = os.path.join(REPO_ROOT, cleaned.lstrip('/'))
                else:
                    target = os.path.normpath(os.path.join(os.path.dirname(source), cleaned))
                if not os.path.exists(target):
                    missing.append(f"{path} referenced in {os.path.relpath(source, REPO_ROOT)}")
        if missing:
            self.fail("Missing files:\n" + "\n".join(sorted(missing)))

if __name__ == '__main__':
    unittest.main()
