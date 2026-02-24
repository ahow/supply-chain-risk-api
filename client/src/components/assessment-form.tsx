import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { useQuery } from "@tanstack/react-query";
import { Search, Globe, Factory, Settings2 } from "lucide-react";
import type { CountryInfo, SectorInfo } from "@shared/schema";

interface AssessmentFormProps {
  onSubmit: (params: {
    country: string;
    sector: string;
    skip_climate: boolean;
    top_n: number;
  }) => void;
  isLoading: boolean;
}

export function AssessmentForm({ onSubmit, isLoading }: AssessmentFormProps) {
  const [country, setCountry] = useState("");
  const [sector, setSector] = useState("");
  const [skipClimate, setSkipClimate] = useState(false);
  const [topN, setTopN] = useState(10);

  const { data: countries } = useQuery<CountryInfo[]>({
    queryKey: ["/api/countries"],
  });

  const { data: sectors } = useQuery<SectorInfo[]>({
    queryKey: ["/api/sectors"],
  });

  const groupedCountries = countries
    ? countries.reduce<Record<string, CountryInfo[]>>((acc, c) => {
        if (!acc[c.region]) acc[c.region] = [];
        acc[c.region].push(c);
        return acc;
      }, {})
    : {};

  const groupedSectors = sectors
    ? sectors.reduce<Record<string, SectorInfo[]>>((acc, s) => {
        if (!acc[s.category]) acc[s.category] = [];
        acc[s.category].push(s);
        return acc;
      }, {})
    : {};

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (country && sector) {
      onSubmit({ country, sector, skip_climate: skipClimate, top_n: topN });
    }
  };

  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-base">
          <Settings2 className="w-4 h-4 text-muted-foreground" />
          Assessment Parameters
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label className="flex items-center gap-1.5 text-sm">
                <Globe className="w-3.5 h-3.5" />
                Country
              </Label>
              <Select value={country} onValueChange={setCountry} data-testid="select-country">
                <SelectTrigger data-testid="select-country-trigger">
                  <SelectValue placeholder="Select country" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(groupedCountries)
                    .sort(([a], [b]) => a.localeCompare(b))
                    .map(([region, items]) => (
                      <div key={region}>
                        <div className="px-2 py-1.5 text-xs font-semibold text-muted-foreground">
                          {region}
                        </div>
                        {items
                          .sort((a, b) => a.name.localeCompare(b.name))
                          .map((c) => (
                            <SelectItem key={c.code} value={c.code} data-testid={`option-country-${c.code}`}>
                              {c.name} ({c.code})
                            </SelectItem>
                          ))}
                      </div>
                    ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label className="flex items-center gap-1.5 text-sm">
                <Factory className="w-3.5 h-3.5" />
                Sector
              </Label>
              <Select value={sector} onValueChange={setSector} data-testid="select-sector">
                <SelectTrigger data-testid="select-sector-trigger">
                  <SelectValue placeholder="Select sector" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(groupedSectors)
                    .sort(([a], [b]) => a.localeCompare(b))
                    .map(([category, items]) => (
                      <div key={category}>
                        <div className="px-2 py-1.5 text-xs font-semibold text-muted-foreground">
                          {category}
                        </div>
                        {items.map((s) => (
                          <SelectItem key={s.code} value={s.code} data-testid={`option-sector-${s.code}`}>
                            {s.name}
                          </SelectItem>
                        ))}
                      </div>
                    ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <Switch
                  id="include-climate"
                  checked={!skipClimate}
                  onCheckedChange={(checked) => setSkipClimate(!checked)}
                  data-testid="switch-climate"
                />
                <Label htmlFor="include-climate" className="text-sm cursor-pointer">
                  Include climate financial impact
                </Label>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <Label className="text-sm text-muted-foreground whitespace-nowrap">
                Top suppliers: {topN}
              </Label>
              <Slider
                value={[topN]}
                onValueChange={([val]) => setTopN(val)}
                min={1}
                max={10}
                step={1}
                className="w-24"
                data-testid="slider-top-n"
              />
            </div>

            <Button
              type="submit"
              disabled={!country || !sector || isLoading}
              data-testid="button-assess"
            >
              <Search className="w-4 h-4 mr-1.5" />
              {isLoading ? "Assessing..." : "Assess Risk"}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
