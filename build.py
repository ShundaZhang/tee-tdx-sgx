"""Build the static bilingual TEE / TDX / SGX atlas (stdlib only)."""
from pathlib import Path

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
<html lang="{'zh-CN' if zh else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#101b2a"><meta name="description" content="{DESCRIPTIONS[lang]}"><title>{TITLES[lang][idx]} · ShundaZhang</title><link rel="stylesheet" href="style.css"><script src="language.js"></script></head>
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
    brief = '<div class="signal"><strong>Remote attestation in one paragraph</strong>SGX and TDX can produce measured reports and remote quotes. A remote verifier checks evidence against a policy before an application trusts the environment. This site introduces those instructions only; quote formats, certificate chains and key release deserve a separate attestation study.</div>'
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
    brief = '<div class="signal"><strong>用一段话定位远程证明</strong>SGX 与 TDX 可产生带测量信息的 report 和远程 quote；远端验证者按策略检查证据，应用才决定是否信任该环境。本站只介绍相关指令的作用。Quote 格式、证书链与密钥释放将留给独立的远程证明专题。</div>'
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
    return hero + article('01 / PLATFORM SUPPORT', 'First verify hardware and firmware', '“This CPU family supports SGX” does not prove the particular machine exposes a usable enclave facility.', hardware, 'hardware') + article('02 / MEMORY MODEL', 'Four structures to keep in view', 'Follow one page from ordinary memory into EPC and through CPU metadata checks.', memory, 'memory') + article('03 / INSTRUCTION MAP', 'Read the lifecycle as ENCLS and ENCLU', 'Do not memorize opcodes first. Group the leaves by who executes them and which state transition they make.', instructions, 'instructions') + article('04 / EXECUTION TRACE', 'One enclave from creation to interruption', 'AEX and resumption are especially important when reasoning about interrupts and untrusted scheduling.', flow, 'flow') + article('05 / SECURITY BOUNDARY', 'What isolation still leaves to software', 'The enclave protects direct access to its pages; its host interface and side-channel behavior are separate design work.', boundary)


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
    return hero + article('01 / 平台支持', '先确认硬件与固件', '“这个 CPU 家族支持 SGX”并不证明眼前的机器提供可用的 enclave 功能。', hardware, 'hardware') + article('02 / 内存模型', '记住四个关键结构', '跟随一个页面从普通内存进入 EPC，并经过 CPU 元数据检查。', memory, 'memory') + article('03 / 指令地图', '按 ENCLS 与 ENCLU 读生命周期', '先按执行者和状态变化分组，再去记操作码。', instructions, 'instructions') + article('04 / 执行路径', '从创建到中断的一次运行', 'AEX 与恢复是理解中断和不可信调度的关键。', flow, 'flow') + article('05 / 安全边界', '隔离仍留给软件的问题', 'Enclave 阻止页面被直接读取；宿主接口和侧信道行为仍需单独设计。', boundary)


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
        ('Guest TD · <code>TDCALL</code>', '<code>TDG.MR.REPORT</code>', 'Generate a local TD report; remote attestation is covered only briefly here.')
    ]) + '<p class="source-note">SEAMCALL and TDCALL are CPU instructions; the TDH.* and TDG.* names are TDX module API leaves. TDVMCALL is the TDG.VP.VMCALL leaf, not a third instruction. Verify operands, status codes and version-specific behavior in Intel’s <a class="inline-link" href="https://cdrdv2-public.intel.com/853289/intel-tdx-module-abi-spec-348551006.pdf">TDX module ABI specification</a>.</p>'
    flow = '<div class="stack">' + ''.join([
        '<div class="stack-row"><b>PREPARE</b><span>Firmware enables TDX and loads the module; the Linux host initializes it and exposes KVM capabilities.</span></div>',
        '<div class="stack-row"><b>BUILD</b><span>VMM issues KVM TDX ioctls; KVM uses SEAMCALL leaves to create the TD, add initial memory, create vCPUs and finalize the initial image.</span></div>',
        '<div class="stack-row"><b>RUN</b><span>Host uses TDH.VP.ENTER; guest code runs privately and may call TDG.MEM.PAGE.ACCEPT or TDG.VP.INFO through TDCALL.</span></div>',
        '<div class="stack-row"><b>EXIT</b><span>TD exit returns control to the host for permitted handling. TDG.VP.VMCALL explicitly asks for a host service; a virtualization exception (#VE) can instead be handled within the guest.</span></div>'
    ]) + '</div><p class="source-note">The <a class="inline-link" href="https://docs.kernel.org/virt/kvm/x86/intel-tdx.html">Linux KVM TDX guide</a> documents the userspace ioctl layer; it is distinct from the SEAMCALL ABI.</p>'
    boundary = '<div class="split"><div class="panel"><h3>Private TD state</h3><p>CPU, module and memory metadata protect private guest pages and TD state from direct host access. The host still controls scheduling and supplies virtual devices.</p></div><div class="panel"><h3>Shared boundary</h3><p>Guest-shared pages, emulated I/O and VMM responses are untrusted inputs. TDX does not by itself guarantee availability or eliminate timing and microarchitectural side channels.</p></div></div>'
    return hero + article('01 / PLATFORM SUPPORT', 'A chain of hardware and software prerequisites', 'Confirm the actual processor, firmware settings, TDX module, host KVM and guest capabilities separately.', hardware, 'hardware') + article('02 / MEMORY MODEL', 'How private pages remain private', 'SEAM, KeyIDs, Secure EPT and PAMT work together. Shared pages are an explicit exception.', memory, 'memory') + article('03 / CALL MAP', 'Separate host SEAMCALL from guest TDCALL', 'The leaf name tells you which side requested the operation and what state transition it needs.', calls, 'calls') + article('04 / LIFECYCLE', 'Build, enter, run and exit a TD', 'Keep the userspace KVM interface, module ABI and guest interface as three layers.', flow, 'flow') + article('05 / SECURITY BOUNDARY', 'What the VMM still controls', 'Read the private/shared split before placing secrets or trusting virtual devices.', boundary)


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
        ('Guest TD · <code>TDCALL</code>', '<code>TDG.MR.REPORT</code>', '生成本地 TD report；这里仅简要涉及远程证明。')
    ]) + '<p class="source-note">SEAMCALL 和 TDCALL 是 CPU 指令；TDH.* 与 TDG.* 是 TDX 模块 API 的 leaf。TDVMCALL 是 TDG.VP.VMCALL leaf，不是第三条指令。操作数、状态码和版本差异请查 Intel <a class="inline-link" href="https://cdrdv2-public.intel.com/853289/intel-tdx-module-abi-spec-348551006.pdf">TDX 模块 ABI 规范</a>。</p>'
    flow = '<div class="stack">' + ''.join([
        '<div class="stack-row"><b>准备</b><span>固件启用 TDX 并加载模块；Linux 宿主初始化模块，暴露 KVM 能力。</span></div>',
        '<div class="stack-row"><b>构建</b><span>VMM 发出 KVM TDX ioctl；KVM 用 SEAMCALL leaf 创建 TD、添加初始内存和 vCPU，并完成初始镜像。</span></div>',
        '<div class="stack-row"><b>运行</b><span>宿主用 TDH.VP.ENTER；Guest 私有执行，并可通过 TDCALL 调用 TDG.MEM.PAGE.ACCEPT 或 TDG.VP.INFO。</span></div>',
        '<div class="stack-row"><b>退出</b><span>TD exit 把控制权交还宿主处理允许的事件。TDG.VP.VMCALL 显式请求宿主服务；虚拟化异常 #VE 则可由 Guest 内部处理。</span></div>'
    ]) + '</div><p class="source-note"><a class="inline-link" href="https://docs.kernel.org/virt/kvm/x86/intel-tdx.html">Linux KVM TDX 指南</a>记录用户态 ioctl 层，它与 SEAMCALL ABI 不是同一层。</p>'
    boundary = '<div class="split"><div class="panel"><h3>TD 私有状态</h3><p>CPU、模块和内存元数据阻止宿主直接访问私有 Guest 页面及 TD 状态。宿主仍控制调度，并提供虚拟设备。</p></div><div class="panel"><h3>共享边界</h3><p>Guest 共享页、模拟 I/O 与 VMM 响应都是不可信输入。TDX 本身不保证可用性，也不会消除时序和微架构侧信道。</p></div></div>'
    return hero + article('01 / 平台支持', '硬件与软件缺一不可', '分别确认具体处理器、固件设置、TDX 模块、宿主 KVM 与 Guest 能力。', hardware, 'hardware') + article('02 / 内存模型', '私有页如何保持私有', 'SEAM、KeyID、Secure EPT 和 PAMT 协同工作；共享页是明确的例外。', memory, 'memory') + article('03 / 调用地图', '分清宿主 SEAMCALL 与 Guest TDCALL', '从 leaf 名称即可看出请求来自哪一方，以及需要哪种状态转换。', calls, 'calls') + article('04 / 生命周期', '构建、进入、运行与退出 TD', '把用户态 KVM 接口、模块 ABI 和 Guest 接口视为三个不同层次。', flow, 'flow') + article('05 / 安全边界', 'VMM 仍控制什么', '放置秘密或信任虚拟设备前，先读懂私有/共享边界。', boundary)


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
