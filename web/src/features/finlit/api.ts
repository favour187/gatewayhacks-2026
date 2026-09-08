import { api } from "../../lib/api";
import type { CoachReply, FinancingOut, Goal, GradeResult, ModuleDetail, ModuleDTO, Overview, PlanIn, PlanResult, PlannerMeta, SavedPlan, SimData } from "./types";
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
    assessment: () => api<{ questions: { question_id: string; stem: string; options: string[] }[] }>("/finance/assessment"),
    assess: (kind: "pre" | "post", answers: {
        question_id: string;
        chosen_index: number;
    }[]) => api<{
        kind: string;
        score: number;
        correct: number;
        total: number;
        explanations: { question_id: string; chosen_index: number | null; correct: boolean; correct_answer: string; explanation: string }[];
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
    plannerMeta: () => api<PlannerMeta>("/finance/planner/meta"),
    plannerPreview: (plan: PlanIn) => api<PlanResult>("/finance/planner/preview", { method: "POST", body: plan }),
    plannerGet: () => api<{ plan: SavedPlan | null }>("/finance/planner"),
    plannerSave: (plan: PlanIn) => api<SavedPlan>("/finance/planner", { method: "PUT", body: plan }),
    financing: (price: number, monthly_payment: number, months: number) => api<FinancingOut>("/finance/planner/financing", { method: "POST", body: { price, monthly_payment, months } }),
    coach: (message: string, extra?: { plan?: PlanIn | null; financing?: { price: number; monthly_payment: number; months: number } | null }) => api<CoachReply>("/finance/coach", { method: "POST", body: { message, plan: extra?.plan ?? null, financing: extra?.financing ?? null } }),
};
