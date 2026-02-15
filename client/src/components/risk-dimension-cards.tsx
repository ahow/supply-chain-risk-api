import { Card, CardContent } from "@/components/ui/card";
import { RiskScoreBadge, getRiskBgColor } from "./risk-score-badge";
import { Progress } from "@/components/ui/progress";
import type { RiskContribution } from "@shared/schema";
import { Cloud, Users, Shield, Droplets, Leaf } from "lucide-react";

const dimensions = [
  { key: "climate" as const, label: "Climate", icon: Cloud, description: "Physical climate hazard exposure" },
  { key: "modern_slavery" as const, label: "Modern Slavery", icon: Users, description: "Forced labor and trafficking prevalence" },
  { key: "political" as const, label: "Political", icon: Shield, description: "Stability and institutional quality" },
  { key: "water_stress" as const, label: "Water Stress", icon: Droplets, description: "Water demand vs. supply ratio" },
  { key: "nature_loss" as const, label: "Nature Loss", icon: Leaf, description: "Ecosystem and biodiversity degradation" },
];

interface RiskDimensionCardsProps {
  directRisk: RiskContribution;
  indirectRisk: RiskContribution;
  totalRisk: RiskContribution;
}

export function RiskDimensionCards({ directRisk, indirectRisk, totalRisk }: RiskDimensionCardsProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
      {dimensions.map(({ key, label, icon: Icon, description }) => {
        const total = totalRisk[key];
        return (
          <Card key={key} className={getRiskBgColor(total)} data-testid={`card-risk-${key}`}>
            <CardContent className="p-4">
              <div className="flex items-start justify-between gap-2 mb-3">
                <div className="flex items-center gap-2">
                  <Icon className="w-4 h-4 text-muted-foreground" />
                  <span className="text-sm font-medium">{label}</span>
                </div>
              </div>
              <div className="mb-3">
                <RiskScoreBadge score={total} />
              </div>
              <Progress value={(total / 5) * 100} className="h-1.5 mb-3" />
              <div className="space-y-1 text-xs text-muted-foreground">
                <div className="flex justify-between">
                  <span>Direct</span>
                  <span className="font-mono">{directRisk[key].toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Indirect</span>
                  <span className="font-mono">{indirectRisk[key].toFixed(2)}</span>
                </div>
              </div>
              <p className="text-xs text-muted-foreground mt-2 leading-relaxed">{description}</p>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
