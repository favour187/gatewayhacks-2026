export function money(value: number): string {
    return `$${value.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 2 })}`;
}
export function pct(value: number): string {
    return `${Math.round(value)}%`;
}
export function signMoney(value: number): string {
    const s = value > 0 ? "+" : value < 0 ? "−" : "";
    return `${s}${money(Math.abs(value))}`;
}
export function qualityLabel(quality: number): string {
    if (quality >= 0.8)
        return "Sharp";
    if (quality >= 0.6)
        return "Solid";
    if (quality >= 0.4)
        return "Okay";
    return "Costly";
}
