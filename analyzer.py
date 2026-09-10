"""
Ranking Coefficient Analyzer Module
Calculates ranking coefficients for qualification groups
"""

import pandas as pd
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RankingAnalyzer:
    def __init__(self, top_runners_count: int = 4):
        """
        Initialize analyzer
        
        Args:
            top_runners_count: Number of top runners to include in coefficient calculation
        """
        self.top_runners_count = top_runners_count

    def calculate_category_coefficient(self, category_data: pd.DataFrame) -> Dict:
        """
        Calculate ranking coefficient for a specific category
        
        The coefficient is the average of coefficients of top N runners
        
        Args:
            category_data: DataFrame with ranking data for specific category
            
        Returns:
            Dict with calculation results and coefficient
        """
        if len(category_data) == 0:
            logger.warning(f"No data available for category")
            return {
                'coefficient': 0,
                'top_runners': [],
                'runner_count': 0,
                'status': 'NO_DATA'
            }
        
        # Sort by coefficient descending (higher is better)
        sorted_data = category_data.sort_values('coefficient', ascending=False)
        
        # Get top runners
        top_runners = sorted_data.head(self.top_runners_count)
        
        if len(top_runners) == 0:
            return {
                'coefficient': 0,
                'top_runners': [],
                'runner_count': 0,
                'status': 'NO_RUNNERS'
            }
        
        # Calculate average coefficient
        avg_coefficient = top_runners['coefficient'].mean()
        
        # Prepare result
        runner_details = []
        for idx, (_, row) in enumerate(top_runners.iterrows(), 1):
            runner_details.append({
                'position': idx,
                'name': row.get('name', 'Unknown'),
                'coefficient': row.get('coefficient', 0)
            })
        
        result = {
            'coefficient': round(avg_coefficient, 4),
            'top_runners': runner_details,
            'runner_count': len(top_runners),
            'status': 'OK'
        }
        
        logger.info(
            f"Calculated coefficient: {result['coefficient']} "
            f"from {len(top_runners)} runners"
        )
        
        return result

    def analyze_all_categories(
        self, 
        ranking_df: pd.DataFrame, 
        target_categories: List[str]
    ) -> Dict[str, Dict]:
        """
        Analyze all target categories
        
        Args:
            ranking_df: DataFrame with all ranking data
            target_categories: List of category codes to analyze (e.g., ['H21', 'D21'])
            
        Returns:
            Dict with results for each category
        """
        results = {}
        
        for category in target_categories:
            logger.info(f"Analyzing category: {category}")
            
            # Filter data for this category
            category_data = ranking_df[
                ranking_df['category'].str.strip() == category.strip()
            ].copy()
            
            if len(category_data) == 0:
                logger.warning(f"No data found for category {category}")
                results[category] = {
                    'coefficient': 0,
                    'top_runners': [],
                    'runner_count': 0,
                    'status': 'NOT_FOUND'
                }
            else:
                results[category] = self.calculate_category_coefficient(category_data)
        
        return results

    def get_summary(self, results: Dict[str, Dict]) -> pd.DataFrame:
        """
        Create summary DataFrame from analysis results
        
        Args:
            results: Results from analyze_all_categories
            
        Returns:
            Summary DataFrame
        """
        summary_data = []
        
        for category, data in results.items():
            summary_data.append({
                'Category': category,
                'Coefficient': data['coefficient'],
                'Top Runners': data['runner_count'],
                'Status': data['status']
            })
        
        return pd.DataFrame(summary_data)
