---
title: FencePost
description: "Link previews for Carnegie Mellon websites: the image and the Open Graph tags."
nav_order: 4
---

# FencePost

<div class="cmu-split">
  <div>
    <p class="cmu-lead">Link previews for Carnegie Mellon websites: the image and the Open Graph tags.</p>
    <p><a class="btn" href="https://fencepost.andrew.cmu.edu/">Go to FencePost</a></p>
  </div>
  <figure class="cmu-shot cmu-shot--browser"><img src="https://fencepost.andrew.cmu.edu/images/cmu-web-preview.webp" alt="FencePost's home page." width="1040" height="656"></figure>
</div>

## What It Does

- **Check a link** before you share it: see what Slack, Teams or a social
  post will show, and what to fix, checked against the Web Kilt's Link
  Previews / Open Graph standard.
- **Make a preview:** give it a page and get the 1200 by 630 image, under
  300 KB, and the Open Graph tags that go with it. Nothing is stored.
- **Carnegie Mellon sites only:** pages on cmu.edu and approved Carnegie
  Mellon domains, captured signed out, the way a social site sees them.

## Who It's For

Anyone about to share a CMU page, or putting the finishing touches on a site. It's named for The Fence, where Carnegie Mellon students paint what they want everyone to see.

## For AI Coding Assistants

FencePost has an MCP server, so an assistant like Claude, Copilot or Cursor can
use it while it works. Add it as a remote server in the assistant's settings:

| Setting | Value |
| --- | --- |
| Transport | Streamable HTTP |
| URL | `https://fencepost.andrew.cmu.edu/mcp` |
| Authentication | None |

An assistant can check a page's link preview and make a preview image and tags for it.

## Code and License

The code is on GitHub at [cmu-web-fencepost](https://github.com/cmu-web/cmu-web-fencepost){: .external}, under
the BSD 3-Clause License. CMU's names, marks and artwork aren't covered by
that license. To report a problem or suggest something, open an issue there.
