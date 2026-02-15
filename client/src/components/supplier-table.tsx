import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { RiskScoreBadge, getRiskColor } from "./risk-score-badge";
import type { Supplier } from "@shared/schema";
import { TrendingUp, Globe, Factory } from "lucide-react";

interface SupplierTableProps {
  suppliers: Supplier[];
}

export function SupplierTable({ suppliers }: SupplierTableProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between gap-2 space-y-0 pb-3">
        <CardTitle className="flex items-center gap-2 text-base">
          <TrendingUp className="w-4 h-4 text-muted-foreground" />
          Top Suppliers by I-O Coefficient
        </CardTitle>
      </CardHeader>
      <CardContent className="p-0">
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
              {suppliers.map((supplier, index) => (
                <TableRow key={index} data-testid={`row-supplier-${index}`}>
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
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
}
