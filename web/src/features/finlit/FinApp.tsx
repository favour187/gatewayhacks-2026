import { useCallback, useEffect, useState } from "react";
import { finlitApi } from "./api";
import { Assessment } from "./Assessment";
import { Coach } from "./Coach";
import { Goals } from "./Goals";
import { Learn } from "./Learn";
import { Planner } from "./Planner";
import { Sim } from "./Sim";
import { money, pct, qualityLabel } from "./format";
import { useAuth } from "../../lib/auth";
import { Badge, Button, Card, ErrorBanner, Input, ProgressBar, Spinner, cx } from "../../ui/components";
import type { Overview } from "./types";
type View = "landing" | "home" | "learn" | "sim" | "goals" | "planner" | "assess_pre" | "assess_post";
export function FinApp() {
    const auth = useAuth();
    const [view, setView] = useState<View>("landing");
    const [overview, setOverview] = useState<Overview | null>(null);
    const [error, setError] = useState<string | null>(null);
    const load = useCallback(async () => {
        if (!auth.user)
            return;
        try {
            const data = await finlitApi.overview();
            setOverview(data);
            setView((v) => (v === "landing" ? "home" : v));
        }
        catch (err) {
            setError((err as Error).message);
        }
    }, [auth.user]);
    useEffect(() => {
        if (!auth.user) {
            setView("landing");
            return;
        }
        void load();
    }, [auth.user, load]);
    if (!auth.user)
        return <Landing />;
    if (!overview) {
        return (<div style={{ display: "grid", placeItems: "center", minHeight: "40vh" }}>
        <Spinner size={26}/>
        {error && <ErrorBanner message={error}/>}
      </div>);
    }
    const p = overview.profile;
    return (<div>
      <nav className="spread" style={{ padding: "14px 0", gap: 8, flexWrap: "wrap" }}>
        <div className="row" style={{ gap: 8, flexWrap: "wrap" }}>
        {([
            ["home", "Dashboard"],
            ["learn", "Learn"],
            ["sim", "Money moves"],
            ["planner", "Planner"],
            ["goals", "Goals"],
        ] as [
            View,
            string
        ][]).map(([v, label]) => (<button key={v} className={cx("btn", view === v ? "btn-primary" : "btn-secondary", "btn-sm")} onClick={() => setView(v)}>
            {label}
          </button>))}
        </div>
        <div className="row" style={{ gap: 8 }}>
          <span style={{ fontSize: 13, color: "var(--text-2)" }}>{auth.user.display_name}</span>
          <Button variant="ghost" size="sm" onClick={() => void auth.logout()}>Sign out</Button>
        </div>
      </nav>
      {error && <ErrorBanner message={error}/>}
      {view === "home" && (<div className="page">
          <div className="spread">
            <div>
              <h1 style={{ margin: 0 }}>Your money skills</h1>
              <p style={{ color: "var(--text-2)", margin: "8px 0 0" }}>
                Learn → decide → save. Outcomes are measured, not vibes.
              </p>
            </div>
            <div className="row">
              <Badge tone={p.streak > 0 ? "success" : "neutral"}>🔥 {p.streak}-day streak</Badge>
              <Badge tone="accent">sim score {qualityLabel(p.sim.quality)}</Badge>
            </div>
          </div>

          <div className="grid-2">
            <Card className="stack">
              <span className="spread">
                <h3 style={{ margin: 0 }}>Assessment</h3>
                <Badge tone={p.post_taken && p.score_gain > 0 ? "success" : "neutral"}>{p.pre_taken ? `baseline ${pct(p.pre_score)}` : "no baseline"}{p.post_taken ? ` → now ${pct(p.post_score)}` : ""}</Badge>
              </span>
              <ProgressBar value={p.post_taken ? p.post_score : p.pre_score} label={p.post_taken ? `Latest · ${pct(p.post_score)}` : p.pre_taken ? `Baseline · ${pct(p.pre_score)}` : "Not measured yet"}/>
              <p style={{ margin: 0, fontSize: 13, color: "var(--text-2)" }}>
                {p.post_taken
                ? p.score_gain > 0
                    ? `You gained ${Math.round(p.score_gain)} points since the baseline.`
                    : "No gain yet — review the modules you found hardest and retake."
                : p.pre_taken
                ? "Baseline set. Finish the modules, then take the post-assessment."
                : "Take the 6-question baseline first so your progress is measurable."}
              </p>
              <div className="row" style={{ gap: 8, flexWrap: "wrap" }}>
                {!p.pre_taken && <Button size="sm" onClick={() => setView("assess_pre")}>Take baseline</Button>}
                {p.pre_taken && <Button size="sm" variant={overview.modules_done > 0 ? "primary" : "secondary"} onClick={() => setView("assess_post")}>{p.post_taken ? "Retake post-assessment" : "Post-assessment"}</Button>}
              </div>
            </Card>
            <Card className="stack">
              <span className="spread">
                <h3 style={{ margin: 0 }}>Learning</h3>
                <Badge tone="success">{overview.modules_done}/{overview.modules_total} modules done</Badge>
              </span>
              <ProgressBar value={(overview.modules_done / overview.modules_total) * 100} label="modules completed"/>
              <Button onClick={() => setView("learn")}>Continue learning</Button>
            </Card>
          </div>

          <div className="grid-2">
            <Card className="stack">
              <span className="spread">
                <h3 style={{ margin: 0 }}>Money moves</h3>
                <Badge tone="neutral">{p.sim.decisions} decisions</Badge>
              </span>
              <div className="row">
                <Badge tone="success">wallet {money(p.sim.balance)}</Badge>
                <Badge tone={p.sim.debt > 0 ? "danger" : "success"}>debt {money(p.sim.debt)}</Badge>
                <Badge tone="accent">confidence {p.sim.confidence}/100</Badge>
              </div>
              <Button variant="secondary" onClick={() => setView("sim")}>Play scenarios</Button>
            </Card>
            <Card className="stack">
              <span className="spread">
                <h3 style={{ margin: 0 }}>Savings goals</h3>
                <Badge tone="neutral">{overview.goals.length} active</Badge>
              </span>
              {overview.goals.length === 0 ? (<p style={{ margin: 0, color: "var(--text-2)", fontSize: 14 }}>
                  Name a goal and the math does the rest.
                </p>) : (overview.goals.slice(0, 3).map((g) => (<div key={g.id}>
                    <div className="spread" style={{ fontSize: 13 }}>
                      <strong>{g.name}</strong>
                      <span style={{ color: "var(--text-2)" }}>
                        {money(g.contributed)} / {money(g.target)}
                      </span>
                    </div>
                    <ProgressBar value={g.progress}/>
                  </div>)))}
              <Button variant="secondary" onClick={() => setView("goals")}>Manage goals</Button>
            </Card>
          </div>
        </div>)}
      {view === "home" && <div style={{ marginTop: 16 }}><Coach compact /></div>}
      {view === "assess_pre" && <Assessment kind="pre" onDone={() => void load()} onBack={() => setView("home")}/>}
      {view === "assess_post" && <Assessment kind="post" onDone={() => void load()} onBack={() => setView("home")}/>}
      {view === "learn" && <Learn onDone={() => void load()}/>}
      {view === "planner" && <Planner onDone={() => void load()}/>}
      {view === "sim" && <Sim onDone={() => void load()}/>}
      {view === "goals" && <Goals onDone={() => void load()}/>}
    </div>);
}
function Landing() {
    const auth = useAuth();
    const [mode, setMode] = useState<"login" | "register">("login");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [name, setName] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [busy, setBusy] = useState(false);
    async function submit() {
        if (!email || !password || (mode === "register" && !name)) {
            setError("Fill in all fields.");
            return;
        }
        setBusy(true);
        setError(null);
        try {
            if (mode === "login")
                await auth.login(email, password);
            else
                await auth.register(email, password, name);
        }
        catch (err) {
            setError((err as Error).message);
        }
        finally {
            setBusy(false);
        }
    }
    return (<div>
      <section style={{ textAlign: "center", padding: "var(--space-8) var(--space-4)", display: "grid", gap: 16, justifyItems: "center" }}>
        <Badge tone="success">Money skills for students · GatewayHacks 2026</Badge>
        <h1 style={{ fontSize: "clamp(30px, 6vw, 50px)", maxWidth: 780, margin: 0 }}>
          Money is a skill. <span style={{ color: "var(--accent)" }}>Practice it.</span>
        </h1>
        <p style={{ maxWidth: 620, color: "var(--text-2)", fontSize: 17, margin: 0 }}>
          Short lessons, decisions with real consequences, and a savings planner with honest math —
          built to move your financial knowledge from vague to measurable.
        </p>
      </section>

      <div className="grid-2" style={{ maxWidth: 900, margin: "0 auto" }}>
        {[
            ["📚", "Learn", "Eight short modules: budgets, saving, credit, spending traps, investing, goal math, earning, and scam safety — each with a 3-question check that explains every answer."],
            ["🎮", "Decide", "Run 'Money Moves' — real-life scenarios where every choice moves your wallet, debt and confidence."],
            ["🧮", "Apply it", "The Planner takes your real allowance or paycheck, in your currency, and compares it with the 50/30/20 guide. A coach explains what to change."],
        ].map(([icon, title, body], i) => (<Card key={title} style={{ textAlign: "left" }}>
            <div style={{ fontSize: 28 }}>{icon}</div>
            <h3 style={{ margin: "10px 0 6px" }}>{i + 1}. {title}</h3>
            <p style={{ margin: 0, fontSize: 14, color: "var(--text-2)" }}>{body}</p>
          </Card>))}
      </div>

      <div style={{ maxWidth: 460, margin: "var(--space-7) auto 0" }}>
        <Card className="stack">
          <h3 style={{ margin: 0 }}>{mode === "login" ? "Welcome back" : "Create an account"}</h3>
          <ErrorBanner message={error}/>
          {mode === "register" && <Input label="Name" value={name} onChange={(e) => setName(e.target.value)}/>}
          <Input label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)}/>
          <Input label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)}/>
          <Button size="lg" loading={busy} onClick={() => void submit()}>
            {mode === "login" ? "Log in" : "Create account"}
          </Button>
          <button className="btn btn-ghost" style={{ width: "100%" }} onClick={() => setMode(mode === "login" ? "register" : "login")}>
            {mode === "login" ? "New here? Create an account" : "Have an account? Log in"}
          </button>
          {mode === "login" && (<p style={{ fontSize: 12, color: "var(--text-3)", margin: 0, textAlign: "center" }}>
              Demo account: demo@example.com · demo-password-123
            </p>)}
        </Card>
      </div>
    </div>);
}
