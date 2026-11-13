"""Confidential Containers chapter for the bilingual TEE atlas."""

from html import escape

from diagram_core import arrow, flow, frame, node, sequence, tr

DOCS = 'https://confidentialcontainers.org/docs/'
DESIGN = DOCS + 'architecture/design-overview/'
TRUST = DOCS + 'architecture/trust-model/trust-model/'
INIT_DATA = DOCS + 'features/initdata/'
POLICIES = DOCS + 'attestation/policies/'
ENCRYPTED = DOCS + 'features/encrypted-images/'
SIGNED = DOCS + 'features/signed-images/'
SEALED = DOCS + 'features/sealed-secrets/'
INSTALL = DOCS + 'getting-started/installation/'
PEERS = DOCS + 'cloud-providers/'
TRUSTEE = 'https://github.com/confidential-containers/trustee'
GUEST = 'https://github.com/confidential-containers/guest-components'
PROTOCOL = TRUSTEE + '/blob/main/kbs/docs/kbs_attestation_protocol.md'
RUNTIME_CLASS = 'https://kubernetes.io/docs/concepts/containers/runtime-class/'
KATA = 'https://github.com/kata-containers/kata-containers'


def coco_page(lang, *, page_hero, article, table, link):
    def t(en, zh):
        return tr(lang, en, zh)

    def figure(ident, title, body, caption, url, source):
        return frame(lang, ident, t(*title), body, t(*caption), url, source)

    def steps(*items):
        parts = []
        for title, text, tone in items:
            if parts:
                parts.append(arrow())
            parts.append(node(t(*title), t(*text), tone))
        return flow(parts)

    def notes(*items):
        return ''.join(f'<p>{t(*item)}</p>' for item in items)

    def listing(*items):
        return '<ol>' + ''.join(f'<li>{t(*item)}</li>' for item in items) + '</ol>'

    def code(value):
        return f'<pre class="code"><code>{escape(value)}</code></pre>'

    topics = (
        ('trust-boundary', t('Trust boundary', '信任边界')),
        ('pod-launch', t('Pod launch', 'Pod 启动')),
        ('attestation', t('Trustee and attestation', 'Trustee 与远程证明')),
        ('policy', t('Init-Data and policy', 'Init-Data 与策略')),
        ('images', t('Images and secrets', '镜像与秘密')),
        ('lab', t('Deployment and lab', '部署与实验')),
        ('sources', t('Documentation and code', '文档与源码')),
    )
    contents = ''.join(f'<li><a href="#{ident}">{label}</a></li>' for ident, label in topics)
    nav = f'<nav class="tdx-contents" aria-label="{t("Chapter contents", "章节目录")}"><ul class="wrap">{contents}</ul></nav>'
    hero = page_hero(
        lang, 'CONFIDENTIAL CONTAINERS',
        t('Confidential Containers<br><em>From Pod to confidential VM</em>',
          '机密容器<br><em>从 Kubernetes Pod 到机密虚拟机</em>'),
        t('Follow one Kubernetes Pod through Kata Containers, guest-side image loading, remote attestation and policy-gated secret delivery.',
          '跟踪一个 Kubernetes Pod，理解 Kata Containers 如何创建机密虚拟机，Guest 如何拉取镜像，以及 Trustee 如何依据证明和策略发放秘密。'),
    )

    boundary_figure = figure(
        'coco-boundaries', ('Where the components run', '组件分别运行在哪里'),
        '<div class="viz-three">'
        + node(t('Kubernetes and worker', 'Kubernetes 与 Worker'),
               t('API server, kubelet, containerd, Kata shim and host VMM', 'API Server、kubelet、containerd、Kata shim 与宿主 VMM'),
               'outside', t('OUTSIDE THE WORKLOAD TRUST BOUNDARY', '位于工作负载信任边界之外'))
        + node(t('PodVM', 'PodVM'),
               t('Guest firmware and kernel, Kata Agent, guest components and Pod containers', 'Guest 固件与内核、Kata Agent、Guest 组件及 Pod 中的容器'),
               'protected', t('CONFIDENTIAL GUEST', '机密 Guest'))
        + node('Trustee',
               t('KBS, Attestation Service, reference values and secret storage', 'KBS、Attestation Service、参考值与秘密存储'),
               'neutral', t('TRUSTED BY THE WORKLOAD OWNER', '由工作负载所有者信任'))
        + '</div>',
        ('The PodVM is the hardware isolation boundary. Init containers, app containers and sidecars in the same Pod share its guest kernel.',
         'PodVM 是硬件隔离边界。同一 Pod 的 init container、应用容器和 sidecar 共享 Guest 内核。'),
        TRUST, 'CoCo Trust Model',
    )
    modes = table(t(('Model', 'Isolation boundary', 'What the workload relies on'), ('模型', '隔离边界', '工作负载依赖什么')), [
        (t('Ordinary OCI container', '普通 OCI 容器'),
         t('Namespaces, cgroups and kernel security controls', 'namespace、cgroup 和内核安全机制'),
         t('The workload shares the worker’s kernel. A privileged host can inspect its state.', '工作负载共享 Worker 内核，拥有宿主特权的一方可以读取其状态。')),
        ('Kata Containers',
         t('A VM per Pod sandbox with a separate guest kernel', 'Pod 沙箱拥有独立虚拟机与 Guest 内核'),
         t('VM isolation separates workloads from the worker. The protections against a privileged host depend on the VM technology.', '虚拟化隔离将工作负载与 Worker 分开。能否抵御拥有特权的宿主，取决于虚拟机使用的技术。')),
        (t('CoCo on a hardware TEE', '运行于硬件 TEE 上的 CoCo'),
         t('A confidential PodVM backed by a platform such as Intel TDX or AMD SEV-SNP', '由 Intel TDX 或 AMD SEV-SNP 等平台提供保护的机密 PodVM'),
         t('Hardware protects private guest state. The workload owner uses remote evidence and policy to authorize sensitive resources.', '硬件保护 Guest 私有状态，工作负载所有者依据远程证据和策略授权敏感资源。')),
    ])
    boundary = article(
        t('SECURITY MODEL', '安全模型'),
        t('A sandboxed Pod and a confidential Pod', '容器沙箱与机密 Pod 的区别'),
        t('Container security can cover isolation, image provenance or protection from the infrastructure operator. CoCo addresses the third case by running the Pod in a confidential VM and verifying its initial state before granting access to secrets.',
          '容器安全可以指运行隔离、镜像来源验证，或防止基础设施运营者读取工作负载。CoCo 处理第三类问题，把 Pod 放进机密 VM，并在授权秘密前验证 Guest 的初始状态。'),
        modes + boundary_figure + notes((
            'The workload depends on the CPU and firmware, guest OS, in-guest runtime, application and the trusted verification and release services. The host still controls scheduling and can interrupt the VM. Shared I/O, traffic metadata and application logs need their own controls. Plaintext in a Pod manifest, Kubernetes Secret or host-backed mount is already available to the infrastructure handling it.',
            '工作负载依赖 CPU 与固件、Guest OS、Guest 内运行时、应用以及可信的验证和发放服务。宿主仍能控制调度或中断 VM。共享 I/O、流量元数据和应用日志各自需要保护。写入 Pod YAML、普通 Kubernetes Secret 或宿主挂载的明文，会被处理它们的基础设施看到。',
        )), 'trust-boundary',
    )

    launch = figure(
        'coco-launch', ('Follow CreatePodSandbox and CreateContainer', '跟踪 CreatePodSandbox 与 CreateContainer'),
        steps(
            (('kubelet → CRI', 'kubelet → CRI'), ('RuntimeClass selects a configured handler', 'RuntimeClass 选择已配置的 handler'), 'outside'),
            (('Kata shim → VMM', 'Kata shim → VMM'), ('Boot a measured guest for the Pod sandbox', '为 Pod 沙箱启动可度量的 Guest'), 'outside'),
            (('Kata Agent → CDH', 'Kata Agent → CDH'), ('Check allowed RPCs and arrange the guest-side image pull', '检查 RPC 是否允许，并在 Guest 内准备镜像'), 'protected'),
            (('Guest runtime → containers', 'Guest 运行时 → 容器'), ('Unpack the rootfs and start the workload inside the VM', '在 VM 内解包 rootfs 并启动工作负载'), 'protected'),
        ),
        ('Simplified local Kata path. The host snapshotter and the guest image service cooperate so that the host need not unpack the workload layers.',
         '图示简化了本地 Kata 路径。宿主 snapshotter 与 Guest 镜像服务协作，使工作负载的镜像层可直接在 Guest 内解包。'),
        DESIGN, 'CoCo Design Overview',
    )
    pod = article(
        t('IMPLEMENTATION', '实现'),
        t('How Kubernetes creates a PodVM', 'Kubernetes 如何创建 PodVM'),
        t('Follow the local Kata runtime path, then compare where the VM is provisioned with Peer Pods.',
          '先看本地 Kata 运行时如何创建虚拟机，再看 Peer Pods 如何改变虚拟机的部署位置。'),
        launch + listing(
            ('<strong>Select a runtime.</strong> The Pod’s <code>runtimeClassName</code> refers to a RuntimeClass. Its handler selects a runtime configured in the node’s CRI implementation.',
             '<strong>选择运行时。</strong> Pod 的 <code>runtimeClassName</code> 引用 RuntimeClass，后者的 handler 指向节点 CRI 中已配置的运行时。'),
            ('<strong>Boot the sandbox.</strong> The Kata shim starts the VMM and the guest boots. The shim forwards lifecycle calls over a transport such as vsock. The Kata Agent checks the applicable guest policy before acting on host requests.',
             '<strong>启动沙箱。</strong> Kata shim 启动 VMM，Guest 随之引导。shim 通过 vsock 等传输转发生命周期 RPC，Guest 中的 Kata Agent 按策略检查宿主请求。'),
            ('<strong>Prepare the root filesystem.</strong> In the containerd design, a snapshotter such as Nydus routes image preparation to the guest. The Kata Agent invokes the Confidential Data Hub (CDH) image pull API. The guest uses <code>image-rs</code> for OCI image retrieval and unpacking and <code>ocicrypt-rs</code> for encrypted layers.',
             '<strong>准备根文件系统。</strong> 在 containerd 架构中，Nydus 等 snapshotter 将镜像准备工作引导到 Guest。Kata Agent 调用 Confidential Data Hub（CDH）的镜像拉取 API。Guest 用 <code>image-rs</code> 获取并解包 OCI 镜像，用 <code>ocicrypt-rs</code> 处理加密层。'),
        ) + notes((
            'With Peer Pods, Cloud API Adaptor (CAA) calls a provider API to create a separate PodVM beside the worker and forwards the agent traffic. The worker can itself be a VM. The actual confidentiality properties still depend on the selected instance, guest image and verifiable hardware evidence.',
            '在 Peer Pods 模式中，Cloud API Adaptor（CAA）调用云平台 API，在 Worker 旁创建独立的 PodVM，并转发 Agent 流量。Worker 本身可以是虚拟机。机密保护取决于实例类型、Guest 镜像以及可验证的硬件证据。',
        )), 'pod-launch',
    )

    attestation_flow = figure(
        'coco-rcar', ('Challenge, evidence and resource release', '挑战、证据与秘密发放'),
        sequence(lang, [
            ('PodVM', t('CDH + Attestation Agent', 'CDH 与 Attestation Agent'), 'protected'),
            ('KBS', t('Session and resource authorization', '会话与资源授权'), 'neutral'),
            ('AS / RVPS', t('Evidence appraisal and reference values', '证据评估与参考值'), 'neutral'),
        ], [
            (0, 1, t('<code>POST /kbs/v0/auth</code> to start a session', '<code>POST /kbs/v0/auth</code> 发起会话')),
            (1, 0, t('Return a fresh nonce', '返回新鲜 nonce')),
            (0, 1, t('<code>POST /kbs/v0/attest</code> with evidence bound to the nonce and guest public key', '<code>POST /kbs/v0/attest</code> 提交绑定 nonce 和 Guest 公钥的证据')),
            (1, 2, t('Verify evidence and evaluate the platform claims', '验签并评估平台声明')),
            (2, 1, t('Return attestation results', '返回证明评估结果')),
            (0, 1, t('<code>GET /kbs/v0/resource/…</code> for a specific key or secret', '<code>GET /kbs/v0/resource/…</code> 请求指定密钥或秘密')),
            (1, 0, t('If policy allows, return the resource encrypted to the attested guest key', '策略通过后，返回加密给已证明 Guest 公钥的资源')),
        ]),
        ('The KBS returns an attestation token after the Request–Challenge–Attestation–Response (RCAR) exchange. The client then requests a resource using its session or an accepted token. The KBS checks resource policy and returns the approved data as an encrypted JWE payload.',
         '完成 Request–Challenge–Attestation–Response（RCAR）后，KBS 返回证明令牌。客户端使用会话或 KBS 接受的令牌请求资源。KBS 检查资源策略，将获准的数据封装为加密的 JWE 响应。'),
        PROTOCOL, 'Trustee KBS Protocol',
    )
    attestation = article(
        t('TRUSTEE', 'TRUSTEE'),
        t('From a hardware report to a resource decision', '从硬件报告到资源授权'),
        t('The Attestation Agent (AA) obtains TEE evidence. Trustee evaluates it on behalf of the workload owner. The CDH consumes the resulting protected resource inside the guest.',
          'Attestation Agent（AA）获取 TEE 证据。Trustee 代表工作负载所有者评估证据，CDH 在 Guest 内使用受保护的资源。'),
        attestation_flow + table(t(('Service', 'Responsibility'), ('服务', '职责')), [
            ('Key Broker Service (KBS)',
             t('Manages the attestation exchange. Uses the verified claims and requested resource path to make a release decision. Encrypts the resource response for the attested guest key.',
               '管理证明交互，根据已验证的声明与资源路径作出发放决定。用已证明的 Guest 公钥保护返回的资源。')),
            ('Attestation Service (AS)',
             t('Runs the platform verifier, checks evidence and its bindings, and appraises TCB claims against policy. A TDX Quote and an SNP report have different endorsement and verification procedures.',
               '运行对应平台的验证器，检查证据及其绑定，按策略评估 TCB 声明。TDX Quote 与 SNP report 使用各自的背书和验证流程。')),
            ('Reference Value Provider Service (RVPS)',
             t('Supplies approved reference values to AS, such as expected measurements. Their provenance and update process belong to the trusted deployment.',
               '向 AS 提供预期度量等经批准的参考值。参考值的来源与更新流程属于可信部署的一部分。')),
        ]) + notes((
            'The evidence binds the KBS challenge to the public key generated in the guest. Freshness prevents reuse of an old report for the new challenge. The key binding lets KBS encrypt the response to the guest that produced the evidence, even when the infrastructure relays the traffic.',
            '证据绑定 KBS 的挑战值和 Guest 内生成的公钥。新鲜度检查阻止旧报告被用于新的挑战。公钥绑定让 KBS 能将响应加密给生成证据的 Guest，即使流量经由基础设施转发。',
        )), 'attestation',
    )

    policy_flow = figure(
        'coco-init-data', ('Bind workload policy to the attested VM', '把工作负载策略绑定到已证明的 VM'),
        steps(
            (('Workload owner', '工作负载所有者'), ('Prepare Init-Data with the expected agent policy', '准备含预期 Agent 策略的 Init-Data'), 'neutral'),
            (('PodVM launch', 'PodVM 启动'), ('Bind the digest in a platform configuration field', '在平台配置字段中绑定摘要'), 'protected'),
            (('Guest + AS', 'Guest 与 AS'), ('Check config integrity and appraise the bound evidence', '检查配置完整性并评估绑定后的证据'), 'protected'),
            (('KBS', 'KBS'), ('Authorize a named secret using approved identity claims', '根据获准的身份声明授权指定秘密'), 'neutral'),
        ),
        ('Kata Agent enforces the in-guest rules. The remote side verifies the policy identity and applies its own resource rules.',
         'Kata Agent 在 Guest 内执行规则。远端验证策略身份，并执行自己的资源授权规则。'),
        INIT_DATA, 'CoCo Init-Data',
    )
    policy = article(
        t('MEASURED CONFIGURATION', '配置度量'),
        t('Three policies and one evidence chain', '三类策略如何协作'),
        t('The VM launch measurement identifies the initial guest environment. Workload images arrive later. CoCo can bind workload-specific configuration through Init-Data and enforce it in the measured guest.',
          'VM 启动度量标识初始 Guest 环境。工作负载镜像在后续加载。CoCo 可用 Init-Data 绑定该工作负载的配置，由已度量的 Guest 执行策略。'),
        policy_flow + table(t(('Policy', 'Enforced by', 'Example decision'), ('策略', '执行者', '决策示例')), [
            ('Kata Agent Policy', 'Kata Agent',
             t('Allow only approved container image digests and mount settings. Deny <code>ExecProcessRequest</code> when the workload disallows host-initiated exec.',
               '只允许指定的容器镜像 digest 与挂载配置。若应用禁止宿主发起 exec，则拒绝 <code>ExecProcessRequest</code>。')),
            ('Attestation Service Policy', 'Trustee AS',
             t('Check a platform TCB baseline and expected guest measurements.',
               '检查平台 TCB 基线和预期的 Guest 度量。')),
            ('KBS Resource Policy', 'Trustee KBS',
             t('Release the payments service’s key only for the approved workload identity and resource path.',
               '只有身份声明符合预期且资源路径匹配时，才发放支付服务的密钥。')),
        ]) + notes((
            'Kata’s <code>genpolicy</code> can generate an agent policy from workload manifests. Review the resulting rules, then package the policy and guest settings in Init-Data. In the documented CoCo configuration, the launch binds its digest to TDX <code>MRCONFIGID</code> or SNP <code>HOST_DATA</code>. The guest checks the configuration against the bound value. The remote side must still compare that value or its verified claims against the owner’s approved configuration.',
            'Kata 的 <code>genpolicy</code> 可以根据工作负载清单生成 Agent 策略。审阅规则后，将策略与 Guest 配置打包为 Init-Data。按 CoCo 文档，启动时可把其摘要绑定到 TDX 的 <code>MRCONFIGID</code> 或 SNP 的 <code>HOST_DATA</code>。Guest 核对配置与绑定值，远端还需把该值或经验证的声明与所有者批准的配置比较。',
        ), (
            'Treat Init-Data as integrity-protected configuration that can pass through the control plane. Deliver sensitive material through the KBS or a sealed secret.',
            'Init-Data 是可经过控制面的完整性受保护配置。敏感材料通过 KBS 或 Sealed Secret 交付。',
        )), 'policy',
    )

    image_flow = figure(
        'coco-image', ('Encrypted layers, attested key, guest rootfs', '加密镜像层、经证明授权的密钥、Guest rootfs'),
        steps(
            (('Build pipeline', '构建流水线'), ('Encrypt OCI layers and publish the resulting image', '加密 OCI 层并发布镜像'), 'neutral'),
            (('OCI registry', 'OCI Registry'), ('Serve encrypted blobs and OCI metadata', '提供加密 blob 与 OCI 元数据'), 'outside'),
            (('Guest image service', 'Guest 镜像服务'), ('Resolve the layer key through CDH and Trustee', '通过 CDH 与 Trustee 取得层密钥'), 'protected'),
            (('Guest rootfs', 'Guest rootfs'), ('Decrypt and unpack inside PodVM', '在 PodVM 内解密并解包'), 'protected'),
        ),
        ('The registry distributes the image. The broker controls access to the decryption resource. The guest handles both image acceptance and plaintext.',
         'Registry 分发镜像，KBS 控制解密资源的访问，Guest 负责验证镜像和处理明文。'),
        ENCRYPTED, 'CoCo Encrypted Images',
    )
    images = article(
        t('IMAGE AND DATA PATH', '镜像与数据路径'),
        t('How encrypted OCI layers become a running container', '加密 OCI 镜像如何变成运行中的容器'),
        t('A build pipeline encrypts layers and publishes the image to an OCI registry. The resulting OCI descriptors can carry key-provider metadata. The matching key resource is provisioned into Trustee or its configured secret backend.',
          '构建流水线加密镜像层，并将镜像发布到 OCI Registry。加密后的 OCI descriptor 可携带 key provider 元数据，匹配的密钥资源预先配置到 Trustee 或它使用的秘密后端。'),
        image_flow + notes((
            'The guest pulls the encrypted blobs, and CDH handles the key-provider path. When the required resource is gated by attestation, KBS evaluates the resource policy before returning it. The guest decrypts the layers and prepares the container root filesystem. Manifest and descriptor metadata can remain visible to the registry and infrastructure.',
            'Guest 拉取加密 blob，由 CDH 处理 key provider 路径。需要证明才能访问的密钥资源，由 KBS 在返回前执行资源策略。Guest 解密镜像层并准备容器根文件系统。Registry 和基础设施仍可能看到 manifest 及 descriptor 元数据。',
        )) + table(t(('Control', 'What to verify'), ('控制措施', '要验证什么')), [
            (t('Image digest and signature', '镜像 digest 与签名'),
             t('Pin the expected digest and use guest-side signature policy to verify the publisher. Verify the artifact that is actually deployed.',
               '固定预期 digest，并在 Guest 内通过签名策略核对发布者身份。验证实际部署的镜像制品。')),
            (t('OCI layer encryption', 'OCI 镜像层加密'),
             t('Verify that encrypted layers require the intended key resource and that rejected guests cannot retrieve it.',
               '确认加密层只能用预期的密钥资源解密，并检查被拒绝的 Guest 无法取到资源。')),
            (t('Sealed Secrets and protected storage', 'Sealed Secrets 与受保护存储'),
             t('A sealed secret can reference a broker-held secret or wrap ciphertext with key material available to an authorized guest. Evaluate writable volumes separately for encryption, integrity and rollback requirements.',
               'Sealed Secret 可以引用 KBS 保存的秘密，也可封装密文，由获准的 Guest 取用相应密钥。可写卷需要独立评估加密、完整性与回滚防护。')),
        ]), 'images',
    )

    manifest = """apiVersion: v1
kind: Pod
metadata:
  name: coco-smoke
spec:
  runtimeClassName: kata-qemu-coco-dev
  restartPolicy: Never
  containers:
    - name: hello
      image: docker.io/library/busybox:1.36
      command: ["sh", "-c", "echo CoCo-sandbox-ready; sleep 300"]"""
    lab = article(
        t('HANDS-ON', '动手实验'),
        t('Start a Pod, then test a denied key request', '先启动 Pod，再验证密钥拒绝路径'),
        t('On a Kubernetes lab cluster with the CoCo Helm chart and the matching CRI configuration, start with a public image and dummy data. The development runtime exercises the lifecycle with a regular VM.',
          '在已安装 CoCo Helm chart、配置匹配 CRI 的 Kubernetes 实验集群里，从公开镜像和测试数据开始。开发运行时用普通 VM 验证生命周期。'),
        code(manifest) + code('kubectl get runtimeclass\nkubectl apply -f coco-smoke.yaml\nkubectl describe pod coco-smoke\nkubectl logs coco-smoke\nkubectl delete pod coco-smoke')
        + listing(
            ('<strong>Confirm sandbox creation.</strong> Save the YAML as <code>coco-smoke.yaml</code>. Look for <code>CoCo-sandbox-ready</code>. If it fails, inspect RuntimeClass, Pod scheduling, shim and guest boot before investigating attestation.',
             '<strong>确认沙箱启动。</strong> 将 YAML 保存为 <code>coco-smoke.yaml</code>。在日志中找 <code>CoCo-sandbox-ready</code>。失败时先检查 RuntimeClass、Pod 调度、shim 和 Guest 启动，再排查证明。'),
            ('<strong>Exercise hardware evidence.</strong> On a compatible TDX or SNP node, select the installed hardware handler, such as <code>kata-qemu-tdx</code> or <code>kata-qemu-snp</code>. Configure Trustee, accepted reference values, Init-Data and an encrypted test image using the linked CoCo guides. Confirm that a matching Guest can retrieve only its test key and start the image.',
             '<strong>验证硬件证据。</strong> 在兼容的 TDX 或 SNP 节点选择已安装的硬件 handler，例如 <code>kata-qemu-tdx</code> 或 <code>kata-qemu-snp</code>。按 CoCo 指南配置 Trustee、参考值、Init-Data 和加密测试镜像，确认匹配的 Guest 只能取得获准的测试密钥并启动镜像。'),
            ('<strong>Change one condition at a time.</strong> Start a new PodVM with a different but internally consistent Init-Data that KBS policy does not authorize. Check that evidence can be evaluated but the key request is denied. Then separately change an allowed resource path or test a Guest whose measurements fail AS policy. Inspect Trustee and guest logs. A valid session denied a resource by KBS policy should receive HTTP 403.',
             '<strong>每次只改一个条件。</strong> 启动新的 PodVM，使用摘要正确但未被 KBS 策略授权的另一份 Init-Data。确认硬件证据能被评估，但取钥被拒绝。再单独请求未获授权的资源路径，或测试度量不符合 AS 策略的 Guest。通过 Trustee 和 Guest 日志定位失败阶段。会话有效但资源策略拒绝时，KBS 应返回 HTTP 403。'),
        ) + notes((
            'To test the guest-side boundary independently, apply a policy that denies <code>ExecProcessRequest</code> and check that an otherwise Kubernetes-authorized exec request is rejected by Kata Agent. A successful development Pod tests orchestration. The hardware test adds attestation and real release-policy checks.',
            '要独立验证 Guest 侧边界，可部署拒绝 <code>ExecProcessRequest</code> 的策略，检查已通过 Kubernetes 授权的 exec 请求是否仍被 Kata Agent 拒绝。开发 Pod 的成功用于确认编排，硬件实验再验证证明和真实的资源发放策略。',
        )), 'lab',
    )

    references = [
        (DESIGN, ('CoCo Design Overview', 'CoCo 设计总览'), ('Architecture and implementation map', '整体架构与实现地图')),
        (TRUST, ('CoCo Trust Model', 'CoCo 信任模型'), ('Trusted components and exposed interfaces', '可信组件与跨边界接口')),
        (KATA + '/tree/main/src', ('Kata Containers source', 'Kata Containers 源码'), ('Host runtime, shim and in-guest agent', '宿主运行时、shim 和 Guest Agent')),
        (GUEST, ('Guest Components source', 'Guest Components 源码'), ('CDH, Attestation Agent, image-rs and ocicrypt-rs', 'CDH、Attestation Agent、image-rs 与 ocicrypt-rs')),
        (DOCS + 'attestation/architecture/', ('Trustee architecture', 'Trustee 架构'), ('KBS, AS and RVPS roles', 'KBS、AS 与 RVPS 分工')),
        (PROTOCOL, ('Trustee KBS protocol', 'Trustee KBS 协议'), ('Challenge, evidence fields and resource response', '挑战值、证据字段与资源响应')),
        (INIT_DATA, ('CoCo Init-Data', 'CoCo Init-Data'), ('genpolicy and measured configuration', 'genpolicy 与配置度量')),
        (POLICIES, ('CoCo policy guide', 'CoCo 策略指南'), ('Attestation and resource policy examples', '证明策略与资源授权策略示例')),
        (ENCRYPTED, ('Encrypted OCI images', '加密 OCI 镜像'), ('Layer encryption and test-key provisioning', '镜像层加密和测试密钥配置')),
        (SIGNED, ('Signed OCI images', '签名 OCI 镜像'), ('Guest verification policy and image signing', 'Guest 验签策略和镜像签名')),
        (SEALED, ('Sealed Secrets', 'Sealed Secrets'), ('Vault and envelope secret flows', 'Vault 和 Envelope 两种秘密交付流程')),
        (INSTALL, ('CoCo installation', 'CoCo 安装指南'), ('Helm, prerequisites and RuntimeClass', 'Helm、环境要求和 RuntimeClass')),
        (PEERS, ('CoCo Peer Pods', 'CoCo Peer Pods'), ('Cloud API Adaptor and provider options', 'Cloud API Adaptor 与云平台配置')),
        (RUNTIME_CLASS, ('Kubernetes RuntimeClass', 'Kubernetes RuntimeClass'), ('Runtime handlers and Pod selection', '运行时 handler 与 Pod 选择机制')),
    ]
    sources = article(
        t('PRIMARY SOURCES', '一手资料'),
        t('Read the design, then trace the code', '从设计文档走到源码'),
        t('Start at the Kata runtime and agent, then follow the guest image and attestation requests through Guest Components and Trustee.',
          '从 Kata 运行时与 Agent 开始，再到 Guest Components 和 Trustee 中追踪镜像与证明请求。'),
        '<div class="source-grid tdx-sources">'
        + ''.join(link(url, t(*title), t(*description)) for url, title, description in references)
        + '</div>', 'sources',
    )
    return hero + nav + boundary + pod + attestation + policy + images + lab + sources
