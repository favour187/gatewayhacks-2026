export interface SimState {
    balance: number;
    debt: number;
    confidence: number;
    decisions: number;
    quality: number;
}
export interface Profile {
    pre_score: number;
    post_score: number;
    score_gain: number;
    streak: number;
    sim: SimState;
}
export interface ModuleProgress {
    module_id: string;
    best_score: number;
    attempts: number;
    completed: boolean;
    completed_at: string | null;
}
export interface ModuleDTO {
    module_id: string;
    title: string;
    topic: string;
    lessons: string[];
    quiz_count: number;
    progress: ModuleProgress | null;
}
export interface ModuleDetail extends ModuleDTO {
    quiz: {
        question_id: string;
        stem: string;
        options: string[];
    }[];
}
export interface GradeResult {
    module_id: string;
    title: string;
    passed: boolean;
    detail: {
        correct: number;
        total: number;
        score: number;
    };
    explanations: {
        question_id: string;
        chosen_index: number | null;
        correct_answer: string;
        explanation: string;
    }[];
    progress: ModuleProgress;
}
export interface ScenarioDTO {
    scenario_id: string;
    title: string;
    setup: string;
    choices: {
        choice_id: string;
        label: string;
    }[];
}
export interface SimHistoryItem {
    id: string;
    scenario_id: string;
    choice_id: string;
    delta: {
        money: number;
        debt: number;
        confidence: number;
        quality: number;
    };
    created_at: string;
}
export interface SimData {
    state: SimState;
    wallet: {
        balance: number;
        debt: number;
    };
    scenarios: ScenarioDTO[];
    history: SimHistoryItem[];
}
export interface Contribute {
    id: string;
    amount: number;
    created_at: string;
}
export interface Goal {
    id: string;
    name: string;
    target: number;
    weekly: number;
    apy: number;
    status: string;
    contributed: number;
    remaining: number;
    progress: number;
    months_to_target: number | null;
    target_eta: string | null;
    contributions: Contribute[];
    created_at: string;
}
export interface Overview {
    profile: Profile;
    modules: ModuleDTO[];
    modules_done: number;
    modules_total: number;
    goals: Goal[];
    sim_history_count: number;
}
