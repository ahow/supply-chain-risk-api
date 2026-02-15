import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { HazardBreakdownChart } from "./risk-bar-chart";
import { DollarSign, TrendingDown, Calendar } from "lucide-react";
import type { ExpectedLoss } from "@shared/schema";

interface FinancialImpactCardProps {
  expectedLoss: ExpectedLoss;
}

export function FinancialImpactCard({ expectedLoss }: FinancialImpactCardProps) {
  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-base">
          <DollarSign className="w-4 h-4 text-muted-foreground" />
          Financial Impact Assessment
        </CardTitle>
        <p className="text-xs text-muted-foreground">
          Per $1M asset value, based on probabilistic catastrophe modeling
        </p>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
          <div className="flex items-start gap-3 p-3 rounded-md bg-card">
            <TrendingDown className="w-5 h-5 text-destructive mt-0.5" />
            <div>
              <p className="text-xs text-muted-foreground">Annual Expected Loss</p>
              <p className="text-lg font-semibold font-mono">
                ${expectedLoss.total_annual_loss.toLocaleString(undefined, { maximumFractionDigits: 0 })}
              </p>
            </div>
          </div>
          <div className="flex items-start gap-3 p-3 rounded-md bg-card">
            <DollarSign className="w-5 h-5 text-orange-500 dark:text-orange-400 mt-0.5" />
            <div>
              <p className="text-xs text-muted-foreground">% of Asset Value</p>
              <p className="text-lg font-semibold font-mono">
                {expectedLoss.total_annual_loss_pct.toFixed(2)}%
              </p>
            </div>
          </div>
          <div className="flex items-start gap-3 p-3 rounded-md bg-card">
            <Calendar className="w-5 h-5 text-muted-foreground mt-0.5" />
            <div>
              <p className="text-xs text-muted-foreground">30-Year Present Value</p>
              <p className="text-lg font-semibold font-mono">
                ${(expectedLoss.present_value_30yr / 1000).toFixed(0)}k
              </p>
            </div>
          </div>
        </div>
        <Separator className="my-4" />
        <p className="text-sm font-medium mb-3">Loss by Hazard Type</p>
        <HazardBreakdownChart breakdown={expectedLoss.risk_breakdown} />
      </CardContent>
    </Card>
  );
}
