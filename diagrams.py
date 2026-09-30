"""Bilingual architecture diagrams for SGX and TDX."""
from diagram_core import tr, node, arrow, frame, flow

def sgx_memory(lang):
    t = lambda en, zh: tr(lang, en, zh)
    host = '<div class="viz-zone outside"><span class="viz-zone-label">' + t('UNTRUSTED OS / HOST PROCESS', '不可信 OS / 宿主进程') + '</span>'
    host += '<div class="viz-two">' + node(t('Ordinary process memory', '普通进程内存'), t('Inputs, buffers and host code', '输入、缓冲区与宿主代码'), 'outside')
    host += '<div class="viz-zone protected"><span class="viz-zone-label">' + t('ENCLAVE · CPU ACCESS BOUNDARY', 'ENCLAVE · CPU 访问边界') + '</span>'
    host += node(t('Code + secrets', '代码与秘密'), t('Live enclave code/data backed by EPC', '运行中的 enclave 代码/数据由 EPC 承载'), 'protected')
    host += '<div class="viz-chips"><span>SECS · ' + t('enclave state', 'enclave 状态') + '</span><span>TCS · ' + t('thread entry', '线程入口') + '</span></div></div></div>'
    host += '<div class="viz-strip">' + t('The host supplies inputs and scheduling; it cannot directly read live private pages', '宿主提供输入并控制调度；不能直接读取运行中的私有页面') + '</div></div>'
    path = flow([node(t('Virtual address', '虚拟地址'), tone='neutral'), arrow(), node(t('x86 page-table checks', 'x86 页表检查'), t('OS-managed mapping', 'OS 管理映射')), arrow('+'), node(t('EPCM checks', 'EPCM 检查'), t('Owner · type · permissions', '所有者 · 类型 · 权限'), 'protected'), arrow(), node(t('EPC page', 'EPC 页面'), t('Access only if both checks permit', '两层检查都允许才能访问'), 'protected')])
    return frame(lang, 'sgx-boundary-diagram', t('The OS maps pages; the CPU enforces the enclave boundary', 'OS 映射页面，CPU 执行 enclave 边界'), host + path, t('Conceptual view: SECS and TCS are EPC page types; EPCM is CPU metadata, not another OS page table. An enclave may access outside memory, but must validate it.', '概念图：SECS 与 TCS 是 EPC 页面类型；EPCM 是 CPU 元数据，并非另一张 OS 页表。Enclave 可访问外部内存，但须校验其内容。'), 'https://docs.kernel.org/arch/x86/sgx.html', 'Linux SGX')


def sgx_execution(lang):
    t = lambda en, zh: tr(lang, en, zh)
    build = '<div class="viz-lane"><span class="viz-lane-label">ENCLS · ' + t('privileged build', '特权构建') + '</span>'
    build += flow([node('ECREATE', 'SECS'), arrow(), node('EADD / EEXTEND', t('Add pages / measure content', '添加页面 / 度量内容')), arrow(), node('EINIT', t('Finalize initialization', '完成初始化'), 'protected')]) + '</div>'
    run = '<div class="viz-lane"><span class="viz-lane-label">ENCLU · ' + t('normal entry and exit', '正常进入与退出') + '</span>'
    run += flow([node(t('Host thread', '宿主线程'), tone='outside'), arrow('EENTER'), node(t('Enclave runs', 'Enclave 执行'), 'TCS', 'protected'), arrow('EEXIT'), node(t('Host thread', '宿主线程'), tone='outside')]) + '</div>'
    aex = '<div class="viz-lane"><span class="viz-lane-label">AEX · ' + t('asynchronous path', '异步路径') + '</span>'
    aex += flow([node(t('Enclave runs', 'Enclave 执行'), tone='protected'), arrow(t('Interrupt / exception', '中断 / 异常')), node('AEX', t('Save state in SSA; leave enclave', '状态保存到 SSA；离开 enclave'), 'outside'), arrow(t('Host handling → ERESUME', '宿主处理 → ERESUME')), node(t('Resume enclave', '恢复 enclave'), t('Restore saved state', '恢复保存状态'), 'protected')]) + '</div>'
    return frame(lang, 'sgx-execution-diagram', t('Build once, then distinguish two exit paths', '先构建，再区分两条退出路径'), build + run + aex, t('Simplified SGX1 baseline. AEX is a CPU event, not an instruction or an EEXIT call. SSA stores interrupted enclave state; resumption has architectural preconditions.', '简化的 SGX1 基线路径。AEX 是 CPU 事件，不是指令，也不是调用 EEXIT。SSA 保存被中断状态；恢复须满足架构前提。'), 'https://www.intel.com/content/www/us/en/developer/articles/technical/overview-of-an-intel-software-guard-extensions-enclave-life-cycle.html', 'Intel SGX lifecycle')


def tdx_memory(lang):
    t = lambda en, zh: tr(lang, en, zh)
    body = flow([node(t('Guest virtual address', 'Guest 虚拟地址'), 'GVA', 'protected'), arrow(t('Guest page tables', 'Guest 页表')), node(t('Guest physical address', 'Guest 物理地址'), 'GPA', 'neutral')])
    body += '<div class="viz-fork"><div class="viz-branch protected"><span class="viz-tag">' + t('PRIVATE GPA', '私有 GPA') + '</span>'
    body += node('Secure EPT', t('TDX module manages private mappings', 'TDX 模块管理私有映射'), 'protected') + arrow(direction='down') + node(t('Private physical page', '私有物理页'), t('TD KeyID · PAMT ownership/type checks', 'TD KeyID · PAMT 所有权/类型检查'), 'protected')
    body += '<p>' + t('Host cannot directly obtain private plaintext', '宿主不能直接获得私有明文') + '</p></div>'
    body += '<div class="viz-branch outside"><span class="viz-tag">' + t('SHARED GPA', '共享 GPA') + '</span>'
    body += node(t('Host-controlled mapping', '宿主控制映射'), t('Shared communication path', '共享通信路径'), 'outside') + arrow(direction='down') + node(t('Shared physical page', '共享物理页'), t('VMM / device buffers visible to host', 'VMM / 设备缓冲区对宿主可见'), 'outside')
    body += '<p>' + t('Guest validates data crossing this boundary', 'Guest 校验跨边界数据') + '</p></div></div>'
    return frame(lang, 'tdx-memory-diagram', t('One GPA space, two different trust paths', '同一 GPA 空间，两条不同信任路径'), body, t('Logical mapping view, not a cycle-by-cycle CPU pipeline. Private/shared conversion follows the defined guest/host protocol; encryption alone does not make shared I/O trustworthy.', '逻辑映射图，并非 CPU 逐周期流水线。私有/共享转换须遵循 Guest/宿主协议；加密本身不能让共享 I/O 变得可信。'), 'https://docs.kernel.org/arch/x86/tdx.html', 'Linux TDX')


def tdx_calls(lang):
    t = lambda en, zh: tr(lang, en, zh)
    body = '<div class="viz-three">'
    body += '<div class="viz-zone outside"><span class="viz-zone-label">' + t('HOST', '宿主') + '</span>' + node('VMM → KVM', t('Userspace ioctl layer', '用户态 ioctl 层'), 'outside') + '</div>'
    body += '<div class="viz-zone neutral"><span class="viz-zone-label">SEAM</span>' + node('Intel TDX module', t('TDH.* host API · TDG.* guest API', 'TDH.* 宿主 API · TDG.* Guest API'), 'neutral') + '</div>'
    body += '<div class="viz-zone protected"><span class="viz-zone-label">' + t('TRUST DOMAIN', 'TRUST DOMAIN') + '</span>' + node(t('Guest kernel / workload', 'Guest 内核 / 工作负载'), t('Private TD execution', 'TD 私有执行'), 'protected') + '</div></div>'
    body += '<div class="viz-lane"><span class="viz-lane-label">' + t('Host requests module services', '宿主请求模块服务') + '</span>' + flow([node('KVM', tone='outside'), arrow('SEAMCALL'), node('TDH.*', 'TDH.MNG.CREATE / TDH.VP.ENTER', 'neutral')]) + '</div>'
    body += '<div class="viz-lane"><span class="viz-lane-label">' + t('Guest requests module services', 'Guest 请求模块服务') + '</span>' + flow([node('Guest TD', tone='protected'), arrow('TDCALL'), node('TDG.*', 'TDG.VP.INFO / TDG.MEM.PAGE.ACCEPT', 'neutral')]) + '</div>'
    body += '<div class="viz-lane"><span class="viz-lane-label">' + t('Guest asks the host for assistance', 'Guest 请求宿主协助') + '</span>' + flow([node('Guest TD', tone='protected'), arrow('TDCALL'), node('TDG.VP.VMCALL', t('Module mediates a TD exit', '模块介导 TD 退出'), 'neutral'), arrow(t('TD exit', 'TD 退出')), node('VMM', t('Permitted service handling', '处理允许的服务请求'), 'outside')]) + '</div>'
    return frame(lang, 'tdx-calls-diagram', t('Who calls whom in TDX', 'TDX 中谁调用谁'), body, t('TDVMCALL names the TDG.VP.VMCALL leaf of TDCALL. It is not a separate CPU instruction. The diagram shows request directions; return and re-entry paths are omitted.', 'TDVMCALL 指 TDCALL 的 TDG.VP.VMCALL leaf，不是独立 CPU 指令。图中标出请求方向，省略返回和重新进入路径。'), 'https://www.intel.com/content/www/us/en/developer/tools/trust-domain-extensions/documentation.html', 'Intel TDX ABI')


def diagram(name, lang):
    return globals()[name](lang)
