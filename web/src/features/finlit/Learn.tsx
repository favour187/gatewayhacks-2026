import { useEffect, useState } from "react";
import { finlitApi } from "./api";
import { pct } from "./format";
import { Badge, Button, Card, ProgressBar, Spinner, cx } from "../../ui/components";
import type { ModuleDetail, ModuleDTO } from "./types";
export function Learn({ onDone }: {
    onDone: () => void;
}) {
    const [modules, setModules] = useState<ModuleDTO[]>([]);
    const [active, setActive] = useState<string | null>(null);
    const [detail, setDetail] = useState<ModuleDetail | null>(null);
    const [chosen, setChosen] = useState<Record<string, number>>({});
    const [result, setResult] = useState<Awaited<ReturnType<typeof finlitApi.grade>> | null>(null);
    const [busy, setBusy] = useState(false);
    useEffect(() => {
        void finlitApi.modules().then((r) => setModules(r.modules));
    }, []);
    async function open(moduleId: string) {
        setActive(moduleId);
        setResult(null);
        setChosen({});
        const d = await finlitApi.module(moduleId);
        setDetail(d);
    }
    async function submit() {
        if (!detail)
            return;
        const answers = detail.quiz.map((q) => ({
            question_id: q.question_id,
            chosen_index: chosen[q.question_id] ?? 0,
        }));
        setBusy(true);
        try {
            const res = await finlitApi.grade(detail.module_id, answers);
            setResult(res);
            onDone();
        }
        finally {
            setBusy(false);
        }
    }
    if (!active || !detail) {
        return (<div className="page">
        {modules.length === 0 ? (<Spinner />) : (<div className="grid-2">
            {modules.map((m) => (<Card key={m.module_id} className="stack">
                <div className="spread">
                  <h3 style={{ margin: 0 }}>{m.title}</h3>
                  {m.progress?.completed ? <Badge tone="success">done</Badge> : <Badge tone="neutral">{m.quiz_count} questions</Badge>}
                </div>
                <p style={{ margin: 0, fontSize: 14, color: "var(--text-2)" }}>{m.topic}</p>
                {m.progress && <ProgressBar value={m.progress.best_score} label={`best · ${pct(m.progress.best_score)}`}/>}
                <Button variant="secondary" onClick={() => void open(m.module_id)}>
                  {m.progress ? "Review" : "Start"}
                </Button>
              </Card>))}
          </div>)}
      </div>);
    }
    return (<div className="page" style={{ maxWidth: 720, margin: "0 auto" }}>
      <div className="spread">
        <div>
          <Button variant="ghost" size="sm" onClick={() => setActive(null)}>
            ← All modules
          </Button>
          <h1 style={{ margin: "6px 0 0" }}>{detail.title}</h1>
          <p style={{ color: "var(--text-2)", margin: "6px 0 0" }}>{detail.topic}</p>
        </div>
        {result?.passed !== undefined && (<Badge tone={result.passed ? "success" : "warning"}>{result.passed ? "passed" : "try again"}</Badge>)}
      </div>

      {!result && (<Card className="stack">
          {detail.lessons.map((lesson, i) => (<div key={i} className="row" style={{ alignItems: "flex-start", gap: 10 }}>
              <Badge tone="accent">{i + 1}</Badge>
              <p style={{ margin: 0, fontSize: 15 }}>{lesson}</p>
            </div>))}
        </Card>)}

      <h3 style={{ margin: "4px 0" }}>Check yourself</h3>
      <div className="stack">
        {detail.quiz.map((q, qi) => {
            const explanation = result?.explanations.find((e) => e.question_id === q.question_id);
            return (<Card key={q.question_id} className="stack">
              <p style={{ margin: 0, fontWeight: 600 }}>{qi + 1}. {q.stem}</p>
              <div className="stack">
                {q.options.map((option, oi) => (<button key={oi} className={cx("btn", !result && chosen[q.question_id] === oi ? "btn-primary" : "btn-secondary")} style={{ justifyContent: "flex-start", whiteSpace: "normal" }} disabled={!!result} onClick={() => setChosen((c) => ({ ...c, [q.question_id]: oi }))}>
                    {option}
                  </button>))}
              </div>
              {explanation && result && (<div style={{ fontSize: 13, color: "var(--text-2)" }}>
                  <strong>{explanation.correct_answer}</strong> — {explanation.explanation}
                </div>)}
            </Card>);
        })}
      </div>

      {result ? (<div className="stack">
          <Card style={{ textAlign: "center" }}>
            <h3 style={{ margin: "0 0 8px" }}>{result.detail.score}%</h3>
            <p style={{ margin: 0, color: "var(--text-2)" }}>
              {result.detail.correct} of {result.detail.total} correct.{" "}
              {result.passed ? "Module complete." : "Score 60%+ to complete the module."}
            </p>
          </Card>
          <div className="row">
            <Button onClick={() => void open(detail.module_id)}>Retry</Button>
            <Button variant="secondary" onClick={() => setActive(null)}>
              Back to modules
            </Button>
          </div>
        </div>) : (<Button size="lg" loading={busy} onClick={() => void submit()}>
          Grade answers
        </Button>)}
    </div>);
}
