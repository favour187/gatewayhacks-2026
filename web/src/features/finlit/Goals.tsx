import { useEffect, useState } from "react";
import { finlitApi } from "./api";
import { money, pct } from "./format";
import { Badge, Button, Card, Input, ProgressBar } from "../../ui/components";
import type { Goal } from "./types";
export function Goals({ onDone }: {
    onDone: () => void;
}) {
    const [goals, setGoals] = useState<Goal[]>([]);
    const [name, setName] = useState("");
    const [target, setTarget] = useState("600");
    const [weekly, setWeekly] = useState("50");
    const [error, setError] = useState<string | null>(null);
    const [busy, setBusy] = useState(false);
    async function load() {
        const r = await finlitApi.goals();
        setGoals(r.goals);
    }
    useEffect(() => {
        void load();
    }, []);
    async function create() {
        if (!name || Number(target) <= 0) {
            setError("Give the goal a name and a target above zero.");
            return;
        }
        setError(null);
        setBusy(true);
        try {
            await finlitApi.createGoal({
                name,
                target: Number(target),
                weekly: Number(weekly) || 0,
                apy: 0,
            });
            setName("");
            await load();
            onDone();
        }
        finally {
            setBusy(false);
        }
    }
    async function contribute(goal: Goal) {
        const amount = window.prompt(`Add to "${goal.name}" (amount in $)`, "20");
        if (!amount)
            return;
        await finlitApi.contribute(goal.id, Number(amount));
        await load();
        onDone();
    }
    return (<div className="page">
      <h1 style={{ margin: 0 }}>Savings goals</h1>
      <p style={{ color: "var(--text-2)", margin: "6px 0 18px" }}>
        Name it, size it, pick a weekly amount. The app computes the deadline math.
      </p>

      <Card className="stack" style={{ maxWidth: 520 }}>
        <h3 style={{ margin: 0 }}>New goal</h3>
        {error && <p style={{ color: "var(--danger)", fontSize: 13, margin: 0 }}>{error}</p>}
        <Input label="Goal name" value={name} onChange={(e) => setName(e.target.value)} placeholder="New laptop"/>
        <div className="grid-2">
          <Input label="Target amount ($)" type="number" value={target} onChange={(e) => setTarget(e.target.value)}/>
          <Input label="Per week ($)" type="number" value={weekly} onChange={(e) => setWeekly(e.target.value)}/>
        </div>
        <Button loading={busy} onClick={() => void create()}>
          Add goal
        </Button>
      </Card>

      {goals.length === 0 ? (<p style={{ color: "var(--text-2)" }}>No goals yet — add your first one above.</p>) : (<div className="grid-2" style={{ marginTop: 18 }}>
          {goals.map((g) => (<Card key={g.id} className="stack">
              <span className="spread">
                <h3 style={{ margin: 0 }}>{g.name}</h3>
                <Badge tone={g.status === "active" ? "success" : "neutral"}>{g.status}</Badge>
              </span>
              <div className="spread" style={{ fontSize: 14 }}>
                <strong>{money(g.contributed)}</strong>
                <span style={{ color: "var(--text-2)" }}>of {money(g.target)}</span>
              </div>
              <ProgressBar value={g.progress} label={`${pct(g.progress)} saved`}/>
              <div className="row" style={{ fontSize: 13, color: "var(--text-2)", flexWrap: "wrap" }}>
                <Badge tone="neutral">{money(g.remaining)} left</Badge>
                <Badge tone="neutral">{g.target_eta ? `by ${g.target_eta}` : "no weekly rate"}</Badge>
                {g.apy > 0 && <Badge tone="accent">{g.apy}% APY</Badge>}
              </div>
              <Button variant="secondary" onClick={() => void contribute(g)}>
                Add money
              </Button>
            </Card>))}
        </div>)}
    </div>);
}
