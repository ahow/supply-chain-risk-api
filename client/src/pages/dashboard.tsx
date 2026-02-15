import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { AssessmentForm } from "@/components/assessment-form";
import { RiskRadarChart } from "@/components/risk-radar-chart";
import { RiskDimensionCards } from "@/components/risk-dimension-cards";
import { FinancialImpactCard } from "@/components/financial-impact-card";
import { SupplierTable } from "@/components/supplier-table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { apiRequest } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";
import type { AssessmentResponse } from "@shared/schema";
import {
  ShieldAlert,
  Globe,
  Factory,
  Activity,
  AlertTriangle,
  BarChart3,
} from "lucide-react";

export default function Dashboard() {
  const [result, setResult] = useState<AssessmentResponse | null>(null);
  const { toast } = useToast();

  const assessMutation = useMutation({
    mutationFn: async (params: {
      country: string;
      sector: string;
      skip_climate: boolean;
      top_n: number;
    }) => {
      const query = new URLSearchParams({
        country: params.country,
        sector: params.sector,
        skip_climate: String(params.skip_climate),
        top_n: String(params.top_n),
      });
      const res = await apiRequest("GET", `/api/assess?${query.toString()}`);
      return (await res.json()) as AssessmentResponse;
    },
    onSuccess: (data) => {
      setResult(data);
    },
    onError: (error: Error) => {
      toast({
        title: "Assessment Failed",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const avgTotal = result
    ? (
        (result.total_risk.climate +
          result.total_risk.modern_slavery +
          result.total_risk.political +
          result.total_risk.water_stress +
          result.total_risk.nature_loss) /
        5
      ).toFixed(2)
    : null;

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b sticky top-0 z-50 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between gap-4 flex-wrap">
          <div className="flex items-center gap-2.5">
            <ShieldAlert className="w-5 h-5 text-primary" />
            <h1 className="text-lg font-semibold tracking-tight">
              Supply Chain Risk Assessment
            </h1>
            <Badge variant="secondary" className="text-xs">v4.0</Badge>
          </div>
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <span>85 countries</span>
            <Separator orientation="vertical" className="h-3" />
            <span>52 sectors</span>
            <Separator orientation="vertical" className="h-3" />
            <span>5 risk dimensions</span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        <AssessmentForm
          onSubmit={(params) => assessMutation.mutate(params)}
          isLoading={assessMutation.isPending}
        />

        {assessMutation.isPending && (
          <div className="space-y-4" data-testid="loading-skeleton">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
              {Array.from({ length: 5 }).map((_, i) => (
                <Card key={i}>
                  <CardContent className="p-4">
                    <Skeleton className="h-4 w-20 mb-3" />
                    <Skeleton className="h-6 w-24 mb-2" />
                    <Skeleton className="h-1.5 w-full mb-3" />
                    <Skeleton className="h-3 w-full" />
                    <Skeleton className="h-3 w-3/4 mt-1" />
                  </CardContent>
                </Card>
              ))}
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <Card>
                <CardContent className="p-6">
                  <Skeleton className="h-[300px] w-full" />
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6">
                  <Skeleton className="h-[300px] w-full" />
                </CardContent>
              </Card>
            </div>
          </div>
        )}

        {result && !assessMutation.isPending && (
          <div className="space-y-6" data-testid="assessment-results">
            <div className="flex flex-wrap items-center gap-3">
              <div className="flex items-center gap-2">
                <Globe className="w-4 h-4 text-muted-foreground" />
                <span className="font-medium">{result.country_name}</span>
                <Badge variant="outline">{result.country}</Badge>
              </div>
              <Separator orientation="vertical" className="h-4" />
              <div className="flex items-center gap-2">
                <Factory className="w-4 h-4 text-muted-foreground" />
                <span className="font-medium">{result.sector_name}</span>
                <Badge variant="outline">{result.sector}</Badge>
              </div>
              {avgTotal && (
                <>
                  <Separator orientation="vertical" className="h-4" />
                  <div className="flex items-center gap-2">
                    <Activity className="w-4 h-4 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">Avg. Total Risk:</span>
                    <span className="font-mono font-semibold">{avgTotal}</span>
                  </div>
                </>
              )}
            </div>

            <RiskDimensionCards
              directRisk={result.direct_risk}
              indirectRisk={result.indirect_risk}
              totalRisk={result.total_risk}
            />

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="flex items-center gap-2 text-base">
                    <BarChart3 className="w-4 h-4 text-muted-foreground" />
                    Risk Profile
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <RiskRadarChart
                    directRisk={result.direct_risk}
                    indirectRisk={result.indirect_risk}
                    totalRisk={result.total_risk}
                  />
                </CardContent>
              </Card>

              {result.direct_risk.expected_loss && (
                <FinancialImpactCard expectedLoss={result.direct_risk.expected_loss} />
              )}

              {!result.direct_risk.expected_loss && (
                <Card>
                  <CardContent className="flex flex-col items-center justify-center h-full min-h-[300px] gap-3 p-6">
                    <AlertTriangle className="w-8 h-8 text-muted-foreground" />
                    <p className="text-sm text-muted-foreground text-center">
                      Climate financial impact data not included. Enable the
                      "Include climate financial impact" toggle to see expected loss estimates.
                    </p>
                  </CardContent>
                </Card>
              )}
            </div>

            <SupplierTable suppliers={result.top_suppliers} />
          </div>
        )}

        {!result && !assessMutation.isPending && (
          <Card data-testid="empty-state">
            <CardContent className="flex flex-col items-center justify-center py-16 gap-4">
              <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center">
                <ShieldAlert className="w-8 h-8 text-muted-foreground" />
              </div>
              <div className="text-center space-y-2 max-w-md">
                <h2 className="text-lg font-semibold">
                  Assess Supply Chain Risk
                </h2>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  Select a country and economic sector above to generate a comprehensive
                  multi-dimensional risk assessment. The analysis covers climate hazards,
                  modern slavery prevalence, political stability, water stress, and
                  nature loss across your supply chain.
                </p>
              </div>
            </CardContent>
          </Card>
        )}
      </main>

      <footer className="border-t mt-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex flex-wrap items-center justify-between gap-2 text-xs text-muted-foreground">
          <span>Supply Chain Risk Assessment API v4.0.0</span>
          <span>Data: OECD ICIO Tables, Climate API V7, Global Slavery Index, WRI Aqueduct</span>
        </div>
      </footer>
    </div>
  );
}
