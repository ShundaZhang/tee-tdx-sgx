"""AMD SEV chapter for the bilingual TEE atlas."""

from diagram_core import arrow, flow, frame, node, tr

AMD_SEV = 'https://www.amd.com/en/developer/sev.html'
SNP_ABI = 'https://docs.amd.com/v/u/en-US/56860_PUB_SEV_SNP'
SNP_ABI_PDF = 'https://www.amd.com/content/dam/amd/en/documents/developer/56860.pdf'
SNP_PAPER = 'https://docs.amd.com/api/khub/documents/atTablNxGjuR5pX3kM7WdQ/content'
TIO_PAPER = 'https://www.amd.com/content/dam/amd/en/documents/epyc-business-docs/white-papers/sev-tio-whitepaper.pdf'
TIO_ABI = 'https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/specifications/58271.pdf'
AMD_PSB = 'https://www.amd.com/en/products/processors/server/epyc/infinity-guard.html#secure-boot'
KVM = 'https://docs.kernel.org/virt/kvm/x86/amd-memory-encryption.html'
GUEST = 'https://docs.kernel.org/virt/coco/sev-guest.html'
TDISP = 'https://pcisig.com/PCI%20Express/ECN/Base/TEEDeviceInterfaceSecurityProtocol'

FIGURES = {
    'threat-model': (SNP_PAPER, 2, 5, 1373, 747),
    'rmp-checks': (SNP_PAPER, 3, 9, 1052, 555),
    'page-states': (SNP_PAPER, 4, 10, 809, 714),
    'attestation': (SNP_PAPER, 10, 17, 1432, 664),
    'tio-architecture': (TIO_PAPER, 3, 7, 1281, 1086),
    'tio-lifecycle': (TIO_PAPER, 8, 14, 1415, 505),
}


def amd_figure(lang, key, title, caption):
    url, number, page, width, height = FIGURES[key]
    asset = f'assets/amd-sev/{key}.png'
    label = tr(lang, 'Open full-size figure', '打开大图')
    description = tr(lang, f'AMD white paper, Figure {number}, PDF p. {page}', f'AMD 白皮书，图 {number}，PDF 第 {page} 页')
    content = (
        f'<a class="intel-figure-image" href="{asset}" target="_blank" rel="noopener" aria-label="{label} · {title}">'
        f'<img src="{asset}" width="{width}" height="{height}" loading="lazy" decoding="async" alt="{title}"></a>'
    )
    return frame(lang, f'amd-sev-{key}', title, content, caption + ' © Advanced Micro Devices, Inc.',
                 f'{url}#page={page}', description)


def sev_page(lang, *, page_hero, article, table, link):
    t = lambda en, zh: tr(lang, en, zh)
    suffix = t('.html', '.zh.html')
    topics = [
        ('architecture', t('Architecture', '整体架构')),
        ('memory', t('Memory and VM exits', '内存与 VM 退出')),
        ('trust-chain', t('Trust chain and launch', '信任链与启动')),
        ('attestation', t('Remote attestation', '远程证明')),
        ('tee-io', t('Trusted I/O', '可信 I/O')),
        ('migration', t('Migration', '迁移')),
        ('tdx-comparison', t('TDX comparison', '与 TDX 对照')),
        ('sources', t('Sources and exercises', '资料与练习')),
    ]
    items = ''.join(f'<li><a href="#{ident}">{title}</a></li>' for ident, title in topics)
    nav = f'<nav class="tdx-contents" aria-label="{t("SEV contents", "SEV 章节目录")}"><ul class="wrap">{items}</ul></nav>'

    def figure(key, title, caption):
        return amd_figure(lang, key, t(*title), t(*caption))

    def reading_flow(ident, title, steps, caption, url, source):
        elements = []
        for name, desc in steps:
            if elements:
                elements.append(arrow())
            elements.append(node(t(*name), t(*desc), 'protected'))
        return frame(lang, ident, t(*title), flow(elements), t(*caption), url, source)

    hero = page_hero(lang, 'AMD SEV', t('AMD SEV<br><em>From memory encryption to confidential VMs</em>',
                                      'AMD SEV<br><em>从内存加密到机密虚拟机</em>'),
                     t('Follow a VM through page validation, launch measurement, remote attestation, device assignment and migration.',
                       '跟随一台虚拟机，理解页面验证、启动度量、远程证明、可信设备分配与迁移。'))

    versions = table(t(('Technology', 'What it adds', 'Where to focus'), ('技术', '新增机制', '阅读重点')), [
        ('SEV', t('Private guest memory uses a per-VM key.', '用每 VM 密钥保护 Guest 私有内存。'),
         t('ASID selects the guest key. The C-bit distinguishes encrypted guest mappings from shared mappings.', 'ASID 关联 Guest 密钥。C-bit 区分加密的 Guest 映射和共享映射。')),
        ('SEV-ES', t('Protects vCPU register state across VM exits in an encrypted VMSA.', '将 VM 退出时的 vCPU 寄存器状态保存在加密的 VMSA 中。'),
         t('The guest explicitly shares the operands the VMM needs through GHCB.', 'Guest 通过 GHCB 显式共享 VMM 需要的操作数。')),
        ('SEV-SNP', t('Adds the Reverse Map Table, page validation and a guest-requestable signed report.', '加入反向映射表、页面验证和 Guest 可主动请求的签名报告。'),
         t('The CPU checks ownership and mapping. The verifier evaluates the guest and platform TCB.', 'CPU 检查页面所有权和映射。验证者评估 Guest 和平台 TCB。')),
        ('SEV-TIO', t('Extends SNP with trusted device assignment on supported platforms.', '在支持的平台上为 SNP 增加可信设备分配。'),
         t('TDISP, SPDM, PCIe IDE and the IOMMU work together.', 'TDISP、SPDM、PCIe IDE 与 IOMMU 协同工作。')),
    ])
    architecture = article(t('ARCHITECTURE', '架构'), t('Four steps from SEV to trusted I/O', '从 SEV 到可信 I/O'),
        t('SVM runs the virtual machine. The memory controller uses VM-specific encryption keys, while AMD Secure Processor (AMD-SP, also called ASP or PSP) manages key and guest lifecycle operations. SNP adds hardware checks to the host-controlled nested mapping.',
          'SVM 运行虚拟机，内存控制器使用 VM 专属加密密钥。AMD Secure Processor（AMD-SP，也称 ASP 或 PSP）管理密钥和 Guest 生命周期。SNP 在宿主管理的嵌套映射上增加硬件检查。'),
        versions + figure('threat-model', ('SEV-SNP trust boundary', 'SEV-SNP 信任边界'),
            ('Green marks the target guest and AMD hardware and firmware in its trust model. The host, other VMs and ordinary PCI devices sit outside that boundary.',
             '绿色是目标 Guest 及其信任的 AMD 硬件与固件。宿主、其他虚拟机与普通 PCI 设备在这条边界之外。')), 'architecture')

    memory = article(t('MEMORY AND CPU STATE', '内存与 CPU 状态'), t('Follow a private page and a VM exit', '跟踪一次私有页访问与 VM 退出'),
        t('The guest page tables translate GVA to GPA. The VMM-managed Nested Page Table (NPT) translates GPA to system physical address. The CPU checks the Reverse Map Table (RMP), indexed by system physical address, to enforce ownership, the expected GPA and relevant access rights.',
          'Guest 页表将 GVA 转换为 GPA，VMM 管理的 NPT 将 GPA 转换为系统物理地址。CPU 以系统物理地址查询 RMP，核对所有权、预期 GPA 和相关访问权限。'),
        figure('rmp-checks', ('RMP checks after address translation', '地址转换后的 RMP 检查'),
               ('A nested page-table entry supplies the translation. The RMP lets hardware cross-check it against the page assignment.',
                '嵌套页表给出地址转换结果，硬件用 RMP 核对该结果是否符合页面分配记录。'))
        + figure('page-states', ('Host assignment and guest validation', '宿主分配与 Guest 验证'),
                 ('For a runtime private page, RMPUPDATE assigns it and PVALIDATE makes it usable by the guest. Guest software tracks which GPAs it already validated to detect unexpected remapping.',
                  '对于运行时私有页，RMPUPDATE 完成分配，PVALIDATE 让 Guest 可以使用该页。Guest 软件跟踪已验证的 GPA，以识别异常重映射。'))
        + '<p>' + t(
            'SEV-ES and SNP protect the Virtual Machine Save Area (VMSA). For an operation such as an intercepted CPUID that needs host emulation, a #VC handler puts only required fields in the shared Guest-Hypervisor Communication Block (GHCB), executes VMGEXIT, then validates the response.',
            'SEV-ES 和 SNP 保护虚拟机状态保存区（VMSA）。例如 CPUID 被拦截且需要宿主模拟时，#VC 处理程序只将所需字段写入共享 GHCB，执行 VMGEXIT，再校验返回值。'
        ) + '</p><p>' + t(
            'VMPL0–3 are privilege levels inside a SNP guest, with VMPL0 most privileged. An optional Secure VM Service Module (SVSM) can run at VMPL0 and provide services such as vTPM to a guest OS at a lower privilege. RMP permissions apply alongside normal page-table checks.',
            'VMPL0–3 是 SNP Guest 内部的权限层级，VMPL0 权限最高。可选的 Secure VM Service Module（SVSM）可运行在 VMPL0，向较低权限的 Guest OS 提供 vTPM 等服务。RMP 权限与普通页表检查共同生效。'
        ) + '</p>', 'memory')

    launch = reading_flow('sev-launch-flow', ('SNP launch and measurement', 'SNP 启动与度量'), [
        (('AMD-SP ready', 'AMD-SP 就绪'), ('Firmware authenticated by the platform root of trust', '平台信任根认证固件')),
        (('SNP_LAUNCH_START', 'SNP_LAUNCH_START'), ('Create guest context, set policy and initialize launch state', '创建 Guest 上下文，设置策略并初始化启动状态')),
        (('SNP_LAUNCH_UPDATE', 'SNP_LAUNCH_UPDATE'), ('Load and measure initial pages and metadata', '装载并度量初始页面和元数据')),
        (('SNP_LAUNCH_FINISH', 'SNP_LAUNCH_FINISH'), ('Finalize launch and check an optional ID block', '完成启动并检查可选 ID Block')),
    ], ('The VMM requests launch through KVM. The AMD-SP owns the trusted launch context and computes the initial guest digest.',
        'VMM 通过 KVM 发起启动请求。AMD-SP 管理可信启动上下文并计算 Guest 初始度量。'), KVM, 'Linux KVM SEV')
    platform_boot = f'<a class="inline-link" href="{AMD_PSB}">{t("AMD Secure Boot ↗", "AMD 安全启动 ↗")}</a>'
    chain = table(t(('Trust layer', 'Evidence and meaning'), ('信任层', '证据及含义')), [
        (t('Platform firmware', '平台固件'),
         t('AMD-SP boot ROM anchors authentication of AMD firmware. AMD Platform Secure Boot can extend the host firmware chain to OEM BIOS. The SNP report exposes relevant TCB versions for verifier policy.',
           'AMD-SP 的 Boot ROM 是 AMD 固件认证的信任根。AMD Platform Secure Boot 可将宿主固件信任链延伸到 OEM BIOS。SNP 报告提供相关 TCB 版本，供验证者制定策略。') + ' ' + platform_boot),
        (t('Guest launch', 'Guest 启动'),
         t('MEASUREMENT is the SHA-384 launch digest of the measured initial image and page metadata. An optional signed ID Block can bind the expected digest and guest identity. The verifier checks the expected boot image and policy.',
           'MEASUREMENT 是对已度量的初始镜像及页面元数据计算的 SHA-384 启动摘要。可选的签名 ID Block 可绑定预期摘要与 Guest 身份。验证者核对预期启动镜像和策略。')),
        (t('Guest OS and runtime', 'Guest OS 与运行期'),
         t('Guest UEFI Secure Boot can enforce signature policy for later boot stages. To verify later measurements, a deployment needs a separately specified measured boot and evidence binding design, such as a vTPM event log and Quote tied to the attested guest.',
           'Guest UEFI Secure Boot 可对后续启动阶段执行签名策略。若要验证后续度量，需要另有度量启动和证据绑定方案，例如将 vTPM 事件日志和 Quote 绑定到已证明的 Guest。')),
        (t('Report signer', '报告签名者'),
         t('The verifier uses the AMD Root Key (ARK) and the correct intermediate and endorsement certificate for VCEK or VLEK. Signature verification authenticates the report bytes. Deployment policy determines whether the evidence is acceptable.',
           '验证者以 AMD Root Key（ARK）为根，按 VCEK 或 VLEK 选择正确的中间证书与背书证书。验签确认报告字节的真实性，部署策略决定是否接受证据。')),
    ])
    trust = article(t('TRUST CHAIN', '信任链'), t('From AMD-SP firmware to guest launch', '从 AMD-SP 固件到 Guest 启动'),
        t('Read platform firmware authentication, guest launch measurement and report certificate validation as three checks with different inputs.',
          '平台固件认证、Guest 启动度量、报告证书验证分别检查不同的输入。'), launch + chain, 'trust-chain')

    evidence = table(t(('Check', 'What the verifier checks'), ('检查项', '验证者检查什么')), [
        (t('Signer and certificate path', '签名与证书链'),
         t('Read the signing-key indicator. For VCEK, validate ARK → ASK → VCEK and match the chip ID and reported TCB as required by the certificate profile. For VLEK, validate ARK → ASVK → VLEK and its TCB claims. Check revocation and verify the ECDSA P-384 report signature.',
           '读取签名密钥类型。VCEK 走 ARK → ASK → VCEK，并按证书规范匹配芯片 ID 与 reported TCB。VLEK 走 ARK → ASVK → VLEK，并核对 TCB 声明。检查撤销状态并验证报告的 ECDSA P-384 签名。')),
        ('REPORT_DATA',
         t('Recompute the application-defined binding over a fresh verifier nonce and, when provisioning secrets, a guest ephemeral public key or channel transcript. The report field is 64 bytes.',
           '重算应用协议定义的绑定值，纳入验证者的新鲜 nonce。在下发秘密时，同时绑定 Guest 临时公钥或通道握手记录。该字段为 64 字节。')),
        ('MEASUREMENT / POLICY / VMPL',
         t('Compare the launch digest with the expected image. Check policy such as DEBUG and migration-agent allowance, the reporting VMPL and minimum accepted TCB versions.',
           '将启动摘要与预期镜像比较。检查 DEBUG、是否允许迁移代理等策略、生成报告的 VMPL 及最低可接受 TCB 版本。')),
        ('HOST_DATA / REPORT_ID_MA',
         t('HOST_DATA is set by the host at launch and can be compared with an independently known value. For an agent-bound VM, REPORT_ID_MA identifies the MA instance. Evaluate that agent’s own evidence and policy where the deployment relies on it.',
           'HOST_DATA 由宿主在启动时设置，可与独立取得的预期值比较。绑定迁移代理时，REPORT_ID_MA 标识该代理实例。若部署依赖代理，需检查代理自己的证据和策略。')),
    ])
    attestation = article(t('REMOTE ATTESTATION', '远程证明'), t('Request an SNP report and verify it off-host', '请求 SNP 报告并在远端验证'),
        t('The guest sends MSG_REPORT_REQ to AMD-SP using VMPCK-protected guest messages. The hypervisor transports the request. Firmware signs the report directly with VCEK or a provisioned VLEK, according to platform configuration.',
          'Guest 通过受 VMPCK 保护的消息向 AMD-SP 发送 MSG_REPORT_REQ，由 Hypervisor 转发。固件按平台配置使用 VCEK 或已预配的 VLEK 直接签署报告。'),
        figure('attestation', ('Guest key binding and remote verification', 'Guest 公钥绑定与远程验证'),
               ('The original figure shows a public-key hash. A challenge-response protocol also binds a verifier nonce for freshness.',
                '原图展示公钥哈希绑定。挑战应答协议还会绑定验证者的 nonce，以确认报告的新鲜度。'))
        + evidence + '<p>' + t(
            'Linux exposes <code>/dev/sev-guest</code> and <code>SNP_GET_REPORT</code>. An extended request can also return certificates supplied by the host. Treat those certificates as input and validate them to an independently trusted AMD root. Release secrets only after the channel key and evidence pass policy.',
            'Linux 提供 <code>/dev/sev-guest</code> 和 <code>SNP_GET_REPORT</code>。扩展请求还可取得宿主提供的证书。应将这些证书视为输入，并验证到独立信任的 AMD 根。仅在通道密钥和证据通过策略后下发秘密。'
        ) + '</p>', 'attestation')

    tio_layers = table(t(('Mechanism', 'Responsibility'), ('机制', '职责')), [
        ('TDISP / TDI', t('PCI-SIG defines assignment and state for each TEE Device Interface, such as one SR-IOV VF. The endpoint Device Security Manager (DSM) enforces device-side rules.',
                          'PCI-SIG 定义每个 TEE 设备接口的分配与状态，例如一个 SR-IOV VF。设备端 DSM 执行接口侧规则。')),
        ('SPDM / DOE', t('AMD-SP acts as the host TEE Security Manager (TSM). It uses a secure SPDM session with the DSM for identity, measurements and control messages. The VMM can relay the bytes through a PCIe DOE mailbox.',
                          'AMD-SP 承担宿主 TEE Security Manager（TSM）的角色，通过与 DSM 的 SPDM 安全会话处理身份、度量和控制消息。VMM 可通过 PCIe DOE 邮箱转发消息。')),
        ('Selective IDE', t('Protects PCIe transaction traffic between configured endpoints, including confidentiality, integrity and replay protection for the selected stream.',
                            '保护所配置端点之间的 PCIe 事务，为选定的流提供机密性、完整性与抗重放。')),
        ('AMD IOMMU / RMP', t('A Secure Device Table Entry (SDTE) and RMP checks restrict trusted DMA to authorized guest mappings. The guest validates the assigned MMIO ranges before using them.',
                              '安全设备表项（SDTE）与 RMP 检查将可信 DMA 限制在获准的 Guest 映射。Guest 使用设备前验证所分配的 MMIO 范围。')),
    ])
    tio = article(t('TRUSTED I/O', '可信 I/O'), t('Assign a trusted PCIe function with SEV-TIO', '用 SEV-TIO 分配可信 PCIe 功能'),
        t('Ordinary SNP devices use shared buffers for DMA. SEV-TIO extends the trust boundary to an accepted device interface and enables direct DMA to authorized private pages.',
          '普通 SNP 设备通过共享缓冲区做 DMA。SEV-TIO 将信任边界扩展到 Guest 接受的设备接口，允许设备直接 DMA 到获准的私有页。'),
        figure('tio-architecture', ('AMD SEV-TIO system architecture', 'AMD SEV-TIO 系统架构'),
               ('Trace the ASP configuration path and the separate data path through the IOMMU, root complex and IDE link.',
                '沿图追踪 ASP 的配置路径，再看穿过 IOMMU、PCIe 根复合体与 IDE 链路的数据路径。'))
        + tio_layers
        + figure('tio-lifecycle', ('Device and TDI lifecycle', '设备与 TDI 生命周期'),
                 ('The host discovers and binds the interface. The guest checks the device evidence and interface configuration before authorizing its own use. Unbind revokes the trusted mappings.',
                  '宿主发现并绑定接口。Guest 检查设备证据与接口配置后才授权使用。解绑会撤销可信映射。'))
        + '<p>' + t(
            'Read the TDISP CONFIG_UNLOCKED, CONFIG_LOCKED, RUN and ERROR states separately from guest acceptance of the TDI. For example, ABI 0.91 allows <code>TIO_TDI_BIND</code> to put the interface in RUN before the guest accepts it. The guest still validates MMIO with <code>TIO_MSG_MMIO_VALIDATE_REQ</code> and grants private DMA with <code>TIO_MSG_SDTE_WRITE_REQ</code>. AMD lists trusted I/O via TDISP for EPYC 9005 and lists TIO ABI revision 0.92 in its documentation index. Check the specific CPU, platform firmware, device firmware and host/guest driver stack.',
            '阅读 TDISP 的 CONFIG_UNLOCKED、CONFIG_LOCKED、RUN 和 ERROR 状态时，也要跟踪 Guest 何时接受 TDI。例如 ABI 0.91 允许 <code>TIO_TDI_BIND</code> 先将接口置为 RUN，Guest 随后才接受该接口。Guest 仍需用 <code>TIO_MSG_MMIO_VALIDATE_REQ</code> 验证 MMIO，再通过 <code>TIO_MSG_SDTE_WRITE_REQ</code> 授权私有内存 DMA。AMD 将基于 TDISP 的可信 I/O 列在 EPYC 9005 功能中，并在文档索引列出 TIO ABI 0.92。部署需核对具体 CPU、平台与设备固件，以及宿主和 Guest 驱动。'
        ) + '</p>', 'tee-io')

    migration_flow = reading_flow('sev-migration-flow', ('SNP migration with a migration agent', '通过迁移代理迁移 SNP Guest'), [
        (('Source VM and MA', '源 VM 与 MA'), ('Launch policy and AMD-SP bind the MA', '启动策略和 AMD-SP 建立代理绑定')),
        (('Export at source', '源端导出'), ('AMD-SP checks agent authorization and exports context', 'AMD-SP 检查代理授权并导出上下文')),
        (('Protected transfer', '受保护传输'), ('Migration software authenticates endpoints and transfers context and protected pages', '迁移软件认证两端并传输上下文及受保护页面')),
        (('Import and resume', '导入并恢复'), ('Destination AMD-SP imports context and restores pages', '目的端 AMD-SP 导入上下文并恢复页面')),
    ], ('Conceptual firmware flow. The migration agent and VMM implement the transport and orchestration around these operations.',
        '固件流程示意。传输与编排由迁移代理和 VMM 在这些操作之外实现。'), SNP_ABI_PDF, 'AMD SNP firmware ABI §4.11, §7')
    migration = article(t('MIGRATION', '迁移'), t('Follow the migration agent and guest context', '跟踪迁移代理与 Guest 上下文'),
        t('A Migration Agent (MA) can be a separate SNP VM associated with a guest at launch. Guest policy controls whether association is allowed. AMD-SP enforces which guest or MA can request export or import.',
          'Migration Agent（MA）可作为独立 SNP VM，在启动时与待迁移 Guest 关联。Guest 策略控制是否允许关联。AMD-SP 执行导出和导入请求的授权检查。'),
        migration_flow + '<ol>' + ''.join(f'<li>{step}</li>' for step in [
            t('In the host-assisted swap path, the source uses <code>SNP_PAGE_SWAP_OUT</code> for private pages and metadata. The Offline Encryption Key (OEK) protects those page images. <code>MSG_EXPORT_REQ</code> obtains the guest context under the firmware’s export rules.',
              '在宿主协助的换出路径中，源端用 <code>SNP_PAGE_SWAP_OUT</code> 换出私有页和元数据，离线加密密钥（OEK）保护这些页面镜像。<code>MSG_EXPORT_REQ</code> 按固件导出规则取得 Guest 上下文。'),
            t('The migration solution authenticates the peer and transports the exported context over a protected channel. The destination creates a context, imports it with <code>MSG_IMPORT_REQ</code> and restores pages. The ABI also defines a guest-assisted path involving an Incoming Migration Image and an absorb request.',
              '迁移方案认证对端，经受保护通道传输导出的上下文。目的端创建上下文，通过 <code>MSG_IMPORT_REQ</code> 导入并恢复页面。ABI 还定义了由 Guest 协助的路径，使用 Incoming Migration Image 与 absorb 请求。'),
            t('After migration, a relying party can request fresh evidence from the destination and recheck its TCB, identity and agent policy before resuming key delivery. Product support for live migration, vTPM and assigned devices depends on the actual stack and migration policy.',
              '迁移后，依赖方可向目的端请求新证据，重新核对 TCB、身份和代理策略，再恢复密钥下发。热迁移、vTPM 和直通设备能否迁移，取决于实际软件栈和迁移策略。'),
        ]) + '</ol>', 'migration')

    comparison_rows = [
        (t('Platform trust root', '平台信任根'), t('AMD-SP boot ROM, signed firmware and AMD TCB versions', 'AMD-SP Boot ROM、签名固件与 AMD TCB 版本'),
         t('SEAM Loader and measured TDX module in SEAM root', 'SEAM Loader 与 SEAM root 中经度量的 TDX 模块'), 'platform-boot'),
        (t('Private memory and page acceptance', '私有内存与页面接受'), 'ASID / C-bit, NPT + RMP, RMPUPDATE / PVALIDATE',
         'KeyID, Secure EPT + PAMT, TDG.MEM.PAGE.ACCEPT', 'memory'),
        (t('CPU state and guest/host interface', 'CPU 状态及宿主接口'), 'VMSA, #VC, GHCB / VMGEXIT',
         'TDVPS, TDCALL / SEAMCALL, TDG.VP.VMCALL', 'calls'),
        (t('Build measurement', '构建期度量'), 'SNP_LAUNCH_*, MEASUREMENT',
         'TDH.MR.*, MRTD and guest runtime RTMRs', 'td-measurement'),
        (t('Evidence and signing chain', '证据与签名链'), t('AMD-SP signs SNP report with VCEK or VLEK', 'AMD-SP 以 VCEK 或 VLEK 签署 SNP 报告'),
         t('TDREPORT → DCAP TDQE signs Quote; Intel PCK chain certifies the platform', 'TDREPORT → DCAP TDQE 签署 Quote；Intel PCK 证书链认证平台'), 'remote-attestation'),
        (t('Services in the trusted boundary', '可信边界内的服务'), t('SVSM runs inside the VM at VMPL0. A migration agent can be a separate SNP VM.', 'SVSM 位于 VM 内部的 VMPL0。迁移代理可作为独立 SNP VM。'),
         t('Service TD is a separate TD bound to its target, for example MigTD.', 'Service TD 是绑定到目标 TD 的独立 TD，例如 MigTD。'), 'service-td'),
        (t('Trusted device assignment', '可信设备分配'), 'SEV-TIO, AMD-SP as TSM, AMD IOMMU + RMP',
         'TDX Connect, TDX module as TSM, trusted VT-d', 'tdx-connect'),
        (t('Migration', '迁移'), t('SNP MA and firmware context export/import, with platform-specific transport', 'SNP MA 与固件上下文导出/导入，传输由具体平台实现'),
         t('MigTD evaluates policy and exchanges session keys. TDX modules export/import protected state.', 'MigTD 评估策略并交换会话密钥，TDX 模块导出/导入受保护状态。'), 'migration'),
    ]
    comparison = article(t('ARCHITECTURE COMPARISON', '架构对照'), t('AMD SEV-SNP and Intel TDX side by side', 'AMD SEV-SNP 与 Intel TDX 逐项对照'),
        t('Each Intel entry links to the corresponding chapter. The rows pair comparable responsibilities across the two architectures.',
          'Intel 一栏可跳到对应章节。每行对照两套架构中承担相近职责的机制。'),
        table(t(('Responsibility', 'AMD SEV-SNP', 'Intel TDX'), ('职责', 'AMD SEV-SNP', 'Intel TDX')),
              [(role, amd, f'<a class="inline-link" href="tdx{suffix}#{ident}">{intel} ↗</a>')
               for role, amd, intel, ident in comparison_rows]), 'tdx-comparison')

    references = [
        (AMD_SEV, ('AMD SEV documentation', 'AMD SEV 文档入口'), ('Hardware matrix, firmware versions, APM, GHCB and SVSM', '硬件矩阵、固件版本、APM、GHCB 与 SVSM')),
        (SNP_ABI, ('SNP firmware ABI', 'SNP 固件 ABI'), ('Launch, reports, guest messages and migration', '启动、报告、Guest 消息与迁移')),
        (TIO_ABI, ('SEV-TIO firmware ABI rev. 0.91', 'SEV-TIO 固件 ABI 0.91'), ('Versioned public reference for device operations', '可直接阅读的设备操作版本参考')),
        (TDISP, ('PCI-SIG TDISP', 'PCI-SIG TDISP'), ('Common device interface and binding standard', '设备接口与绑定通用规范')),
        ('https://docs.amd.com/v/u/en-US/57230', ('AMD VCEK and KDS', 'AMD VCEK 与 KDS'), ('Chip endorsement chain and certificate retrieval', '芯片背书证书链与证书获取')),
        ('https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/user-guides/58369-010-versioned-loaded-endorsement-key-certificate-definition.pdf',
         ('AMD VLEK certificate', 'AMD VLEK 证书'), ('Loaded endorsement key certificate chain', '加载式背书密钥证书链')),
        (KVM, ('Linux KVM host API', 'Linux KVM 宿主 API'), ('Host-side launch operations and feature enumeration', '宿主启动操作与能力枚举')),
        (GUEST, ('Linux SNP guest API', 'Linux SNP Guest API'), ('Request a report from /dev/sev-guest', '通过 /dev/sev-guest 请求报告')),
        ('https://github.com/virtee/snpguest', ('VirTEE snpguest', 'VirTEE snpguest'), ('Read a report and verify it with endorsement certificates', '读取报告并用背书证书验证')),
    ]
    source_cards = '<div class="source-grid tdx-sources">' + ''.join(
        link(url, t(*title), t(*description)) for url, title, description in references
    ) + '</div>'
    exercise = '<p>' + t(
        'Try two checks on a supported SNP guest. Request a report with a fresh challenge and verify its signature and measurement. Then keep the report fixed and change the expected challenge to see the application binding fail while the report signature remains valid.',
        '在支持 SNP 的 Guest 上做两个检查。用新鲜挑战值请求报告，验证签名和启动度量。随后保持报告不变，只改验证者预期的挑战值，观察报告签名依旧有效，但应用层绑定检查失败。'
    ) + '</p>'
    sources = article(t('SOURCE READING', '资料与练习'), t('Read the specs and inspect a real SNP report', '读规范并检查一份 SNP 报告'),
        t('Start with the AMD architecture and the two Linux interfaces, then follow the certificate and trusted I/O references.',
          '先读 AMD 架构与 Linux 宿主、Guest 两侧接口，再按需查看证书与可信 I/O 规范。'),
        exercise + source_cards, 'sources')
    return hero + nav + architecture + memory + trust + attestation + tio + migration + comparison + sources
