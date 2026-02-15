import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useToast } from "@/hooks/use-toast";
import { apiRequest } from "@/lib/queryClient";
import {
  Brain,
  Clock,
  DollarSign,
  Zap,
  Hash,
  AlertCircle,
} from "lucide-react";
import type {
  AssessmentResponse,
  LLMProvider,
  LLMAnalysisResponse,
} from "@shared/schema";
import { llmProviderDetails } from "@shared/schema";

interface AIAnalysisPanelProps {
  assessmentData: AssessmentResponse;
}

const providerColors: Record<LLMProvider, string> = {
  gemini: "bg-blue-500/10 text-blue-700 dark:text-blue-400",
  claude: "bg-orange-500/10 text-orange-700 dark:text-orange-400",
  deepseek: "bg-emerald-500/10 text-emerald-700 dark:text-emerald-400",
  minimax: "bg-purple-500/10 text-purple-700 dark:text-purple-400",
};

export function AIAnalysisPanel({ assessmentData }: AIAnalysisPanelProps) {
  const [selectedProvider, setSelectedProvider] = useState<LLMProvider | null>(
    null
  );
  const [results, setResults] = useState<
    Record<string, LLMAnalysisResponse>
  >({});
  const { toast } = useToast();

  const providersQuery = useQuery<{ providers: LLMProvider[] }>({
    queryKey: ["/api/llm-providers"],
  });

  const analyzeMutation = useMutation({
    mutationFn: async (provider: LLMProvider) => {
      const res = await apiRequest("POST", "/api/analyze", {
        provider,
        assessmentData,
      });
      return (await res.json()) as LLMAnalysisResponse;
    },
    onSuccess: (data) => {
      setResults((prev) => ({ ...prev, [data.provider]: data }));
      if (data.error) {
        toast({
          title: `${llmProviderDetails[data.provider].name} Error`,
          description: data.error,
          variant: "destructive",
        });
      }
    },
    onError: (error: Error) => {
      toast({
        title: "Analysis Failed",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const handleAnalyze = (provider: LLMProvider) => {
    setSelectedProvider(provider);
    analyzeMutation.mutate(provider);
  };

  const availableProviders = providersQuery.data?.providers || [];

  const activeResult = selectedProvider ? results[selectedProvider] : null;

  const completedResults = Object.values(results).filter((r) => !r.error);

  return (
    <Card data-testid="ai-analysis-panel">
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-base">
          <Brain className="w-4 h-4 text-muted-foreground" />
          AI Risk Analysis
          <Badge variant="secondary" className="text-xs">
            {availableProviders.length} models
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex flex-wrap gap-2" data-testid="llm-provider-buttons">
          {providersQuery.isLoading && (
            <div className="flex gap-2">
              {Array.from({ length: 4 }).map((_, i) => (
                <Skeleton key={i} className="h-9 w-28" />
              ))}
            </div>
          )}
          {availableProviders.map((provider) => {
            const info = llmProviderDetails[provider];
            const hasResult = !!results[provider];
            const isActive =
              selectedProvider === provider && analyzeMutation.isPending;

            return (
              <Button
                key={provider}
                variant={selectedProvider === provider ? "default" : "outline"}
                onClick={() => handleAnalyze(provider)}
                disabled={isActive}
                data-testid={`button-analyze-${provider}`}
                
              >
                {isActive ? (
                  <Zap className="w-4 h-4 animate-pulse" />
                ) : (
                  <Brain className="w-4 h-4" />
                )}
                {info.name}
                {hasResult && !results[provider].error && (
                  <Badge variant="secondary" className="text-xs ml-1">
                    {(results[provider].estimatedCost * 100).toFixed(2)}c
                  </Badge>
                )}
              </Button>
            );
          })}
        </div>

        {completedResults.length > 1 && (
          <div
            className="grid grid-cols-2 sm:grid-cols-4 gap-2"
            data-testid="llm-comparison-metrics"
          >
            {completedResults.map((r) => {
              const info = llmProviderDetails[r.provider];
              return (
                <button
                  key={r.provider}
                  onClick={() => setSelectedProvider(r.provider)}
                  className={`p-3 rounded-md text-left transition-colors hover-elevate ${
                    selectedProvider === r.provider
                      ? "bg-muted ring-1 ring-border"
                      : "bg-muted/40"
                  }`}
                  data-testid={`metric-card-${r.provider}`}
                >
                  <p className="text-xs text-muted-foreground font-medium truncate">
                    {info.name}
                  </p>
                  <div className="flex items-center gap-1.5 mt-1">
                    <Clock className="w-3 h-3 text-muted-foreground shrink-0" />
                    <span className="text-sm font-mono">
                      {(r.responseTimeMs / 1000).toFixed(1)}s
                    </span>
                  </div>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <DollarSign className="w-3 h-3 text-muted-foreground shrink-0" />
                    <span className="text-sm font-mono">
                      ${r.estimatedCost.toFixed(4)}
                    </span>
                  </div>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <Hash className="w-3 h-3 text-muted-foreground shrink-0" />
                    <span className="text-xs text-muted-foreground">
                      {r.inputTokens + r.outputTokens} tokens
                    </span>
                  </div>
                </button>
              );
            })}
          </div>
        )}

        {analyzeMutation.isPending && (
          <div className="space-y-3" data-testid="analysis-loading">
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-5/6" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-2/3" />
          </div>
        )}

        {activeResult && !analyzeMutation.isPending && (
          <div className="space-y-3" data-testid="analysis-result">
            {activeResult.error ? (
              <div className="flex items-start gap-2 p-3 bg-destructive/10 rounded-md">
                <AlertCircle className="w-4 h-4 text-destructive mt-0.5 shrink-0" />
                <div>
                  <p className="text-sm font-medium text-destructive">
                    Error from {llmProviderDetails[activeResult.provider].name}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    {activeResult.error}
                  </p>
                </div>
              </div>
            ) : (
              <>
                <div className="flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
                  <span
                    className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full ${providerColors[activeResult.provider]}`}
                  >
                    {llmProviderDetails[activeResult.provider].name}
                  </span>
                  <span className="font-mono">{activeResult.model}</span>
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {(activeResult.responseTimeMs / 1000).toFixed(1)}s
                  </span>
                  <span className="flex items-center gap-1">
                    <DollarSign className="w-3 h-3" />$
                    {activeResult.estimatedCost.toFixed(4)}
                  </span>
                  <span className="flex items-center gap-1">
                    <Hash className="w-3 h-3" />
                    {activeResult.inputTokens}in / {activeResult.outputTokens}
                    out
                  </span>
                </div>
                <div
                  className="prose prose-sm dark:prose-invert max-w-none text-sm leading-relaxed whitespace-pre-wrap"
                  data-testid="text-analysis-content"
                >
                  {activeResult.analysis}
                </div>
              </>
            )}
          </div>
        )}

        {!selectedProvider && !analyzeMutation.isPending && (
          <div className="flex flex-col items-center justify-center py-8 gap-3 text-center">
            <Brain className="w-8 h-8 text-muted-foreground" />
            <div className="space-y-1 max-w-sm">
              <p className="text-sm text-muted-foreground">
                Select an AI model above to generate risk analysis insights.
                Run multiple models to compare quality, speed, and cost.
              </p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
