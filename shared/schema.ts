import { z } from "zod";

export const riskDimensions = ["climate", "modern_slavery", "political", "water_stress", "nature_loss"] as const;
export type RiskDimension = typeof riskDimensions[number];

export const riskBreakdownSchema = z.object({
  annual_loss: z.number(),
  annual_loss_pct: z.number(),
});

export const expectedLossSchema = z.object({
  total_annual_loss: z.number(),
  total_annual_loss_pct: z.number(),
  present_value_30yr: z.number(),
  risk_breakdown: z.object({
    hurricane: riskBreakdownSchema,
    flood: riskBreakdownSchema,
    heat_stress: riskBreakdownSchema,
    drought: riskBreakdownSchema,
    extreme_precipitation: riskBreakdownSchema,
  }),
});

export const directRiskSchema = z.object({
  climate: z.number(),
  modern_slavery: z.number(),
  political: z.number(),
  water_stress: z.number(),
  nature_loss: z.number(),
  expected_loss: expectedLossSchema.optional(),
});

export const indirectRiskSchema = z.object({
  climate: z.number(),
  modern_slavery: z.number(),
  political: z.number(),
  water_stress: z.number(),
  nature_loss: z.number(),
  expected_loss: z.object({
    total_annual_loss: z.number(),
    total_annual_loss_pct: z.number(),
  }).optional(),
});

export const riskContributionSchema = z.object({
  climate: z.number(),
  modern_slavery: z.number(),
  political: z.number(),
  water_stress: z.number(),
  nature_loss: z.number(),
});

export const supplierSchema = z.object({
  country: z.string(),
  sector: z.string(),
  coefficient: z.number(),
  country_name: z.string(),
  sector_name: z.string(),
  direct_risk: riskContributionSchema,
  risk_contribution: riskContributionSchema,
  expected_loss_contribution: z.object({
    annual_loss: z.number(),
    present_value_30yr: z.number(),
  }).optional(),
});

export const assessmentResponseSchema = z.object({
  country: z.string(),
  country_name: z.string(),
  sector: z.string(),
  sector_name: z.string(),
  direct_risk: directRiskSchema,
  indirect_risk: indirectRiskSchema,
  total_risk: riskContributionSchema,
  top_suppliers: z.array(supplierSchema),
});

export const assessmentRequestSchema = z.object({
  country: z.string().min(2).max(3),
  sector: z.string().min(1),
  skip_climate: z.boolean().default(false),
  top_n: z.number().int().min(1).max(20).default(5),
});

export type RiskBreakdown = z.infer<typeof riskBreakdownSchema>;
export type ExpectedLoss = z.infer<typeof expectedLossSchema>;
export type DirectRisk = z.infer<typeof directRiskSchema>;
export type IndirectRisk = z.infer<typeof indirectRiskSchema>;
export type RiskContribution = z.infer<typeof riskContributionSchema>;
export type Supplier = z.infer<typeof supplierSchema>;
export type AssessmentResponse = z.infer<typeof assessmentResponseSchema>;
export type AssessmentRequest = z.infer<typeof assessmentRequestSchema>;

export interface CountryInfo {
  code: string;
  name: string;
  region: string;
}

export interface SectorInfo {
  code: string;
  name: string;
  category: string;
}

export const llmProviders = ["gemini", "claude", "deepseek", "minimax"] as const;
export type LLMProvider = typeof llmProviders[number];

export interface LLMProviderInfo {
  id: LLMProvider;
  name: string;
  model: string;
  costPerInputToken: number;
  costPerOutputToken: number;
}

export const llmProviderDetails: Record<LLMProvider, LLMProviderInfo> = {
  gemini: {
    id: "gemini",
    name: "Google Gemini",
    model: "gemini-2.5-flash",
    costPerInputToken: 0.00000015,
    costPerOutputToken: 0.0000006,
  },
  claude: {
    id: "claude",
    name: "Anthropic Claude",
    model: "claude-sonnet-4-20250514",
    costPerInputToken: 0.000003,
    costPerOutputToken: 0.000015,
  },
  deepseek: {
    id: "deepseek",
    name: "DeepSeek",
    model: "deepseek-chat",
    costPerInputToken: 0.00000027,
    costPerOutputToken: 0.0000011,
  },
  minimax: {
    id: "minimax",
    name: "MiniMax",
    model: "MiniMax-M2.5",
    costPerInputToken: 0.00000015,
    costPerOutputToken: 0.00000055,
  },
};

export interface LLMAnalysisRequest {
  provider: LLMProvider;
  assessmentData: AssessmentResponse;
}

export interface LLMAnalysisResponse {
  provider: LLMProvider;
  model: string;
  analysis: string;
  responseTimeMs: number;
  inputTokens: number;
  outputTokens: number;
  estimatedCost: number;
  error?: string;
}
