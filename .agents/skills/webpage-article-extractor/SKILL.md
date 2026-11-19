---
name: webpage-article-extractor
description: Extract the main article from a webpage, preserve its title and source attribution, and verify the extracted text against the page.
prompt-source: prompt.toon
---
skill: "webpage-article-extractor"
sections[2]:
  - "\n"
  - "# Extract an article from a webpage\n\n1. Open the supplied page with an available browser or retrieval tool.\n2. Identify the title, author, date when present, canonical source, and main article.\n3. Separate navigation, advertisements, related links, and repeated interface text.\n4. Preserve paragraph order and source attribution. Check the extracted text\n   against the rendered article, including tables and code relevant to the request.\n5. Return the requested summary or a permitted excerpt with the source link.\n   Report inaccessible or missing content instead of inventing it.\n"
