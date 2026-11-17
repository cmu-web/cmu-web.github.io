---
title: QRnegie
description: "QR codes with Carnegie Mellon character, from Scotty portraits to campus landmarks."
nav_order: 3
---

# QRnegie

<div class="cmu-split">
  <div>
    <p class="cmu-lead">QR codes with Carnegie Mellon character, from Scotty portraits to campus landmarks.</p>
    <p><a class="btn" href="https://qrnegie.andrew.cmu.edu/">Go to QRnegie</a></p>
  </div>
  <figure class="cmu-shot cmu-shot--browser"><img src="https://qrnegie.andrew.cmu.edu/images/cmu-web-preview.webp" alt="QRnegie's home page." width="1040" height="656"></figure>
</div>

## What It Does

- **Designs from campus,** like a Scotty portrait or Wean Hall's turtle eating
  a Cheeto, as an SVG or PNG.
- **No tracking or redirect.** A QR code holds your text exactly as entered,
  so it keeps working without QRnegie.
- **Tested before you get it:** every style is checked by decoding the
  finished image.
- **Links, contact cards, events and Wi-Fi networks** from the builder, or any
  text from an image address.

## Who It's For

Anyone making a QR code for a CMU poster, slide, table tent or web page.

## For AI Coding Assistants

QRnegie has an MCP server, so an assistant like Claude, Copilot or Cursor can
use it while it works. Add it as a remote server in the assistant's settings:

| Setting | Value |
| --- | --- |
| Transport | Streamable HTTP |
| URL | `https://qrnegie.andrew.cmu.edu/mcp` |
| Authentication | None |

An assistant can make a QR code in any style and look up which styles and sizes fit.

## Code and License

The code is on GitHub at [cmu-web-qrnegie](https://github.com/cmu-web/cmu-web-qrnegie){: .external}, under
the BSD 3-Clause License. CMU's names, marks and artwork aren't covered by
that license. To report a problem or suggest something, open an issue there.
