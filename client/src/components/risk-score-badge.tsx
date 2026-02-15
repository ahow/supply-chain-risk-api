import { Badge } from "@/components/ui/badge";

function getRiskLevel(score: number): { label: string; className: string } {
  if (score <= 1) return { label: "Low", className: "bg-emerald-600 dark:bg-emerald-500 text-white border-emerald-700 dark:border-emerald-400" };
  if (score <= 2) return { label: "Moderate", className: "bg-yellow-500 dark:bg-yellow-500 text-white border-yellow-600 dark:border-yellow-400" };
  if (score <= 3) return { label: "Elevated", className: "bg-orange-500 dark:bg-orange-500 text-white border-orange-600 dark:border-orange-400" };
  if (score <= 4) return { label: "High", className: "bg-red-600 dark:bg-red-500 text-white border-red-700 dark:border-red-400" };
  return { label: "Extreme", className: "bg-red-800 dark:bg-red-700 text-white border-red-900 dark:border-red-600" };
}

interface RiskScoreBadgeProps {
  score: number;
  showScore?: boolean;
}

export function RiskScoreBadge({ score, showScore = true }: RiskScoreBadgeProps) {
  const { label, className } = getRiskLevel(score);
  return (
    <Badge className={`no-default-hover-elevate no-default-active-elevate ${className}`}>
      {showScore ? `${score.toFixed(2)} - ${label}` : label}
    </Badge>
  );
}

export function getRiskColor(score: number): string {
  if (score <= 1) return "text-emerald-600 dark:text-emerald-400";
  if (score <= 2) return "text-yellow-600 dark:text-yellow-400";
  if (score <= 3) return "text-orange-600 dark:text-orange-400";
  if (score <= 4) return "text-red-600 dark:text-red-400";
  return "text-red-800 dark:text-red-300";
}

export function getRiskBgColor(score: number): string {
  if (score <= 1) return "bg-emerald-50 dark:bg-emerald-950/30";
  if (score <= 2) return "bg-yellow-50 dark:bg-yellow-950/30";
  if (score <= 3) return "bg-orange-50 dark:bg-orange-950/30";
  if (score <= 4) return "bg-red-50 dark:bg-red-950/30";
  return "bg-red-100 dark:bg-red-950/50";
}
