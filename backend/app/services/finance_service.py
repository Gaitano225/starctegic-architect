from typing import Dict, Any, List

class FinanceService:
    """
    Service to calculate infrastructure costs and ROI for technical projects.
    """
    
    # Standard monthly costs (estimates)
    CLOUD_PRICES = {
        "aws": {
            "small": 50,    # t3.medium + RDS + S3 mini
            "medium": 250,  # t3.large + Managed DB + Cache + Data
            "large": 800    # Cluster EKS + Multi-AZ DB + CloudFront
        },
        "gcp": {
            "small": 45,
            "medium": 230,
            "large": 750
        },
        "vps_local": {
            "small": 10,    # Entry level VPS (OVH/DigitalOcean/Local)
            "medium": 40,   # 8GB RAM + 4 vCPU
            "large": 150    # Dedicated resources
        }
    }

    def estimate_infra_monthly_cost(self, scale: str, provider: str = "vps_local") -> float:
        """
        Estimate monthly infra cost based on scale and provider.
        """
        provider_data = self.CLOUD_PRICES.get(provider, self.CLOUD_PRICES["vps_local"])
        return provider_data.get(scale, provider_data["medium"])

    def calculate_roi_3years(self, 
                             initial_dev_cost: float, 
                             monthly_infra_cost: float, 
                             expected_monthly_revenue: float,
                             revenue_growth_rate: float = 0.1) -> Dict[str, Any]:
        """
        Calculate ROI projections over 3 years.
        """
        projections = []
        total_cost = initial_dev_cost
        total_revenue = 0
        current_revenue = expected_monthly_revenue
        
        for month in range(1, 37):
            total_cost += monthly_infra_cost
            total_revenue += current_revenue
            
            # Record milestone years
            if month % 12 == 0:
                year = month // 12
                projections.append({
                    "year": year,
                    "cumulative_cost": round(total_cost, 2),
                    "cumulative_revenue": round(total_revenue, 2),
                    "net_profit": round(total_revenue - total_cost, 2),
                    "roi_percent": round(((total_revenue - total_cost) / total_cost) * 100, 2) if total_cost > 0 else 0
                })
            
            # Apply growth every month
            current_revenue *= (1 + revenue_growth_rate / 12)

        return {
            "break_even_month": self._find_break_even(initial_dev_cost, monthly_infra_cost, expected_monthly_revenue, revenue_growth_rate),
            "projections": projections,
            "summary": projections[-1]
        }

    def _find_break_even(self, initial_dev_cost, monthly_infra_cost, monthly_rev, growth) -> int:
        total_cost = initial_dev_cost
        total_revenue = 0
        current_rev = monthly_rev
        for m in range(1, 120): # Up to 10 years
            total_cost += monthly_infra_cost
            total_revenue += current_rev
            if total_revenue >= total_cost:
                return m
            current_rev *= (1 + growth / 12)
        return -1 # Never breaks even
