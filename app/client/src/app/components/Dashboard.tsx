import { SummaryCards } from "./client/summary/SummaryCards";
import { PriceDistributionChart } from "./client/charts/PriceDistributionChart";
import { TopBrandsChart } from "./client/charts/TopBrandsChart";
import { TopCategoriesChart } from "./client/charts/TopCategoriesChart";
import type { ProductStats } from "@/app/types/stats";

interface Props {
  stats: ProductStats;
}

export function Dashboard({ stats }: Props) {
  return (
    <div className="space-y-6">
      <SummaryCards stats={stats} />
      <PriceDistributionChart data={stats.price_ranges} />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <TopBrandsChart data={stats.top_brands} />
        <TopCategoriesChart data={stats.categories} />
      </div>
    </div>
  );
}
