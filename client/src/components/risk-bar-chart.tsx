import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Cell,
} from "recharts";

interface HazardBreakdownProps {
  breakdown: {
    hurricane: { annual_loss: number; annual_loss_pct: number };
    flood: { annual_loss: number; annual_loss_pct: number };
    heat_stress: { annual_loss: number; annual_loss_pct: number };
    drought: { annual_loss: number; annual_loss_pct: number };
    extreme_precipitation: { annual_loss: number; annual_loss_pct: number };
  };
}

const hazardColors = [
  "hsl(var(--chart-1))",
  "hsl(var(--chart-2))",
  "hsl(var(--chart-5))",
  "hsl(var(--chart-3))",
  "hsl(var(--chart-4))",
];

const hazardLabels: Record<string, string> = {
  hurricane: "Hurricane",
  flood: "Flood",
  heat_stress: "Heat Stress",
  drought: "Drought",
  extreme_precipitation: "Extreme Precip.",
};

export function HazardBreakdownChart({ breakdown }: HazardBreakdownProps) {
  const data = Object.entries(breakdown).map(([key, val]) => ({
    hazard: hazardLabels[key] || key,
    annual_loss: val.annual_loss,
    annual_loss_pct: val.annual_loss_pct,
  }));

  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={data} layout="vertical" margin={{ left: 8, right: 16, top: 4, bottom: 4 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" horizontal={false} />
        <XAxis
          type="number"
          tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 11 }}
          tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
        />
        <YAxis
          dataKey="hazard"
          type="category"
          tick={{ fill: "hsl(var(--foreground))", fontSize: 11 }}
          width={100}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: "hsl(var(--card))",
            borderColor: "hsl(var(--border))",
            borderRadius: 6,
            fontSize: 12,
          }}
          formatter={(value: number) => [`$${value.toLocaleString()}`, "Annual Loss"]}
        />
        <Bar dataKey="annual_loss" radius={[0, 4, 4, 0]} maxBarSize={28}>
          {data.map((_, index) => (
            <Cell key={index} fill={hazardColors[index % hazardColors.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
