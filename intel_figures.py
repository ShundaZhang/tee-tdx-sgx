"""Figure excerpts from Intel's TDX architecture and design documents."""
from html import escape

from diagram_core import frame, tr

BASE = ('Intel TDX Module Base Architecture Specification', '348549-008US',
        'https://cdrdv2.intel.com/v1/dl/getContent/733575')
LOADER = ('Intel TDX SEAM Loader Interface Specification', '343755-004US',
          'https://cdrdv2.intel.com/v1/dl/getContent/733584')
TDVF = ('Intel TDX Virtual Firmware Design Guide', '344991-004US',
        'https://cdrdv2-public.intel.com/733585/tdx-virtual-firmware-design-guide-rev-004-20231206.pdf')
MIGRATION = ('Intel TDX Module TD Migration Architecture Specification', '348550-008US',
             'https://cdrdv2.intel.com/v1/dl/getContent/733578')
CONNECT = ('Intel TDX Connect Architecture Specification', '354629-003US',
           'https://cdrdv2.intel.com/v1/dl/getContent/773614')

# Document, figure number, PDF page (1-based), and pixel dimensions.
FIGURES = {
    'architecture': (BASE, '2.1', 22, 1345, 912),
    'seam-range': (LOADER, '1-2', 12, 1477, 576),
    'module-lifecycle': (BASE, '4.1', 48, 1611, 1263),
    'execution-modes': (BASE, '2.2', 24, 1666, 775),
    'secure-ept': (BASE, '2.3', 26, 1216, 955),
    'connect': (CONNECT, '2.1', 8, 1457, 1194),
    'measurement': (BASE, '12.1', 147, 1461, 848),
    'service-binding': (BASE, '13.1', 154, 1491, 1053),
    'attestation': (TDVF, '8-3', 46, 1202, 852),
    'migration-architecture': (MIGRATION, '2.2', 12, 1628, 912),
    'migration-in-order': (MIGRATION, '6.2', 39, 1619, 830),
    'migration-out-of-order': (MIGRATION, '6.3', 40, 1589, 844),
}


def intel_figure(lang, name, title, alt, caption):
    (document, revision, pdf), number, page, width, height = FIGURES[name]
    asset = f'assets/intel-tdx/{name}.png'
    open_label = tr(lang, 'Open full-size figure', '打开大图')
    image = (
        f'<a class="intel-figure-image" href="{asset}" target="_blank" rel="noopener" '
        f'aria-label="{open_label} · {escape(title, quote=True)}">'
        f'<img src="{asset}" width="{width}" height="{height}" loading="lazy" decoding="async" '
        f'alt="{escape(alt, quote=True)}"></a>'
    )
    source = tr(lang, f'{document} ({revision}), Figure {number}, PDF p. {page}',
                f'{document}（{revision}），图 {number}，PDF 第 {page} 页')
    return frame(lang, f'intel-tdx-{name}', title, image, caption + ' © Intel Corporation.',
                 f'{pdf}#page={page}', source)
