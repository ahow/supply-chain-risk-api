import type { Express } from "express";
import { createServer, type Server } from "http";
import {
  assessRisk,
  getCountries,
  getSectors,
  isValidCountry,
  isValidSector,
} from "./risk-calculator";
import { analyzeWithLLM, getAvailableProviders } from "./llm-service";
import { llmProviders, assessmentResponseSchema, type LLMProvider } from "@shared/schema";

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {
  app.get("/api/health", (_req, res) => {
    res.json({
      status: "healthy",
      version: "4.0.0",
      countries: getCountries().length,
      sectors: getSectors().length,
    });
  });

  app.get("/api/countries", (_req, res) => {
    res.json(getCountries());
  });

  app.get("/api/sectors", (_req, res) => {
    res.json(getSectors());
  });

  app.get("/api/assess", (req, res) => {
    const country = (req.query.country as string || "").toUpperCase();
    const sector = req.query.sector as string || "";
    const skipClimate = req.query.skip_climate === "true";
    const topN = Math.min(Math.max(parseInt(req.query.top_n as string) || 5, 1), 20);

    if (!country) {
      return res.status(400).json({
        error: "Bad Request",
        message: "Missing required parameter: country",
        details: "Country code must be a valid ISO-3 code (e.g., USA, CHN, GBR)",
      });
    }

    if (!sector) {
      return res.status(400).json({
        error: "Bad Request",
        message: "Missing required parameter: sector",
        details: "Sector code must be a valid OECD sector code (e.g., B06, C10-C12)",
      });
    }

    if (!isValidCountry(country)) {
      return res.status(400).json({
        error: "Bad Request",
        message: `Invalid country code: ${country}`,
        details: "Country code must be a valid ISO-3 code (e.g., USA, CHN, GBR)",
      });
    }

    if (!isValidSector(sector)) {
      return res.status(400).json({
        error: "Bad Request",
        message: `Invalid sector code: ${sector}`,
        details: "Sector code must be a valid OECD sector code (e.g., B06, C10-C12)",
      });
    }

    try {
      const result = assessRisk(country, sector, skipClimate, topN);
      res.json(result);
    } catch (error: any) {
      console.error("Assessment error:", error);
      res.status(500).json({
        error: "Internal Server Error",
        message: "Failed to complete risk assessment",
        details: error.message,
      });
    }
  });

  app.get("/api/llm-providers", (_req, res) => {
    const available = getAvailableProviders();
    res.json({ providers: available });
  });

  app.post("/api/analyze", async (req, res) => {
    const { provider, assessmentData } = req.body;

    if (!provider || !assessmentData) {
      return res.status(400).json({
        error: "Bad Request",
        message: "Missing required fields: provider, assessmentData",
      });
    }

    if (!llmProviders.includes(provider as LLMProvider)) {
      return res.status(400).json({
        error: "Bad Request",
        message: `Invalid provider: ${provider}. Must be one of: ${llmProviders.join(", ")}`,
      });
    }

    const parsed = assessmentResponseSchema.safeParse(assessmentData);
    if (!parsed.success) {
      return res.status(400).json({
        error: "Bad Request",
        message: "Invalid assessment data format",
        details: parsed.error.issues.map((i) => i.message).join(", "),
      });
    }

    const available = getAvailableProviders();
    if (!available.includes(provider as LLMProvider)) {
      return res.status(400).json({
        error: "Bad Request",
        message: `Provider ${provider} is not configured. Available: ${available.join(", ")}`,
      });
    }

    try {
      const result = await analyzeWithLLM(
        provider as LLMProvider,
        assessmentData
      );
      res.json(result);
    } catch (error: any) {
      console.error("LLM analysis error:", error);
      res.status(500).json({
        error: "Internal Server Error",
        message: "Failed to complete LLM analysis",
        details: error.message,
      });
    }
  });

  return httpServer;
}
