import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { RiskScoreBadge, getRiskColor } from "./risk-score-badge";
import type { TierSummary, Supplier } from "@shared/schema";
import { TrendingUp, Globe, Factory, Layers } from "lucide-react";
import { useState } from "react";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { ChevronDown, ChevronRight } from "lucide-react";

const tierLabels: Record<number, string> = {
  1: "Tier 1 — Direct Suppliers",
  2: "Tier 2 — Sub-suppliers",
  3: "Tier 3 — Deep Supply Chain",
};

const tierColors: Record<number, string> = {
  1: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
  2: "bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200",
  3: "bg-slate-100 text-slate-800 dark:bg-slate-900 dark:text-slate-200",
};

interface SupplierTableProps {
  tiers: TierSummary[];
}

function SupplierRow({ supplier, index }: { supplier: Supplier; index: number }) {
  return (
    <TableRow key={index} data-testid={`row-supplier-${supplier.tier}-${index}`}>
      <TableCell className="pl-6">
        <div className="flex flex-col gap-0.5">
          <span className="flex items-center gap-1.5 font-medium text-sm">
            <Globe className="w-3.5 h-3.5 text-muted-foreground" />
            {supplier.country_name}
          </span>
          <span className="flex items-center gap-1.5 text-xs text-muted-foreground">
            <Factory className="w-3 h-3" />
            {supplier.sector_name}
          </span>
        </div>
      </TableCell>
      <TableCell>
        <span className="font-mono text-sm">
          {(supplier.coefficient * 100).toFixed(2)}%
        </span>
      </TableCell>
      <TableCell>
        <span className={`font-mono text-sm ${getRiskColor(supplier.direct_risk.climate)}`}>
          {supplier.direct_risk.climate.toFixed(2)}
        </span>
      </TableCell>
      <TableCell>
        <span className={`font-mono text-sm ${getRiskColor(supplier.direct_risk.modern_slavery)}`}>
          {supplier.direct_risk.modern_slavery.toFixed(2)}
        </span>
      </TableCell>
      <TableCell>
        <span className={`font-mono text-sm ${getRiskColor(supplier.direct_risk.political)}`}>
          {supplier.direct_risk.political.toFixed(2)}
        </span>
      </TableCell>
      <TableCell>
        <span className={`font-mono text-sm ${getRiskColor(supplier.direct_risk.water_stress)}`}>
          {supplier.direct_risk.water_stress.toFixed(2)}
        </span>
      </TableCell>
      <TableCell>
        <span className={`font-mono text-sm ${getRiskColor(supplier.direct_risk.nature_loss)}`}>
          {supplier.direct_risk.nature_loss.toFixed(2)}
        </span>
      </TableCell>
      <TableCell className="pr-6 text-right">
        {supplier.expected_loss_contribution ? (
          <span className="font-mono text-sm">
            ${supplier.expected_loss_contribution.annual_loss.toLocaleString(undefined, {
              maximumFractionDigits: 0,
            })}
          </span>
        ) : (
          <span className="text-muted-foreground text-xs">N/A</span>
        )}
      </TableCell>
    </TableRow>
  );
}

export function SupplierTable({ tiers }: SupplierTableProps) {
  const [openTiers, setOpenTiers] = useState<Record<number, boolean>>({ 1: true, 2: false, 3: false });

  const toggleTier = (tier: number) => {
    setOpenTiers((prev) => ({ ...prev, [tier]: !prev[tier] }));
  };

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between gap-2 space-y-0 pb-3">
        <CardTitle className="flex items-center gap-2 text-base">
          <Layers className="w-4 h-4 text-muted-foreground" />
          Supply Chain Exposure by Tier
        </CardTitle>
        <div className="flex gap-2">
          {tiers.map((tier) => (
            <Badge key={tier.tier} variant="outline" className="text-xs">
              T{tier.tier}: {(tier.weight * 100)}% weight
            </Badge>
          ))}
        </div>
      </CardHeader>
      <CardContent className="p-0">
        {tiers.map((tier) => (
          <Collapsible
            key={tier.tier}
            open={openTiers[tier.tier]}
            onOpenChange={() => toggleTier(tier.tier)}
          >
            <CollapsibleTrigger className="w-full" data-testid={`trigger-tier-${tier.tier}`}>
              <div className="flex items-center justify-between px-6 py-3 border-b bg-muted/30 cursor-pointer">
                <div className="flex items-center gap-3">
                  {openTiers[tier.tier] ? (
                    <ChevronDown className="w-4 h-4 text-muted-foreground" />
                  ) : (
                    <ChevronRight className="w-4 h-4 text-muted-foreground" />
                  )}
                  <Badge className={tierColors[tier.tier]}>
                    {tierLabels[tier.tier]}
                  </Badge>
                  <span className="text-xs text-muted-foreground">
                    {tier.supplier_count} suppliers
                  </span>
                </div>
                <div className="flex items-center gap-4 text-xs text-muted-foreground">
                  <span>Avg risk: <span className="font-mono">{((tier.risk.climate + tier.risk.modern_slavery + tier.risk.political + tier.risk.water_stress + tier.risk.nature_loss) / 5).toFixed(2)}</span></span>
                  {tier.expected_loss && (
                    <span>EAL: <span className="font-mono">${tier.expected_loss.total_annual_loss.toLocaleString(undefined, { maximumFractionDigits: 0 })}</span></span>
                  )}
                </div>
              </div>
            </CollapsibleTrigger>
            <CollapsibleContent>
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="pl-6">Supplier</TableHead>
                      <TableHead>Coefficient</TableHead>
                      <TableHead>Climate</TableHead>
                      <TableHead>Slavery</TableHead>
                      <TableHead>Political</TableHead>
                      <TableHead>Water</TableHead>
                      <TableHead>Nature</TableHead>
                      <TableHead className="pr-6 text-right">Loss Contribution</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {tier.suppliers.map((supplier, index) => (
                      <SupplierRow key={index} supplier={supplier} index={index} />
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CollapsibleContent>
          </Collapsible>
        ))}
      </CardContent>
    </Card>
  );
}
