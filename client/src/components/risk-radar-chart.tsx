import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from "recharts";
import type { RiskContribution } from "@shared/schema";

interface RiskRadarChartProps {
  directRisk: RiskContribution;
  indirectRisk: RiskContribution;
  totalRisk: RiskContribution;
}

const dimensionLabels: Record<string, string> = {
  climate: "Climate",
  modern_slavery: "Modern Slavery",
  political: "Political",
  water_stress: "Water Stress",
  nature_loss: "Nature Loss",
};

export function RiskRadarChart({ directRisk, indirectRisk, totalRisk }: RiskRadarChartProps) {
  const data = Object.keys(dimensionLabels).map((key) => ({
    dimension: dimensionLabels[key],
    direct: directRisk[key as keyof RiskContribution],
    indirect: indirectRisk[key as keyof RiskContribution],
    total: totalRisk[key as keyof RiskContribution],
  }));

  return (
    <ResponsiveContainer width="100%" height={320}>
      <RadarChart data={data} cx="50%" cy="50%" outerRadius="72%">
        <PolarGrid stroke="hsl(var(--border))" />
        <PolarAngleAxis
          dataKey="dimension"
          tick={{ fill: "hsl(var(--foreground))", fontSize: 11 }}
        />
        <PolarRadiusAxis
          angle={90}
          domain={[0, 5]}
          tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 10 }}
          tickCount={6}
        />
        <Radar
          name="Direct"
          dataKey="direct"
          stroke="hsl(var(--chart-1))"
          fill="hsl(var(--chart-1))"
          fillOpacity={0.15}
          strokeWidth={2}
        />
        <Radar
          name="Indirect"
          dataKey="indirect"
          stroke="hsl(var(--chart-2))"
          fill="hsl(var(--chart-2))"
          fillOpacity={0.1}
          strokeWidth={2}
        />
        <Radar
          name="Total"
          dataKey="total"
          stroke="hsl(var(--chart-4))"
          fill="hsl(var(--chart-4))"
          fillOpacity={0.08}
          strokeWidth={2}
          strokeDasharray="5 5"
        />
        <Legend
          wrapperStyle={{ fontSize: 12, paddingTop: 8 }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: "hsl(var(--card))",
            borderColor: "hsl(var(--border))",
            borderRadius: 6,
            fontSize: 12,
          }}
          formatter={(value: number) => value.toFixed(2)}
        />
      </RadarChart>
    </ResponsiveContainer>
  );
}
