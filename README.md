# TEE / TDX / SGX Atlas

A bilingual learning site focused on Intel SGX and TDX principles, hardware requirements, memory structures, SGX instructions, and TDX module calls. It assumes familiarity with x86 and virtualization. The English edition is the default; visitors can switch to Chinese, and the preference is shared with the other ShundaZhang sites on the same GitHub Pages origin.

The site is static HTML and CSS with a small language-selection script. Run `python3 build.py` to rebuild the eight pages. Remote attestation is summarized only briefly; its protocols and validation belong in a separate study.

Published at <https://shundazhang.github.io/tee-tdx-sgx/>. Primary documentation is linked on the Labs & sources page. Content last checked on September 30, 2026.

## Visual guides

Bilingual architecture and message-flow figures sit next to the corresponding
explanations. They use semantic HTML and local CSS, with captions and primary
source links. Figures remain readable without JavaScript or a diagram CDN.
On small screens, flows stack vertically; sequence diagrams preserve their
three lifelines in a keyboard-focusable horizontal scroll region.

Edit `diagrams.py` for content, `diagram_core.py` for figure primitives, and
`diagrams.css` for presentation, then rebuild with `python3 -B build.py`.
