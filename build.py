"""Build the static bilingual TEE / TDX / SGX atlas (stdlib only)."""
from pathlib import Path

ROOT = Path(__file__).parent
PAGES = ('index', 'architecture', 'attestation', 'labs')
NAV = {
    'en': ('Overview', 'Architecture', 'Attestation', 'Labs & sources'),
    'zh': ('总览', '架构与边界', '远程证明', '实验与资料'),
}
TITLES = {
    'en': ('TEE / TDX / SGX Atlas', 'Architecture & threat models', 'Attestation & key release', 'Labs & primary sources'),
    'zh': ('TEE / TDX / SGX 地图', '架构与威胁模型', '远程证明与密钥释放', '实验与一手资料'),
}
DESCRIPTIONS = {
    'en': 'A security-first learning path through Intel SGX, Intel TDX, trust boundaries, remote attestation, and confidential computing.',
    'zh': '从安全视角学习 Intel SGX、Intel TDX、信任边界、远程证明与机密计算。',
}


def link(href, title, desc='', category='PRIMARY SOURCE'):
    return f'<a class="source" href="{href}" target="_blank" rel="noopener noreferrer"><span class="source-type">{category}</span><strong>{title} ↗</strong><small>{desc}</small></a>'


def card(num, title, text, href, action):
    return f'<article class="card"><span class="num">{num}</span><h3>{title}</h3><p>{text}</p><a href="{href}">{action} ↗</a></article>'


def route(num, title, text, href, action):
    return f'<article class="route-item"><span class="step-num">{num}</span><div><h3>{title}</h3><p>{text}</p><a href="{href}">{action} ↗</a></div></article>'


def shell(lang, page, body):
    zh = lang == 'zh'
    idx = PAGES.index(page)
    suffix = '.zh.html' if zh else '.html'
    nav = ''
    for i, (name, label) in enumerate(zip(PAGES, NAV[lang])):
        current = 'aria-current="page" ' if i == idx else ''
        nav += f'<a {current}href="{name}{suffix}">{label}</a>'
    lang_label = '语言选择' if zh else 'Language selection'
    en_current = '' if zh else 'aria-current="page" '
    zh_current = 'aria-current="page" ' if zh else ''
    languages = f'<nav class="langbar" aria-label="{lang_label}"><a data-atlas-lang="en" {en_current}href="{page}.html">EN</a><a data-atlas-lang="zh" {zh_current}href="{page}.zh.html">中文</a></nav>'
    foot = ('面向安全工程师的学习地图。具体平台能力、补丁与证明策略请以厂商和系统文档为准。' if zh else 'A field guide for security engineers. Verify platform capabilities, updates, and attestation policy against vendor and OS documentation.')
    return f'''<!doctype html>
<html lang="{'zh-CN' if zh else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#101b2a"><meta name="description" content="{DESCRIPTIONS[lang]}"><title>{TITLES[lang][idx]} · ShundaZhang</title><link rel="stylesheet" href="style.css"><script src="language.js"></script><script defer src="app.js"></script></head>
<body>{languages}<a class="skip" href="#main">{'跳至正文' if zh else 'Skip to content'}</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="index{suffix}"><span class="brand-mark">T//</span><span class="brand-name">TEE / TDX / SGX ATLAS</span></a><nav class="nav" aria-label="{'主导航' if zh else 'Main navigation'}">{nav}</nav></div></header>
<main id="main">{body}</main><footer class="footer"><div class="wrap footer-inner"><div><strong>TEE / TDX / SGX ATLAS</strong><p>{foot}</p></div><div><a href="https://shundazhang.github.io/">{'个人主页' if zh else 'Home'}</a><a href="https://github.com/ShundaZhang/tee-tdx-sgx">GitHub ↗</a></div></div></footer></body></html>'''


def section(label, title, intro, content, tone='', section_id=''):
    ident = f' id="{section_id}"' if section_id else ''
    return f'<section class="section {tone}"{ident}><div class="wrap"><div class="section-head"><div><span class="kicker">{label}</span><h2>{title}</h2></div><p>{intro}</p></div>{content}</div></section>'


def index_en():
    hero = '''<section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">CONFIDENTIAL COMPUTING / SECURITY FIELD GUIDE</span><h1>Know the boundary<br><em>before trusting the box</em></h1><p>SGX protects an enclave inside a process. TDX protects a virtual machine from its host. Both need attestation, deliberate key release, and a threat model that includes untrusted I/O and side channels.</p><div class="buttons"><a class="button primary" href="#route">Follow the learning path ↗</a><a class="button ghost" href="attestation.html">Try the policy lab ↗</a></div><div class="hero-note">START WITH WHAT IS PROTECTED · THEN ASK WHAT REMAINS EXPOSED</div></div><div class="boundary-visual" role="img" aria-label="Untrusted host contains an SGX enclave and a TDX trust domain, each with a separate protected boundary and remote verifier"><div class="visual-head"><span>TRUST BOUNDARIES / 01</span><span>HOST ≠ TEE</span></div><div class="host-box"><span>UNTRUSTED HOST / OS / VMM</span><div class="protected-row"><div class="protect-box"><small>PROCESS-LEVEL</small><b>SGX</b><p>Enclave code + data<br>inside an application</p></div><div class="protect-box"><small>VM-LEVEL</small><b>TDX</b><p>Private memory + state<br>of a guest VM</p></div></div></div><div class="visual-connector"></div><div class="verifier-box"><span>EVIDENCE → VERIFIER → POLICY</span><strong>KEY?</strong></div></div></div></section>'''
    cards = '<div class="card-grid">' + ''.join([
        card('01 / ISOLATION', 'SGX is an enclave', 'A process selects a small region of code and data. The kernel helps create it but cannot directly read enclave memory. The host app and enclave runtime remain security-relevant.', 'architecture.html#sgx', 'Trace the process boundary'),
        card('02 / ISOLATION', 'TDX is a trust domain', 'A VM runs with private memory and CPU state protected from the host VMM. Guest OS and applications live inside the trust boundary, along with a larger trusted software stack.', 'architecture.html#tdx', 'Trace the VM boundary'),
        card('03 / DECISION', 'Attestation is a policy input', 'A signed quote is evidence about a measured environment, not a blanket verdict. A verifier checks authenticity and state; a relying party decides whether to release a secret.', 'attestation.html', 'Follow the evidence')
    ]) + '</div>'
    comparison = '''<div class="comparison"><table><thead><tr><th>Question</th><th>Intel SGX</th><th>Intel TDX</th></tr></thead><tbody><tr><td>Protected unit</td><td>Enclave inside a user process</td><td>Trust Domain (confidential VM)</td></tr><tr><td>Untrusted manager</td><td>Host application and OS</td><td>Host VMM / hypervisor</td></tr><tr><td>Work inside boundary</td><td>Selected code, data, enclave runtime</td><td>Guest firmware, OS, services, workload</td></tr><tr><td>Evidence to inspect</td><td>Enclave identity and signer attributes in SGX evidence</td><td>TD and runtime measurements plus TDX platform state</td></tr><tr><td>Typical blind spot</td><td>Host-controlled calls and data, page/access patterns</td><td>Shared pages, emulated devices, guest software and host-controlled timing</td></tr></tbody></table></div><p class="source-note">Protection details vary by processor generation and configuration. Do not infer side-channel immunity or availability from an “encrypted memory” label.</p>'''
    paths = '<div class="route">' + ''.join([
        route('01', 'Start with the attacker', 'Write down who controls the host, physical machine, network, guest, and verifier.', 'architecture.html#model', 'Build a threat model'),
        route('02', 'Map SGX vs TDX', 'Compare enclave entry, VM entry/exit, private memory, shared data, and the trusted computing base.', 'architecture.html', 'Read the architecture'),
        route('03', 'Learn the RATS vocabulary', 'Separate attester, evidence, verifier, reference values, result, and relying party.', 'attestation.html#roles', 'Follow the roles'),
        route('04', 'Check the quote and policy', 'Inspect measurement, TCB status, freshness and key/session binding before secret release.', 'attestation.html#policy', 'Run the policy lab'),
        route('05', 'Trace real attack surfaces', 'Host I/O, shared pages, malicious inputs, paging and microarchitectural leakage remain relevant.', 'architecture.html#surfaces', 'Review the boundaries'),
        route('06', 'Move to a real stack', 'Check Linux, Intel DCAP, KVM TDX and Trustee. Hardware-free exercises come first.', 'labs.html', 'Open the lab guide')
    ]) + '</div>'
    bridges = '<div class="card-grid">' + ''.join([
        card('ISA → TEE', 'RISC-V & CoVE', 'Compare Intel VM isolation with RISC-V confidential computing and the privilege model.', 'https://shundazhang.github.io/riscv-security-atlas/', 'Open RISC-V atlas'),
        card('LEAKAGE', 'CPU side channels', 'A TEE changes who may read memory directly; it does not make cache or timing leakage disappear.', 'https://shundazhang.github.io/side-channel-atlas/index.html', 'Open side-channel atlas'),
        card('LONG-TERM', 'PQC & attestation', 'Attestation chains, certificates, signatures and archived evidence also need crypto-agility planning.', 'https://shundazhang.github.io/quantum-pqc-atlas/', 'Open PQC atlas')
    ]) + '</div>'
    return hero + section('01 / ORIENTATION', 'One label, two very different perimeters', 'Use the protected unit—not the marketing term “TEE”—to choose the right mental model.', cards, 'white') + section('02 / SIDE BY SIDE', 'SGX and TDX at a glance', 'The question is not which one is “more secure”; it is which boundary matches the workload and attacker.', comparison) + section('03 / LEARNING PATH', 'Six steps from CPU isolation to secret release', 'For engineers who already know x86, virtualization and systems security, start at the boundary rather than at introductory CPU material.', paths, 'tinted', 'route') + section('04 / NEXT CONNECTIONS', 'Carry the model into adjacent topics', 'Use the same threat-model questions across architecture, leakage and cryptography.', bridges, 'white')


def index_zh():
    hero = '''<section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">CONFIDENTIAL COMPUTING / SECURITY FIELD GUIDE</span><h1>先看清边界<br><em>再决定信任什么</em></h1><p>SGX 保护进程中的 enclave，TDX 保护虚拟机免受宿主机直接窥探。两者都需要远程证明、审慎的密钥释放策略，以及把不可信 I/O 和侧信道纳入考虑的威胁模型。</p><div class="buttons"><a class="button primary" href="#route">开始学习路径 ↗</a><a class="button ghost" href="attestation.zh.html">体验策略实验 ↗</a></div><div class="hero-note">先问保护了什么，再问还有什么暴露在外</div></div><div class="boundary-visual" role="img" aria-label="不可信宿主机中有 SGX enclave 与 TDX 信任域，它们拥有不同保护边界，并由远端验证者评估"><div class="visual-head"><span>TRUST BOUNDARIES / 01</span><span>HOST ≠ TEE</span></div><div class="host-box"><span>不可信宿主机 / OS / VMM</span><div class="protected-row"><div class="protect-box"><small>进程级</small><b>SGX</b><p>应用中的 enclave<br>代码与数据</p></div><div class="protect-box"><small>虚拟机级</small><b>TDX</b><p>Guest VM 的私有内存<br>与 CPU 状态</p></div></div></div><div class="visual-connector"></div><div class="verifier-box"><span>证据 → 验证者 → 策略</span><strong>密钥？</strong></div></div></div></section>'''
    cards = '<div class="card-grid">' + ''.join([
        card('01 / 隔离', 'SGX 是 enclave', '进程选出一小部分代码和数据。内核协助创建 enclave，但不能直接读取其中内存。宿主应用和 enclave 运行时仍与安全相关。', 'architecture.zh.html#sgx', '追踪进程边界'),
        card('02 / 隔离', 'TDX 是信任域', '虚拟机的私有内存和 CPU 状态受到保护，不让宿主 VMM 直接读取。Guest OS 和应用位于边界内，也扩大了可信软件栈。', 'architecture.zh.html#tdx', '追踪 VM 边界'),
        card('03 / 决策', '证明是策略输入', '签名 quote 是关于测量环境的证据，不是“安全”判决。验证者检查真实性与状态，依赖方决定是否释放秘密。', 'attestation.zh.html', '跟随证据链')
    ]) + '</div>'
    comparison = '''<div class="comparison"><table><thead><tr><th>问题</th><th>Intel SGX</th><th>Intel TDX</th></tr></thead><tbody><tr><td>保护对象</td><td>用户进程中的 enclave</td><td>Trust Domain（机密虚拟机）</td></tr><tr><td>不可信管理者</td><td>宿主应用与 OS</td><td>宿主 VMM / Hypervisor</td></tr><tr><td>边界内的软件</td><td>选定代码、数据和 enclave 运行时</td><td>Guest 固件、OS、服务与工作负载</td></tr><tr><td>证明重点</td><td>SGX 证据中的 enclave 身份与签名者属性</td><td>TD 与运行时测量值及 TDX 平台状态</td></tr><tr><td>常见盲点</td><td>宿主控制的调用和输入、页面访问模式</td><td>共享页、模拟设备、Guest 软件与宿主控制的时序</td></tr></tbody></table></div><p class="source-note">具体保护属性随处理器代际和配置变化。不要从“内存已加密”直接推断具备抗侧信道能力或高可用性。</p>'''
    paths = '<div class="route">' + ''.join([
        route('01', '先定义攻击者', '写清宿主、物理机器、网络、Guest 与验证服务分别由谁控制。', 'architecture.zh.html#model', '建立威胁模型'),
        route('02', '画出 SGX 与 TDX 边界', '比较 enclave 进入、VM 进入与退出、私有内存、共享数据和可信计算基。', 'architecture.zh.html', '阅读架构'),
        route('03', '掌握 RATS 术语', '分清证明方、证据、验证者、参考值、证明结果与依赖方。', 'attestation.zh.html#roles', '跟随角色关系'),
        route('04', '验证 quote 与策略', '在释放秘密前检查测量值、TCB 状态、新鲜度、密钥与会话绑定。', 'attestation.zh.html#policy', '运行策略实验'),
        route('05', '追踪真实攻击面', '宿主 I/O、共享页、恶意输入、分页和微架构泄漏仍需审查。', 'architecture.zh.html#surfaces', '审查边界'),
        route('06', '走向真实技术栈', '核对 Linux、Intel DCAP、KVM TDX 和 Trustee；先做无需专用硬件的实验。', 'labs.zh.html', '打开实验指南')
    ]) + '</div>'
    bridges = '<div class="card-grid">' + ''.join([
        card('ISA → TEE', 'RISC-V 与 CoVE', '对照 Intel 的 VM 隔离与 RISC-V 机密计算和特权模型。', 'https://shundazhang.github.io/riscv-security-atlas/', '打开 RISC-V 专题'),
        card('泄漏', 'CPU 侧信道', 'TEE 改变谁能直接读取内存，但不会让缓存和时序泄漏消失。', 'https://shundazhang.github.io/side-channel-atlas/index.html', '打开侧信道专题'),
        card('长期安全', 'PQC 与远程证明', '证明链、证书、签名与长期保存的证据也要纳入密码敏捷性规划。', 'https://shundazhang.github.io/quantum-pqc-atlas/', '打开 PQC 专题')
    ]) + '</div>'
    return hero + section('01 / 定位', '同叫 TEE，边界并不相同', '先看被保护的对象，再决定如何理解和使用这项技术。', cards, 'white') + section('02 / 对照', 'SGX 与 TDX 速览', '关键不是哪个“更安全”，而是哪个边界符合工作负载和攻击者模型。', comparison) + section('03 / 学习路径', '从隔离到释放秘密的六步', '已有 x86、虚拟化或系统安全基础，可以直接从边界入手。', paths, 'tinted', 'route') + section('04 / 延伸', '把模型带入相邻专题', '架构、泄漏和密码学可以使用同一组威胁模型问题。', bridges, 'white')


def page_hero(lang, crumb, title, intro):
    home = '主页' if lang == 'zh' else 'OVERVIEW'
    suffix = '.zh.html' if lang == 'zh' else '.html'
    return f'<section class="page-hero"><div class="wrap"><div class="crumb"><a href="index{suffix}">{home}</a> / {crumb}</div><h1>{title}</h1><p>{intro}</p></div></section>'


def article_section(label, title, lead, content, section_id=''):
    ident = f' id="{section_id}"' if section_id else ''
    return f'<section class="article-section"{ident}><div class="wrap"><span class="kicker">{label}</span><h2>{title}</h2><p>{lead}</p>{content}</div></section>'


def detail(label, title, text):
    return f'<article class="detail-card"><span class="badge">{label}</span><h3>{title}</h3><p>{text}</p></article>'


def architecture_en():
    intro = page_hero('en', 'ARCHITECTURE', 'Draw the trust boundary<br><em>before drawing conclusions</em>', 'A TEE does not replace a system threat model. Compare what the CPU enforces, what software remains trusted, and what an adversarial host can still influence.')
    model = '<div class="detail-grid">' + ''.join([
        detail('ASSET', 'What is the secret?', 'Name the data, code, keys or computation being protected. Ask whether the secret ever enters shared memory, a log, a device buffer or an untrusted return value.'),
        detail('ACTOR', 'Who is the attacker?', 'Distinguish a hostile application, kernel, hypervisor, neighboring workload, physical operator, and network peer. SGX and TDX place different actors outside the boundary.'),
        detail('CONTROL', 'What can they schedule or supply?', 'The host may manage resources, interrupt or delay execution, and provide I/O. Such control creates availability and leakage concerns even when private memory is isolated.'),
        detail('DECISION', 'What would evidence prove?', 'A measurement identifies a particular initial or runtime state, subject to evidence format and policy. It cannot prove arbitrary application correctness or future behavior.')
    ]) + '</div>'
    sgx = '<div class="split"><div class="panel"><h3>Inside the enclave</h3><ul><li>Selected code and data live in enclave pages; CPU-enforced access control blocks direct reads from other software.</li><li>Enclave identity and signer attributes can be reflected in attestation evidence.</li><li>Smaller protected code can reduce the software TCB, but an enclave runtime and its interfaces still need review.</li></ul></div><div class="panel"><h3>Outside the enclave</h3><ul><li>Host process and OS perform ordinary I/O, scheduling and resource management.</li><li>ECALL/OCALL-style transitions and untrusted inputs require validation and careful serialization.</li><li>Access patterns, interrupts, page behavior and microarchitectural leakage remain part of the security analysis.</li></ul></div></div><p class="source-note">Start with the <a class="inline-link" href="https://docs.kernel.org/arch/x86/sgx.html">Linux SGX architecture guide</a>; consult the actual platform generation and SGX SDK/DCAP versions before claiming a specific memory-integrity property.</p>'
    tdx = '<div class="split"><div class="panel"><h3>Inside the TD</h3><ul><li>The guest VM runs with private memory and CPU state isolated from the host VMM by TDX hardware and module mechanisms.</li><li>Guest firmware, OS, drivers and workload are inside the owner’s trust decision; attest and patch the stack you actually run.</li><li>TD and runtime measurements can contribute to a policy decision before secrets enter the guest.</li></ul></div><div class="panel"><h3>Outside the TD</h3><ul><li>The VMM still controls resource allocation and may deny service; TDX does not promise availability against it.</li><li>Shared pages, virtual devices, MMIO, hypercalls and host-provided CPUID/MSR data are explicit trust crossings.</li><li>Guest software must treat such inputs as hostile; the encryption boundary does not sanitize them.</li></ul></div></div><p class="source-note">The <a class="inline-link" href="https://docs.kernel.org/security/snp-tdx-threat-model.html">Linux CoCo threat model</a> and <a class="inline-link" href="https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/best-practices/trusted-domain-security-guidance-for-developers.html">Intel TD developer guidance</a> give concrete host interfaces to review.</p>'
    surfaces = '<div class="comparison"><table><thead><tr><th>Surface</th><th>Question for the reviewer</th><th>What the TEE does not settle</th></tr></thead><tbody><tr><td>Shared memory &amp; I/O</td><td>Who writes the buffer and who checks its length, origin and lifetime?</td><td>Host-provided bytes remain untrusted, even if copied into private memory.</td></tr><tr><td>Measurement &amp; boot</td><td>Which firmware, kernel, configuration and workload does the measurement cover?</td><td>A valid quote may identify the wrong image for your policy.</td></tr><tr><td>Side channels</td><td>Can timing, cache activity, interrupts or access patterns reveal secrets?</td><td>Direct memory isolation does not imply constant-time execution.</td></tr><tr><td>Availability</td><td>Can an untrusted manager pause, reset, starve or terminate the workload?</td><td>Confidentiality and integrity do not guarantee progress.</td></tr><tr><td>Updates &amp; rollback</td><td>Which TCB levels are acceptable, and who maintains reference values?</td><td>Signed but outdated evidence may not meet your current policy.</td></tr></tbody></table></div>'
    closing = '<div class="signal"><strong>A useful security claim has boundaries</strong>“This workload, in this measured guest or enclave, on a platform meeting this TCB policy, received this secret through a channel bound to this attestation result.” Then state what remains outside that claim.</div>'
    return intro + article_section('01 / THREAT MODEL', 'Begin with five concrete questions', 'These questions keep the protected asset, attacker and trusted computing base visible.', model, 'model') + article_section('02 / SGX', 'A protected region inside a process', 'SGX is a process-level enclave mechanism. It changes memory access rules, but applications still need secure interfaces and runtime code.', sgx, 'sgx') + article_section('03 / TDX', 'A protected guest inside a host', 'TDX is a VM-level confidential-computing mechanism. The host VMM remains a manager, but is excluded from direct access to TD private state.', tdx, 'tdx') + article_section('04 / ATTACK SURFACES', 'Review every crossing, not just DRAM', 'An attacker can still influence data and timing at boundaries exposed by the workload.', surfaces, 'surfaces') + article_section('05 / CLAIM', 'Write the assurance statement precisely', 'A TEE is useful when its security claim can be tested against evidence and policy.', closing)


def architecture_zh():
    intro = page_hero('zh', '架构与边界', '先画信任边界<br><em>再讨论安全结论</em>', 'TEE 不能替代系统威胁模型。需要分清 CPU 强制保护了什么、哪些软件仍须信任、恶意宿主仍能影响什么。')
    model = '<div class="detail-grid">' + ''.join([
        detail('资产', '要保护的秘密是什么？', '明确数据、代码、密钥或计算。追踪秘密是否进入共享内存、日志、设备缓冲区或不可信返回值。'),
        detail('攻击者', '谁掌握哪一级权限？', '区分恶意应用、内核、Hypervisor、相邻工作负载、物理操作者与网络对端。SGX 和 TDX 将不同角色排除在边界外。'),
        detail('控制权', '攻击者能安排或提供什么？', '宿主可能管理资源、打断或延迟执行并提供 I/O。即使私有内存被隔离，这些控制仍影响可用性和泄漏面。'),
        detail('判断', '证据究竟能证明什么？', '测量值可标识某个初始或运行状态，但含义取决于证据格式和策略。它不能证明任意应用都正确，也不能保证未来行为。')
    ]) + '</div>'
    sgx = '<div class="split"><div class="panel"><h3>Enclave 内部</h3><ul><li>选定代码和数据位于 enclave 页面；CPU 强制访问控制阻止其他软件直接读取。</li><li>enclave 身份与签名者属性可体现在远程证明证据中。</li><li>较小的受保护代码有利于缩小软件 TCB，但运行时和接口仍需审查。</li></ul></div><div class="panel"><h3>Enclave 外部</h3><ul><li>宿主进程和 OS 负责普通 I/O、调度与资源管理。</li><li>ECALL/OCALL 等边界跨越及不可信输入需要验证与安全序列化。</li><li>访问模式、中断、页面行为与微架构泄漏仍属于安全分析范围。</li></ul></div></div><p class="source-note">先读 <a class="inline-link" href="https://docs.kernel.org/arch/x86/sgx.html">Linux SGX 架构说明</a>；涉及内存完整性时，需按具体处理器代际与 SDK/DCAP 版本核对，不能笼统断言。</p>'
    tdx = '<div class="split"><div class="panel"><h3>TD 内部</h3><ul><li>Guest VM 的私有内存和 CPU 状态由 TDX 硬件与模块机制隔离，宿主 VMM 不能直接读取。</li><li>Guest 固件、OS、驱动和工作负载属于所有者的信任决策，必须证明和更新实际运行的软件栈。</li><li>TD 与运行时测量值可在秘密进入 Guest 前参与策略判断。</li></ul></div><div class="panel"><h3>TD 外部</h3><ul><li>VMM 仍负责资源分配，并可能拒绝服务；TDX 不承诺对恶意宿主提供可用性。</li><li>共享页、虚拟设备、MMIO、Hypercall 与宿主提供的 CPUID/MSR 数据都是明确的信任跨越。</li><li>Guest 软件必须把这些输入视为不可信；内存加密边界不会自动清理它们。</li></ul></div></div><p class="source-note"><a class="inline-link" href="https://docs.kernel.org/security/snp-tdx-threat-model.html">Linux CoCo 威胁模型</a>和<a class="inline-link" href="https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/best-practices/trusted-domain-security-guidance-for-developers.html">Intel TD 开发者安全指南</a>列出了值得审查的宿主接口。</p>'
    surfaces = '<div class="comparison"><table><thead><tr><th>攻击面</th><th>审查问题</th><th>TEE 未自动解决的事</th></tr></thead><tbody><tr><td>共享内存与 I/O</td><td>谁写入缓冲区？谁检查长度、来源和生命周期？</td><td>宿主提供的字节即使被复制进私有内存，仍是不可信输入。</td></tr><tr><td>测量与启动</td><td>测量值覆盖哪些固件、内核、配置与工作负载？</td><td>有效 quote 仍可能代表不符合自身策略的镜像。</td></tr><tr><td>侧信道</td><td>时序、缓存、中断或访问模式能否透露秘密？</td><td>直接内存隔离不等于常数时间执行。</td></tr><tr><td>可用性</td><td>不可信管理者能否暂停、重置、饿死或终止工作负载？</td><td>机密性和完整性不保证进展。</td></tr><tr><td>更新与回滚</td><td>接受哪些 TCB 级别？参考值由谁维护？</td><td>有签名但过时的证据未必符合当前策略。</td></tr></tbody></table></div>'
    closing = '<div class="signal"><strong>有用的安全声明必须带边界</strong>“这个工作负载位于这台满足 TCB 策略的平台上、这个经过测量的 Guest 或 enclave 中，并通过与证明结果绑定的通道收到了秘密。”随后说明这一声明没有覆盖什么。</div>'
    return intro + article_section('01 / 威胁模型', '先回答五个具体问题', '让受保护资产、攻击者与可信计算基始终可见。', model, 'model') + article_section('02 / SGX', '进程中的受保护区域', 'SGX 是进程级 enclave 机制。它改变了内存访问规则，但应用仍需要安全的接口和运行时代码。', sgx, 'sgx') + article_section('03 / TDX', '宿主机中的受保护 Guest', 'TDX 是虚拟机级机密计算机制。宿主 VMM 继续管理资源，但不能直接访问 TD 私有状态。', tdx, 'tdx') + article_section('04 / 攻击面', '审查每一次边界跨越', '攻击者仍可能通过工作负载暴露的边界影响数据和时序。', surfaces, 'surfaces') + article_section('05 / 安全声明', '把保证写得足够精确', 'TEE 只有在安全声明可对照证据与策略检验时才真正有用。', closing)


def attestation_en():
    intro = page_hero('en', 'ATTESTATION', 'A quote is evidence<br><em>not authorization</em>', 'Remote attestation tells a verifier something about a measured environment. Only an application policy can decide whether that is enough to release a key, admit a workload, or trust a result.')
    roles = '<div class="flow">' + ''.join([
        '<div class="flow-item"><span class="num">01 / ATTESTER</span><h3>Produce evidence</h3><p>The enclave or TD requests a hardware-backed report and quote.</p></div>',
        '<div class="flow-item"><span class="num">02 / ENDORSER</span><h3>Supply collateral</h3><p>Manufacturer material helps establish a quote verification chain and platform status.</p></div>',
        '<div class="flow-item"><span class="num">03 / VERIFIER</span><h3>Appraise evidence</h3><p>Check signatures, TCB, measurement and freshness against reference values.</p></div>',
        '<div class="flow-item"><span class="num">04 / RESULT</span><h3>Return claims</h3><p>A verifier issues an attestation result with scoped claims and validity.</p></div>',
        '<div class="flow-item"><span class="num">05 / RELYING PARTY</span><h3>Apply policy</h3><p>The key service decides whether and how to release a secret.</p></div>'
    ]) + '</div><p class="source-note">These role names follow <a class="inline-link" href="https://www.rfc-editor.org/rfc/rfc9334.html">RFC 9334 (RATS)</a>. Implementations may combine roles or use different wire protocols.</p>'
    tracks = '<div class="comparison"><table><thead><tr><th>Step</th><th>SGX / DCAP</th><th>TDX / DCAP</th></tr></thead><tbody><tr><td>Local statement</td><td>The enclave creates a report carrying identity and application-chosen report data.</td><td>The TD obtains a TDREPORT carrying TD measurements and report data.</td></tr><tr><td>Remote evidence</td><td>Quoting infrastructure produces an SGX quote for remote verification.</td><td>Quoting infrastructure produces a TDX quote from the TD report.</td></tr><tr><td>What policy sees</td><td>Enclave identity/signer, attributes and platform TCB status.</td><td>TD measurements, runtime measurements, attributes and platform TCB status.</td></tr><tr><td>Owner decision</td><td>Allow only the enclave identity and state expected by the application.</td><td>Allow only the guest image, runtime state and TCB expected by the application.</td></tr></tbody></table></div><p class="source-note">This is a conceptual route, not a byte-level quote parser. Check the current <a class="inline-link" href="https://www.intel.com/content/www/us/en/developer/tools/trust-domain-extensions/documentation.html">Intel TDX documentation</a> and <a class="inline-link" href="https://github.com/intel/confidential-computing.sgx">Intel SGX/DCAP repository</a> for concrete formats and APIs.</p>'
    rules = '<ul class="checklist"><li><b>01</b> Verify the quote signature and certificate/collateral chain against the intended trust anchors.</li><li><b>02</b> Compare measurements, attributes, debug mode and workload configuration to owner-controlled reference values.</li><li><b>03</b> Check platform TCB status, revocation and patch policy; “signed” is not synonymous with “currently acceptable.”</li><li><b>04</b> Require freshness appropriate to the protocol, for example a verifier challenge or bounded evidence lifetime.</li><li><b>05</b> Bind evidence to an authenticated session or ephemeral public key before sending a secret; otherwise the recipient can be substituted.</li><li><b>06</b> Limit the released secret by workload, time, purpose and rotation policy, and log the decision.</li></ul>'
    lab = '''<div class="policy-lab" data-policy-lab><h3>Practice: would you release the test secret?</h3><p>Choose a hypothetical evidence bundle. This browser-only illustration checks five policy gates; it does not generate or validate a hardware quote and never handles a real secret.</p><div class="scenario-buttons" role="group" aria-label="Sample evidence scenarios"><button type="button" data-scenario="healthy">Expected state</button><button type="button" data-scenario="stale">Stale challenge</button><button type="button" data-scenario="changed">Changed image</button><button type="button" data-scenario="unbound">Unbound key</button><button type="button" data-scenario="outdated">Outdated TCB</button></div><div class="lab-grid"><ul class="checks" data-checks aria-label="Policy checks"></ul><div class="verdict" role="status" aria-live="polite"><strong data-verdict></strong><p data-verdict-detail></p></div></div></div>'''
    pitfall = '<div class="detail-grid">' + ''.join([
        detail('REPLAY', 'Old quote, new request', 'A once-valid quote may be replayed if the relying party does not enforce freshness and bind the evidence to this request.'),
        detail('CONFUSION', 'Right platform, wrong code', 'A valid platform chain does not mean the enclave, guest image or workload matches the owner’s approved reference values.'),
        detail('SUBSTITUTION', 'Good quote, wrong recipient', 'If a session key is not bound to the attested environment, an attacker can relay evidence and receive the secret elsewhere.'),
        detail('STATUS', 'Signature valid, TCB stale', 'Authentic evidence may describe a platform that fails the owner’s update or revocation policy.')
    ]) + '</div>'
    return intro + article_section('01 / RATS ROLES', 'Five roles, one decision chain', 'Keep evidence appraisal separate from authorization. This makes trust assumptions visible.', roles, 'roles') + article_section('02 / PLATFORM TRACKS', 'How SGX and TDX evidence differ', 'Both use a report-to-quote pattern, but the measured subject and policy fields differ.', tracks) + article_section('03 / POLICY', 'Six gates before secret release', 'The exact format is platform-specific. These questions apply to most attestation-driven key-release systems.', rules, 'policy') + article_section('04 / INTERACTIVE LAB', 'Try the policy decisions', 'Change one claim at a time to see why a single failure should stop release.', lab) + article_section('05 / FAILURE MODES', 'Four mistakes worth memorizing', 'A verified signature alone cannot settle any of these.', pitfall)


def attestation_zh():
    intro = page_hero('zh', '远程证明', 'Quote 是证据<br><em>不是授权决定</em>', '远程证明让验证者了解被测量环境。只有应用策略才能决定这些信息是否足以释放密钥、接纳工作负载或信任结果。')
    roles = '<div class="flow">' + ''.join([
        '<div class="flow-item"><span class="num">01 / 证明方</span><h3>产生证据</h3><p>Enclave 或 TD 请求硬件支持的 report 与 quote。</p></div>',
        '<div class="flow-item"><span class="num">02 / 背书方</span><h3>提供证明材料</h3><p>厂商材料帮助建立 quote 验证链并判断平台状态。</p></div>',
        '<div class="flow-item"><span class="num">03 / 验证者</span><h3>评估证据</h3><p>对照参考值验证签名、TCB、测量值与新鲜度。</p></div>',
        '<div class="flow-item"><span class="num">04 / 结果</span><h3>返回声明</h3><p>验证者签发有范围和有效期的证明结果。</p></div>',
        '<div class="flow-item"><span class="num">05 / 依赖方</span><h3>应用策略</h3><p>密钥服务决定是否及如何释放秘密。</p></div>'
    ]) + '</div><p class="source-note">这些角色名称来自 <a class="inline-link" href="https://www.rfc-editor.org/rfc/rfc9334.html">RFC 9334（RATS）</a>。具体实现可以合并角色或使用不同协议。</p>'
    tracks = '<div class="comparison"><table><thead><tr><th>步骤</th><th>SGX / DCAP</th><th>TDX / DCAP</th></tr></thead><tbody><tr><td>本地声明</td><td>Enclave 生成含身份和应用自选 report data 的 report。</td><td>TD 获得包含 TD 测量值和 report data 的 TDREPORT。</td></tr><tr><td>远程证据</td><td>引用基础设施生成可供远程验证的 SGX quote。</td><td>引用基础设施根据 TD report 生成 TDX quote。</td></tr><tr><td>策略查看</td><td>Enclave 身份/签名者、属性和平台 TCB 状态。</td><td>TD 测量值、运行时测量值、属性和平台 TCB 状态。</td></tr><tr><td>所有者决策</td><td>仅接受应用预期的 enclave 身份与状态。</td><td>仅接受应用预期的 Guest 镜像、运行状态与 TCB。</td></tr></tbody></table></div><p class="source-note">此处是概念流程，不是逐字节 quote 解析器。具体格式和 API 请核对最新 <a class="inline-link" href="https://www.intel.com/content/www/us/en/developer/tools/trust-domain-extensions/documentation.html">Intel TDX 文档</a>及 <a class="inline-link" href="https://github.com/intel/confidential-computing.sgx">Intel SGX/DCAP 仓库</a>。</p>'
    rules = '<ul class="checklist"><li><b>01</b> 对照预期信任锚验证 quote 签名、证书与证明材料链。</li><li><b>02</b> 把测量值、属性、调试模式和工作负载配置与所有者维护的参考值比较。</li><li><b>03</b> 检查平台 TCB 状态、撤销和补丁策略；“有签名”不等于“当前可接受”。</li><li><b>04</b> 按协议要求新鲜度，例如验证者挑战值或证据有效期限制。</li><li><b>05</b> 发送秘密前把证据绑定到认证会话或临时公钥，否则收件者可能被替换。</li><li><b>06</b> 按工作负载、时间和用途限制秘密，并记录决策与轮换策略。</li></ul>'
    lab = '''<div class="policy-lab" data-policy-lab><h3>练习：你会释放测试秘密吗？</h3><p>选择一份假设的证据包。这个纯浏览器示意检查五道策略门槛；它不会生成或验证真实硬件 quote，也不处理真实秘密。</p><div class="scenario-buttons" role="group" aria-label="示例证据场景"><button type="button" data-scenario="healthy">预期状态</button><button type="button" data-scenario="stale">过期挑战</button><button type="button" data-scenario="changed">镜像变化</button><button type="button" data-scenario="unbound">密钥未绑定</button><button type="button" data-scenario="outdated">TCB 过旧</button></div><div class="lab-grid"><ul class="checks" data-checks aria-label="策略检查"></ul><div class="verdict" role="status" aria-live="polite"><strong data-verdict></strong><p data-verdict-detail></p></div></div></div>'''
    pitfall = '<div class="detail-grid">' + ''.join([
        detail('重放', '旧 quote，新请求', '如果依赖方不检查新鲜度、不把证据绑定到当前请求，过去有效的 quote 可以被重放。'),
        detail('混淆', '平台正确，代码错误', '有效的平台证明链不代表 enclave、Guest 镜像或工作负载符合所有者的参考值。'),
        detail('替换', 'Quote 正确，收件者错误', '如果会话密钥未绑定到被证明环境，攻击者可能转发证据，在其他地方收到秘密。'),
        detail('状态', '签名有效，TCB 过时', '真实证据也可能描述未通过所有者更新或撤销策略的平台。')
    ]) + '</div>'
    return intro + article_section('01 / RATS 角色', '五种角色，一条决策链', '把证据评估和授权分开，才能看见真正的信任假设。', roles, 'roles') + article_section('02 / 平台证据', 'SGX 与 TDX 的证据差异', '两者都可走 report 到 quote 的路径，但测量对象与策略字段不同。', tracks) + article_section('03 / 策略', '释放秘密前的六道门槛', '具体格式依赖平台，但这些问题适用于多数由远程证明驱动的密钥释放系统。', rules, 'policy') + article_section('04 / 交互实验', '试做策略决策', '每次改变一项声明，观察为什么一项失败就应停止释放。', lab) + article_section('05 / 失败模式', '值得记住的四种错误', '仅验证签名不能解决其中任何一项。', pitfall)


def labs_en():
    intro = page_hero('en', 'LABS & SOURCES', 'Practice the decisions<br><em>before renting hardware</em>', 'Begin with a threat model and attestation-policy exercise. Then inspect hardware support, follow a current vendor sample, and finally connect attestation to secret delivery.')
    nohw = '<div class="route">' + ''.join([
        route('01', 'Draw the perimeter', 'Take a secret-processing service. Mark what an SGX enclave would contain and what a TDX guest would contain. List all host-facing interfaces.', 'architecture.html#model', 'Open boundary guide'),
        route('02', 'Write an acceptance policy', 'Specify allowed measurement, signer or guest image, debug state, TCB level, freshness window and key binding.', 'attestation.html#policy', 'Open policy guide'),
        route('03', 'Flip one claim', 'Use the on-page simulator to reject an outdated TCB, changed image, stale challenge or unbound key. Explain which party makes the decision.', 'attestation.html#policy', 'Run interactive lab'),
        route('04', 'Audit the blind spots', 'List shared memory, device input, denial of service, side channels and software bugs excluded from the claim.', 'architecture.html#surfaces', 'Review attack surfaces')
    ]) + '</div><div class="signal" style="margin-top:20px"><strong>What you can claim after these exercises</strong>You can explain and test an illustrative policy. You have not generated genuine SGX or TDX evidence, verified a real quote, or established the security of any workload.</div>'
    hw = '<div class="split"><div class="panel"><h3>SGX route</h3><p>On an authorized Linux test machine, check processor and OS support. Then use Intel’s maintained SDK sample enclave and DCAP quote-verification documentation. Simulation mode can teach calling conventions; it is not hardware attestation.</p><pre class="code">grep -w sgx /proc/cpuinfo | head -1\nls -l /dev/sgx_enclave 2>/dev/null</pre><p>Build a sample only after checking its current prerequisites and whether the processor/BIOS actually enables SGX.</p></div><div class="panel"><h3>TDX route</h3><p>Use a TD-capable host or supported confidential-VM provider. Read the Linux KVM TDX host interface and guest report API before collecting evidence. A TDREPORT is local report material, not a remotely trusted verdict by itself.</p><pre class="code">ls -l /dev/tdx-guest 2>/dev/null</pre><p>Record guest image, firmware, module and collateral versions before comparing reports or debugging failures.</p></div></div>'
    production = '<div class="stack">' + ''.join([
        '<div class="stack-row"><b>01 / REQUEST</b><span>The guest or enclave requests an attestation challenge and produces evidence bound to the request or session.</span></div>',
        '<div class="stack-row"><b>02 / VERIFY</b><span>A verifier checks manufacturer endorsements, quote authenticity, TCB and owner-controlled reference values.</span></div>',
        '<div class="stack-row"><b>03 / DECIDE</b><span>A relying party applies its own policy to the result and releases only the required secret to the bound recipient.</span></div>',
        '<div class="stack-row"><b>04 / OPERATE</b><span>Rotate secrets, update policy/collateral, monitor revocation and re-attest at meaningful lifecycle boundaries.</span></div>'
    ]) + '</div><p class="source-note">For an open-source reference architecture, inspect <a class="inline-link" href="https://github.com/confidential-containers/trustee">Confidential Containers Trustee</a> and its verifier, reference-value and key-broker components.</p>'
    sources = '<div class="source-grid">' + ''.join([
        link('https://www.intel.com/content/www/us/en/developer/tools/trust-domain-extensions/documentation.html', 'Intel TDX documentation hub', 'Architecture, module specifications, attestation and security guidance.', 'INTEL / TDX'),
        link('https://docs.kernel.org/virt/kvm/x86/intel-tdx.html', 'Linux KVM Intel TDX', 'Host-side KVM interfaces and feature status.', 'LINUX / TDX'),
        link('https://docs.kernel.org/virt/coco/tdx-guest.html', 'Linux TDX guest API', 'Guest report device and userspace API; check your kernel version.', 'LINUX / TDX'),
        link('https://docs.kernel.org/arch/x86/sgx.html', 'Linux SGX architecture', 'Enclave memory, build, runtime and driver behavior.', 'LINUX / SGX'),
        link('https://github.com/intel/confidential-computing.sgx', 'Intel SGX SDK & DCAP', 'Maintained code and quote-generation/verification components.', 'INTEL / SGX'),
        link('https://www.rfc-editor.org/rfc/rfc9334.html', 'RFC 9334 · RATS architecture', 'Architecture-neutral roles, evidence, verifier and relying party.', 'IETF / RATS'),
        link('https://docs.kernel.org/security/snp-tdx-threat-model.html', 'Linux CoCo threat model', 'Untrusted-host attack surfaces for confidential VMs.', 'LINUX / SECURITY'),
        link('https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/best-practices/trusted-domain-security-guidance-for-developers.html', 'TD developer security guidance', 'Shared memory, host interfaces and side-channel considerations.', 'INTEL / SECURITY'),
        link('https://github.com/confidential-containers/trustee', 'Trustee · attestation and key delivery', 'Open-source KBS, verifier and reference-value components.', 'COCO / IMPLEMENTATION'),
        link('https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/tdx-security-research-and-assurance.html', 'TDX research and assurance', 'Intel’s research focus and evolving threat model.', 'INTEL / RESEARCH')
    ]) + '</div><p class="source-note">Source review: September 30, 2026. Vendor advisories, supported processors and kernel interfaces change; check the linked upstream pages before deployment.</p>'
    return intro + article_section('01 / NO SPECIAL HARDWARE', 'Four exercises anyone can complete', 'These teach the reasoning required for a real deployment without pretending to produce trustworthy evidence.', nohw) + article_section('02 / WHEN HARDWARE IS AVAILABLE', 'Two practical entry points', 'Use your own authorized machine or a supported provider. Do not infer support from a marketing name alone.', hw, 'hardware') + article_section('03 / SYSTEM PATH', 'From evidence to a protected workload', 'Hardware isolation is only one step. Verification, policy and key delivery complete the workflow.', production) + article_section('04 / SOURCE LIBRARY', 'Return to primary documentation', 'Start with the Linux and Intel material for the feature you are testing; use the RATS model to keep roles clear.', sources, 'sources')


def labs_zh():
    intro = page_hero('zh', '实验与资料', '先练习决策<br><em>再使用专用硬件</em>', '先做威胁模型与证明策略练习，再检查硬件支持、跟随最新厂商样例，最后把证明接到秘密交付。')
    nohw = '<div class="route">' + ''.join([
        route('01', '画保护边界', '选一个处理秘密的服务，标出 SGX enclave 与 TDX Guest 各应包含什么，列出所有面向宿主的接口。', 'architecture.zh.html#model', '打开边界导读'),
        route('02', '写接受策略', '指定允许的测量值、签名者或 Guest 镜像、调试状态、TCB 级别、新鲜度窗口与密钥绑定。', 'attestation.zh.html#policy', '打开策略导读'),
        route('03', '翻转一项声明', '用站内模拟器拒绝过旧 TCB、镜像变化、过期挑战或未绑定密钥，并解释是谁做了决定。', 'attestation.zh.html#policy', '运行交互实验'),
        route('04', '审查盲点', '列出安全声明未覆盖的共享内存、设备输入、拒绝服务、侧信道和软件漏洞。', 'architecture.zh.html#surfaces', '审查攻击面')
    ]) + '</div><div class="signal" style="margin-top:20px"><strong>完成后可以如何表述</strong>你能够解释并测试示意策略；还没有生成真实的 SGX 或 TDX 证据、验证真正的 quote，也没有证明某个工作负载安全。</div>'
    hw = '<div class="split"><div class="panel"><h3>SGX 路线</h3><p>在获授权的 Linux 测试机上检查处理器和 OS 支持，再使用 Intel 维护的 SDK 示例 enclave 与 DCAP quote 验证文档。模拟模式可以学习调用接口，但不构成硬件证明。</p><pre class="code">grep -w sgx /proc/cpuinfo | head -1\nls -l /dev/sgx_enclave 2>/dev/null</pre><p>构建样例前先核对当前依赖，以及处理器和 BIOS 是否实际启用 SGX。</p></div><div class="panel"><h3>TDX 路线</h3><p>使用支持 TD 的宿主机或机密 VM 服务。收集证据前先读 Linux KVM TDX 宿主接口和 Guest report API。TDREPORT 只是本地报告材料，不是可直接远程信任的结论。</p><pre class="code">ls -l /dev/tdx-guest 2>/dev/null</pre><p>比较报告或排查失败前，记录 Guest 镜像、固件、模块和证明材料版本。</p></div></div>'
    production = '<div class="stack">' + ''.join([
        '<div class="stack-row"><b>01 / 请求</b><span>Guest 或 enclave 请求证明挑战，并产生绑定到请求或会话的证据。</span></div>',
        '<div class="stack-row"><b>02 / 验证</b><span>验证者检查厂商背书、quote 真实性、TCB 和所有者维护的参考值。</span></div>',
        '<div class="stack-row"><b>03 / 决策</b><span>依赖方对结果应用自己的策略，只向绑定的收件者释放所需秘密。</span></div>',
        '<div class="stack-row"><b>04 / 运行</b><span>轮换秘密、更新策略和证明材料、监控撤销，并在重要生命周期边界重新证明。</span></div>'
    ]) + '</div><p class="source-note">开源架构参考：<a class="inline-link" href="https://github.com/confidential-containers/trustee">Confidential Containers Trustee</a> 及其验证、参考值和密钥代理组件。</p>'
    sources = '<div class="source-grid">' + ''.join([
        link('https://www.intel.com/content/www/us/en/developer/tools/trust-domain-extensions/documentation.html', 'Intel TDX 文档中心', '架构、模块规范、证明与安全指南。', 'INTEL / TDX'),
        link('https://docs.kernel.org/virt/kvm/x86/intel-tdx.html', 'Linux KVM Intel TDX', '宿主 KVM 接口与功能状态。', 'LINUX / TDX'),
        link('https://docs.kernel.org/virt/coco/tdx-guest.html', 'Linux TDX Guest API', 'Guest report 设备与用户态 API；应核对具体内核版本。', 'LINUX / TDX'),
        link('https://docs.kernel.org/arch/x86/sgx.html', 'Linux SGX 架构', 'Enclave 内存、构建、运行时与驱动行为。', 'LINUX / SGX'),
        link('https://github.com/intel/confidential-computing.sgx', 'Intel SGX SDK 与 DCAP', '维护中的代码及 quote 生成与验证组件。', 'INTEL / SGX'),
        link('https://www.rfc-editor.org/rfc/rfc9334.html', 'RFC 9334 · RATS 架构', '跨平台的角色、证据、验证者与依赖方模型。', 'IETF / RATS'),
        link('https://docs.kernel.org/security/snp-tdx-threat-model.html', 'Linux CoCo 威胁模型', '机密 VM 面对不可信宿主的攻击面。', 'LINUX / SECURITY'),
        link('https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/best-practices/trusted-domain-security-guidance-for-developers.html', 'TD 开发者安全指南', '共享内存、宿主接口与侧信道考虑。', 'INTEL / SECURITY'),
        link('https://github.com/confidential-containers/trustee', 'Trustee · 证明与密钥交付', '开源 KBS、验证者与参考值组件。', 'COCO / 实现'),
        link('https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/tdx-security-research-and-assurance.html', 'TDX 安全研究与保障', 'Intel 的研究重点与持续演进的威胁模型。', 'INTEL / RESEARCH')
    ]) + '</div><p class="source-note">资料核对：2026 年 9 月 30 日。厂商公告、受支持处理器及内核接口会变化；部署前请重新核对上游页面。</p>'
    return intro + article_section('01 / 无需专用硬件', '人人可做的四个练习', '这些练习培养真实部署所需的判断能力，不冒充可信硬件证据。', nohw) + article_section('02 / 有硬件时', '两条实践入口', '使用自有授权设备或受支持的服务；不能仅凭产品名称判断支持情况。', hw, 'hardware') + article_section('03 / 系统路径', '从证据到受保护工作负载', '硬件隔离只是一步，验证、策略与密钥交付才让工作流闭环。', production) + article_section('04 / 一手资料', '回到原始文档', '先看对应功能的 Linux 与 Intel 文档，再用 RATS 模型理清各个角色。', sources, 'sources')


if __name__ == '__main__':
    content = {
        'en': (index_en, architecture_en, attestation_en, labs_en),
        'zh': (index_zh, architecture_zh, attestation_zh, labs_zh),
    }
    for lang in ('en', 'zh'):
        for name, builder in zip(PAGES, content[lang]):
            target = ROOT / f'{name}{".zh" if lang == "zh" else ""}.html'
            target.write_text(shell(lang, name, builder()), encoding='utf-8')
            print(target.name)
