(() => {
  const panel = document.querySelector('[data-policy-lab]');
  if (!panel) return;
  const zh = document.documentElement.lang.startsWith('zh');
  const copy = zh ? {
    pass: '允许释放测试密钥', fail: '拒绝释放测试密钥',
    passDetail: '所有示例条件都通过。真实系统仍须验证厂商签名、证书链、TCB 状态和应用策略。',
    failDetail: '至少有一项示例条件不满足。真实依赖方应拒绝密钥释放，并记录失败原因。',
    names: ['证据来源', '预期测量值', '平台 TCB', '新鲜度', '会话绑定'],
    good: '通过', bad: '失败'
  } : {
    pass: 'Release the test secret', fail: 'Deny the test secret',
    passDetail: 'All illustrative checks pass. A real deployment must also verify vendor signatures, certificate chains, TCB status, and application policy.',
    failDetail: 'At least one illustrative check fails. A real relying party should deny release and record the reason.',
    names: ['Evidence origin', 'Expected measurement', 'Platform TCB', 'Freshness', 'Session binding'],
    good: 'Pass', bad: 'Fail'
  };
  const scenarios = {
    healthy: [true, true, true, true, true],
    stale: [true, true, true, false, true],
    changed: [true, false, true, true, true],
    unbound: [true, true, true, true, false],
    outdated: [true, true, false, true, true]
  };
  const output = panel.querySelector('[data-verdict]');
  const detail = panel.querySelector('[data-verdict-detail]');
  const checks = panel.querySelector('[data-checks]');
  function render(name) {
    const values = scenarios[name];
    if (!values) return;
    const pass = values.every(Boolean);
    output.textContent = pass ? copy.pass : copy.fail;
    output.dataset.pass = String(pass);
    detail.textContent = pass ? copy.passDetail : copy.failDetail;
    checks.innerHTML = values.map((value, i) => `<li class="${value ? 'ok' : 'bad'}"><span>${copy.names[i]}</span><b>${value ? copy.good : copy.bad}</b></li>`).join('');
    panel.querySelectorAll('[data-scenario]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.scenario === name));
    });
  }
  panel.addEventListener('click', event => {
    const button = event.target.closest('[data-scenario]');
    if (button) render(button.dataset.scenario);
  });
  render('healthy');
})();
