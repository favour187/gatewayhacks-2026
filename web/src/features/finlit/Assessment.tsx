import { useEffect, useState } from "react";
import { finlitApi } from "./api";
import { Badge, Button, Card, Spinner, cx } from "../../ui/components";

type Result = Awaited<ReturnType<typeof finlitApi.assess>>;

export function Assessment({ kind, onDone, onBack }: { kind: "pre" | "post"; onDone: () => void; onBack: () => void }) {
  const [questions, setQuestions] = useState<{ question_id: string; stem: string; options: string[] }[] | null>(null);
  const [chosen, setChosen] = useState<Record<string, number>>({});
  const [result, setResult] = useState<Result | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    void finlitApi.assessment().then((r) => setQuestions(r.questions));
  }, []);

  async function submit() {
    if (!questions) return;
    setBusy(true);
    try {
      const res = await finlitApi.assess(kind, questions.map((q) => ({ question_id: q.question_id, chosen_index: chosen[q.question_id] ?? 0 })));
      setResult(res);
      onDone();
    } finally {
      setBusy(false);
    }
  }

  if (!questions) return <Spinner />;
  const answered = questions.filter((q) => chosen[q.question_id] !== undefined).length;

  return (
    <div className="page" style={{ maxWidth: 720, margin: "0 auto" }}>
      <div className="spread">
        <div>
          <Button variant="ghost" size="sm" onClick={onBack}>← Back</Button>
          <h1 style={{ margin: "6px 0 0" }}>{kind === "pre" ? "Baseline check" : "Post-assessment"}</h1>
          <p style={{ color: "var(--text-2)", margin: "6px 0 0" }}>
            {kind === "pre"
              ? "Six quick questions before you start. No studying — this is the 'before' photo."
              : "Same six questions after the modules. The difference is your measured gain."}
          </p>
        </div>
        {result && <Badge tone="success">{result.score}%</Badge>}
      </div>
      <div className="stack">
        {questions.map((q, qi) => {
          const ex = result?.explanations.find((e) => e.question_id === q.question_id);
          return (
            <Card key={q.question_id} className="stack">
              <p style={{ margin: 0, fontWeight: 600 }}>{qi + 1}. {q.stem}</p>
              <div className="stack">
                {q.options.map((option, oi) => (
                  <button
                    key={oi}
                    className={cx("btn", !result && chosen[q.question_id] === oi ? "btn-primary" : "btn-secondary")}
                    style={{ justifyContent: "flex-start", whiteSpace: "normal", borderColor: ex ? (option === ex.correct_answer ? "var(--success)" : ex.chosen_index === oi ? "var(--danger)" : undefined) : undefined }}
                    disabled={!!result}
                    onClick={() => setChosen((c) => ({ ...c, [q.question_id]: oi }))}
                  >
                    {option}
                  </button>
                ))}
              </div>
              {ex && (
                <div style={{ fontSize: 13, color: "var(--text-2)" }}>
                  <Badge tone={ex.correct ? "success" : "danger"}>{ex.correct ? "correct" : "not quite"}</Badge> <strong>{ex.correct_answer}</strong> — {ex.explanation}
                </div>
              )}
            </Card>
          );
        })}
      </div>
      {result ? (
        <Card style={{ textAlign: "center" }}>
          <h3 style={{ margin: "0 0 8px" }}>{result.correct} of {result.total} correct · {result.score}%</h3>
          <p style={{ margin: "0 0 12px", color: "var(--text-2)" }}>
            {kind === "pre" ? "Baseline saved. Now work through the modules — then take the post-assessment to see the gain." : "Saved. Compare with your baseline on the dashboard."}
          </p>
          <Button onClick={onBack}>Back to dashboard</Button>
        </Card>
      ) : (
        <Button size="lg" loading={busy} disabled={answered < questions.length} onClick={() => void submit()}>
          {answered < questions.length ? `Answer all ${questions.length} (${answered} done)` : "Submit"}
        </Button>
      )}
    </div>
  );
}
