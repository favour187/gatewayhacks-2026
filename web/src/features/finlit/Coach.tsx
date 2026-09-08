import { useState } from "react";
import { finlitApi } from "./api";
import { Badge, Button, Card, Input } from "../../ui/components";

const PROMPTS = [
  "How is my budget looking?",
  "Where do my goals stand?",
  "What should I do next?",
  "What is compound interest?",
  "Is buy-now-pay-later a bad idea?",
];

interface Turn {
  role: "user" | "coach";
  text: string;
  provider?: string;
}

export function Coach({ compact = false }: { compact?: boolean }) {
  const [turns, setTurns] = useState<Turn[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);

  async function ask(message: string) {
    if (!message.trim() || busy) return;
    setTurns((t) => [...t, { role: "user", text: message }]);
    setInput("");
    setBusy(true);
    try {
      const res = await finlitApi.coach(message);
      setTurns((t) => [...t, { role: "coach", text: res.reply, provider: res.provider }]);
    } catch (err) {
      setTurns((t) => [...t, { role: "coach", text: `Sorry — ${(err as Error).message}` }]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <Card className="stack">
      <div className="spread" style={{ flexWrap: "wrap", gap: 8 }}>
        <h3 style={{ margin: 0 }}>Money coach</h3>
        <span style={{ fontSize: 12, color: "var(--text-3)" }}>Answers use your own plan, goals and scores · works offline</span>
      </div>
      <div className="row" style={{ gap: 6, flexWrap: "wrap" }}>
        {PROMPTS.slice(0, compact ? 3 : PROMPTS.length).map((p) => (
          <button key={p} className="btn btn-ghost btn-sm" onClick={() => void ask(p)} disabled={busy}>{p}</button>
        ))}
      </div>
      {turns.length > 0 && (
        <div style={{ display: "grid", gap: 8, maxHeight: 340, overflowY: "auto" }}>
          {turns.map((t, i) => (
            <div key={i} style={{ justifySelf: t.role === "user" ? "end" : "start", maxWidth: "92%", padding: "10px 12px", borderRadius: "var(--radius)", background: t.role === "user" ? "var(--accent)" : "var(--surface-2)", color: t.role === "user" ? "#fff" : "var(--text)", whiteSpace: "pre-wrap", fontSize: 14, lineHeight: 1.5 }}>
              {t.text}
              {t.provider && <div style={{ marginTop: 6 }}><Badge tone="neutral">{t.provider === "local-demo" ? "offline coach" : t.provider}</Badge></div>}
            </div>
          ))}
        </div>
      )}
      <form className="row" style={{ gap: 8, alignItems: "flex-end" }} onSubmit={(e) => { e.preventDefault(); void ask(input); }}>
        <div style={{ flex: 1 }}>
          <Input placeholder="Ask about budgets, goals, debt, saving…" value={input} onChange={(e) => setInput(e.target.value)} />
        </div>
        <Button type="submit" loading={busy} disabled={!input.trim()}>Ask</Button>
      </form>
    </Card>
  );
}
