# TEE Atlas

A bilingual learning site focused on Intel SGX and TDX principles, hardware requirements, memory structures, SGX instructions, TDX module calls, and AMD SEV-SNP architecture. It assumes familiarity with x86 and virtualization. The English edition is the default; visitors can switch to Chinese, and the preference is shared with the other ShundaZhang sites on the same GitHub Pages origin.

The site is static HTML and CSS with a small language-selection script. Run `python3 build.py` to rebuild the twelve pages. The SGX chapter covers privilege levels, enclave call paths, local and remote attestation, and single- and multi-package provisioning. The TDX chapter covers module startup, TD measurement, trusted I/O, Service TD binding, DCAP remote attestation, and live migration. The AMD SEV chapter covers SNP memory validation, guest launch, report verification, trusted I/O, migration and a comparison with Intel TDX. The CoCo chapter covers PodVM launch, Trustee attestation, measured Init-Data, encrypted OCI layers, and a Kubernetes lab.

Published at <https://shundazhang.github.io/tee-tdx-sgx/>. Primary documentation is linked from each platform chapter and the Labs & sources page.

## Visual guides

Bilingual architecture and message-flow figures sit next to the corresponding
explanations. They use semantic HTML and local CSS, with captions and primary
source links. Figures remain readable without JavaScript or a diagram CDN.
On small screens, flows stack vertically; sequence diagrams preserve their
three lifelines in a keyboard-focusable horizontal scroll region. Intel figure
excerpts retain their original labels and link to the source figure and PDF
page. These assets are credited to Intel Corporation in their captions and
PNG metadata. Their document references are in `intel_figures.py`.

Edit `diagrams.py` for content, `diagram_core.py` for figure primitives, and
`diagrams.css` for presentation, then rebuild with `python3 -B build.py`.
