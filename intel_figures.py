"""Figure excerpts from Intel's SGX and TDX documentation."""
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
SGX_SDM = 'https://cdrdv2.intel.com/v1/dl/getContent/671269'
SGX_EDL = 'https://www.intel.com/content/dam/develop/external/us/en/documents/input-types-and-boundary-checking-edl-737361.pdf'
SGX_FS = 'https://cdrdv2-public.intel.com/671174/sgx-protected-file-system.pdf'
SGX_DCAP = 'https://cc-enabling.trustedservices.intel.com/intel-sgx-tdx-pccs/02/overview/'
SGX_MP = 'https://cc-enabling.trustedservices.intel.com/intel-dcap-mp-ra/'
CC_BY = 'https://creativecommons.org/licenses/by/4.0/'

# Asset, dimensions, exact source URL, source title in English and Chinese.
SGX_FIGURES = {
    'architecture': ('architecture.png', 1539, 622, SGX_SDM + '#page=3', 'Intel SDM 3D (332831-093US), Figure 37-1', 'Intel SDM 3D（332831-093US），图 37-1'),
    'enclave-layout': ('enclave-layout.png', 1548, 802, SGX_SDM + '#page=27', 'Intel SDM 3D (332831-093US), Figure 39-1', 'Intel SDM 3D（332831-093US），图 39-1'),
    'measurement': ('measurement.png', 1561, 802, SGX_SDM + '#page=33', 'Intel SDM 3D (332831-093US), Figure 39-2', 'Intel SDM 3D（332831-093US），图 39-2'),
    'edge-routines': ('edge-routines.png', 1444, 764, SGX_EDL + '#page=3', 'Intel EDL white paper (737361), Figure 2', 'Intel EDL 白皮书（737361），图 2'),
    'ssa': ('ssa.png', 1552, 718, SGX_SDM + '#page=44', 'Intel SDM 3D (332831-093US), Figure 40-2', 'Intel SDM 3D（332831-093US），图 40-2'),
    'protected-fs': ('protected-fs.png', 826, 610, SGX_FS + '#page=2', 'Intel SGX Protected File System, Figure 1', 'Intel SGX 受保护文件系统白皮书，图 1'),
    'local-attestation': ('local-attestation.png', 1553, 589, SGX_SDM + '#page=35', 'Intel SDM 3D (332831-093US), Figure 39-3', 'Intel SDM 3D（332831-093US），图 39-3'),
    'dcap': ('dcap.png', 1014, 803, SGX_DCAP + '#img_intel_sgx_dcap_architecture_diagram', 'Intel PCCS Design Guide, DCAP architecture', 'Intel PCCS 设计指南，DCAP 架构'),
    'multi-package': ('multi-package.svg', 2975, 1267, SGX_MP + '01/introduction/', 'Intel Multi-Package DCAP Guide, server overview', 'Intel 多路 DCAP 指南，服务器概览'),
    'platform-key-lifecycle': ('platform-key-lifecycle.svg', 3662, 2063, SGX_MP + '02/overview/', 'Intel Multi-Package DCAP Guide, platform key lifecycle', 'Intel 多路 DCAP 指南，平台密钥生命周期'),
}

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
    source = tr(lang, f'{document} ({revision}), Figure {number}, PDF p. {page}',
                f'{document}（{revision}），图 {number}，PDF 第 {page} 页')
    return _render_figure(lang, 'tdx', name, f'{name}.png', width, height,
                          title, alt, caption, f'{pdf}#page={page}', source)


def sgx_figure(lang, name, title, alt, caption):
    filename, width, height, url, en, zh = SGX_FIGURES[name]
    if name in ('dcap', 'multi-package', 'platform-key-lifecycle'):
        caption += f' <a class="intel-license" href="{CC_BY}">CC BY 4.0</a>.'
    return _render_figure(lang, 'sgx', name, filename, width, height, title, alt, caption, url, tr(lang, en, zh))


def _render_figure(lang, family, name, filename, width, height, title, alt, caption, url, source):
    asset = f'assets/intel-{family}/{filename}'
    open_label = tr(lang, 'Open full-size figure', '打开大图')
    image = (
        f'<a class="intel-figure-image" href="{asset}" target="_blank" rel="noopener" '
        f'aria-label="{open_label} · {escape(title, quote=True)}">'
        f'<img src="{asset}" width="{width}" height="{height}" loading="lazy" decoding="async" '
        f'alt="{escape(alt, quote=True)}"></a>'
    )
    return frame(lang, f'intel-{family}-{name}', title, image, caption + ' © Intel Corporation.', url, source)
