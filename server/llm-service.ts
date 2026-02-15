import { GoogleGenAI } from "@google/genai";
import Anthropic from "@anthropic-ai/sdk";
import type {
  LLMProvider,
  LLMAnalysisResponse,
  AssessmentResponse,
  LLMProviderInfo,
} from "@shared/schema";
import { llmProviderDetails } from "@shared/schema";

function buildPrompt(data: AssessmentResponse): string {
  const topRisks = Object.entries(data.total_risk)
    .sort(([, a], [, b]) => b - a)
    .map(([k, v]) => `${k.replace(/_/g, " ")}: ${v.toFixed(2)}`);

  const supplierSummary = data.top_suppliers
    .slice(0, 3)
    .map(
      (s) =>
        `${s.country_name} / ${s.sector_name} (coeff: ${s.coefficient.toFixed(4)})`
    );

  const lossInfo = data.direct_risk.expected_loss
    ? `Expected annual loss: $${data.direct_risk.expected_loss.total_annual_loss.toLocaleString()} (${data.direct_risk.expected_loss.total_annual_loss_pct.toFixed(2)}% of output). 30-year present value: $${data.direct_risk.expected_loss.present_value_30yr.toLocaleString()}.`
    : "Climate financial impact data not available.";

  return `You are a supply chain risk analyst. Analyze the following risk assessment data and provide actionable insights.

Country: ${data.country_name} (${data.country})
Sector: ${data.sector_name} (${data.sector})

Total Risk Scores (0-10 scale):
${topRisks.map((r) => `  - ${r}`).join("\n")}

Direct Risk: climate=${data.direct_risk.climate.toFixed(2)}, modern_slavery=${data.direct_risk.modern_slavery.toFixed(2)}, political=${data.direct_risk.political.toFixed(2)}, water_stress=${data.direct_risk.water_stress.toFixed(2)}, nature_loss=${data.direct_risk.nature_loss.toFixed(2)}

Indirect Risk: climate=${data.indirect_risk.climate.toFixed(2)}, modern_slavery=${data.indirect_risk.modern_slavery.toFixed(2)}, political=${data.indirect_risk.political.toFixed(2)}, water_stress=${data.indirect_risk.water_stress.toFixed(2)}, nature_loss=${data.indirect_risk.nature_loss.toFixed(2)}

${lossInfo}

Top upstream suppliers by I-O coefficient:
${supplierSummary.map((s) => `  - ${s}`).join("\n")}

Provide a concise analysis (300-400 words) covering:
1. Key risk hotspots and their severity
2. Supply chain vulnerability assessment (direct vs indirect exposure)
3. Top 3 actionable mitigation recommendations
4. Financial impact interpretation

Use specific numbers from the data. Be direct and practical.`;
}

async function callGemini(
  prompt: string,
  info: LLMProviderInfo
): Promise<Omit<LLMAnalysisResponse, "provider" | "responseTimeMs">> {
  const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY || "" });
  const response = await ai.models.generateContent({
    model: info.model,
    contents: [{ role: "user", parts: [{ text: prompt }] }],
  });

  const text = response.text || "";
  const inputTokens = prompt.length / 4;
  const outputTokens = text.length / 4;

  return {
    model: info.model,
    analysis: text,
    inputTokens: Math.round(inputTokens),
    outputTokens: Math.round(outputTokens),
    estimatedCost:
      inputTokens * info.costPerInputToken +
      outputTokens * info.costPerOutputToken,
  };
}

async function callClaude(
  prompt: string,
  info: LLMProviderInfo
): Promise<Omit<LLMAnalysisResponse, "provider" | "responseTimeMs">> {
  const anthropic = new Anthropic({
    apiKey: process.env.CLAUDE_API_KEY || "",
  });

  const message = await anthropic.messages.create({
    model: info.model,
    max_tokens: 1024,
    messages: [{ role: "user", content: prompt }],
  });

  const text =
    message.content[0].type === "text" ? message.content[0].text : "";
  const inputTokens = message.usage.input_tokens;
  const outputTokens = message.usage.output_tokens;

  return {
    model: info.model,
    analysis: text,
    inputTokens,
    outputTokens,
    estimatedCost:
      inputTokens * info.costPerInputToken +
      outputTokens * info.costPerOutputToken,
  };
}

async function callDeepSeek(
  prompt: string,
  info: LLMProviderInfo
): Promise<Omit<LLMAnalysisResponse, "provider" | "responseTimeMs">> {
  const response = await fetch("https://api.deepseek.com/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.DEEPSEEK_API_KEY || ""}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: info.model,
      messages: [{ role: "user", content: prompt }],
      max_tokens: 1024,
    }),
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`DeepSeek API error ${response.status}: ${err}`);
  }

  const data = await response.json();
  const text = data.choices?.[0]?.message?.content || "";
  const inputTokens = data.usage?.prompt_tokens || Math.round(prompt.length / 4);
  const outputTokens = data.usage?.completion_tokens || Math.round(text.length / 4);

  return {
    model: info.model,
    analysis: text,
    inputTokens,
    outputTokens,
    estimatedCost:
      inputTokens * info.costPerInputToken +
      outputTokens * info.costPerOutputToken,
  };
}

async function callMiniMax(
  prompt: string,
  info: LLMProviderInfo
): Promise<Omit<LLMAnalysisResponse, "provider" | "responseTimeMs">> {
  const response = await fetch(
    "https://api.minimax.io/v1/text/chatcompletion_v2",
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.MINIMAX_API_KEY || ""}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: info.model,
        messages: [
          { role: "system", name: "analyst", content: "You are a supply chain risk analyst." },
          { role: "user", name: "user", content: prompt },
        ],
        max_completion_tokens: 1024,
      }),
    }
  );

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`MiniMax API error ${response.status}: ${err}`);
  }

  const data = await response.json();
  if (data.base_resp?.status_code !== 0) {
    throw new Error(
      `MiniMax error: ${data.base_resp?.status_msg || "Unknown error"}`
    );
  }
  const text = data.choices?.[0]?.message?.content || "";
  const inputTokens = data.usage?.prompt_tokens || Math.round(prompt.length / 4);
  const outputTokens = data.usage?.completion_tokens || Math.round(text.length / 4);

  return {
    model: info.model,
    analysis: text,
    inputTokens,
    outputTokens,
    estimatedCost:
      inputTokens * info.costPerInputToken +
      outputTokens * info.costPerOutputToken,
  };
}

export async function analyzeWithLLM(
  provider: LLMProvider,
  assessmentData: AssessmentResponse
): Promise<LLMAnalysisResponse> {
  const info = llmProviderDetails[provider];
  const prompt = buildPrompt(assessmentData);
  const startTime = Date.now();

  try {
    let result: Omit<LLMAnalysisResponse, "provider" | "responseTimeMs">;

    switch (provider) {
      case "gemini":
        result = await callGemini(prompt, info);
        break;
      case "claude":
        result = await callClaude(prompt, info);
        break;
      case "deepseek":
        result = await callDeepSeek(prompt, info);
        break;
      case "minimax":
        result = await callMiniMax(prompt, info);
        break;
      default:
        throw new Error(`Unknown provider: ${provider}`);
    }

    return {
      provider,
      responseTimeMs: Date.now() - startTime,
      ...result,
    };
  } catch (error: any) {
    return {
      provider,
      model: info.model,
      analysis: "",
      responseTimeMs: Date.now() - startTime,
      inputTokens: 0,
      outputTokens: 0,
      estimatedCost: 0,
      error: error.message || "Unknown error",
    };
  }
}

export function getAvailableProviders(): LLMProvider[] {
  const available: LLMProvider[] = [];
  if (process.env.GEMINI_API_KEY) available.push("gemini");
  if (process.env.CLAUDE_API_KEY) available.push("claude");
  if (process.env.DEEPSEEK_API_KEY) available.push("deepseek");
  if (process.env.MINIMAX_API_KEY) available.push("minimax");
  return available;
}
