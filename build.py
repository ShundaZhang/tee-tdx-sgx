"""Build the static bilingual TEE / TDX / SGX atlas (stdlib only)."""
from pathlib import Path
from diagram_core import arrow, flow as diagram_flow, frame, node, tr
from diagrams import TDISP_SPEC, TDX_CONNECT_ARCH, diagram
from intel_figures import BASE, MIGRATION, intel_figure

ROOT = Path(__file__).parent
PAGES = ('index', 'sgx', 'tdx', 'labs')
NAV = {
    'en': ('Overview', 'Intel SGX', 'Intel TDX', 'Labs & sources'),
    'zh': ('总览', 'Intel SGX', 'Intel TDX', '实验与资料'),
}
TITLES = {
    'en': ('TEE / TDX / SGX Atlas', 'Intel SGX architecture & instructions', 'Intel TDX architecture & calls', 'Hardware labs & primary sources'),
    'zh': ('TEE / TDX / SGX 地图', 'Intel SGX 原理与指令', 'Intel TDX 原理与调用', '硬件实验与一手资料'),
}
DESCRIPTIONS = {
    'en': 'A focused guide to Intel SGX and TDX architecture, hardware support, SGX instructions, TDCALL and SEAMCALL.',
    'zh': '聚焦 Intel SGX 与 TDX 的架构、硬件支持、SGX 指令、TDCALL 和 SEAMCALL。',
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
    foot = ('聚焦 SGX 与 TDX 的硬件和软件机制。功能支持及指令接口以具体处理器、模块和系统版本为准。' if zh else 'A focused SGX and TDX field guide. Check processor, module and OS versions for actual feature and ABI support.')
    return f'''<!doctype html>
<html lang="{'zh-CN' if zh else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#101b2a"><meta name="description" content="{DESCRIPTIONS[lang]}"><title>{TITLES[lang][idx]} · ShundaZhang</title><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="diagrams.css"><script src="language.js"></script></head>
<body>{languages}<a class="skip" href="#main">{'跳至正文' if zh else 'Skip to content'}</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="index{suffix}"><span class="brand-mark">T//</span><span class="brand-name">TEE / TDX / SGX ATLAS</span></a><nav class="nav" aria-label="{'主导航' if zh else 'Main navigation'}">{nav}</nav></div></header>
<main id="main">{body}</main><footer class="footer"><div class="wrap footer-inner"><div><strong>TEE / TDX / SGX ATLAS</strong><p>{foot}</p></div><div><a href="https://shundazhang.github.io/">{'个人主页' if zh else 'Home'}</a><a href="https://github.com/ShundaZhang/tee-tdx-sgx">GitHub ↗</a></div></div></footer></body></html>'''


def section(label, title, intro, content, tone='', section_id=''):
    ident = f' id="{section_id}"' if section_id else ''
    return f'<section class="section {tone}"{ident}><div class="wrap"><div class="section-head"><div><span class="kicker">{label}</span><h2>{title}</h2></div><p>{intro}</p></div>{content}</div></section>'


def page_hero(lang, crumb, title, intro):
    home = '总览' if lang == 'zh' else 'OVERVIEW'
    suffix = '.zh.html' if lang == 'zh' else '.html'
    return f'<section class="page-hero"><div class="wrap"><div class="crumb"><a href="index{suffix}">{home}</a> / {crumb}</div><h1>{title}</h1><p>{intro}</p></div></section>'


def article(label, title, lead, content, ident=''):
    aid = f' id="{ident}"' if ident else ''
    return f'<section class="article-section"{aid}><div class="wrap"><span class="kicker">{label}</span><h2>{title}</h2><p>{lead}</p>{content}</div></section>'


def detail(label, title, text):
    return f'<article class="detail-card"><span class="badge">{label}</span><h3>{title}</h3><p>{text}</p></article>'


def table(headers, rows):
    return '<div class="comparison"><table><thead><tr>' + ''.join(f'<th>{h}</th>' for h in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>' for row in rows) + '</tbody></table></div>'


def index_en():
    hero = '''<section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">INTEL CONFIDENTIAL COMPUTING / HARDWARE FIELD GUIDE</span><h1>Understand SGX<br><em>and TDX from the CPU up</em></h1><p>Two independent mechanisms to learn on their own terms: SGX protects an enclave inside a process; TDX protects a guest VM. Start with supported hardware, memory structures, entry and exit, and the instructions each mechanism exposes.</p><div class="buttons"><a class="button primary" href="sgx.html">Explore SGX ↗</a><a class="button ghost" href="tdx.html">Explore TDX ↗</a></div><div class="hero-note">ARCHITECTURE → INSTRUCTIONS → SOFTWARE STACK → HANDS-ON CHECKS</div></div><div class="boundary-visual" role="img" aria-label="An untrusted host surrounds an SGX process enclave and a TDX virtual machine, with different CPU instruction paths"><div class="visual-head"><span>CPU ISOLATION / TWO MODELS</span><span>SGX ≠ TDX</span></div><div class="host-box"><span>HOST APPLICATION / OS / VMM</span><div class="protected-row"><div class="protect-box"><small>PROCESS-LEVEL</small><b>SGX</b><p>EPC + EPCM<br>ENCLS / ENCLU</p></div><div class="protect-box"><small>VM-LEVEL</small><b>TDX</b><p>SEAM + SEPT + PAMT<br>TDCALL / SEAMCALL</p></div></div></div><div class="visual-connector"></div><div class="verifier-box"><span>PRIVATE MEMORY ≠ SHARED I/O</span><strong>CPU</strong></div></div></div></section>'''
    cards = '<div class="card-grid">' + ''.join([
        card('01 / ENCLAVE', 'Intel SGX', 'Follow how enclave pages are built and measured, why EPCM checks matter, and how EENTER, EEXIT and AEX change execution.', 'sgx.html', 'Study SGX'),
        card('02 / TRUST DOMAIN', 'Intel TDX', 'Follow a TD from host creation through guest entry, private page acceptance and exits. Separate TDCALL from SEAMCALL and TDVMCALL.', 'tdx.html', 'Study TDX'),
        card('03 / PRACTICE', 'Hardware and software stack', 'Check CPU model, firmware enablement, Linux interfaces, module version and samples before assuming either feature is usable.', 'labs.html', 'Open the lab guide')
    ]) + '</div>'
    compare = table(('Question', 'SGX', 'TDX'), [
        ('Protected unit', 'Enclave within a process', 'Trust Domain: a confidential VM'),
        ('Primary CPU structures', 'EPC pages, EPCM metadata, SECS and TCS', 'SEAM/TDX module, Secure EPT, PAMT and private KeyIDs'),
        ('Main call boundary', 'ENCLS by privileged software; ENCLU by user/enclave code', 'SEAMCALL by host; TDCALL by guest TD'),
        ('Memory outside boundary', 'Ordinary process memory is untrusted to the enclave', 'Shared guest pages and device I/O remain visible to the host'),
        ('Software integration', 'Partition code or use an enclave runtime', 'Run a TD-aware guest OS and VMM stack')
    ])
    path = '<div class="route">' + ''.join([
        route('01', 'Check the platform', 'Distinguish CPU support, firmware enablement, OS driver and actual usable device nodes.', 'labs.html#hardware', 'Run support checks'),
        route('02', 'Trace SGX memory', 'Understand EPC, EPCM, SECS, TCS and the measured enclave build.', 'sgx.html#memory', 'Open SGX memory model'),
        route('03', 'Read SGX instruction flow', 'Follow ECREATE → EADD/EEXTEND → EINIT → EENTER/EEXIT and AEX/ERESUME.', 'sgx.html#instructions', 'Open SGX instruction map'),
        route('04', 'Trace TDX memory', 'Understand SEAM, private KeyIDs, PAMT, Secure EPT and private/shared pages.', 'tdx.html#memory', 'Open TDX memory model'),
        route('05', 'Read TDX call flow', 'Follow host SEAMCALLs and guest TDCALLs, including TDG.VP.VMCALL.', 'tdx.html#calls', 'Open TDX call map'),
        route('06', 'Revisit in source', 'Map each architectural step to Linux KVM, guest code, Intel specs and a reproducible lab.', 'labs.html#sources', 'Open primary sources')
    ]) + '</div>'
    brief = '<div class="signal"><strong>Remote attestation in one paragraph</strong>SGX and TDX can produce measured reports and remote quotes. A remote verifier checks the evidence against a policy before an application trusts the environment. <a class="inline-link" href="tdx.html#remote-attestation">Trace the TDX attestation architecture ↗</a></div>'
    return hero + section('01 / THE TWO MECHANISMS', 'Learn each boundary on its own terms', 'SGX and TDX solve different isolation problems. The pages below go into the CPU mechanisms, not a single unified deployment story.', cards, 'white') + section('02 / ARCHITECTURE MAP', 'The important differences at a glance', 'Use this as a map before reading the instruction tables.', compare) + section('03 / LEARNING ROUTE', 'Six concrete steps', 'The route assumes familiarity with x86, virtual memory and virtualization; it goes straight to the new mechanisms.', path, 'tinted') + section('04 / BRIEF CONTEXT', 'Where attestation fits', 'A small bridge from local isolation to remote use, without making it the center of this site.', brief, 'white', 'attestation')


def index_zh():
    hero = '''<section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">INTEL CONFIDENTIAL COMPUTING / HARDWARE FIELD GUIDE</span><h1>从 CPU 出发<br><em>读懂 SGX 与 TDX</em></h1><p>把两项机制分别学清楚：SGX 保护进程中的 enclave，TDX 保护一个 Guest VM。先看硬件支持、内存结构、进入与退出，再读各自暴露的指令和调用。</p><div class="buttons"><a class="button primary" href="sgx.zh.html">学习 SGX ↗</a><a class="button ghost" href="tdx.zh.html">学习 TDX ↗</a></div><div class="hero-note">架构 → 指令 → 软件栈 → 动手检查</div></div><div class="boundary-visual" role="img" aria-label="不可信宿主包含 SGX enclave 与 TDX 虚拟机，两者有不同 CPU 指令路径"><div class="visual-head"><span>CPU ISOLATION / TWO MODELS</span><span>SGX ≠ TDX</span></div><div class="host-box"><span>宿主应用 / OS / VMM</span><div class="protected-row"><div class="protect-box"><small>进程级</small><b>SGX</b><p>EPC + EPCM<br>ENCLS / ENCLU</p></div><div class="protect-box"><small>虚拟机级</small><b>TDX</b><p>SEAM + SEPT + PAMT<br>TDCALL / SEAMCALL</p></div></div></div><div class="visual-connector"></div><div class="verifier-box"><span>私有内存 ≠ 共享 I/O</span><strong>CPU</strong></div></div></div></section>'''
    cards = '<div class="card-grid">' + ''.join([
        card('01 / ENCLAVE', 'Intel SGX', '跟随 enclave 页面构建与测量，理解 EPCM 检查，以及 EENTER、EEXIT 和 AEX 如何改变执行。', 'sgx.zh.html', '学习 SGX'),
        card('02 / TRUST DOMAIN', 'Intel TDX', '跟随 TD 从宿主创建到 Guest 进入、私有页接受与退出；分清 TDCALL、SEAMCALL 和 TDVMCALL。', 'tdx.zh.html', '学习 TDX'),
        card('03 / 实践', '硬件与软件栈', '核对 CPU 型号、固件开关、Linux 接口、模块版本与样例，再判断功能是否真的可用。', 'labs.zh.html', '打开实验指南')
    ]) + '</div>'
    compare = table(('问题', 'SGX', 'TDX'), [
        ('保护对象', '进程中的 enclave', 'Trust Domain：机密虚拟机'),
        ('主要 CPU 结构', 'EPC 页面、EPCM 元数据、SECS 与 TCS', 'SEAM/TDX 模块、Secure EPT、PAMT 与私有 KeyID'),
        ('主要调用边界', '特权软件用 ENCLS；用户态/enclave 用 ENCLU', '宿主用 SEAMCALL；Guest TD 用 TDCALL'),
        ('边界外内存', '普通进程内存对 enclave 不可信', 'Guest 共享页与设备 I/O 对宿主可见'),
        ('软件接入', '拆分代码或使用 enclave 运行时', '使用支持 TD 的 Guest OS 与 VMM 软件栈')
    ])
    path = '<div class="route">' + ''.join([
        route('01', '先检查平台', '分开核对 CPU 支持、固件开关、OS 驱动和可用的设备节点。', 'labs.zh.html#hardware', '运行支持检查'),
        route('02', '追踪 SGX 内存', '理解 EPC、EPCM、SECS、TCS 与经过测量的 enclave 构建。', 'sgx.zh.html#memory', '看 SGX 内存模型'),
        route('03', '读 SGX 指令路径', '跟随 ECREATE → EADD/EEXTEND → EINIT → EENTER/EEXIT 及 AEX/ERESUME。', 'sgx.zh.html#instructions', '看 SGX 指令地图'),
        route('04', '追踪 TDX 内存', '理解 SEAM、私有 KeyID、PAMT、Secure EPT 与私有/共享页。', 'tdx.zh.html#memory', '看 TDX 内存模型'),
        route('05', '读 TDX 调用路径', '跟随宿主 SEAMCALL 与 Guest TDCALL，包括 TDG.VP.VMCALL。', 'tdx.zh.html#calls', '看 TDX 调用地图'),
        route('06', '回到源码', '把每一步对应到 Linux KVM、Guest 代码、Intel 规范与可复现实验。', 'labs.zh.html#sources', '打开一手资料')
    ]) + '</div>'
    brief = '<div class="signal"><strong>用一段话定位远程证明</strong>SGX 与 TDX 可产生包含度量信息的报告和 Quote。远程验证者按策略检查证据，应用据此决定是否信任该环境。<a class="inline-link" href="tdx.zh.html#remote-attestation">查看 TDX 远程证明架构 ↗</a></div>'
    return hero + section('01 / 两项机制', '分别学清各自的边界', 'SGX 与 TDX 解决不同隔离问题。下面的章节深入 CPU 机制，不把它们强行塞进一条部署故事。', cards, 'white') + section('02 / 架构地图', '先看重要差异', '读指令表前，先用它建立坐标。', compare) + section('03 / 学习路径', '六个具体步骤', '假设你已有 x86、虚拟内存和虚拟化基础，直接进入新增机制。', path, 'tinted') + section('04 / 简要背景', '远程证明在什么位置', '只交代本地隔离如何延伸到远端使用，不让它占据此站主线。', brief, 'white', 'attestation')


def sgx_en():
    hero = page_hero('en', 'INTEL SGX', 'An enclave is a new<br><em>CPU access boundary</em>', 'Understand the physical EPC and EPCM checks, how an enclave is measured and initialized, and which instructions cross the boundary.')
    hardware = '<div class="detail-grid">' + ''.join([
        detail('CPU', 'Check the exact processor', 'SGX support is SKU-specific. Intel lists supported Xeon families and models; older consumer CPUs vary. CPUID leaf 0x12 enumerates SGX capabilities when enabled.'),
        detail('FIRMWARE', 'Enable it in BIOS/UEFI', 'A capable CPU is not sufficient if platform firmware disables SGX or allocates no EPC. BIOS policy can also affect launch control and EPC size.'),
        detail('OS', 'Look for the Linux interface', 'The Linux SGX driver exposes /dev/sgx_enclave for enclave construction. A missing device can mean unsupported hardware, disabled firmware, or missing kernel support.'),
        detail('VARIANTS', 'Separate SGX1 from SGX2', 'SGX1 provides the baseline enclave lifecycle. SGX2 adds dynamic page management; software must check what the running platform enumerates.')
    ]) + '</div><p class="source-note">Hardware references: <a class="inline-link" href="https://www.intel.com/content/www/us/en/architecture-and-technology/software-guard-extensions-processors.html">Intel processor list</a> and <a class="inline-link" href="https://docs.kernel.org/arch/x86/sgx.html">Linux SGX guide</a>.</p>'
    memory = '<div class="stack">' + ''.join([
        '<div class="stack-row"><b>EPC</b><span>Enclave Page Cache: protected physical pages for enclave code, data and metadata. The OS manages allocation and paging, but cannot directly read a live enclave page.</span></div>',
        '<div class="stack-row"><b>EPCM</b><span>Enclave Page Cache Map: CPU-maintained metadata identifying page ownership, type and permissions. EPCM checks add restrictions beyond ordinary page tables.</span></div>',
        '<div class="stack-row"><b>SECS</b><span>Enclave Control Structure: enclave-wide attributes, range and identity state used during creation.</span></div>',
        '<div class="stack-row"><b>TCS</b><span>Thread Control Structure: an entry point and execution state for one enclave thread.</span></div>'
    ]) + '</div><div class="signal" style="margin-top:20px"><strong>Why the OS page table is not enough</strong>The OS still maps virtual addresses and manages resources. The CPU also checks EPCM ownership and permissions before an enclave page is used. Memory encryption and integrity details vary across SGX processor generations; check the actual platform rather than assuming one uniform property.</div>'
    instructions = table(('Class / privilege', 'Leaf', 'What to remember'), [
        ('ENCLS · privileged', '<code>ECREATE</code>', 'Create SECS and begin a new enclave.'),
        ('ENCLS · privileged', '<code>EADD</code> / <code>EEXTEND</code>', 'Add EPC pages and extend the measurement over selected contents.'),
        ('ENCLS · privileged', '<code>EINIT</code>', 'Validate initialization requirements and finalize the enclave before entry.'),
        ('ENCLS · privileged', '<code>EREMOVE</code>', 'Remove an EPC page during teardown or reclamation.'),
        ('ENCLU · user', '<code>EENTER</code> / <code>EEXIT</code>', 'Enter and leave enclave execution through its defined interface.'),
        ('ENCLU · user', '<code>ERESUME</code>', 'Resume after an asynchronous enclave exit (AEX).'),
        ('ENCLU · enclave', '<code>EREPORT</code> / <code>EGETKEY</code>', 'Create a local report or derive an enclave-specific key.'),
        ('SGX2 · optional', '<code>EACCEPT</code>', 'Accept dynamically added or modified pages where SGX2 is supported.')
    ]) + '<p class="source-note">ENCLS/ENCLU names refer to instruction groups; the named operations are leaves. See Intel’s <a class="inline-link" href="https://www.intel.com/content/www/us/en/developer/articles/technical/overview-of-an-intel-software-guard-extensions-enclave-life-cycle.html">enclave lifecycle overview</a> and the <a class="inline-link" href="https://www.intel.com/content/dam/develop/external/us/en/documents/329298-002-629101.pdf">programming reference</a> for operands and exceptions.</p>'
    flow = '<div class="stack">' + ''.join([
        '<div class="stack-row"><b>BUILD</b><span>OS/runtime: ECREATE → EADD pages → EEXTEND measured content → EINIT.</span></div>',
        '<div class="stack-row"><b>RUN</b><span>Host thread: EENTER → enclave code → EEXIT, with trusted/untrusted parameter handling at the interface.</span></div>',
        '<div class="stack-row"><b>INTERRUPT</b><span>An interrupt or exception can trigger AEX (an event, not an instruction). The host handles it; ERESUME re-enters when appropriate.</span></div>',
        '<div class="stack-row"><b>EXTEND</b><span>SGX2 may add/change pages dynamically, with enclave acceptance before use.</span></div>'
    ]) + '</div>'
    boundary = '<div class="split"><div class="panel"><h3>Inside the enclave</h3><p>Keep secrets and only the code that needs them. Validate every value returned by host calls. Minimize runtime and serialization logic that must be trusted.</p></div><div class="panel"><h3>Outside the enclave</h3><p>The OS and host process can schedule, interrupt and feed input. Page-fault patterns, caches and timing may reveal information unless the application accounts for them.</p></div></div>'
    return hero + article('01 / PLATFORM SUPPORT', 'First verify hardware and firmware', '“This CPU family supports SGX” does not prove the particular machine exposes a usable enclave facility.', hardware, 'hardware') + article('02 / MEMORY MODEL', 'Four structures to keep in view', 'Follow one page from ordinary memory into EPC and through CPU metadata checks.', diagram('sgx_memory', 'en') + memory, 'memory') + article('03 / INSTRUCTION MAP', 'Read the lifecycle as ENCLS and ENCLU', 'Do not memorize opcodes first. Group the leaves by who executes them and which state transition they make.', instructions, 'instructions') + article('04 / EXECUTION TRACE', 'One enclave from creation to interruption', 'AEX and resumption are especially important when reasoning about interrupts and untrusted scheduling.', diagram('sgx_execution', 'en') + flow, 'flow') + article('05 / SECURITY BOUNDARY', 'What isolation still leaves to software', 'The enclave protects direct access to its pages; its host interface and side-channel behavior are separate design work.', boundary)


def sgx_zh():
    hero = page_hero('zh', 'INTEL SGX', 'Enclave 是新的<br><em>CPU 访问边界</em>', '理解 EPC 与 EPCM 的硬件检查、enclave 如何测量和初始化，以及哪些指令跨越边界。')
    hardware = '<div class="detail-grid">' + ''.join([
        detail('CPU', '核对准确型号', 'SGX 支持与具体 SKU 有关。Intel 列出受支持的 Xeon 家族与型号；较早的消费级 CPU 情况不一。启用后可用 CPUID leaf 0x12 枚举 SGX 能力。'),
        detail('固件', '在 BIOS/UEFI 中启用', '即使 CPU 有能力，固件禁用 SGX 或未分配 EPC 时仍无法使用。BIOS 策略还可能影响 launch control 和 EPC 大小。'),
        detail('OS', '寻找 Linux 接口', 'Linux SGX 驱动通过 /dev/sgx_enclave 构建 enclave。设备缺失可能是硬件不支持、固件关闭或内核缺少支持。'),
        detail('变体', '分清 SGX1 与 SGX2', 'SGX1 提供基本 enclave 生命周期；SGX2 增加动态页面管理，软件应检查实际平台枚举的能力。')
    ]) + '</div><p class="source-note">硬件资料：<a class="inline-link" href="https://www.intel.com/content/www/us/en/architecture-and-technology/software-guard-extensions-processors.html">Intel 处理器列表</a>与 <a class="inline-link" href="https://docs.kernel.org/arch/x86/sgx.html">Linux SGX 导读</a>。</p>'
    memory = '<div class="stack">' + ''.join([
        '<div class="stack-row"><b>EPC</b><span>Enclave Page Cache：保存 enclave 代码、数据和元数据的受保护物理页面。OS 管理分配和换页，但不能直接读取运行中的 enclave 页面。</span></div>',
        '<div class="stack-row"><b>EPCM</b><span>Enclave Page Cache Map：CPU 维护的元数据，记录页面所有者、类型与权限。EPCM 检查在普通页表之外增加限制。</span></div>',
        '<div class="stack-row"><b>SECS</b><span>Enclave Control Structure：创建时使用的全局属性、范围和身份状态。</span></div>',
        '<div class="stack-row"><b>TCS</b><span>Thread Control Structure：一个 enclave 线程的入口与执行状态。</span></div>'
    ]) + '</div><div class="signal" style="margin-top:20px"><strong>为什么 OS 页表还不够</strong>OS 仍映射虚拟地址并管理资源；CPU 使用 EPCM 再检查 enclave 页面所有权和权限。内存加密与完整性的细节因 SGX 处理器代际而异，不能假定所有平台具有完全相同的属性。</div>'
    instructions = table(('指令组 / 权限', 'Leaf', '应记住的作用'), [
        ('ENCLS · 特权态', '<code>ECREATE</code>', '创建 SECS，开始新 enclave。'),
        ('ENCLS · 特权态', '<code>EADD</code> / <code>EEXTEND</code>', '添加 EPC 页面，对选定内容扩展测量值。'),
        ('ENCLS · 特权态', '<code>EINIT</code>', '验证初始化条件，并在进入前完成 enclave 初始化。'),
        ('ENCLS · 特权态', '<code>EREMOVE</code>', '在拆除或回收时移除 EPC 页面。'),
        ('ENCLU · 用户态', '<code>EENTER</code> / <code>EEXIT</code>', '通过定义好的接口进入和离开 enclave 执行。'),
        ('ENCLU · 用户态', '<code>ERESUME</code>', '在异步 enclave 退出（AEX）后恢复。'),
        ('ENCLU · enclave', '<code>EREPORT</code> / <code>EGETKEY</code>', '生成本地报告或派生 enclave 专属密钥。'),
        ('SGX2 · 可选', '<code>EACCEPT</code>', '在支持 SGX2 时接受动态加入或更改的页面。')
    ]) + '<p class="source-note">ENCLS/ENCLU 是指令组，表中的名称是对应 leaf。操作数与异常请看 Intel 的 <a class="inline-link" href="https://www.intel.com/content/www/us/en/developer/articles/technical/overview-of-an-intel-software-guard-extensions-enclave-life-cycle.html">enclave 生命周期导读</a>和<a class="inline-link" href="https://www.intel.com/content/dam/develop/external/us/en/documents/329298-002-629101.pdf">编程参考</a>。</p>'
    flow = '<div class="stack">' + ''.join([
        '<div class="stack-row"><b>构建</b><span>OS/运行时：ECREATE → EADD 页面 → EEXTEND 测量内容 → EINIT。</span></div>',
        '<div class="stack-row"><b>运行</b><span>宿主线程：EENTER → enclave 代码 → EEXIT；边界上的可信/不可信参数要审查。</span></div>',
        '<div class="stack-row"><b>中断</b><span>中断或异常可能触发 AEX（事件，不是一条指令）。宿主处理后，适当情况下用 ERESUME 再进入。</span></div>',
        '<div class="stack-row"><b>扩展</b><span>SGX2 可动态增加或更改页面；enclave 接受后才能使用。</span></div>'
    ]) + '</div>'
    boundary = '<div class="split"><div class="panel"><h3>Enclave 内部</h3><p>只保留秘密和需要处理秘密的代码。校验宿主调用返回的每个值。尽量缩小必须信任的运行时与序列化逻辑。</p></div><div class="panel"><h3>Enclave 外部</h3><p>OS 和宿主进程可以调度、打断并提供输入。若应用未处理页面故障模式、缓存和时序，它们仍可能泄露信息。</p></div></div>'
    return hero + article('01 / 平台支持', '先确认硬件与固件', '“这个 CPU 家族支持 SGX”并不证明眼前的机器提供可用的 enclave 功能。', hardware, 'hardware') + article('02 / 内存模型', '记住四个关键结构', '跟随一个页面从普通内存进入 EPC，并经过 CPU 元数据检查。', diagram('sgx_memory', 'zh') + memory, 'memory') + article('03 / 指令地图', '按 ENCLS 与 ENCLU 读生命周期', '先按执行者和状态变化分组，再去记操作码。', instructions, 'instructions') + article('04 / 执行路径', '从创建到中断的一次运行', 'AEX 与恢复是理解中断和不可信调度的关键。', diagram('sgx_execution', 'zh') + flow, 'flow') + article('05 / 安全边界', '隔离仍留给软件的问题', 'Enclave 阻止页面被直接读取；宿主接口和侧信道行为仍需单独设计。', boundary)


def tdx_contents(lang):
    t = lambda en, zh: tr(lang, en, zh)
    entries = [
        ('architecture', t('Architecture', '整体架构')),
        ('platform-boot', t('Platform startup', '平台启动')),
        ('memory', t('Private memory', '私有内存')),
        ('calls', t('Module calls', '模块调用')),
        ('flow', t('TD lifecycle', 'TD 生命周期')),
        ('td-measurement', t('TD measurement', 'TD 度量')),
        ('tdx-connect', 'TDX Connect'),
        ('service-td', 'Service TD'),
        ('remote-attestation', t('Remote attestation', '远程证明')),
        ('migration', t('TD migration', 'TD 迁移')),
    ]
    items = ''.join(f'<li><a href="#{ident}">{label}</a></li>' for ident, label in entries)
    return f'<nav class="tdx-contents" aria-label="{t("TDX contents", "TDX 章节目录")}"><ul class="wrap">{items}</ul></nav>'


def tdx_overview(lang):
    t = lambda en, zh: tr(lang, en, zh)
    figure = intel_figure(lang, 'architecture', t('Intel TDX components overview', 'Intel TDX 组件全景'),
        t('Legacy VMs sit above the host VMM. Trust Domains run beside them, with the TDX module below them in SEAM root mode.',
          '传统虚拟机由宿主 VMM 管理。Trust Domain 与传统虚拟机并存，由处于 SEAM root 的 TDX 模块管理保护边界。'),
        t('Compare the access-control boundaries around the legacy VMs and the TDs. The host schedules both, while the module controls private TD state and mappings.',
          '对照图中传统虚拟机与 TD 周围的访问控制边界。宿主调度两类虚拟机，模块控制 TD 私有状态与映射。'))
    return tdx_contents(lang) + article(t('ARCHITECTURE', '架构总览'), t('The platform, the module and the Trust Domain', '平台、TDX 模块与 Trust Domain'),
        t('A TDX-aware VMM supplies resources and schedules vCPUs. The Intel TDX module runs in SEAM root and enforces TD isolation using CPU virtualization, protected memory mappings and private KeyIDs.',
          '支持 TDX 的 VMM 提供资源并调度 vCPU。Intel TDX 模块运行在 SEAM root，借助 CPU 虚拟化、受保护的内存映射和私有 KeyID 执行 TD 隔离。'), figure, 'architecture')


def tdx_startup(lang):
    t = lambda en, zh: tr(lang, en, zh)
    path = diagram_flow([
        node(t('Platform firmware', '平台固件'), t('SEAMRR, CMRs and private KeyIDs', '配置 SEAMRR、CMR 与私有 KeyID')),
        arrow(), node('NP-SEAMLDR ACM', t('Installs P-SEAMLDR', '安装 P-SEAMLDR')),
        arrow(), node('P-SEAMLDR', t('Verifies and installs the TDX module', '验证并安装 TDX 模块')),
        arrow(), node(t('TDX module ready', 'TDX 模块就绪'), t('Host calls initialize CPUs and memory', '宿主调用初始化 CPU 与内存'), 'protected'),
    ])
    boot_flow = frame(lang, 'tdx-startup-flow', t('From platform boot to module readiness', '从平台启动到模块就绪'), path,
        t('Firmware or host software can drive loading according to the platform design. The host initializes the installed module before creating TDs.',
          '固件或宿主软件可按平台设计发起加载。创建 TD 之前，宿主还需初始化已安装的模块。'),
        BASE[2] + '#page=33', t('Intel TDX Base Architecture §3.1.1', 'Intel TDX 基础架构 §3.1.1'))
    range_figure = intel_figure(lang, 'seam-range', t('SEAMRR and the two SEAM subranges', 'SEAMRR 与 SEAM 的两个子区域'),
        t('NP-SEAMLDR installs P-SEAMLDR into its reserved range. P-SEAMLDR installs the TDX module into MODULE_RANGE.',
          'NP-SEAMLDR 把 P-SEAMLDR 装入其保留区，后者将 TDX 模块装入 MODULE_RANGE。'),
        t('Follow the two install arrows. The firmware programs SEAMRR to define the protected range that contains both subranges.',
          '沿图中的两条安装箭头阅读。固件用 SEAMRR 定义受保护的物理地址范围，其中包含这两个子区域。'))
    init_figure = intel_figure(lang, 'module-lifecycle', t('TDX module initialization and lifecycle', 'TDX 模块初始化与状态机'),
        t('The module progresses from SYSINIT_PENDING to SYSINIT_DONE, SYSCONFIG_DONE and SYS_READY. Other paths cover disable and shutdown.',
          '模块依次经过 SYSINIT_PENDING、SYSINIT_DONE、SYSCONFIG_DONE 和 SYS_READY。图中也给出停用与关闭路径。'),
        t('Trace the first-time initialization path through the yellow states to SYS_READY. The arrows also show optional module lifecycle operations.',
          '沿黄色状态追踪首次初始化，直到 SYS_READY。其余箭头展示可选的模块生命周期操作。'))
    return '<h3 class="tdx-subhead" id="platform-boot">' + t('Platform startup and SEAM Loader', '平台启动与 SEAM Loader') + '</h3>' + boot_flow + range_figure + '<p>' + t(
        'The Non-Persistent SEAM Loader is an Authenticated Code Module (ACM). It installs the Persistent SEAM Loader, which accepts <code>SEAMLDR.INSTALL</code> via SEAMCALL. P-SEAMLDR checks the signed module information, measures the loaded image and records its identity for attestation. This measurement identifies the platform module.',
        'NP-SEAMLDR 是经认证的代码模块（ACM）。它安装常驻的 P-SEAMLDR，后者通过 SEAMCALL 接收 <code>SEAMLDR.INSTALL</code>，核验已签名的模块信息，对加载的镜像做度量，并记录用于证明的模块身份。这份度量对应平台上的 TDX 模块。',
    ) + '</p>' + init_figure + '<p>' + t(
        'The host calls <code>TDH.SYS.INIT</code>, initializes each logical processor with <code>TDH.SYS.LP.INIT</code>, configures the TDMRs and PAMT with <code>TDH.SYS.CONFIG</code>, and configures the global key on each package. <code>TDH.SYS.TDMR.INIT</code> initializes the associated PAMT ranges before the memory can back TD private pages.',
        '宿主先调用 <code>TDH.SYS.INIT</code> 做全局初始化，再对每个逻辑处理器调用 <code>TDH.SYS.LP.INIT</code>，用 <code>TDH.SYS.CONFIG</code> 配置 TDMR 和 PAMT，并在每个处理器封装上配置模块全局密钥。<code>TDH.SYS.TDMR.INIT</code> 初始化相应的 PAMT 区域后，内存才可用于 TD 私有页。',
    ) + '</p>'


def tdx_mode_figure(lang):
    t = lambda en, zh: tr(lang, en, zh)
    return intel_figure(lang, 'execution-modes', t('VMX and SEAM execution modes', 'VMX 与 SEAM 执行模式'),
        t('The right-hand SEAM region shows the TD and the TDX module, linked to the host VMM by entry, exit and SEAMCALL paths.',
          '右侧 SEAM 区域包含 TD 与 TDX 模块，并展示与宿主 VMM 之间的进入、退出和 SEAMCALL 路径。'),
        t('Start at the Host VMM in the middle and follow SEAMCALL into the module. Then trace the guest-side function from the TD on the upper right.',
          '从中部 Host VMM 沿 SEAMCALL 进入模块，再从右上角的 TD 沿 Guest-side Function 进入模块。'))


def tdx_ept_figure(lang):
    t = lambda en, zh: tr(lang, en, zh)
    return intel_figure(lang, 'secure-ept', t('Secure EPT and shared EPT', 'Secure EPT 与共享 EPT'),
        t('The GPA shared bit selects shared or secure extended page tables. The two paths use different memory encryption keys.',
          'GPA 的共享位决定使用共享 EPT 还是 Secure EPT。两条路径使用不同的内存加密密钥。'),
        t('Follow GPA.SHARED in the lower half. Shared and private guest physical addresses use separate translation paths and map into host physical memory.',
          '沿图下半部的 GPA.SHARED 阅读。共享和私有 Guest 物理地址分别走不同的转换路径，最终映射到宿主物理内存。'))


def tdx_measurement(lang):
    t = lambda en, zh: tr(lang, en, zh)
    build = diagram_flow([
        node('TDH.MNG.INIT', t('Initialize MRTD', '初始化 MRTD')),
        arrow(), node('TDH.MEM.PAGE.ADD', t('Add an initial page and measure its GPA', '添加初始页并纳入 GPA')),
        arrow(), node('TDH.MR.EXTEND', t('Measure selected contents in 256-byte blocks', '按 256 字节块纳入选定内容')),
        arrow(), node('TDH.MR.FINALIZE', t('Finalize MRTD', '完成 MRTD'), 'protected'),
    ])
    build_flow = frame(lang, 'td-build-measurement', t('Build-time measurement', '构建期度量'), build,
        t('The VMM repeats page addition and extension as needed. Initial TD firmware commonly contributes to this SHA-384 digest.',
          'VMM 按需重复添加页面和扩展操作。初始 TD 固件通常纳入这份 SHA-384 摘要。'),
        BASE[2] + '#page=145', t('Intel TDX Base Architecture §12.2.1', 'Intel TDX 基础架构 §12.2.1'))
    reporting = intel_figure(lang, 'measurement', t('From module and TD measurements to TDREPORT', '模块与 TD 度量如何进入 TDREPORT'),
        t('TEE_TCB_INFO and TDINFO_STRUCT are separately hashed into REPORTMACSTRUCT, which also carries REPORTDATA and a MAC.',
          'TEE_TCB_INFO 和 TDINFO_STRUCT 分别计算摘要并写入 REPORTMACSTRUCT，后者还包含 REPORTDATA 和 MAC。'),
        t('Figure 12.1 covers report structure versions 0, 1 and 3. Follow MRSEAM at the top and MRTD and RTMRs below it. REPORTDATA comes from the guest caller.',
          '图 12.1 对应报告结构版本 0、1 和 3。先看上方的 MRSEAM，再看下方的 MRTD 与 RTMR。REPORTDATA 由 Guest 调用者提供。'))
    fields = table(t(('Field', 'How to read it'), ('字段', '含义')), [
        ('<code>MRSEAM</code>', t('Identity measurement of the loaded TDX module in TEE_TCB_INFO.', 'TEE_TCB_INFO 中已加载的 TDX 模块身份度量。')),
        ('<code>MRTD</code>', t('Build digest over the recorded initial TD layout and explicitly extended contents.', '记录初始 TD 布局和显式纳入度量的内容。')),
        ('<code>RTMR[0..3]</code>', t('Four SHA-384 registers the guest can extend via <code>TDG.MR.RTMR.EXTEND</code>. Firmware and guest software can measure boot events and record them in an event log for replay by a verifier.',
                                 '四个 SHA-384 寄存器，Guest 可通过 <code>TDG.MR.RTMR.EXTEND</code> 扩展。固件和 Guest 软件可度量启动事件，并记录事件日志供验证者重算。')),
        ('<code>REPORTDATA</code>', t('64 bytes provided by the guest when requesting a report. A protocol can use them to bind a challenge and the guest’s public key to the evidence.',
                                     'Guest 请求报告时提供的 64 字节。证明协议可用它将挑战值和 Guest 公钥绑定到证据。')),
    ])
    return '<h3 class="tdx-subhead" id="td-measurement">' + t('TD build and runtime measurements', 'TD 构建期与运行期度量') + '</h3>' + build_flow + fields + reporting


def tdx_connect(lang):
    t = lambda en, zh: tr(lang, en, zh)
    framework = intel_figure(lang, 'connect', t('Intel TDX Connect framework', 'Intel TDX Connect 框架'),
        t('A host with a TDX module, IOMMU and Root Port connects to an endpoint with a DSM and TDIs. A secure SPDM session and a Selective IDE stream cross the fabric.',
          '宿主的 TDX 模块、IOMMU 和根端口连接到包含 DSM 与 TDI 的设备端点。SPDM 安全会话和 Selective IDE 流跨越 PCIe 互连。'),
        t('Trace the dashed red SPDM session for control messages and the solid red IDE stream for protected PCIe traffic. The figure also shows two TDs with separately assigned device interfaces.',
          '红色虚线表示承载控制消息的 SPDM 会话，红色实线表示保护 PCIe 数据事务的 IDE 流。图中还展示了分别分配给两个 TD 的设备接口。'))
    protocols = table(
        t(('Layer', 'What it does', 'Where it runs'), ('层次', '解决什么问题', '在哪里执行')),
        [
            ('PCIe DOE', t('Data Object Exchange provides a mailbox for control messages.', 'Data Object Exchange 为控制消息提供邮箱。'),
             t('PCIe configuration space. The VMM can relay mailbox traffic.', '位于 PCIe 配置空间。VMM 可转发邮箱消息。')),
            ('DMTF SPDM', t('Authenticates the device, retrieves measurements and establishes a secure session for management messages.', '认证设备身份、获取度量，并建立管理消息的安全会话。'),
             t('Between the TEE Security Manager (TSM) and the device security manager (DSM).', '会话端点是 TEE 安全管理器（TSM）和设备安全管理器（DSM）。')),
            ('PCI-SIG TDISP', t('Locks, reports, starts and stops an individual TEE Device Interface (TDI).', '锁定、查询、启动和停止单个 TEE 设备接口（TDI）。'),
             t('TSM and DSM exchange TDISP messages inside the SPDM secure session.', 'TSM 和 DSM 在 SPDM 安全会话内交换 TDISP 消息。')),
            ('PCIe IDE / IDE_KM', t('Selective IDE protects the confidentiality and integrity of PCIe transaction packets and guards against replay. IDE_KM provisions stream keys.', 'Selective IDE 保护 PCIe 事务包的机密性和完整性，并防止重放。IDE_KM 配置流密钥。'),
             t('IDE protects traffic between the Root Port and the endpoint. IDE_KM messages use the SPDM session.', 'IDE 保护根端口与设备端点之间的流量。IDE_KM 消息通过 SPDM 会话传输。')),
            ('Intel VT-d / IOMMU', t('Translates and restricts trusted DMA to the pages authorized for the assigned TDI.', '转换可信 DMA 地址，并将访问限制在该 TDI 获准访问的页面。'),
             t('The TDX module controls trusted mappings. The host manages ordinary shared I/O mappings.', 'TDX 模块控制可信映射。宿主管理普通共享 I/O 映射。')),
        ],
    )
    lifecycle = '<ol>' + ''.join(f'<li>{step}</li>' for step in [
        t('<b>Connect the physical device.</b> Establish the SPDM session and set up a Selective IDE stream. Device identity and firmware measurements are inputs to the TD’s trust decision.',
          '<b>连接物理设备。</b>建立 SPDM 会话并配置 Selective IDE 流。设备身份和固件度量供 TD 作信任判断。'),
        t('<b>Lock and inspect the function.</b> <code>LOCK_INTERFACE_REQUEST</code> freezes security-relevant configuration. <code>GET_DEVICE_INTERFACE_REPORT</code> retrieves the locked interface configuration, including its MMIO ranges. The TD evaluates that report and the SPDM evidence against its policy.',
          '<b>锁定并检查设备功能。</b><code>LOCK_INTERFACE_REQUEST</code> 锁定与安全相关的配置。<code>GET_DEVICE_INTERFACE_REPORT</code> 获取锁定后的接口配置，包括 MMIO 范围。TD 按自己的策略检查接口报告和 SPDM 证据。'),
        t('<b>Authorize trusted I/O.</b> The TD accepts the TDI and the appropriate mappings. <code>START_INTERFACE_REQUEST</code> puts the interface in <code>RUN</code>. The device can DMA to permitted TD private pages, and the TD can access the assigned device registers through trusted MMIO.',
          '<b>授权可信 I/O。</b>TD 接受 TDI 及相应映射后，<code>START_INTERFACE_REQUEST</code> 使接口进入 <code>RUN</code>。设备可 DMA 到获准的 TD 私有页，TD 可通过可信 MMIO 访问分配给它的设备寄存器。'),
        t('<b>Stop and unbind.</b> <code>STOP_INTERFACE_REQUEST</code> quiesces the interface and drains outstanding traffic. The platform revokes trusted MMIO and DMA access and invalidates cached I/O translations before reusing resources.',
          '<b>停止并解绑。</b><code>STOP_INTERFACE_REQUEST</code> 让接口停止工作并处理在途事务。平台撤销可信 MMIO 和 DMA 访问，并使缓存的 I/O 地址转换失效，再回收资源。'),
    ]) + '</ol>'
    example = '<div class="split">' + ''.join([
        '<div class="panel"><h3>' + t('Example · assign an accelerator VF', '示例 · 分配一个加速器 VF') + '</h3><p>' + t(
            'A capable SR-IOV device can expose several Virtual Functions (VFs). Each assigned TDI belongs exclusively to one TD at a time. After accepting its VF, the TD can submit work via MMIO, and the VF can DMA into authorized private buffers. The device’s firmware and isolation between functions now matter to the TD’s security.',
            '支持 SR-IOV 的设备可以提供多个虚拟功能（VF）。同一时刻，一个已分配的 TDI 只属于一个 TD。TD 接受自己的 VF 后，可通过 MMIO 提交任务，由 VF 对获准的私有缓冲区执行 DMA。设备固件与功能之间的隔离由此进入 TD 的安全边界。',
        ) + '</p></div>',
        '<div class="panel"><h3>' + t('Check the entire stack', '核对整套软硬件') + '</h3><p>' + t(
            'Check the exact server SKU and firmware, Root Port and trusted VT-d support, the TDX module, the host kernel and VMM, guest drivers, and endpoint firmware with DOE, SPDM, Selective IDE and TDISP. The VMM can still withhold or revoke a device, so availability remains under host control.',
            '逐项核对服务器 SKU 与固件、根端口与可信 VT-d、TDX 模块、宿主内核与 VMM、Guest 驱动，以及设备端是否支持 DOE、SPDM、Selective IDE 和 TDISP。VMM 仍可拒绝分配或撤下设备，设备可用性由宿主控制。',
        ) + '</p></div>',
    ]) + '</div>'
    status = '<h3>' + t('Public specification status · November 2026', '公开规范进展 · 2026 年 11 月') + '</h3><p>' + t(
        'Intel lists TEE I/O as a TDX 2.0 extension. Its September 2026 Connect ABI (2.1 V0.66) is a community review draft. In that draft, the VMM calls <code>TDH.TDI.BIND</code> via SEAMCALL, while the guest uses TDCALL leaves such as <code>TDG.TDI.RD</code> to retrieve evidence hashes and <code>TDG.TDI.START</code> to authorize the same bind instance. GHCI 2.0 describes the guest–VMM message layer. These interfaces are versioned, so check the ABI for the target stack.',
        'Intel 将 TEE I/O 列为 TDX 2.0 扩展。2026 年 9 月发布的 Connect ABI（2.1 V0.66）是社区评审稿。在该稿中，VMM 通过 SEAMCALL 调用 <code>TDH.TDI.BIND</code>，Guest 通过 TDCALL 使用 <code>TDG.TDI.RD</code> 读取证据摘要，再用 <code>TDG.TDI.START</code> 授权同一次绑定。GHCI 2.0 描述 Guest 与 VMM 的消息接口。接口随版本演进，部署时以目标平台 ABI 为准。',
    ) + '</p><p>' + t(
        'PCI-SIG also published an Extended TEE (XT) ECN for PCIe 6.3 that adds rules for IDE and Address Translation Services (ATS). Check XT separately from baseline TDISP support.',
        'PCI-SIG 还为 PCIe 6.3 发布了 Extended TEE（XT）ECN，增加了与 IDE 和地址转换服务（ATS）相关的规则。XT 支持需要在基础 TDISP 支持之外单独核对。',
    ) + '</p>'
    sources = '<div class="source-grid">' + ''.join([
        link(TDX_CONNECT_ARCH, t('Intel TDX Connect architecture', 'Intel TDX Connect 架构规范'), t('TEE I/O trust model, hardware and lifecycle', 'TEE I/O 信任模型、硬件与生命周期')),
        link(TDISP_SPEC, t('PCI-SIG TDISP', 'PCI-SIG TDISP'), t('Trusted device assignment and the TDI lifecycle', '可信设备分配与 TDI 生命周期')),
        link('https://pcisig.com/PCI%20Express/ECN/Base/IntegrityandDataEncryption', t('PCI-SIG PCIe IDE', 'PCI-SIG PCIe IDE'), t('Protection for PCIe transaction packets', 'PCIe 事务包保护')),
        link('https://www.dmtf.org/standards/spdm', t('DMTF SPDM', 'DMTF SPDM 标准'), t('Device authentication, measurements and secure messaging', '设备认证、度量和安全消息')),
        link('https://www.intel.com/content/www/us/en/developer/tools/trust-domain-extensions/documentation.html', t('Intel TDX documentation index', 'Intel TDX 文档索引'), t('Connect ABI review draft, GHCI 2.0 and device guide', 'Connect ABI 评审稿、GHCI 2.0 与设备指南')),
        link('https://cdrdv2.intel.com/v1/dl/getContent/858625', t('Intel TDX Connect ABI review draft', 'Intel TDX Connect ABI 评审稿'), t('TDH and TDG leaves in revision 2.1 V0.66', '2.1 V0.66 中的 TDH 和 TDG leaf')),
        link('https://cdrdv2.intel.com/v1/dl/getContent/858627', t('Intel GHCI 2.0', 'Intel GHCI 2.0'), t('Guest–VMM messages for trusted device assignment', '可信设备分配的 Guest 与 VMM 消息')),
        link('https://pcisig.com/PCIExpress/ECN/Base/TDISPeXtendedTEEExtensions', t('PCI-SIG Extended TEE (XT) ECN', 'PCI-SIG Extended TEE（XT）ECN'), t('PCIe 6.3 extensions to IDE, ATS and TDISP', '对 PCIe 6.3 的 IDE、ATS 与 TDISP 扩展')),
    ]) + '</div>'
    return article(t('06 / TRUSTED DEVICE I/O', '06 / 可信设备 I/O'),
                   t('TDX Connect and TDISP', 'TDX Connect 与 TDISP'),
                   t('Base TDX protects the VM’s private CPU and memory state. Conventional I/O often uses shared buffers, with software copying or encrypting sensitive data as needed. TDX Connect extends the TD’s trust boundary to a specifically accepted PCIe device function and lets it access authorized private buffers directly.',
                     '基础 TDX 保护虚拟机的私有 CPU 状态与内存。普通 I/O 常通过共享缓冲区中转，软件按需复制或加密敏感数据。TDX Connect 将 TD 的信任边界扩展到明确接受的 PCIe 设备功能，使其能直接访问获准的私有缓冲区。'),
                   framework + diagram('tdx_connect_paths', lang) + protocols + diagram('tdisp_states', lang) + lifecycle + example + status + sources,
                   'tdx-connect')


def tdx_service(lang):
    t = lambda en, zh: tr(lang, en, zh)
    binding = intel_figure(lang, 'service-binding', t('Service TD binding state machine', 'Service TD 绑定状态机'),
        t('A target TD binding slot can be not bound, pre-bound, bound, or approved for rebind.',
          '目标 TD 的绑定槽可处于未绑定、预绑定、已绑定或已授权重绑状态。'),
        t('Follow PRE_BIND from NOT_BOUND to PRE_BOUND, then BIND into BOUND. The lower path covers optional rebind support.',
          '从 NOT_BOUND 沿预绑定路径到 PRE_BOUND，再通过 BIND 进入 BOUND。下方是可选的重绑路径。'))
    details = '<ol>' + ''.join(f'<li>{step}</li>' for step in [
        t('<b>Declare the service.</b> The host can use <code>TDH.SERVTD.PREBIND</code> to record an expected service measurement, type and attributes in a slot in the target TD’s TDCS. The service instance can be attached later.',
          '<b>声明服务。</b>宿主可用 <code>TDH.SERVTD.PREBIND</code> 在目标 TD 的 TDCS 绑定槽中登记预期的服务度量、类型和属性，随后再绑定服务实例。'),
        t('<b>Bind an instance.</b> <code>TDH.SERVTD.BIND</code> checks the applicable binding parameters and returns a handle. The target’s <code>SERVTD_HASH</code> reflects the service binding configuration for attestation.',
          '<b>绑定实例。</b><code>TDH.SERVTD.BIND</code> 检查适用的绑定参数并返回句柄。目标 TD 的 <code>SERVTD_HASH</code> 将服务绑定配置纳入证明。'),
        t('<b>Access allowed fields.</b> The module checks the service instance and its binding type when it handles <code>TDG.SERVTD.RD</code> or <code>TDG.SERVTD.WR</code>. The binding authorizes selected target metadata fields.',
          '<b>访问获准字段。</b>模块处理 <code>TDG.SERVTD.RD</code> 或 <code>TDG.SERVTD.WR</code> 时检查服务实例和绑定类型。授权范围是目标 TD 的特定元数据字段。'),
    ]) + '</ol>'
    return article(t('07 / SERVICE TD', '07 / 服务 TD'), t('Bind a Service TD to a target TD', '把 Service TD 绑定到目标 TD'),
        t('A Service TD is a separate Trust Domain with a module-enforced relationship to the target. Migration TD (MigTD) is the service type described in the current base architecture.',
          'Service TD 是独立运行的 Trust Domain。它与目标 TD 的绑定关系由模块执行。当前基础架构规范描述的服务类型是 Migration TD（MigTD）。'),
        binding + details, 'service-td')


def tdx_attestation(lang):
    t = lambda en, zh: tr(lang, en, zh)
    path = diagram_flow([
        node(t('Remote verifier', '远程验证者'), t('Issues a fresh challenge', '发出新鲜挑战值')),
        arrow(), node(t('Guest TD', 'Guest TD'), t('Binds challenge to TDREPORT', '将挑战值绑定到 TDREPORT'), 'protected'),
        arrow(), node(t('Quoting component', 'Quote 生成组件'), t('Authenticates the report and signs a quote', '校验报告并签署 Quote')),
        arrow(), node(t('Remote verifier', '远程验证者'), t('Checks the quote, collateral and policy', '检查 Quote、验证材料与策略'), 'protected'),
    ])
    round_trip = frame(lang, 'tdx-remote-attestation-flow', t('The remote attestation round trip', '远程证明的往返流程'), path,
        t('The verifier checks the returned REPORTDATA against its challenge and the protocol’s binding rules.',
          '验证者根据自己发出的挑战值和协议的绑定规则核对返回的 REPORTDATA。'),
        'https://cc-enabling.trustedservices.intel.com/intel-tdx-enabling-guide/02/infrastructure_setup/', 'Intel TDX Enabling Guide')
    quote = intel_figure(lang, 'attestation', t('Intel’s SGX-based TDX quote generation path', 'Intel 基于 SGX 的 TDX Quote 生成路径'),
        t('A guest requests a MAC-protected report through the TDX module. A TD Quoting Enclave on the same platform verifies it and produces a signed quote.',
          'Guest 通过 TDX 模块生成受 MAC 保护的报告。同平台的 TD Quoting Enclave 校验报告并生成签名 Quote。'),
        t('The right side generates the report. The left side shows the TD Quoting Enclave and EVERIFYREPORT2. Remote verification happens after this figure’s signed quote leaves the platform.',
          '右侧生成报告，左侧是 TD Quoting Enclave 与 EVERIFYREPORT2。图中签名 Quote 离开平台后，才进入远程验证。'))
    verification = table(t(('Stage', 'Actor and security check'), ('阶段', '参与者与安全检查')), [
        (t('Challenge and report', '挑战与报告'), t('The attester puts a protocol-defined challenge or challenge/key digest into <code>REPORTDATA</code> and calls <code>TDG.MR.REPORT</code>. The module returns a platform-local <code>TDREPORT</code> authenticated by a hardware-backed MAC.',
                                                '证明方按协议将挑战值或挑战值与公钥的摘要放入 <code>REPORTDATA</code>，调用 <code>TDG.MR.REPORT</code>。模块返回带有硬件支持 MAC 的本地 <code>TDREPORT</code>。')),
        (t('Quote generation', '生成 Quote'), t('In the DCAP path in the figure, the guest submits its report to the host Quote Generation Service (QGS). The local TD Quoting Enclave (TDQE) verifies the report and produces an ECDSA-signed quote. The guest–host transport depends on the implementation.',
                                              '在图中的 DCAP 路径里，Guest 将报告交给宿主 Quote Generation Service（QGS）。本机 TD Quoting Enclave（TDQE）校验报告后生成 ECDSA 签名的 Quote。Guest 与宿主之间的传输方式取决于实现。')),
        (t('Remote verification', '远程验证'), t('The verifier checks the quote signature and certification chain using Intel collateral such as PCK certificates, revocation lists, TCB Info and QE Identity. It checks freshness and any key binding through <code>REPORTDATA</code>, then evaluates module TCB, TD measurements and attributes against its own policy.',
                                              '验证者使用 Intel 的 PCK 证书、撤销列表、TCB Info、QE Identity 等材料验证 Quote 签名及认证链，通过 <code>REPORTDATA</code> 检查新鲜度及公钥绑定，再按自己的策略评估模块 TCB、TD 度量及属性。')),
    ])
    sources = '<div class="source-grid tdx-sources">' + ''.join([
        link('https://cc-enabling.trustedservices.intel.com/intel-tdx-enabling-guide/02/infrastructure_setup/',
             t('Intel TDX Enabling Guide', 'Intel TDX 启用指南'), t('QGS, PCCS and attestation infrastructure', 'QGS、PCCS 与证明基础设施')),
        link(BASE[2] + '#page=149', t('Intel TDX Base Architecture §12.6', 'Intel TDX 基础架构 §12.6'),
             t('SGX-based quoting and Security Engine / Quoting TD models', '基于 SGX 的 Quote 以及 Security Engine / Quoting TD 模型')),
    ]) + '</div>'
    alternatives = '<p>' + t(
        'Intel also describes Security Engine-backed attestation and Quoting TD on supported platforms. The platform and deployment determine which quoting path and evidence format are available.',
        'Intel 也描述了由 Security Engine 支持的证明及 Quoting TD 模型。可用的 Quote 生成路径和证据格式由具体平台与部署决定。',
    ) + '</p>'
    return article(t('08 / REMOTE ATTESTATION', '08 / 远程证明'), t('From TDREPORT to a remote trust decision', '从 TDREPORT 到远程信任决策'),
        t('A local report binds TD measurements to data supplied by the guest. A quoting component produces evidence a remote verifier can authenticate and evaluate.',
          '本地报告将 TD 度量与 Guest 提供的数据绑定。Quote 生成组件将它转换为可由远端验证者认证和评估的证据。'),
        round_trip + quote + verification + alternatives + sources, 'remote-attestation')


def tdx_migration(lang):
    t = lambda en, zh: tr(lang, en, zh)
    architecture = intel_figure(lang, 'migration-architecture', t('Source and destination migration components', '源端与目的端的迁移组件'),
        t('Both platforms have a Migration TD, a TDX module and a host VMM. The Migration TDs exchange keys and the VMMs move protected migration bundles.',
          '两侧平台各有 Migration TD、TDX 模块与宿主 VMM。Migration TD 交换密钥，VMM 搬运受保护的迁移数据包。'),
        t('Follow the upper path between the two MigTDs for policy and key exchange, and the lower path between host VMMs for transport.',
          '上方连接两个 MigTD 的路径用于策略与密钥协商，下方连接两个宿主 VMM 的路径用于传输。'))
    in_order = intel_figure(lang, 'migration-in-order', t('Live export and the pause window', '在线导出与暂停窗口'),
        t('The source can run during live export. It then pauses before export of the final TD and vCPU state and issuance of the start token.',
          '源端在在线导出期间可运行，随后暂停并导出最终 TD 和 vCPU 状态，生成启动令牌。'),
        t('Compare LIVE_EXPORT with PAUSED_EXPORT. The arrows connect the ordered exports at source to the corresponding imports at destination.',
          '对照 LIVE_EXPORT 与 PAUSED_EXPORT。箭头将源端有序导出操作与目的端对应的导入操作相连。'))
    out_of_order = intel_figure(lang, 'migration-out-of-order', t('Destination commit and remaining memory import', '目的端提交与剩余内存导入'),
        t('After the start token, remaining memory may be imported out of order. Commit allows the destination to run while memory import continues.',
          '接收启动令牌后，剩余内存可乱序导入。提交后目的端可以恢复运行，同时继续导入内存。'),
        t('Read the green band at the bottom for the point at which the destination may run. IMPORT.END closes the session after import is complete.',
          '底部绿色区域标出目的端获准运行的时点。导入完成后，IMPORT.END 结束迁移会话。'))
    steps = '<ol>' + ''.join(f'<li>{step}</li>' for step in [
        t('<b>Prepare both endpoints.</b> The destination VMM creates a TD skeleton. Bound MigTDs establish trust according to migration policy, agree on a protocol version and securely transfer the ephemeral migration session keys. The modules use AES-256-GCM to protect the TD private state in transit.',
          '<b>准备两端。</b>目的端 VMM 创建 TD 骨架。绑定的 MigTD 按迁移策略建立信任，协商协议版本并安全传递临时迁移会话密钥。模块用 AES-256-GCM 保护传输中的 TD 私有状态。'),
        t('<b>Export while the source is running, then pause.</b> The modules process <code>TDH.EXPORT.*</code> and <code>TDH.IMPORT.*</code> calls for metadata and memory. Live migration can export memory while the source runs. After the source pauses, the module exports the final non-memory state and issues a start token at the end of the in-order phase.',
          '<b>源端运行时导出，再进入暂停窗口。</b>模块通过 <code>TDH.EXPORT.*</code> 和 <code>TDH.IMPORT.*</code> 处理元数据与内存。热迁移可在源端运行时导出内存。暂停后，模块导出最终非内存状态，并在有序阶段结束时发出启动令牌。'),
        t('<b>Commit and resume.</b> The destination consumes the start token. <code>TDH.IMPORT.COMMIT</code> can permit execution before all remaining memory arrives. The session state and tokens constrain when either side can run and govern whether an abort can return control to the source.',
          '<b>提交并恢复运行。</b>目的端接收并验证启动令牌。<code>TDH.IMPORT.COMMIT</code> 可在剩余内存全部到达前允许目的端运行。会话状态和令牌约束两端各自何时可运行，以及中止时能否回到源端。'),
    ]) + '</ol>'
    references = '<div class="source-grid tdx-sources">' + ''.join([
        link(MIGRATION[2], t('Intel TD Migration Architecture', 'Intel TD 迁移架构规范'), t('June 2026 baseline, session and state machines', '2026 年 6 月基线，会话与状态机')),
        link('https://cdrdv2.intel.com/v1/dl/getContent/733580', t('Intel Migration TD Design Guide', 'Intel Migration TD 设计指南'), t('MigTD software, peer trust and migration policy', 'MigTD 软件、对端信任与迁移策略')),
    ]) + '</div>'
    return article(t('09 / TD MIGRATION', '09 / TD 迁移'), t('Move a TD between two TDX platforms', '在两台 TDX 平台之间迁移 TD'),
        t('MigTD handles trust policy and key exchange. The source and destination modules protect private state during export and import. The host VMMs orchestrate the session and transport migration bundles.',
          'MigTD 负责信任策略与密钥交换，源端和目的端的模块在导出和导入时保护私有状态，宿主 VMM 负责会话编排与迁移数据包传输。'),
        architecture + steps + in_order + out_of_order + references, 'migration')


def tdx_en():
    hero = page_hero('en', 'INTEL TDX', 'A VM boundary enforced<br><em>below the hypervisor</em>', 'Follow the TDX module in SEAM, private memory translation, and the distinct calls made by a host VMM and a guest Trust Domain.')
    hardware = '<div class="detail-grid">' + ''.join([
        detail('CPU', 'Check the exact Xeon SKU', 'TDX host support begins with selected 4th Gen Intel Xeon Scalable processors and continues on selected later server platforms. Generation alone is not a support guarantee.'),
        detail('FIRMWARE', 'Initialize the platform', 'BIOS/UEFI must enable TDX and configure SEAM, SEAMRR and private KeyIDs. A compatible Intel TDX module must be loaded before the host can create TDs.'),
        detail('HOST', 'Check KVM and the VMM', 'The Linux host must initialize TDX; KVM and the VMM then provide the userspace VM creation path. Feature availability also depends on kernel and module ABI versions.'),
        detail('GUEST', 'Use a TD-aware guest', 'A TD guest handles private/shared memory transitions, accepts pages when required, and uses TDCALL for TDX module services or host-assisted operations.')
    ]) + '</div><p class="source-note">Start with Intel’s <a class="inline-link" href="https://www.intel.com/content/www/us/en/support/articles/000091103/processors/intel-xeon-processors.html">TDX processor support note</a> and the <a class="inline-link" href="https://docs.kernel.org/arch/x86/tdx.html">Linux TDX host guide</a>.</p>'
    memory = '<div class="stack">' + ''.join([
        '<div class="stack-row"><b>SEAM</b><span>Secure Arbitration Mode isolates the Intel TDX module from ordinary host software. The host enters the module through SEAMCALL; the guest uses TDCALL.</span></div>',
        '<div class="stack-row"><b>KeyIDs</b><span>TD private memory uses dedicated memory-encryption KeyIDs. A host mapping cannot simply read a private TD page as plaintext.</span></div>',
        '<div class="stack-row"><b>Secure EPT</b><span>The module manages a TD’s private guest-physical-to-host-physical mappings. Ordinary host EPT control alone cannot authorize access to private TD pages.</span></div>',
        '<div class="stack-row"><b>PAMT</b><span>Physical Address Metadata Table records TDX ownership and page type for protected physical pages, constraining host reuse or aliasing.</span></div>',
        '<div class="stack-row"><b>SHARED</b><span>Shared guest pages support VMM and device communication. They are intentionally outside the TD private-memory boundary; their contents need ordinary input validation.</span></div>'
    ]) + '</div><div class="signal" style="margin-top:20px"><strong>One useful mental trace</strong>Guest virtual address → guest page table → guest physical address → private Secure EPT mapping → protected host physical page. For a shared GPA, communication crosses back to host-controlled memory.</div>'
    calls = table(('Caller / instruction', 'Leaf or operation', 'Role in the flow'), [
        ('Host VMM · <code>SEAMCALL</code>', '<code>TDH.MNG.CREATE</code>', 'Create the TD root control structure (TDR).'),
        ('Host VMM · <code>SEAMCALL</code>', '<code>TDH.MNG.INIT</code>', 'Initialize TD-wide configuration.'),
        ('Host VMM · <code>SEAMCALL</code>', '<code>TDH.MEM.PAGE.ADD</code>', 'Add an initial private page to the TD.'),
        ('Host VMM · <code>SEAMCALL</code>', '<code>TDH.VP.ENTER</code>', 'Enter or resume a TD virtual processor.'),
        ('Guest TD · <code>TDCALL</code>', '<code>TDG.VP.INFO</code>', 'Query TD and virtual-processor information.'),
        ('Guest TD · <code>TDCALL</code>', '<code>TDG.MEM.PAGE.ACCEPT</code>', 'Accept a pending private page before use.'),
        ('Guest TD · <code>TDCALL</code>', '<code>TDG.VP.VMCALL</code>', 'Request host VMM service; often called TDVMCALL.'),
        ('Guest TD · <code>TDCALL</code>', '<code>TDG.MR.REPORT</code>', 'Generate a local TD report for the <a class="inline-link" href="#remote-attestation">quote generation flow</a>.')
    ]) + '<p class="source-note">SEAMCALL and TDCALL are CPU instructions; the TDH.* and TDG.* names are TDX module API leaves. TDVMCALL is the TDG.VP.VMCALL leaf, not a third instruction. Verify operands, status codes and version-specific behavior in Intel’s <a class="inline-link" href="https://cdrdv2-public.intel.com/853289/intel-tdx-module-abi-spec-348551006.pdf">TDX module ABI specification</a>.</p>'
    flow = '<div class="stack">' + ''.join([
        '<div class="stack-row"><b>PREPARE</b><span>Firmware enables TDX. After <a class="inline-link" href="#platform-boot">module installation and initialization</a>, Linux exposes KVM capabilities.</span></div>',
        '<div class="stack-row"><b>BUILD</b><span>VMM issues KVM TDX ioctls; KVM uses SEAMCALL leaves to create the TD, add initial memory, create vCPUs and finalize the initial image.</span></div>',
        '<div class="stack-row"><b>RUN</b><span>Host uses TDH.VP.ENTER; guest code runs privately and may call TDG.MEM.PAGE.ACCEPT or TDG.VP.INFO through TDCALL.</span></div>',
        '<div class="stack-row"><b>EXIT</b><span>TD exit returns control to the host for permitted handling. TDG.VP.VMCALL explicitly asks for a host service; a virtualization exception (#VE) can instead be handled within the guest.</span></div>'
    ]) + '</div><p class="source-note">The <a class="inline-link" href="https://docs.kernel.org/virt/kvm/x86/intel-tdx.html">Linux KVM TDX guide</a> documents the userspace ioctl layer; it is distinct from the SEAMCALL ABI.</p>'
    boundary = '<div class="split"><div class="panel"><h3>Private TD state</h3><p>CPU, module and memory metadata protect private guest pages and TD state from direct host access. The host still controls scheduling and supplies virtual devices.</p></div><div class="panel"><h3>Shared boundary</h3><p>Guest-shared pages, emulated I/O and VMM responses are untrusted inputs. TDX does not by itself guarantee availability or eliminate timing and microarchitectural side channels.</p></div></div>'
    return (
        hero
        + tdx_overview('en')
        + article('01 / PLATFORM SUPPORT', 'A chain of hardware and software prerequisites', 'Confirm the actual processor, firmware settings, TDX module, host KVM and guest capabilities separately.', hardware + tdx_startup('en'), 'hardware')
        + article('02 / MEMORY MODEL', 'How private pages remain private', 'SEAM, KeyIDs, Secure EPT and PAMT work together. Shared pages are an explicit exception.', diagram('tdx_memory', 'en') + memory + tdx_ept_figure('en'), 'memory')
        + article('03 / CALL MAP', 'Separate host SEAMCALL from guest TDCALL', 'The leaf name tells you which side requested the operation and what state transition it needs.', diagram('tdx_calls', 'en') + calls + tdx_mode_figure('en'), 'calls')
        + article('04 / LIFECYCLE', 'Build, enter, run and exit a TD', 'Keep the userspace KVM interface, module ABI and guest interface as three layers.', flow + tdx_measurement('en'), 'flow')
        + article('05 / SECURITY BOUNDARY', 'What the VMM still controls', 'Read the private/shared split before placing secrets or trusting virtual devices.', boundary)
        + tdx_connect('en')
        + tdx_service('en')
        + tdx_attestation('en')
        + tdx_migration('en')
    )


def tdx_zh():
    hero = page_hero('zh', 'INTEL TDX', '在 Hypervisor 之下<br><em>建立虚拟机边界</em>', '跟随 SEAM 中的 TDX 模块、私有内存地址转换，以及宿主 VMM 与 Guest Trust Domain 各自发出的调用。')
    hardware = '<div class="detail-grid">' + ''.join([
        detail('CPU', '核对 Xeon 具体 SKU', '宿主 TDX 支持始于部分第 4 代 Intel Xeon Scalable 处理器，并延续到部分更新的服务器平台；仅凭代际不能确定支持。'),
        detail('固件', '初始化平台', 'BIOS/UEFI 需要启用 TDX，配置 SEAM、SEAMRR 与私有 KeyID。宿主创建 TD 前须加载兼容的 Intel TDX 模块。'),
        detail('宿主', '检查 KVM 与 VMM', 'Linux 宿主须初始化 TDX；KVM 与 VMM 再提供用户态创建虚拟机的路径。功能还取决于内核及模块 ABI 版本。'),
        detail('Guest', '使用 TD 感知的系统', 'TD Guest 处理私有/共享内存转换，在需要时接受页面，并以 TDCALL 请求模块服务或宿主协助。')
    ]) + '</div><p class="source-note">先看 Intel 的 <a class="inline-link" href="https://www.intel.com/content/www/us/en/support/articles/000091103/processors/intel-xeon-processors.html">TDX 处理器支持说明</a>和 <a class="inline-link" href="https://docs.kernel.org/arch/x86/tdx.html">Linux TDX 宿主指南</a>。</p>'
    memory = '<div class="stack">' + ''.join([
        '<div class="stack-row"><b>SEAM</b><span>Secure Arbitration Mode 把 Intel TDX 模块与普通宿主软件隔离。宿主通过 SEAMCALL 进入模块；Guest 使用 TDCALL。</span></div>',
        '<div class="stack-row"><b>KeyID</b><span>TD 私有内存使用专用的内存加密 KeyID。宿主映射不能直接把私有 TD 页面读成明文。</span></div>',
        '<div class="stack-row"><b>Secure EPT</b><span>模块管理 TD 私有的 Guest 物理地址到宿主物理地址映射。仅控制普通宿主 EPT 不足以授权访问私有页。</span></div>',
        '<div class="stack-row"><b>PAMT</b><span>Physical Address Metadata Table 记录受保护物理页的 TDX 所有权和类型，限制宿主复用或别名映射。</span></div>',
        '<div class="stack-row"><b>共享页</b><span>Guest 共享页用于 VMM 和设备通信，明确处于 TD 私有内存边界之外；其内容仍需作为不可信输入校验。</span></div>'
    ]) + '</div><div class="signal" style="margin-top:20px"><strong>追踪一次地址访问</strong>Guest 虚拟地址 → Guest 页表 → Guest 物理地址 → 私有 Secure EPT 映射 → 受保护的宿主物理页。若 GPA 标记为共享，则通信回到宿主可控内存。</div>'
    calls = table(('调用者 / 指令', 'Leaf 或操作', '在路径中的作用'), [
        ('宿主 VMM · <code>SEAMCALL</code>', '<code>TDH.MNG.CREATE</code>', '创建 TD 根控制结构 TDR。'),
        ('宿主 VMM · <code>SEAMCALL</code>', '<code>TDH.MNG.INIT</code>', '初始化 TD 级配置。'),
        ('宿主 VMM · <code>SEAMCALL</code>', '<code>TDH.MEM.PAGE.ADD</code>', '为 TD 增加初始私有页面。'),
        ('宿主 VMM · <code>SEAMCALL</code>', '<code>TDH.VP.ENTER</code>', '进入或恢复 TD 虚拟处理器。'),
        ('Guest TD · <code>TDCALL</code>', '<code>TDG.VP.INFO</code>', '查询 TD 与虚拟处理器信息。'),
        ('Guest TD · <code>TDCALL</code>', '<code>TDG.MEM.PAGE.ACCEPT</code>', '使用前接受待确认的私有页。'),
        ('Guest TD · <code>TDCALL</code>', '<code>TDG.VP.VMCALL</code>', '请求宿主 VMM 服务，常称 TDVMCALL。'),
        ('Guest TD · <code>TDCALL</code>', '<code>TDG.MR.REPORT</code>', '生成供<a class="inline-link" href="#remote-attestation">后续 Quote 流程</a>使用的本地 TD 报告。')
    ]) + '<p class="source-note">SEAMCALL 和 TDCALL 是 CPU 指令；TDH.* 与 TDG.* 是 TDX 模块 API 的 leaf。TDVMCALL 是 TDG.VP.VMCALL leaf，不是第三条指令。操作数、状态码和版本差异请查 Intel <a class="inline-link" href="https://cdrdv2-public.intel.com/853289/intel-tdx-module-abi-spec-348551006.pdf">TDX 模块 ABI 规范</a>。</p>'
    flow = '<div class="stack">' + ''.join([
        '<div class="stack-row"><b>准备</b><span>固件启用 TDX。<a class="inline-link" href="#platform-boot">安装并初始化模块</a>后，Linux 宿主提供 KVM 能力。</span></div>',
        '<div class="stack-row"><b>构建</b><span>VMM 发出 KVM TDX ioctl；KVM 用 SEAMCALL leaf 创建 TD、添加初始内存和 vCPU，并完成初始镜像。</span></div>',
        '<div class="stack-row"><b>运行</b><span>宿主用 TDH.VP.ENTER；Guest 私有执行，并可通过 TDCALL 调用 TDG.MEM.PAGE.ACCEPT 或 TDG.VP.INFO。</span></div>',
        '<div class="stack-row"><b>退出</b><span>TD exit 把控制权交还宿主处理允许的事件。TDG.VP.VMCALL 显式请求宿主服务；虚拟化异常 #VE 则可由 Guest 内部处理。</span></div>'
    ]) + '</div><p class="source-note"><a class="inline-link" href="https://docs.kernel.org/virt/kvm/x86/intel-tdx.html">Linux KVM TDX 指南</a>记录用户态 ioctl 层，它与 SEAMCALL ABI 不是同一层。</p>'
    boundary = '<div class="split"><div class="panel"><h3>TD 私有状态</h3><p>CPU、模块和内存元数据阻止宿主直接访问私有 Guest 页面及 TD 状态。宿主仍控制调度，并提供虚拟设备。</p></div><div class="panel"><h3>共享边界</h3><p>Guest 共享页、模拟 I/O 与 VMM 响应都是不可信输入。TDX 本身不保证可用性，也不会消除时序和微架构侧信道。</p></div></div>'
    return (
        hero
        + tdx_overview('zh')
        + article('01 / 平台支持', '硬件与软件缺一不可', '分别确认具体处理器、固件设置、TDX 模块、宿主 KVM 与 Guest 能力。', hardware + tdx_startup('zh'), 'hardware')
        + article('02 / 内存模型', '私有页如何保持私有', 'SEAM、KeyID、Secure EPT 和 PAMT 协同工作；共享页是明确的例外。', diagram('tdx_memory', 'zh') + memory + tdx_ept_figure('zh'), 'memory')
        + article('03 / 调用地图', '分清宿主 SEAMCALL 与 Guest TDCALL', '从 leaf 名称即可看出请求来自哪一方，以及需要哪种状态转换。', diagram('tdx_calls', 'zh') + calls + tdx_mode_figure('zh'), 'calls')
        + article('04 / 生命周期', '构建、进入、运行与退出 TD', '把用户态 KVM 接口、模块 ABI 和 Guest 接口视为三个不同层次。', flow + tdx_measurement('zh'), 'flow')
        + article('05 / 安全边界', 'VMM 仍控制什么', '放置秘密或信任虚拟设备前，先读懂私有/共享边界。', boundary)
        + tdx_connect('zh')
        + tdx_service('zh')
        + tdx_attestation('zh')
        + tdx_migration('zh')
    )


def labs_en():
    hero = page_hero('en', 'LABS & SOURCES', 'Check the platform.<br><em>Trace the real calls.</em>', 'Short exercises for readers who already know x86 and virtualization. Hardware is useful, but source-level tracing works without an SGX or TDX machine.')
    checks = table(('Layer', 'Check', 'Interpretation'), [
        ('SGX CPU', '<code>grep -m1 -o "sgx" /proc/cpuinfo</code>', 'A visible flag is a lead; confirm CPUID capabilities, firmware and EPC size.'),
        ('SGX Linux', '<code>ls -l /dev/sgx_enclave</code>', 'The enclave driver is present; permissions and a working sample still matter.'),
        ('TDX host', '<code>dmesg | grep -i "virt/tdx"</code>', 'Kernel initialization messages help distinguish disabled firmware or a module failure; dmesg may need privilege.'),
        ('TDX host', '<code>cat /sys/devices/faux/tdx_host/version</code>', 'Read the module version if this sysfs path exists on the running kernel.'),
        ('TDX guest', '<code>ls -l /dev/tdx-guest</code>', 'The guest device supports TD report requests; it does not by itself prove a remote verifier accepts the TD.')
    ]) + '<p class="source-note">Run only the commands relevant to your machine. No device node or CPU flag alone establishes end-to-end support.</p>'
    exercises = '<div class="route">' + ''.join([
        route('01', 'Trace an SGX enclave build', 'Read Linux SGX documentation and the Intel lifecycle guide. Sketch which step uses ECREATE, EADD, EEXTEND and EINIT, then map EENTER and AEX.', 'sgx.html#instructions', 'Review instruction map'),
        route('02', 'Separate TDX’s three APIs', 'Read the KVM TDX userspace flow, then the module ABI. Label each operation KVM ioctl, host SEAMCALL or guest TDCALL.', 'tdx.html#calls', 'Review call map'),
        route('03', 'Draw one private and one shared page', 'For each page, write who controls the mapping, which metadata applies, and which data the host can observe.', 'tdx.html#memory', 'Review memory model'),
        route('04', 'Build a support matrix', 'Record exact CPU SKU, firmware revision/settings, kernel, module ABI, guest OS and VMM version. Treat unsupported or unverified entries as unknown.', 'labs.html#sources', 'Open documentation')
    ]) + '</div>'
    sources = '<div class="sources">' + ''.join([
        link('https://www.intel.com/content/www/us/en/architecture-and-technology/software-guard-extensions-processors.html', 'Intel SGX processor support', 'Processor and SKU checks.'),
        link('https://docs.kernel.org/arch/x86/sgx.html', 'Linux SGX guide', 'EPC, driver interface and enclave creation.'),
        link('https://www.intel.com/content/www/us/en/developer/articles/technical/overview-of-an-intel-software-guard-extensions-enclave-life-cycle.html', 'Intel SGX enclave lifecycle', 'Instruction sequence and state transitions.'),
        link('https://www.intel.com/content/dam/develop/external/us/en/documents/329298-002-629101.pdf', 'Intel SGX programming reference', 'Detailed instruction behavior.'),
        link('https://www.intel.com/content/www/us/en/developer/tools/trust-domain-extensions/documentation.html', 'Intel TDX documentation hub', 'Current architecture and ABI documents.'),
        link('https://cdrdv2-public.intel.com/853289/intel-tdx-module-abi-spec-348551006.pdf', 'Intel TDX module ABI', 'SEAMCALL and TDCALL leaves.'),
        link('https://docs.kernel.org/arch/x86/tdx.html', 'Linux TDX host guide', 'Host requirements and initialization.'),
        link('https://docs.kernel.org/virt/kvm/x86/intel-tdx.html', 'Linux KVM TDX guide', 'VMM and KVM creation flow.'),
        link('https://docs.kernel.org/virt/coco/tdx-guest.html', 'Linux TDX guest guide', 'Guest kernel and report device.'),
        link('https://www.intel.com/content/www/us/en/support/articles/000091103/processors/intel-xeon-processors.html', 'Intel TDX processor support', 'Host processor families and caveats.')
    ]) + '</div><p class="source-note">Source list reviewed 30 September 2026. ABI and processor support change; use the version that matches your hardware and software.</p>'
    return hero + article('01 / HARDWARE', 'Verify more than a CPU flag', 'Treat each command as one piece of evidence, not a complete readiness verdict.', checks, 'hardware') + article('02 / SOURCE EXERCISES', 'Learn the mechanics without special hardware', 'Each exercise has a concrete architecture question and a primary-source answer path.', exercises, 'exercises') + article('03 / PRIMARY SOURCES', 'Read the manuals behind the diagrams', 'Intel specifications and Linux documentation take precedence over generalized summaries.', sources, 'sources')


def labs_zh():
    hero = page_hero('zh', '实验与资料', '核对平台<br><em>追踪真实调用</em>', '为已有 x86 与虚拟化基础的读者准备的短练习。有硬件更好；没有 SGX/TDX 机器也能通过源码追踪学习。')
    checks = table(('层次', '检查', '如何理解'), [
        ('SGX CPU', '<code>grep -m1 -o "sgx" /proc/cpuinfo</code>', '出现 flag 只是线索；继续核对 CPUID 能力、固件和 EPC 大小。'),
        ('SGX Linux', '<code>ls -l /dev/sgx_enclave</code>', '说明 enclave 驱动存在；还要检查权限并运行样例。'),
        ('TDX 宿主', '<code>dmesg | grep -i "virt/tdx"</code>', '内核初始化日志可帮助区分固件关闭与模块故障；dmesg 可能需要权限。'),
        ('TDX 宿主', '<code>cat /sys/devices/faux/tdx_host/version</code>', '若当前内核存在该 sysfs 路径，可读取模块版本。'),
        ('TDX Guest', '<code>ls -l /dev/tdx-guest</code>', 'Guest 设备支持请求 TD report；它本身不证明远端验证者接受该 TD。')
    ]) + '<p class="source-note">只在适用机器上运行相应命令。单个设备节点或 CPU flag 都不足以证明端到端可用。</p>'
    exercises = '<div class="route">' + ''.join([
        route('01', '追踪 SGX enclave 构建', '阅读 Linux SGX 文档和 Intel 生命周期导读，标出 ECREATE、EADD、EEXTEND、EINIT 对应步骤，再定位 EENTER 与 AEX。', 'sgx.zh.html#instructions', '查看指令地图'),
        route('02', '分清 TDX 的三层 API', '先读 KVM TDX 用户态流程，再读模块 ABI。把每个操作标成 KVM ioctl、宿主 SEAMCALL 或 Guest TDCALL。', 'tdx.zh.html#calls', '查看调用地图'),
        route('03', '各画一张私有页与共享页', '分别写出谁控制映射、有哪些元数据、宿主能观察到什么。', 'tdx.zh.html#memory', '查看内存模型'),
        route('04', '制作支持矩阵', '记录准确 CPU SKU、固件版本与设置、内核、模块 ABI、Guest OS 与 VMM 版本。未验证的格子标为未知。', 'labs.zh.html#sources', '打开文档')
    ]) + '</div>'
    sources = '<div class="sources">' + ''.join([
        link('https://www.intel.com/content/www/us/en/architecture-and-technology/software-guard-extensions-processors.html', 'Intel SGX 处理器支持', '检查处理器与 SKU。'),
        link('https://docs.kernel.org/arch/x86/sgx.html', 'Linux SGX 指南', 'EPC、驱动接口与 enclave 创建。'),
        link('https://www.intel.com/content/www/us/en/developer/articles/technical/overview-of-an-intel-software-guard-extensions-enclave-life-cycle.html', 'Intel SGX enclave 生命周期', '指令顺序与状态转换。'),
        link('https://www.intel.com/content/dam/develop/external/us/en/documents/329298-002-629101.pdf', 'Intel SGX 编程参考', '指令行为细节。'),
        link('https://www.intel.com/content/www/us/en/developer/tools/trust-domain-extensions/documentation.html', 'Intel TDX 文档中心', '最新架构与 ABI 文档。'),
        link('https://cdrdv2-public.intel.com/853289/intel-tdx-module-abi-spec-348551006.pdf', 'Intel TDX 模块 ABI', 'SEAMCALL 与 TDCALL leaf。'),
        link('https://docs.kernel.org/arch/x86/tdx.html', 'Linux TDX 宿主指南', '宿主前提与初始化。'),
        link('https://docs.kernel.org/virt/kvm/x86/intel-tdx.html', 'Linux KVM TDX 指南', 'VMM 与 KVM 创建流程。'),
        link('https://docs.kernel.org/virt/coco/tdx-guest.html', 'Linux TDX Guest 指南', 'Guest 内核与 report 设备。'),
        link('https://www.intel.com/content/www/us/en/support/articles/000091103/processors/intel-xeon-processors.html', 'Intel TDX 处理器支持', '宿主处理器家族及限制。')
    ]) + '</div><p class="source-note">资料清单复核于 2026 年 9 月 30 日。ABI 与处理器支持会变化，应以匹配当前硬件和软件的版本为准。</p>'
    return hero + article('01 / 硬件', '不只看 CPU flag', '每条命令只是一份证据，不是完整的可用性结论。', checks, 'hardware') + article('02 / 源码练习', '无需专用硬件也能学机制', '每个练习都有具体架构问题，以及从一手资料寻找答案的路径。', exercises, 'exercises') + article('03 / 一手资料', '回到图示背后的手册', '具体细节以 Intel 规范和 Linux 文档为准。', sources, 'sources')


if __name__ == '__main__':
    for name in PAGES:
        for language in ('en', 'zh'):
            body = globals()[f'{name}_{language}']()
            filename = f'{name}{".zh" if language == "zh" else ""}.html'
            (ROOT / filename).write_text(shell(language, name, body), encoding='utf-8')
            print(filename)
