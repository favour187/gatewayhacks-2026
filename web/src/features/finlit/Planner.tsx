import { useEffect, useMemo, useState } from "react";
import { finlitApi } from "./api";
import { fmtCur } from "./format";
import { Badge, Button, Card, ErrorBanner, Input } from "../../ui/components";
import type { FinancingOut, PlanIn, PlanResult, PlannerMeta } from "./types";

const BUCKET_COLORS: Record<string, string> = { needs: "var(--accent)", wants: "#f59e0b", savings: "var(--success)" };
const BUCKET_LABELS: Record<string, string> = { needs: "Needs", wants: "Wants", savings: "Savings & debt" };

const DEFAULT_PLAN: PlanIn = {
  income: 200,
  period: "weekly",
  currency: "USD",
  lines: [
    { category: "transport", amount: 40 },
    { category: "food", amount: 50 },
    { category: "data_airtime", amount: 15 },
    { category: "eating_out", amount: 35 },
    { category: "entertainment", amount: 25 },
    { category: "savings_goal", amount: 20 },
  ],
};

export function Planner({ onDone }: { onDone: () => void }) {
  const [meta, setMeta] = useState<PlannerMeta | null>(null);
  const [plan, setPlan] = useState<PlanIn>(DEFAULT_PLAN);
  const [result, setResult] = useState<PlanResult | null>(null);
  const [saved, setSaved] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [addKey, setAddKey] = useState("");

  useEffect(() => {
    void finlitApi.plannerMeta().then(setMeta);
    void finlitApi.plannerGet().then((r) => {
      if (r.plan) {
        setPlan(r.plan.input);
        setResult(r.plan.result);
        setSaved(true);
      }
    });
  }, []);

  useEffect(() => {
    if (!plan.income || plan.income <= 0) return;
    const t = setTimeout(() => {
      finlitApi
        .plannerPreview(plan)
        .then((r) => {
          setResult(r);
          setError(null);
        })
        .catch((e) => setError((e as Error).message));
    }, 250);
    return () => clearTimeout(t);
  }, [plan]);

  const symbol = meta?.currencies[plan.currency]?.symbol ?? "$";
  const decimals = meta?.currencies[plan.currency]?.decimals ?? 2;
  const catByKey = useMemo(() => Object.fromEntries((meta?.categories ?? []).map((c) => [c.key, c])), [meta]);
  const unused = (meta?.categories ?? []).filter((c) => !plan.lines.some((l) => l.category === c.key));

  function setLine(i: number, amount: number) {
    setSaved(false);
    setPlan((p) => ({ ...p, lines: p.lines.map((l, idx) => (idx === i ? { ...l, amount } : l)) }));
  }
  function removeLine(i: number) {
    setSaved(false);
    setPlan((p) => ({ ...p, lines: p.lines.filter((_, idx) => idx !== i) }));
  }
  function addLine(key: string) {
    if (!key) return;
    setSaved(false);
    setPlan((p) => ({ ...p, lines: [...p.lines, { category: key, amount: 0 }] }));
    setAddKey("");
  }
  function applyTemplate() {
    const inc = plan.income;
    setSaved(false);
    setPlan((p) => ({
      ...p,
      lines: [
        { category: "transport", amount: round(inc * 0.15) },
        { category: "food", amount: round(inc * 0.25) },
        { category: "data_airtime", amount: round(inc * 0.1) },
        { category: "eating_out", amount: round(inc * 0.15) },
        { category: "entertainment", amount: round(inc * 0.15) },
        { category: "savings_goal", amount: round(inc * 0.12) },
        { category: "emergency_fund", amount: round(inc * 0.08) },
      ],
    }));
  }
  async function save() {
    setBusy(true);
    try {
      const r = await finlitApi.plannerSave(plan);
      setResult(r.result);
      setSaved(true);
      onDone();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="page">
      <div className="spread" style={{ flexWrap: "wrap", gap: 8 }}>
        <div>
          <h1 style={{ margin: 0 }}>Planner</h1>
          <p style={{ color: "var(--text-2)", margin: "6px 0 0" }}>Your real money, in your currency, against the 50 / 30 / 20 guide. Saved plans feed the coach.</p>
        </div>
        <Button onClick={() => void save()} loading={busy} disabled={saved || !result}>{saved ? "Saved ✓" : "Save plan"}</Button>
      </div>

      <div className="grid-2" style={{ alignItems: "start" }}>
        <Card className="stack">
          <h3 style={{ margin: 0 }}>What comes in</h3>
          <div className="grid-3">
            <Input label={`Income (${symbol})`} type="number" min={0} value={plan.income} onChange={(e) => { setSaved(false); setPlan((p) => ({ ...p, income: Number(e.target.value) })); }} />
            <div className="field">
              <label className="field-label" htmlFor="period">How often</label>
              <select id="period" className="input" value={plan.period} onChange={(e) => { setSaved(false); setPlan((p) => ({ ...p, period: e.target.value as PlanIn["period"] })); }}>
                <option value="weekly">Weekly</option>
                <option value="biweekly">Every two weeks</option>
                <option value="monthly">Monthly</option>
              </select>
            </div>
            <div className="field">
              <label className="field-label" htmlFor="currency">Currency</label>
              <select id="currency" className="input" value={plan.currency} onChange={(e) => { setSaved(false); setPlan((p) => ({ ...p, currency: e.target.value })); }}>
                {Object.entries(meta?.currencies ?? { USD: { symbol: "$", name: "US dollar" } }).map(([code, c]) => (
                  <option key={code} value={code}>{code} · {c.name}</option>
                ))}
              </select>
            </div>
          </div>
          <div className="spread">
            <h3 style={{ margin: 0 }}>Where it goes</h3>
            <button className="btn btn-ghost btn-sm" onClick={applyTemplate}>Fill a 50/30/20 template</button>
          </div>
          <div className="stack" style={{ gap: 6 }}>
            {plan.lines.map((l, i) => {
              const cat = catByKey[l.category];
              return (
                <div key={`${l.category}-${i}`} className="row" style={{ gap: 8, alignItems: "center", padding: "6px 10px", background: "var(--surface-2)", borderRadius: "var(--radius-sm)" }}>
                  <span style={{ width: 8, height: 8, borderRadius: 999, background: BUCKET_COLORS[cat?.bucket ?? "needs"] }} />
                  <span style={{ flex: 1, fontSize: 14 }}>{cat?.label ?? l.category}</span>
                  <input className="input" type="number" min={0} value={l.amount} aria-label={`${cat?.label ?? l.category} amount`} onChange={(e) => setLine(i, Number(e.target.value))} style={{ width: 110, padding: "6px 8px" }} />
                  <button className="modal-close" aria-label="Remove line" onClick={() => removeLine(i)}>×</button>
                </div>
              );
            })}
          </div>
          <div className="row" style={{ gap: 8 }}>
            <select className="input" value={addKey} onChange={(e) => setAddKey(e.target.value)} aria-label="Add a line">
              <option value="">+ Add a line…</option>
              {unused.map((c) => (
                <option key={c.key} value={c.key}>{c.label} ({BUCKET_LABELS[c.bucket]})</option>
              ))}
            </select>
            <Button variant="secondary" size="sm" onClick={() => addLine(addKey)} disabled={!addKey}>Add</Button>
          </div>
          <ErrorBanner message={error} />
        </Card>

        <div className="stack">
          {result && (
            <Card className="stack">
              <div className="spread">
                <h3 style={{ margin: 0 }}>Plan health</h3>
                <Badge tone={result.health >= 85 ? "success" : result.health >= 65 ? "accent" : result.health >= 40 ? "warning" : "danger"}>{result.health}/100 · {result.verdict}</Badge>
              </div>
              <SplitBar result={result} />
              <div className="grid-3">
                {(["needs", "wants", "savings"] as const).map((b) => (
                  <div key={b} style={{ display: "grid", gap: 2 }}>
                    <span style={{ fontSize: 12, color: "var(--text-2)" }}>{BUCKET_LABELS[b]}</span>
                    <strong style={{ color: BUCKET_COLORS[b] }}>{Math.round(result.shares[b] * 100)}%</strong>
                    <span style={{ fontSize: 12, color: "var(--text-3)" }}>{fmtCur(result.buckets[b], symbol, decimals)} · guide {Math.round(result.target_shares[b] * 100)}%</span>
                  </div>
                ))}
              </div>
              {result.overspend > 0 && <Badge tone="danger">Over income by {fmtCur(result.overspend, symbol, decimals)}</Badge>}
              {result.unallocated > 0 && <Badge tone="warning">{fmtCur(result.unallocated, symbol, decimals)} not assigned</Badge>}
              <ul style={{ margin: 0, paddingLeft: 18, fontSize: 14, color: "var(--text-2)", display: "grid", gap: 6 }}>
                {result.tips.map((t) => <li key={t}>{t}</li>)}
              </ul>
              <p style={{ margin: 0, fontSize: 13, color: "var(--text-3)" }}>
                Over a year: income {fmtCur(result.annual.income, symbol)} · savings {fmtCur(result.annual.savings, symbol)} · wants {fmtCur(result.annual.wants, symbol)}.
              </p>
            </Card>
          )}
          <FinancingCheck symbol={symbol} decimals={decimals} />
        </div>
      </div>
    </div>
  );
}

function SplitBar({ result }: { result: PlanResult }) {
  const total = Math.max(result.income, result.buckets.needs + result.buckets.wants + result.buckets.savings);
  const parts = (["needs", "wants", "savings"] as const).map((b) => ({ b, w: (result.buckets[b] / total) * 100 }));
  const free = Math.max(0, 100 - parts.reduce((s, p) => s + p.w, 0));
  return (
    <div style={{ display: "grid", gap: 6 }}>
      <div style={{ display: "flex", height: 18, borderRadius: 999, overflow: "hidden", background: "var(--surface-2)" }}>
        {parts.map((p) => <div key={p.b} title={BUCKET_LABELS[p.b]} style={{ width: `${p.w}%`, background: BUCKET_COLORS[p.b] }} />)}
        {free > 0 && <div style={{ width: `${free}%`, background: "repeating-linear-gradient(45deg, var(--surface-2), var(--surface-2) 4px, var(--border) 4px, var(--border) 8px)" }} />}
      </div>
      <div style={{ display: "flex", height: 6, borderRadius: 999, overflow: "hidden", opacity: 0.5 }} title="50 / 30 / 20 guide">
        <div style={{ width: "50%", background: BUCKET_COLORS.needs }} />
        <div style={{ width: "30%", background: BUCKET_COLORS.wants }} />
        <div style={{ width: "20%", background: BUCKET_COLORS.savings }} />
      </div>
      <span style={{ fontSize: 11, color: "var(--text-3)" }}>Top bar: your plan · thin bar: the 50/30/20 guide</span>
    </div>
  );
}

function FinancingCheck({ symbol, decimals }: { symbol: string; decimals: number }) {
  const [price, setPrice] = useState("900");
  const [monthly, setMonthly] = useState("45");
  const [months, setMonths] = useState("24");
  const [out, setOut] = useState<FinancingOut | null>(null);
  const [error, setError] = useState<string | null>(null);
  async function run() {
    try {
      setError(null);
      setOut(await finlitApi.financing(Number(price), Number(monthly), Number(months)));
    } catch (e) {
      setError((e as Error).message);
    }
  }
  return (
    <Card className="stack">
      <h3 style={{ margin: 0 }}>"Only {symbol}{monthly || "…"} a month" — the real price</h3>
      <p style={{ margin: 0, fontSize: 13, color: "var(--text-2)" }}>Type in any instalment / buy-now-pay-later offer and see what it truly costs.</p>
      <div className="grid-3">
        <Input label={`Price (${symbol})`} type="number" min={0} value={price} onChange={(e) => setPrice(e.target.value)} />
        <Input label="Per month" type="number" min={0} value={monthly} onChange={(e) => setMonthly(e.target.value)} />
        <Input label="Months" type="number" min={1} value={months} onChange={(e) => setMonths(e.target.value)} />
      </div>
      <Button variant="secondary" onClick={() => void run()}>Reveal the total</Button>
      <ErrorBanner message={error} />
      {out && (
        <div className="row" style={{ gap: 8, flexWrap: "wrap" }}>
          <Badge tone="neutral">You pay {fmtCur(out.total_paid, symbol, decimals)}</Badge>
          <Badge tone={out.extra_paid > 0 ? "danger" : "success"}>{out.extra_paid > 0 ? `+${fmtCur(out.extra_paid, symbol, decimals)} extra (${out.extra_pct}%)` : "no extra cost"}</Badge>
          {out.implied_apr !== null && <Badge tone="warning">≈ {out.implied_apr}% APR</Badge>}
          {out.months_to_save !== null && <Badge tone="success">or save {symbol}{monthly}/mo → buy outright in {out.months_to_save} months</Badge>}
        </div>
      )}
    </Card>
  );
}

function round(n: number) {
  return Math.round(n * 100) / 100;
}
