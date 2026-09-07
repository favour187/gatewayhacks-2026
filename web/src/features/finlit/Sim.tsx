import { useEffect, useState } from "react";
import { finlitApi } from "./api";
import { money, qualityLabel, signMoney } from "./format";
import { Badge, Button, Card, Spinner, cx } from "../../ui/components";
import type { ScenarioDTO, SimData, SimHistoryItem } from "./types";
export function Sim({ onDone }: {
    onDone: () => void;
}) {
    const [data, setData] = useState<SimData | null>(null);
    const [active, setActive] = useState<ScenarioDTO | null>(null);
    const [pendingChoice, setPendingChoice] = useState<string | null>(null);
    const [last, setLast] = useState<{
        explanation: string;
        delta: {
            money: number;
            debt: number;
            confidence: number;
            quality: number;
        };
        state: SimData["state"];
    } | null>(null);
    const [history, setHistory] = useState<SimHistoryItem[]>([]);
    const [busy, setBusy] = useState(false);
    useEffect(() => {
        void finlitApi.sim().then((r) => {
            setData(r);
            setHistory(r.history);
        });
    }, []);
    async function choose(scenario: ScenarioDTO, choiceId: string) {
        setBusy(true);
        setPendingChoice(choiceId);
        try {
            const res = await finlitApi.simulate(scenario.scenario_id, choiceId);
            setLast(res as unknown as typeof last);
            setHistory(res.history as unknown as SimHistoryItem[]);
            setActive(null);
            onDone();
        }
        finally {
            setBusy(false);
            setPendingChoice(null);
        }
    }
    async function reset() {
        await finlitApi.simReset();
        const r = await finlitApi.sim();
        setData(r);
        setHistory(r.history);
        setLast(null);
        onDone();
    }
    if (!data)
        return <Spinner />;
    const s = data.state;
    return (<div className="page">
      <div className="spread">
        <div>
          <h1 style={{ margin: 0 }}>Money Moves</h1>
          <p style={{ margin: "6px 0 0", color: "var(--text-2)" }}>
            Real-life choices. Track your decision quality, wallet and debt.
          </p>
        </div>
        <Button variant="ghost" size="sm" onClick={() => void reset()}>
          Reset game
        </Button>
      </div>

      <div className="grid-3" style={{ marginBottom: 18 }}>
        <Stat label="Wallet" value={money(s.balance)} tone="success"/>
        <Stat label="Debt" value={money(s.debt)} tone={s.debt > 0 ? "danger" : "success"}/>
        <Stat label="Decision quality" value={`${qualityLabel(s.quality)} · ${s.decisions}`} tone="accent"/>
      </div>

      {last && (<Card className="stack" style={{ marginBottom: 18 }}>
          <span className="spread">
            <strong style={{ margin: 0 }}>Outcome</strong>
            <div className="row">
              <Badge tone={last.delta.money >= 0 ? "success" : "danger"}>{signMoney(last.delta.money)} cash</Badge>
              <Badge tone="success">+{(last.delta.confidence).toFixed(0)} confidence</Badge>
              <Badge tone="accent">{qualityLabel(last.delta.quality)}</Badge>
            </div>
          </span>
          <p style={{ margin: 0, fontSize: 14 }}>{last.explanation}</p>
        </Card>)}

      {active ? (<Card className="stack">
          <Badge tone="accent">Scenario · {active.title}</Badge>
          <p style={{ margin: 0, fontSize: 17 }}>{active.setup}</p>
          <div className="stack">
            {active.choices.map((c) => (<button key={c.choice_id} className={cx("btn", "btn-secondary")} style={{ justifyContent: "flex-start", whiteSpace: "normal" }} disabled={busy} onClick={() => void choose(active, c.choice_id)}>
                {pendingChoice === c.choice_id && busy ? "…" : c.label}
              </button>))}
          </div>
        </Card>) : (<div className="grid-2">
          {data.scenarios.map((scenario) => (<Card key={scenario.scenario_id} className="stack">
              <h3 style={{ margin: 0 }}>{scenario.title}</h3>
              <p style={{ margin: 0, fontSize: 14, color: "var(--text-2)" }}>{scenario.setup}</p>
              <Button variant="secondary" size="sm" onClick={() => setActive(scenario)}>
                Play
              </Button>
            </Card>))}
        </div>)}

      {history.length > 0 && (<div className="stack" style={{ marginTop: 18 }}>
          <h3 style={{ margin: "0 0 8px" }}>Decision log</h3>
          {history.slice(0, 6).map((h) => (<Card key={h.id} className="spread" style={{ padding: "10px 14px" }}>
              <span style={{ fontSize: 13, color: "var(--text-2)" }}>
                {data.scenarios.find((x) => x.scenario_id === h.scenario_id)?.title ?? h.scenario_id}
              </span>
              <span className="row">
                <Badge tone={h.delta.quality >= 0.6 ? "success" : "danger"}>{qualityLabel(h.delta.quality)}</Badge>
                <Badge tone={h.delta.money >= 0 ? "success" : "danger"}>{signMoney(h.delta.money)}</Badge>
              </span>
            </Card>))}
        </div>)}
    </div>);
}
function Stat({ label, value, tone }: {
    label: string;
    value: string;
    tone: "success" | "danger" | "accent" | "neutral";
}) {
    return (<Card className="stack" style={{ gap: 4 }}>
      <span style={{ fontSize: 12, color: "var(--text-2)" }}>{label}</span>
      <span style={{ fontSize: 22, fontWeight: 700 }}>
        <Badge tone={tone}>{value}</Badge>
      </span>
    </Card>);
}
