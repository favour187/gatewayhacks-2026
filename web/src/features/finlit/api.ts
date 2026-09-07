import { api } from "../../lib/api";
import type { Goal, GradeResult, ModuleDetail, ModuleDTO, Overview, SimData } from "./types";
import type { SimHistoryItem as HistoryItem } from "./types";
export const finlitApi = {
    overview: () => api<Overview>("/finance/overview"),
    modules: () => api<{
        modules: ModuleDTO[];
    }>("/finance/modules"),
    module: (id: string) => api<ModuleDetail>(`/finance/modules/${id}`),
    grade: (id: string, answers: {
        question_id: string;
        chosen_index: number;
    }[]) => api<GradeResult>(`/finance/modules/${id}/grade`, { method: "POST", body: { answers } }),
    assess: (kind: "pre" | "post", answers: {
        question_id: string;
        chosen_index: number;
    }[]) => api<{
        kind: string;
        score: number;
        correct: number;
        total: number;
        profile: unknown;
    }>("/finance/assess", { method: "POST", body: { kind, answers } }),
    sim: () => api<SimData>("/finance/sim"),
    simulate: (scenario_id: string, choice_id: string) => api<{
        explanation: string;
        delta: {
            money: number;
            debt: number;
            confidence: number;
            quality: number;
        };
        state: SimData["state"];
        history: HistoryItem[];
    }>("/finance/simulate", { method: "POST", body: { scenario_id, choice_id } }),
    simReset: () => api<unknown>("/finance/sim/reset", { method: "POST" }),
    goals: () => api<{
        goals: Goal[];
    }>("/finance/goals"),
    createGoal: (input: {
        name: string;
        target: number;
        weekly: number;
        apy: number;
    }) => api<Goal>("/finance/goals", { method: "POST", body: input }),
    contribute: (goalId: string, amount: number) => api<Goal>(`/finance/goals/${goalId}/contribute`, { method: "POST", body: { amount } }),
};
